#!/usr/bin/env python3
"""Validate docs/skill-work/work-strategy/authorized-sources.yaml against JSON Schema."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--yaml",
        type=Path,
        default=REPO_ROOT / "docs/skill-work/work-strategy/authorized-sources.yaml",
    )
    ap.add_argument(
        "--schema",
        type=Path,
        default=REPO_ROOT / "schemas/work_strategy/authorized_sources.schema.json",
    )
    args = ap.parse_args()

    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        print("error: PyYAML required (pip install pyyaml)", file=sys.stderr)
        return 1
    try:
        import jsonschema
    except ImportError:
        print("error: jsonschema required", file=sys.stderr)
        return 1

    if not args.yaml.is_file():
        print(f"error: missing {args.yaml}", file=sys.stderr)
        return 1
    data = yaml.safe_load(args.yaml.read_text(encoding="utf-8"))
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(data)
    print(f"ok: {args.yaml} ({len(data.get('sources', []))} sources)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
