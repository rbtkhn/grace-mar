#!/usr/bin/env python3
"""
Validate seed_constitution.json (JSON Schema + policy hints).

Usage:
  python3 scripts/validate-constitution.py users/demo/seed-phase
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate seed_constitution.json")
    ap.add_argument("directory", type=Path, help="seed-phase directory")
    args = ap.parse_args()
    target = (REPO_ROOT / args.directory).resolve() if not args.directory.is_absolute() else args.directory
    path = target / "seed_constitution.json"
    if not path.is_file():
        print(f"Missing {path}", file=sys.stderr)
        return 1
    try:
        inst = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(e, file=sys.stderr)
        return 1

    try:
        import jsonschema
        from jsonschema import Draft202012Validator
    except ImportError:
        print("jsonschema required: pip install jsonschema", file=sys.stderr)
        return 1

    schema_path = REPO_ROOT / "schema-registry" / "seed-constitution.v1.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errs = sorted(validator.iter_errors(inst), key=lambda e: e.path)
    if errs:
        print("Schema errors:", file=sys.stderr)
        for e in errs[:25]:
            print(f"  {list(e.path)}: {e.message}", file=sys.stderr)
        return 1

    hier = inst.get("hierarchy") or []
    if hier and hier[0] != "memory_contract":
        print(
            "Policy note: hierarchy[0] is not memory_contract — "
            "early short-circuit optimization expects memory_contract first.",
            file=sys.stderr,
        )

    print("validate-constitution: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
