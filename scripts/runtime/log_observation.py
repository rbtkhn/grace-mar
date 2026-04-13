#!/usr/bin/env python3
"""Append one validated runtime observation to runtime/observations/index.jsonl.

Non-canonical; does not touch Record or recursion-gate. See runtime/observations/README.md.
"""

from __future__ import annotations

import argparse
import json
import os
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

OBS_DIR = ledger_paths.observations_dir()
OBS_FILE = ledger_paths.observations_jsonl()
SCHEMA_PATH = ledger_paths.runtime_observation_schema()

SOURCE_KINDS = frozenset(
    {
        "manual_note",
        "notebook_entry",
        "compression",
        "evidence_ref",
        "agent_output",
        "research_note",
        "candidate_derivation",
    }
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def make_obs_id(ts: datetime) -> str:
    stamp = ts.strftime("%Y%m%dT%H%M%SZ")
    suffix = secrets.token_hex(4)
    return f"obs_{stamp}_{suffix}"


def iso_z(ts: datetime) -> str:
    return ts.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def validate_lane(value: str) -> str:
    value = value.strip()
    if not value:
        raise argparse.ArgumentTypeError("lane must be non-empty")
    return value


def validate_source_kind(value: str) -> str:
    if value not in SOURCE_KINDS:
        allowed = ", ".join(sorted(SOURCE_KINDS))
        raise argparse.ArgumentTypeError(f"invalid source kind: {value}. allowed: {allowed}")
    return value


def validate_confidence(value: str) -> float:
    num = float(value)
    if not (0.0 <= num <= 1.0):
        raise argparse.ArgumentTypeError("confidence must be between 0 and 1")
    return num


def normalize_text(text: str, max_len: int, field_name: str) -> str:
    value = text.strip()
    if not value:
        raise ValueError(f"{field_name} must be non-empty")
    if len(value) > max_len:
        raise ValueError(f"{field_name} exceeds max length {max_len}")
    return value


@dataclass
class RuntimeObservation:
    obs_id: str
    timestamp: str
    lane: str
    source_kind: str
    title: str
    summary: str
    record_mutation_candidate: bool
    source_path: str | None = None
    source_refs: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    confidence: float | None = None
    contradiction_refs: list[str] = field(default_factory=list)
    notes: str | None = None


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
    parser = argparse.ArgumentParser(description="Log a Grace-Mar runtime observation.")
    parser.add_argument("--lane", required=True, type=validate_lane)
    parser.add_argument("--source-kind", required=True, type=validate_source_kind, dest="source_kind")
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--source-path", dest="source_path")
    parser.add_argument("--source-ref", action="append", default=[], dest="source_refs")
    parser.add_argument("--tag", action="append", default=[], dest="tags")
    parser.add_argument("--confidence", type=validate_confidence)
    parser.add_argument(
        "--record-mutation-candidate",
        action="store_true",
        dest="record_mutation_candidate",
    )
    parser.add_argument("--contradiction-ref", action="append", default=[], dest="contradiction_refs")
    parser.add_argument("--notes")
    parser.add_argument("--stdout", action="store_true")
    parser.add_argument("--validate-only", action="store_true", dest="validate_only")
    return parser.parse_args()


def build_observation(args: argparse.Namespace, now: datetime) -> RuntimeObservation:
    notes: str | None = None
    if args.notes is not None:
        notes = normalize_text(args.notes, 2000, "notes")

    return RuntimeObservation(
        obs_id=make_obs_id(now),
        timestamp=iso_z(now),
        lane=args.lane,
        source_kind=args.source_kind,
        title=normalize_text(args.title, 180, "title"),
        summary=normalize_text(args.summary, 1200, "summary"),
        record_mutation_candidate=bool(args.record_mutation_candidate),
        source_path=args.source_path.strip() if args.source_path else None,
        source_refs=[s.strip() for s in args.source_refs if s.strip()],
        tags=[t.strip() for t in args.tags if t.strip()],
        confidence=args.confidence,
        contradiction_refs=[c.strip() for c in args.contradiction_refs if c.strip()],
        notes=notes,
    )


def ensure_storage() -> None:
    OBS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    args = parse_args()
    now = utc_now()

    try:
        obs = build_observation(args, now)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    payload: dict[str, Any] = asdict(obs)
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
    with OBS_FILE.open("a", encoding="utf-8") as f:
        f.write(line)

    root = ledger_paths.REPO_ROOT
    rel = OBS_FILE.relative_to(root) if OBS_FILE.is_relative_to(root) else OBS_FILE
    print(f"logged {obs.obs_id} -> {rel}")
    if args.stdout:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
