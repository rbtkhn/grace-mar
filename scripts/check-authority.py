#!/usr/bin/env python3
"""
Look up authority class for a surface key in config/authority-map.json.

Optional: validate config against schema-registry/authority-map.v1.json when jsonschema is installed.

With --json: print one JSON object including recommended Comprehension Envelope + Reflection Gate
fields derived from authority class (see scripts/authority_comprehension_defaults.py).

Without --json: print only the authority class string (legacy behavior).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    jsonschema = None  # type: ignore

try:
    from authority_comprehension_defaults import recommend_for_authority_class
except ImportError:
    from scripts.authority_comprehension_defaults import recommend_for_authority_class


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "authority-map.json"
SCHEMA_PATH = ROOT / "schema-registry" / "authority-map.v1.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Authority class lookup for a named surface key.")
    parser.add_argument("--surface", required=True, help="Surface key from config authority-map.json")
    parser.add_argument(
        "--config",
        default="",
        help="Path to authority-map.json (default: config/authority-map.json)",
    )
    parser.add_argument(
        "--no-schema-check",
        action="store_true",
        help="Skip JSON Schema validation of config when jsonschema is available",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON with authority_class and recommended envelope/gate staging fields",
    )
    args = parser.parse_args()

    cfg_path = Path(args.config) if args.config else DEFAULT_CONFIG
    if not cfg_path.is_file():
        print(f"ERROR: config not found: {cfg_path}", file=sys.stderr)
        return 1

    config = json.loads(cfg_path.read_text(encoding="utf-8"))

    if not args.no_schema_check and jsonschema is not None and SCHEMA_PATH.is_file():
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema.validate(instance=config, schema=schema)

    surfaces = config.get("surfaces") or {}
    level = surfaces.get(args.surface)
    if not level:
        print("unknown_surface", file=sys.stderr)
        return 1

    if args.json:
        rec = recommend_for_authority_class(level)
        out = {
            "surface": args.surface,
            "authority_class": level,
            **rec,
        }
        print(json.dumps(out, indent=2))
        return 0

    print(level)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
