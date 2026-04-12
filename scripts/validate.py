#!/usr/bin/env python3
"""
Unified validation CLI — read-only orchestrator over existing scripts.

See docs/VALIDATE-CLI.md. Does not modify Record, evidence, or recursion-gate.

  python scripts/validate.py ci --user grace-mar
  python scripts/validate.py fast --json
  python scripts/validate.py full
  python scripts/validate.py expensive
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from ci_validation_inventory import (  # noqa: E402
    CheckSpec,
    checks_for_group,
    default_user,
)

SCHEMA_VERSION = "validation-run.v1"
SNIPPET_MAX = 500


def _run_one(
    spec: CheckSpec,
    user: str,
    json_mode: bool,
) -> dict[str, Any]:
    script_path = REPO_ROOT / spec.script_relpath
    if not script_path.is_file():
        return {
            "id": spec.id,
            "name": spec.label,
            "argv": [],
            "exit_code": -1,
            "duration_ms": 0,
            "stdout_snippet": "",
            "stderr_snippet": "",
            "status": "error",
            "user_scope": spec.user_scope,
            "user_effective": user if spec.user_scope == "required" else None,
            "notes": [f"Missing script: {spec.script_relpath}"],
        }

    if spec.requires_openai and not os.environ.get("OPENAI_API_KEY"):
        return {
            "id": spec.id,
            "name": spec.label,
            "argv": _build_argv(spec, user),
            "cwd": str(REPO_ROOT),
            "exit_code": 0,
            "duration_ms": 0,
            "stdout_snippet": "",
            "stderr_snippet": "",
            "status": "skipped",
            "user_scope": spec.user_scope,
            "user_effective": user if spec.user_scope == "required" else None,
            "notes": ["OPENAI_API_KEY not set; skipped (expensive check)"],
        }

    argv = [sys.executable, str(script_path)] + spec.argv_builder(user)
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(
            argv,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=spec.timeout_sec,
            shell=False,
        )
        rc = proc.returncode
        out = proc.stdout or ""
        err = proc.stderr or ""
        status = "pass" if rc == 0 else "fail"
    except subprocess.TimeoutExpired as e:
        rc = -1
        out = (e.stdout or b"").decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = (e.stderr or b"").decode("utf-8", errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        err = (err or "") + f"\n[timeout after {spec.timeout_sec}s]"
        status = "timeout"
    except OSError as e:
        rc = -1
        out = ""
        err = str(e)
        status = "error"
    dt_ms = int((time.perf_counter() - t0) * 1000)

    if not json_mode:
        sym = {"pass": "OK", "fail": "FAIL", "timeout": "TIMEOUT", "error": "ERROR", "skipped": "SKIP"}.get(
            status, status
        )
        print(f"[{sym}] {spec.label} ({spec.id})", file=sys.stderr)
        if status not in ("skipped",) and rc != 0:
            if err.strip():
                print(err[:2000], file=sys.stderr)

    return {
        "id": spec.id,
        "name": spec.label,
        "argv": argv,
        "cwd": str(REPO_ROOT),
        "exit_code": rc,
        "duration_ms": dt_ms,
        "stdout_snippet": out[:SNIPPET_MAX],
        "stderr_snippet": err[:SNIPPET_MAX],
        "status": status,
        "user_scope": spec.user_scope,
        "user_effective": user if spec.user_scope == "required" else None,
        "requires_network": spec.requires_network,
        "requires_openai": spec.requires_openai,
        "notes": [],
    }


def _build_argv(spec: CheckSpec, user: str) -> list[str]:
    script_path = REPO_ROOT / spec.script_relpath
    return [sys.executable, str(script_path)] + spec.argv_builder(user)


def run_group(
    group: str,
    user: str,
    json_mode: bool,
) -> tuple[dict[str, Any], int]:
    """Returns (result dict, exit code 0 if all passed)."""
    specs = checks_for_group(group)
    run_id = str(uuid.uuid4())
    started = time.time()
    steps: list[dict[str, Any]] = []
    any_fail = False
    for spec in specs:
        step = _run_one(spec, user, json_mode)
        steps.append(step)
        if step["status"] in ("fail", "timeout", "error"):
            any_fail = True

    ended = time.time()
    overall = "pass" if not any_fail else "fail"
    out: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
        "ended_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ended)),
        "duration_ms": int((ended - started) * 1000),
        "mode": group,
        "repo_kind": "instance",
        "repo_root": str(REPO_ROOT),
        "template_pin": None,
        "user": user,
        "overall_status": overall,
        "checks": steps,
        "summary": {
            "total_checks": len(steps),
            "passed": sum(1 for s in steps if s["status"] == "pass"),
            "failed": sum(1 for s in steps if s["status"] in ("fail", "timeout", "error")),
            "skipped": sum(1 for s in steps if s["status"] == "skipped"),
            "ci_parity": group == "ci",
        },
    }
    # Optional: surface template commit from template-source.json
    ts = REPO_ROOT / "template-source.json"
    if ts.is_file():
        try:
            data = json.loads(ts.read_text(encoding="utf-8"))
            out["template_pin"] = data.get("companionSelfCommit")
        except (OSError, json.JSONDecodeError):
            pass

    exit_code = 0 if not any_fail else 1
    return out, exit_code


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Grace-Mar unified validation orchestrator (read-only; wraps existing scripts).",
        epilog=(
            "Global options go before the subcommand, e.g.\n"
            "  python scripts/validate.py --user grace-mar ci\n"
            "  python scripts/validate.py --json fast\n"
            "See docs/VALIDATE-CLI.md."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-u",
        "--user",
        default="",
        help="Target user id under users/ (default: GRACE_MAR_USER_ID or repo heuristic).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit only JSON (validation-run.v1) to stdout; human progress to stderr.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name, desc in (
        ("ci", "CI parity with .github/workflows/test.yml validation steps (no pytest)."),
        ("fast", "Cheap local checks (paths, boundaries, evidence refs, governance)."),
        ("full", "CI checks plus growth/density metrics."),
        ("expensive", "OpenAI-backed uniqueness check (skipped if OPENAI_API_KEY unset)."),
        ("experimental", "Ad-hoc validators (skills, seed-phase template)."),
    ):
        sub.add_parser(name, help=desc)

    args = parser.parse_args()
    user = (args.user or "").strip() or default_user()
    json_mode = args.json

    result, code = run_group(args.command, user, json_mode)
    if json_mode:
        sys.stdout.write(json.dumps(result, indent=2) + "\n")
    else:
        print(
            f"Mode: {args.command}  user={user}  overall={result['overall_status']}",
            file=sys.stderr,
        )
    sys.exit(code)


if __name__ == "__main__":
    main()
