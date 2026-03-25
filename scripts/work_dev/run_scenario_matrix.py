#!/usr/bin/env python3
"""
Map factorial scenario rows to concrete pytest command hints and optional JSONL output.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Canonical keys plus aliases for baseline_scenarios/*.yaml required_checks tokens.
CHECK_TO_TESTS: dict[str, list[str]] = {
    "continuity_required": [
        "tests/test_continuity_receipts.py",
        "tests/test_handback_requires_continuity.py",
    ],
    "lane_scope": [
        "tests/test_lane_scope.py",
    ],
    "compute_ledger": [
        "tests/test_compute_ledger.py",
    ],
    "shadow_log": [
        "tests/test_shadow_decision_log.py",
    ],
    "autonomy_tiers": [
        "tests/test_autonomy_tiers.py",
    ],
    "scenario_generation": [
        "tests/test_scenario_generation.py",
        "tests/test_scenario_matrix.py",
    ],
    "diagnostics": [
        "tests/test_diagnostics_report.py",
    ],
    # Baseline aliases — continuity_failure.yaml
    "handback_returns_428_without_receipt": [
        "tests/test_continuity_receipts.py",
        "tests/test_handback_requires_continuity.py",
    ],
    "verify_continuity_receipt_ttl": [
        "tests/test_continuity_receipts.py",
        "tests/test_handback_requires_continuity.py",
    ],
    # Baseline aliases — lane_bleed.yaml
    "check_lane_scope_fails_or_requires_justification": [
        "tests/test_lane_scope.py",
    ],
    # Baseline aliases — false_recall.yaml
    "voice_abstention_or_lookup_prompt": [
        "tests/test_voice.py",
    ],
    # Baseline aliases — remote_handback.yaml
    "handback_uses_api_key_off_loopback": [
        "tests/test_handback_requires_continuity.py",
    ],
    "provenance_preserved_in_candidate_yaml": [
        "tests/test_gate_block_parser.py",
        "tests/test_handback_requires_continuity.py",
    ],
    # Baseline aliases — provenance_loss.yaml
    "candidate_yaml_includes_candidate_source_when_openclaw": [
        "tests/test_gate_block_parser.py",
    ],
}


def _pytest_targets(required_checks: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for check in required_checks:
        for path in CHECK_TO_TESTS.get(check, []):
            if path not in seen:
                out.append(path)
                seen.add(path)
    if not out:
        out = ["tests/test_scenario_generation.py", "tests/test_scenario_matrix.py"]
    return out


def _risk_bucket(severity: str) -> str:
    sev = severity.lower()
    if sev in {"critical", "high"}:
        return "tail-risk"
    if sev == "medium":
        return "standard"
    return "low-risk"


def build_run_hints(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hints: list[dict[str, Any]] = []
    for row in rows:
        targets = _pytest_targets(list(row.get("required_checks") or []))
        hint = {
            "scenario_id": row["scenario_id"],
            "runtime": row["runtime"],
            "variation": row["variation"],
            "severity": row["severity"],
            "risk_bucket": _risk_bucket(str(row.get("severity") or "medium")),
            "required_checks": row.get("required_checks") or [],
            "pytest_targets": targets,
            "suggested_pytest": "pytest " + " ".join(targets) + " -q",
        }
        hints.append(hint)
    return hints


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit runnable scenario-matrix test hints.")
    ap.add_argument("--scenario", default="", help="Optional scenario_id prefix filter")
    ap.add_argument(
        "--runtimes",
        default="openclaw,cursor,claude-code",
        help="Comma-separated runtimes",
    )
    ap.add_argument("--write-jsonl", type=Path, default=None)
    ap.add_argument("--write-json", type=Path, default=None)
    args = ap.parse_args()

    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "work_dev" / "generate_scenarios.py"),
            "--scenario",
            args.scenario.strip(),
            "--runtimes",
            args.runtimes,
            "--format",
            "json",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(proc.stdout)
    rows = list(payload.get("rows") or [])
    hints = build_run_hints(rows)

    if args.write_json:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(json.dumps({"version": 2, "rows": hints}, indent=2) + "\n", encoding="utf-8")

    if args.write_jsonl:
        args.write_jsonl.parent.mkdir(parents=True, exist_ok=True)
        args.write_jsonl.write_text(
            "".join(json.dumps(item) + "\n" for item in hints),
            encoding="utf-8",
        )
    if not args.write_json and not args.write_jsonl:
        sys.stdout.write("".join(json.dumps(item) + "\n" for item in hints))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
