#!/usr/bin/env python3
"""Validate artifacts/skill-write/write-claims.json against schemas/skill_write/write_claims.schema.json.

Advisory warnings: missing target_surface on surface-adaptation claims,
missing evidence/sample on strong claims, consistent without failure_mode_notes,
independent with scaffolding != none, test_result without test_type.

Usage:
  python3 scripts/validate_write_claims.py
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CLAIMS = REPO_ROOT / "artifacts/skill-write/write-claims.json"
SCHEMA_PATH = REPO_ROOT / "schemas/skill_write/write_claims.schema.json"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--claims", type=Path, default=DEFAULT_CLAIMS)
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

    today = date.today()
    stale_days = 90
    warnings: list[str] = []
    for c in data.get("claims", []):
        cid = c.get("id", "")

        lu = c.get("last_updated")
        if lu:
            try:
                parts = [int(x) for x in lu.split("-")]
                lud = date(parts[0], parts[1], parts[2])
                if (today - lud).days > stale_days:
                    warnings.append(f"stale: {cid} last_updated {lu} (> {stale_days}d)")
            except (ValueError, IndexError):
                pass

        cap_type = c.get("capability_type", "")
        level = c.get("level", "")
        test_type = c.get("test_type")
        test_result = c.get("test_result")
        scaffolding = c.get("scaffolding_level")
        target_surface = c.get("target_surface")
        sample_ref = c.get("sample_ref")
        fm_notes = c.get("failure_mode_notes")

        if cap_type in ("public-copy-adaptation", "surface-trim") and not target_surface:
            warnings.append(f"surface: {cid} capability_type={cap_type} but no target_surface")

        if level in ("consistent", "transferable", "independent"):
            refs = c.get("evidence_refs", [])
            if len(refs) <= 1 and not sample_ref:
                warnings.append(
                    f"evidence: {cid} level={level} but thin evidence (<=1 ref, no sample_ref)"
                )

        if level == "independent" and scaffolding and scaffolding != "none":
            warnings.append(
                f"test-gap: {cid} level=independent but scaffolding={scaffolding} (expected none)"
            )

        if level in ("consistent", "transferable", "independent") and not fm_notes:
            warnings.append(f"test-gap: {cid} level={level} but no failure_mode_notes")

        if test_result and not test_type:
            warnings.append(f"orphan: {cid} has test_result but no test_type")

    for w in warnings:
        print(f"warn: {w}", file=sys.stderr)
    print(f"ok: {args.claims} ({len(data.get('claims', []))} claims)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
