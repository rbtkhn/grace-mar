#!/usr/bin/env python3
"""
Validate seed-phase artifact directories against schema-registry JSON Schemas.

Usage:
  python3 scripts/validate-seed-phase.py users/demo/seed-phase
  python3 scripts/validate-seed-phase.py users/_template/seed-phase --allow-placeholders
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import orjson

REPO_ROOT = Path(__file__).resolve().parent.parent

from cache import load_json_file, load_schema
from seed_phase_artifacts import EXPECTED_ARTIFACT_KEYS, SCHEMA_BY_FILE

REQUIRED_FILES = [
    "README.md",
    *list(SCHEMA_BY_FILE.keys()),
    "seed_dossier.md",
]


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate seed-phase artifact directory")
    ap.add_argument("directory", type=Path, help="e.g. users/demo/seed-phase")
    ap.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Skip jsonschema validation (still require JSON parse + manifest keys)",
    )
    args = ap.parse_args()

    target = (REPO_ROOT / args.directory).resolve() if not args.directory.is_absolute() else args.directory
    if not target.is_dir():
        print(f"Not a directory: {target}", file=sys.stderr)
        sys.exit(1)

    failed = False
    for name in REQUIRED_FILES:
        p = target / name
        if not p.is_file():
            try:
                display = p.relative_to(REPO_ROOT)
            except ValueError:
                display = p
            print(f"Missing: {display}", file=sys.stderr)
            failed = True

    if failed:
        sys.exit(1)

    dossier = target / "seed_dossier.md"
    if dossier.stat().st_size < 20:
        print("seed_dossier.md too small", file=sys.stderr)
        sys.exit(1)

    instances: dict[str, dict] = {}
    for jname in SCHEMA_BY_FILE:
        path = target / jname
        try:
            raw = load_json_file(path)
        except orjson.JSONDecodeError as e:
            print(f"Invalid JSON {path}: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(raw, dict):
            print(f"Expected JSON object in {path}, got {type(raw).__name__}", file=sys.stderr)
            sys.exit(1)
        instances[jname] = raw

    manifest = instances["seed-phase-manifest.json"]
    arts = manifest.get("artifacts") or {}
    if set(arts.keys()) != EXPECTED_ARTIFACT_KEYS:
        print(
            "seed-phase-manifest.json artifacts keys mismatch.\n"
            f"  expected: {sorted(EXPECTED_ARTIFACT_KEYS)}\n"
            f"  got:      {sorted(arts.keys())}",
            file=sys.stderr,
        )
        sys.exit(1)
    for k, v in arts.items():
        if not isinstance(v, str) or not v.endswith(".json"):
            print(f"artifacts.{k} must be a .json filename, got {v!r}", file=sys.stderr)
            sys.exit(1)

    if args.allow_placeholders:
        print("validate-seed-phase: OK (placeholder mode, schema validation skipped)")
        return

    try:
        import jsonschema
        from jsonschema import Draft202012Validator
    except ImportError:
        print(
            "jsonschema is required for strict validation. pip install jsonschema\n"
            "Or use --allow-placeholders for scaffold dirs.",
            file=sys.stderr,
        )
        sys.exit(1)

    for jname, schema_rel in SCHEMA_BY_FILE.items():
        schema = load_schema(schema_rel)
        if not isinstance(schema, dict):
            print(f"Expected JSON object schema at {schema_rel}, got {type(schema).__name__}", file=sys.stderr)
            sys.exit(1)
        validator = Draft202012Validator(schema)
        errs = sorted(validator.iter_errors(instances[jname]), key=lambda e: e.path)
        if errs:
            print(f"Schema errors in {jname}:", file=sys.stderr)
            for e in errs[:20]:
                print(f"  {list(e.path)}: {e.message}", file=sys.stderr)
            if len(errs) > 20:
                print(f"  ... and {len(errs) - 20} more", file=sys.stderr)
            sys.exit(1)

    print("validate-seed-phase: OK (strict schema validation)")


if __name__ == "__main__":
    main()
