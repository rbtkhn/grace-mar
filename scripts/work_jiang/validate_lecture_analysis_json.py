#!/usr/bin/env python3
"""Validate lecture analysis sidecar JSON (stdlib only; no network)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_ROOT = (
    "schema_version",
    "summary",
    "key_claims",
    "predictions",
    "divergences_from_prior",
    "open_questions",
    "cross_links",
)

CLAIM_KEYS = ("claim_text", "claim_type")
PRED_KEYS_MIN = ("claim_summary", "claim_type")
DIV_KEYS_MIN = ("jiang_claim",)


def _err(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


def validate_obj(data: Any, *, path: str = "") -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return [f"{path}root must be a JSON object"]

    for k in REQUIRED_ROOT:
        if k not in data:
            errors.append(f"missing required key: {k}")

    if "summary" in data and not isinstance(data["summary"], str):
        errors.append("summary must be a string")

    for list_key in ("key_claims", "predictions", "divergences_from_prior", "cross_links"):
        if list_key in data and not isinstance(data[list_key], list):
            errors.append(f"{list_key} must be an array")

    if "open_questions" in data:
        oq = data["open_questions"]
        if not isinstance(oq, list):
            errors.append("open_questions must be an array")
        else:
            for i, q in enumerate(oq):
                if not isinstance(q, str):
                    errors.append(f"open_questions[{i}] must be a string")

    if isinstance(data.get("key_claims"), list):
        for i, row in enumerate(data["key_claims"]):
            if not isinstance(row, dict):
                errors.append(f"key_claims[{i}] must be an object")
                continue
            for ck in CLAIM_KEYS:
                if ck not in row:
                    errors.append(f"key_claims[{i}] missing {ck}")
                elif ck == "claim_text" and not isinstance(row[ck], str):
                    errors.append(f"key_claims[{i}].claim_text must be a string")

    if isinstance(data.get("predictions"), list):
        for i, row in enumerate(data["predictions"]):
            if not isinstance(row, dict):
                errors.append(f"predictions[{i}] must be an object")
                continue
            for pk in PRED_KEYS_MIN:
                if pk not in row:
                    errors.append(f"predictions[{i}] missing {pk}")

    if isinstance(data.get("divergences_from_prior"), list):
        for i, row in enumerate(data["divergences_from_prior"]):
            if not isinstance(row, dict):
                errors.append(f"divergences_from_prior[{i}] must be an object")
                continue
            if "jiang_claim" not in row:
                errors.append(f"divergences_from_prior[{i}] missing jiang_claim")

    if isinstance(data.get("cross_links"), list):
        for i, row in enumerate(data["cross_links"]):
            if not isinstance(row, dict):
                errors.append(f"cross_links[{i}] must be an object")
                continue
            if "target" not in row:
                errors.append(f"cross_links[{i}] missing target")

    src = data.get("source")
    if src is not None and not isinstance(src, dict):
        errors.append("source must be an object if present")

    ajv = data.get("analysis_json_version")
    sv = data.get("schema_version")
    if ajv is not None and sv is not None and str(ajv) != str(sv):
        errors.append("analysis_json_version must match schema_version when both are set")

    return errors


def _major_schema(schema_version: str | None) -> int:
    if schema_version is None:
        return 0
    try:
        return int(str(schema_version).strip().split(".")[0])
    except (ValueError, IndexError):
        return 0


def warn_if_below(data: Any, *, below_major: int) -> None:
    if not isinstance(data, dict):
        return
    m = _major_schema(str(data.get("schema_version") or ""))
    if m > 0 and m < below_major:
        print(
            f"WARNING: schema_version major {m} is below {below_major} (consider migrate_analysis_memo.py)",
            file=sys.stderr,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, nargs="?", help="JSON file (default: stdin)")
    parser.add_argument(
        "--warn-below-major",
        type=int,
        metavar="N",
        default=0,
        help="If schema major version is below N, print a warning to stderr (no exit 1).",
    )
    parser.add_argument(
        "--write-bump-major",
        action="store_true",
        help="If validation passes and path is set, bump schema_version to 2.0 when major is 1 (lazy upgrade).",
    )
    args = parser.parse_args()

    if args.path:
        raw = args.path.read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        _err(f"invalid JSON: {e}")
        return 1

    errors = validate_obj(data)
    if errors:
        for e in errors:
            _err(e)
        return 1
    if args.warn_below_major and args.warn_below_major > 0:
        warn_if_below(data, below_major=args.warn_below_major)
    if args.write_bump_major and args.path and isinstance(data, dict):
        m = _major_schema(str(data.get("schema_version") or ""))
        if m == 1:
            data["schema_version"] = "2.0"
            if "analysis_json_version" in data:
                data["analysis_json_version"] = "2.0"
            args.path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
            print(f"Patched schema_version -> 2.0: {args.path}", file=sys.stderr)
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
