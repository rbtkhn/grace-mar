#!/usr/bin/env python3
"""Validate artifacts/skill-think/think-claims.json against schemas/skill_think/think_claims.schema.json.

Advisory warnings: stale last_updated, high confidence with single evidence ref,
optional prose anchor check for THINK- ids.

Usage:
  python3 scripts/validate_think_claims.py
  python3 scripts/validate_think_claims.py --skill-think-md users/grace-mar/skill-think.md
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CLAIMS = REPO_ROOT / "artifacts/skill-think/think-claims.json"
SCHEMA_PATH = REPO_ROOT / "schemas/skill_think/think_claims.schema.json"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--claims",
        type=Path,
        default=DEFAULT_CLAIMS,
    )
    ap.add_argument(
        "--skill-think-md",
        type=Path,
        default=None,
        help="If set, warn when claim id not found as substring in this file",
    )
    args = ap.parse_args()

    try:
        import jsonschema
    except ImportError:
        print("error: jsonschema required", file=sys.stderr)
        return 1

    if not args.claims.is_file():
        print(f"error: missing {args.claims}", file=sys.stderr)
        return 1
    data = json.loads(args.claims.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(data)

    prose = ""
    if args.skill_think_md and args.skill_think_md.is_file():
        prose = args.skill_think_md.read_text(encoding="utf-8", errors="replace")

    today = date.today()
    stale_days = 90
    warnings: list[str] = []
    for c in data.get("claims", []):
        cid = c.get("id", "")
        if prose and cid and cid not in prose:
            warnings.append(f"anchor: {cid} not found as text in {args.skill_think_md}")
        lu = c.get("last_updated")
        if lu:
            try:
                parts = [int(x) for x in lu.split("-")]
                lud = date(parts[0], parts[1], parts[2])
                if (today - lud).days > stale_days:
                    warnings.append(f"stale: {cid} last_updated {lu} (> {stale_days}d)")
            except (ValueError, IndexError):
                pass
        if c.get("confidence") == "high" and len(c.get("evidence_refs", [])) <= 1:
            warnings.append(f"evidence: {cid} confidence high but only one evidence ref")

    for w in warnings:
        print(f"warn: {w}", file=sys.stderr)
    print(f"ok: {args.claims} ({len(data.get('claims', []))} claims)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
