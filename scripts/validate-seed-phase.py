#!/usr/bin/env python3
"""
Validate seed-phase artifact directories against schema-registry JSON Schemas.

Usage:
  python3 scripts/validate-seed-phase.py users/demo/seed-phase
  python3 scripts/validate-seed-phase.py users/_template/seed-phase --allow-placeholders
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "seed-phase-manifest.json",
    "seed_intake.json",
    "seed_identity.json",
    "seed_curiosity.json",
    "seed_pedagogy.json",
    "seed_expression.json",
    "seed_memory_contract.json",
    "seed_trial_report.json",
    "seed_readiness.json",
    "seed_confidence_map.json",
    "work_dev_seed.json",
    "seed_dossier.md",
]

SCHEMA_BY_FILE = {
    "seed-phase-manifest.json": "schema-registry/seed-phase-manifest.v1.json",
    "seed_intake.json": "schema-registry/seed-intake.v1.json",
    "seed_identity.json": "schema-registry/seed-identity.v1.json",
    "seed_curiosity.json": "schema-registry/seed-curiosity.v1.json",
    "seed_pedagogy.json": "schema-registry/seed-pedagogy.v1.json",
    "seed_expression.json": "schema-registry/seed-expression.v1.json",
    "seed_memory_contract.json": "schema-registry/seed-memory-contract.v1.json",
    "seed_trial_report.json": "schema-registry/seed-trial-report.v1.json",
    "seed_readiness.json": "schema-registry/seed-readiness.v1.json",
    "seed_confidence_map.json": "schema-registry/seed-confidence-map.v1.json",
    "work_dev_seed.json": "schema-registry/work-dev-seed.v1.json",
}

# Manifest "artifacts" object uses logical keys -> filename values
EXPECTED_ARTIFACT_KEYS = {
    "seed_intake",
    "seed_identity",
    "seed_curiosity",
    "seed_pedagogy",
    "seed_expression",
    "seed_memory_contract",
    "seed_trial_report",
    "seed_readiness",
    "seed_confidence_map",
    "work_dev_seed",
}


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
            print(f"Missing: {p.relative_to(REPO_ROOT)}", file=sys.stderr)
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
            instances[jname] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"Invalid JSON {path}: {e}", file=sys.stderr)
            sys.exit(1)

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
        schema_path = REPO_ROOT / schema_rel
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
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
