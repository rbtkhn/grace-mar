#!/usr/bin/env python3
"""Validate artifacts/work-dev/*.json against schemas/work_dev schemas."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _validate(path: Path, schema_path: Path) -> None:
    import jsonschema

    data = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(data)


def main() -> int:
    pairs = [
        (
            REPO_ROOT / "artifacts/work-dev/known-gaps.json",
            REPO_ROOT / "schemas/work_dev/known_gaps.schema.json",
        ),
        (
            REPO_ROOT / "artifacts/work-dev/capability-status.json",
            REPO_ROOT / "schemas/work_dev/integration_status.schema.json",
        ),
        (
            REPO_ROOT / "artifacts/work-dev/proof_ledger.json",
            REPO_ROOT / "schemas/work_dev/proof_ledger.schema.json",
        ),
    ]
    for data_path, schema_path in pairs:
        if not data_path.is_file():
            print(f"skip missing {data_path}", file=sys.stderr)
            continue
        _validate(data_path, schema_path)
        print(f"ok: {data_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
