#!/usr/bin/env python3
"""
Dry-run delegator: load Record slices (and optional change-proposal delegationSpec),
print what would be sent to an external runner — no AutoGPT, no writes.

Usage:
  python3 scripts/delegate-with-advisor.py --user-slug grace-mar --dry-run
  python3 scripts/delegate-with-advisor.py -u demo --task "Python list comprehensions" --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from cache import load_json_file
from record_slice_loader import format_minimal_lesson_prompt, load_record_slices_for_lesson


def _load_delegation_spec(user_slug: str, spec_id: str) -> tuple[dict | None, str | None]:
    """Return (spec_dict, error_message)."""
    prop = REPO_ROOT / "users" / user_slug / "review-queue" / "proposals" / f"{spec_id}.json"
    if not prop.is_file():
        return None, f"proposal not found: {prop.relative_to(REPO_ROOT)}"
    try:
        data = load_json_file(prop)
    except Exception as e:  # noqa: BLE001 — operator CLI
        return None, f"invalid JSON: {e}"
    if not isinstance(data, dict):
        return None, "proposal root must be a JSON object"
    spec = data.get("delegationSpec")
    if not isinstance(spec, dict):
        return None, "proposal has no delegationSpec object"
    return spec, None


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Dry-run governed delegation: print Record slices + optional delegationSpec.",
    )
    ap.add_argument("--user-slug", "-u", default="grace-mar", help="Fork id under users/")
    ap.add_argument("--task", default="", help="Operator session focus (not Record truth)")
    ap.add_argument(
        "--spec-id",
        default="",
        help="proposalId stem; loads users/<slug>/review-queue/proposals/<id>.json if present",
    )
    ap.add_argument(
        "--max-chars",
        type=int,
        default=32000,
        help="Total budget for Record excerpts (default 32000)",
    )
    ap.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Print only (default: true). Use --no-dry-run only when a runner exists.",
    )
    ap.add_argument("--json", action="store_true", help="Emit one JSON object on stdout")
    args = ap.parse_args()

    if not args.dry_run:
        print(
            "ERROR: No execution backend is wired in this repo. Use --dry-run (default).",
            file=sys.stderr,
        )
        return 2

    payload = load_record_slices_for_lesson(args.user_slug, max_chars=args.max_chars)
    assembled = format_minimal_lesson_prompt(payload, task_hint=args.task)

    out: dict = {
        "ok": payload.get("ok"),
        "error": payload.get("error"),
        "warnings": payload.get("warnings") or [],
        "provenance": payload.get("provenance") or {},
        "operator_supplied": {"task_hint": args.task or None},
        "assembled_prompt": assembled,
    }

    if args.spec_id.strip():
        spec, err = _load_delegation_spec(args.user_slug, args.spec_id.strip())
        if err:
            print(f"WARNING: {err}", file=sys.stderr)
            out["delegationSpec"] = None
            out["delegationSpec_error"] = err
        else:
            out["delegationSpec"] = spec

    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0 if payload.get("ok") else 1

    print("# delegate-with-advisor (dry-run)\n")
    print(f"user: {args.user_slug}")
    print(f"ok: {payload.get('ok')}  error: {payload.get('error')}")
    for w in payload.get("warnings") or []:
        print(f"warning: {w}")
    print("\n## provenance")
    for k, v in (payload.get("provenance") or {}).items():
        print(f"- {k}: {v}")
    if out.get("delegationSpec") is not None:
        print("\n## delegationSpec (from change proposal)")
        print(json.dumps(out["delegationSpec"], indent=2, ensure_ascii=False))
    elif out.get("delegationSpec_error"):
        print(f"\n## delegationSpec: skipped ({out['delegationSpec_error']})")
    print("\n## assembled_prompt (minimal lesson shape)\n")
    print(assembled)
    return 0 if payload.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
