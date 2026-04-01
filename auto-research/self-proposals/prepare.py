#!/usr/bin/env python3
"""Protected evaluator for the self-proposals auto-research lane."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SELF_PROPOSALS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SELF_PROPOSALS_DIR.parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

for path in (SELF_PROPOSALS_DIR, SCRIPTS_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from contradiction_digest import generate_contradiction_digest
from proposal_io import load_train_payload, validate_grounding, validate_payload
from sandbox_merge import materialize_sandbox
from score_adapter import (
    build_score_bundle,
    parse_growth_density_output,
    parse_measure_uniqueness_output,
)

TRAIN_PATH = SELF_PROPOSALS_DIR / "train.md"
EXPERIMENTS_DIR = SELF_PROPOSALS_DIR / "experiments"
SANDBOX_ROOT_DIR = EXPERIMENTS_DIR / ".sandboxes"
LAST_SCORE_PATH = EXPERIMENTS_DIR / "last_score.json"
LAST_CANDIDATE_PATH = EXPERIMENTS_DIR / "last_candidate.md"


def _run_json_command(command: list[str], cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    stdout = completed.stdout.strip()
    payload: dict[str, Any]
    if stdout:
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            payload = {
                "ok": False,
                "errors": [f"non-json stdout from {' '.join(command)}"],
                "stdout": stdout,
                "stderr": completed.stderr.strip(),
            }
    else:
        payload = {
            "ok": completed.returncode == 0,
            "errors": [] if completed.returncode == 0 else [completed.stderr.strip() or "command failed without JSON output"],
        }
    payload["_returncode"] = completed.returncode
    payload["_stdout"] = stdout
    payload["_stderr"] = completed.stderr.strip()
    return payload


def _run_text_command(command: list[str], cwd: Path) -> tuple[int, str, str]:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    return completed.returncode, completed.stdout, completed.stderr


def _load_baseline_scalar(path: Path | None) -> float | None:
    if not path or not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    value = payload.get("score_bundle", {}).get("scalar")
    if isinstance(value, (int, float)):
        return float(value)
    value = payload.get("scalar")
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _failed_score_bundle(
    *,
    baseline_scalar: float | None,
    validation_errors: list[str],
    grounding_errors: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "ok": False,
        "scalar": 0.0,
        "comparison": {
            "baseline_scalar": baseline_scalar,
            "delta_from_baseline": None if baseline_scalar is None else round(0.0 - baseline_scalar, 4),
        },
        "hard_gates": {
            "integrity_ok": False,
            "governance_ok": False,
        },
        "components": {
            "proposal_quality": 0.0,
            "metrics_health": 0.0,
            "proposal_quality_detail": {},
        },
        "optional_metrics": {
            "uniqueness": {},
            "growth_density": {},
        },
        "validation_errors": validation_errors,
        "grounding_errors": grounding_errors or [],
    }


def _maybe_run_optional_measures(user_id: str, allow_live_benchmarks: bool) -> tuple[dict[str, float] | None, dict[str, float] | None]:
    if not allow_live_benchmarks:
        return None, None

    growth: dict[str, float] | None = None
    uniqueness: dict[str, float] | None = None

    growth_code, growth_out, _ = _run_text_command(
        [sys.executable, str(REPO_ROOT / "scripts" / "measure_growth_and_density.py")],
        REPO_ROOT,
    )
    if growth_code == 0:
        parsed = parse_growth_density_output(growth_out)
        growth = parsed or None

    if os.getenv("OPENAI_API_KEY"):
        uniq_code, uniq_out, _ = _run_text_command(
            [sys.executable, str(REPO_ROOT / "scripts" / "measure_uniqueness.py"), "--limit", "4"],
            REPO_ROOT,
        )
        if uniq_code == 0:
            parsed = parse_measure_uniqueness_output(uniq_out)
            uniqueness = parsed or None

    return uniqueness, growth


def run_prepare(
    *,
    user_id: str = "grace-mar",
    baseline_path: Path | None = None,
    allow_live_benchmarks: bool = False,
    strict_grounding: bool = True,
    strict_maintenance: bool = False,
) -> dict[str, Any]:
    generated_at = datetime.now(timezone.utc).isoformat()
    proposal = load_train_payload(TRAIN_PATH)
    validation_errors = validate_payload(proposal)
    grounding_errors = validate_grounding(proposal, strict=strict_grounding)
    baseline_scalar = _load_baseline_scalar(baseline_path)

    result: dict[str, Any] = {
        "generated_at": generated_at,
        "user_id": user_id,
        "proposal": proposal,
        "validation_errors": validation_errors,
        "grounding_errors": grounding_errors,
    }

    if validation_errors:
        result["score_bundle"] = _failed_score_bundle(
            baseline_scalar=baseline_scalar,
            validation_errors=validation_errors,
            grounding_errors=grounding_errors,
        )
        return result

    if grounding_errors:
        result["score_bundle"] = _failed_score_bundle(
            baseline_scalar=baseline_scalar,
            validation_errors=validation_errors,
            grounding_errors=grounding_errors,
        )
        return result

    SANDBOX_ROOT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="auto-research-self-", dir=SANDBOX_ROOT_DIR) as tmp:
        sandbox_root = Path(tmp)
        sandbox = materialize_sandbox(sandbox_root, proposal, user_id=user_id, repo_root=REPO_ROOT)

        integrity_json = _run_json_command(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "validate-integrity.py"),
                "--users-dir",
                str(sandbox_root / "users"),
                "--user",
                user_id,
                "--json",
                "--require-proposal-class",
            ],
            REPO_ROOT,
        )
        governance_code, governance_stdout, governance_stderr = _run_text_command(
            [sys.executable, str(REPO_ROOT / "scripts" / "governance_checker.py")],
            REPO_ROOT,
        )
        metrics_json = _run_json_command(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "metrics.py"),
                "--user",
                user_id,
                "--json",
            ],
            REPO_ROOT,
        )
        contradiction_digest = generate_contradiction_digest(
            user_id=user_id,
            users_dir=sandbox_root / "users",
            write_path=None,
            strict_mode=strict_maintenance,
        )

        uniqueness, growth_density = _maybe_run_optional_measures(user_id, allow_live_benchmarks)
        from score_adapter import score_proposal_quality

        proposal_quality = score_proposal_quality(proposal, sandbox["candidate_block"])
        score_bundle = build_score_bundle(
            integrity_json=integrity_json,
            governance_ok=(governance_code == 0),
            metrics_json=metrics_json,
            proposal_quality=proposal_quality,
            contradiction_digest=contradiction_digest,
            uniqueness=uniqueness,
            growth_density=growth_density,
            baseline_scalar=baseline_scalar,
            strict_maintenance=strict_maintenance,
        )

        result.update(
            {
                "sandbox": sandbox,
                "integrity_result": integrity_json,
                "metrics_result": metrics_json,
                "contradiction_digest": contradiction_digest,
                "governance_result": {
                    "ok": governance_code == 0,
                    "returncode": governance_code,
                    "stdout": governance_stdout.strip(),
                    "stderr": governance_stderr.strip(),
                },
                "score_bundle": score_bundle,
            }
        )

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a sandboxed self-proposal draft.")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id (default: grace-mar)")
    parser.add_argument("--json", action="store_true", help="Emit the full score bundle as JSON")
    parser.add_argument(
        "--baseline",
        type=Path,
        default=None,
        help="Optional accepted artifact or baseline score file to compare against",
    )
    parser.add_argument(
        "--allow-live-benchmarks",
        action="store_true",
        help="Attempt optional live benchmark scripts when their runtime dependencies are available",
    )
    parser.add_argument(
        "--strict-grounding",
        action="store_true",
        default=True,
        help="Reject placeholder or scaffold-style grounding before sandbox evaluation (default: enabled)",
    )
    parser.add_argument(
        "--allow-scaffold-grounding",
        action="store_true",
        help="Disable strict grounding so scaffold examples can still be scored locally",
    )
    parser.add_argument(
        "--strict-maintenance",
        action="store_true",
        help="Use stricter deterministic contradiction signals in sandbox scoring",
    )
    parser.add_argument(
        "--write-baseline",
        type=Path,
        default=None,
        help="Write the resulting score bundle to this path after a successful run",
    )
    args = parser.parse_args()

    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    result = run_prepare(
        user_id=args.user,
        baseline_path=args.baseline,
        allow_live_benchmarks=args.allow_live_benchmarks,
        strict_grounding=(args.strict_grounding and not args.allow_scaffold_grounding),
        strict_maintenance=args.strict_maintenance,
    )
    LAST_SCORE_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    candidate_block = result.get("sandbox", {}).get("candidate_block")
    if candidate_block:
        LAST_CANDIDATE_PATH.write_text(candidate_block + "\n", encoding="utf-8")

    if args.write_baseline:
        args.write_baseline.parent.mkdir(parents=True, exist_ok=True)
        args.write_baseline.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["score_bundle"]["scalar"])
    return 0 if result["score_bundle"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
