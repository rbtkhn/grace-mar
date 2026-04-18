#!/usr/bin/env python3
"""Append one validated retrieval-miss record to runtime/retrieval-misses/index.jsonl.

Non-canonical; does not touch Record or recursion-gate. See runtime/retrieval-misses/README.md.
"""

from __future__ import annotations

import argparse
import json
import secrets
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_RUNTIME_DIR = Path(__file__).resolve().parent
if str(_RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(_RUNTIME_DIR))

import ledger_paths  # noqa: E402

MISS_DIR = ledger_paths.retrieval_misses_dir()
MISS_FILE = ledger_paths.retrieval_misses_jsonl()
SCHEMA_PATH = ledger_paths.retrieval_miss_schema()

RETRIEVAL_SURFACES = frozenset(
    {
        "prepared_context",
        "evidence_lookup",
        "artifact_lookup",
        "notebook_lookup",
    }
)

FAILURE_CLASSES = frozenset(
    {
        "vocabulary_mismatch",
        "scope_mismatch",
        "stale_ranking",
        "missing_content",
        "aggregation_failure",
        "unknown",
    }
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def make_miss_id(ts: datetime) -> str:
    stamp = ts.strftime("%Y%m%dT%H%M%SZ")
    suffix = secrets.token_hex(4)
    return f"rmiss_{stamp}_{suffix}"


def iso_z(ts: datetime) -> str:
    return ts.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def validate_surface(value: str) -> str:
    if value not in RETRIEVAL_SURFACES:
        allowed = ", ".join(sorted(RETRIEVAL_SURFACES))
        raise argparse.ArgumentTypeError(f"invalid surface: {value}. allowed: {allowed}")
    return value


def validate_failure_class(value: str) -> str:
    if value not in FAILURE_CLASSES:
        allowed = ", ".join(sorted(FAILURE_CLASSES))
        raise argparse.ArgumentTypeError(f"invalid failure_class: {value}. allowed: {allowed}")
    return value


def normalize_text(text: str, max_len: int, field_name: str) -> str:
    value = text.strip()
    if not value:
        raise ValueError(f"{field_name} must be non-empty")
    if len(value) > max_len:
        raise ValueError(f"{field_name} exceeds max length {max_len}")
    return value


@dataclass
class RetrievalMiss:
    miss_id: str
    timestamp: str
    retrieval_surface: str
    query: str
    failure_class: str
    expected_target: str | None = None
    notes: str | None = None
    related_paths: list[str] = field(default_factory=list)
    lane_or_context: str | None = None
    recorded_by: str | None = None


def _load_schema() -> dict[str, Any]:
    raw = SCHEMA_PATH.read_text(encoding="utf-8")
    return json.loads(raw)


def _validate_payload(payload: dict[str, Any]) -> None:
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
    except ImportError:
        print("warning: jsonschema not installed; skipping schema validation", file=sys.stderr)
        return
    schema = _load_schema()
    Draft202012Validator(schema).validate(payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log a Grace-Mar retrieval miss.")
    parser.add_argument("--surface", required=True, type=validate_surface)
    parser.add_argument("--query", required=True)
    parser.add_argument("--failure-class", required=True, type=validate_failure_class, dest="failure_class")
    parser.add_argument("--expected-target", dest="expected_target")
    parser.add_argument("--notes")
    parser.add_argument("--related-path", action="append", default=[], dest="related_paths")
    parser.add_argument("--lane", dest="lane_or_context")
    parser.add_argument("--recorded-by", dest="recorded_by")
    parser.add_argument("--stdout", action="store_true")
    parser.add_argument("--validate-only", action="store_true", dest="validate_only")
    return parser.parse_args()


def build_miss(args: argparse.Namespace, now: datetime) -> RetrievalMiss:
    notes: str | None = None
    if args.notes is not None:
        notes = normalize_text(args.notes, 1000, "notes")

    expected: str | None = None
    if args.expected_target is not None:
        expected = normalize_text(args.expected_target, 500, "expected_target")

    return RetrievalMiss(
        miss_id=make_miss_id(now),
        timestamp=iso_z(now),
        retrieval_surface=args.surface,
        query=normalize_text(args.query, 500, "query"),
        failure_class=args.failure_class,
        expected_target=expected,
        notes=notes,
        related_paths=[p.strip() for p in args.related_paths if p.strip()],
        lane_or_context=args.lane_or_context.strip() if args.lane_or_context else None,
        recorded_by=args.recorded_by.strip() if args.recorded_by else None,
    )


def ensure_storage() -> None:
    MISS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    args = parse_args()
    now = utc_now()

    try:
        miss = build_miss(args, now)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    payload: dict[str, Any] = asdict(miss)
    try:
        _validate_payload(payload)
    except Exception as e:
        print(f"error: schema validation failed: {e}", file=sys.stderr)
        return 2

    if args.validate_only:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    ensure_storage()
    line = json.dumps(payload, ensure_ascii=False) + "\n"
    with MISS_FILE.open("a", encoding="utf-8") as f:
        f.write(line)

    root = ledger_paths.REPO_ROOT
    rel = MISS_FILE.relative_to(root) if MISS_FILE.is_relative_to(root) else MISS_FILE
    print(f"logged {miss.miss_id} -> {rel}")
    if args.stdout:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
