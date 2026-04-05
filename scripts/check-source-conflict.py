#!/usr/bin/env python3
"""
Compare two layer tokens against optional config/source-of-truth.json precedence.

Layer tokens must appear in config precedence (default file at repo root).
Valid tokens: governed_state, accepted_change_objects, prepared_context, evidence

If config is missing, prints embedded default precedence (same as template config).

Optionally validates config against schema-registry/source-of-truth.v1.json when
jsonschema is installed.
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


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "source-of-truth.json"
SCHEMA_PATH = ROOT / "schema-registry" / "source-of-truth.v1.json"

EMBEDDED_DEFAULT = {
    "schemaVersion": "1.0.0",
    "precedence": [
        "governed_state",
        "accepted_change_objects",
        "prepared_context",
        "evidence",
    ],
    "notes": ["Embedded default; add config/source-of-truth.json to customize."],
}


def load_config(path: Path | None) -> dict:
    p = path or DEFAULT_CONFIG
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return dict(EMBEDDED_DEFAULT)


def main() -> int:
    parser = argparse.ArgumentParser(description="Layer precedence check (starter).")
    parser.add_argument(
        "--left-layer",
        required=True,
        help="governed_state | accepted_change_objects | prepared_context | evidence",
    )
    parser.add_argument(
        "--right-layer",
        required=True,
        help="governed_state | accepted_change_objects | prepared_context | evidence",
    )
    parser.add_argument(
        "--config",
        default="",
        help="Path to source-of-truth.json (default: config/source-of-truth.json if present)",
    )
    parser.add_argument(
        "--no-schema-check",
        action="store_true",
        help="Skip JSON Schema validation of config when jsonschema is available",
    )
    args = parser.parse_args()

    cfg_path = Path(args.config) if args.config else None
    config = load_config(cfg_path)

    if not args.no_schema_check and jsonschema is not None and SCHEMA_PATH.is_file():
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema.validate(instance=config, schema=schema)

    precedence = config.get("precedence") or []
    for name in (args.left_layer, args.right_layer):
        if name not in precedence:
            print(f"Unknown layer {name!r}; valid: {precedence}", file=sys.stderr)
            return 1

    li = precedence.index(args.left_layer)
    ri = precedence.index(args.right_layer)
    if li < ri:
        print(f"{args.left_layer} outranks {args.right_layer} in configured precedence")
    elif ri < li:
        print(f"{args.right_layer} outranks {args.left_layer} in configured precedence")
    else:
        print("Same index; review required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
