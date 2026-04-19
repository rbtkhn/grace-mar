#!/usr/bin/env python3
"""
Normalize a markdown tacit capture to deterministic JSON (non-canonical).

Does not write SELF, EVIDENCE, SKILLS, recursion-gate, or prompt surfaces.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_PATH = REPO_ROOT / "schema-registry" / "tacit-capture-normalized.v1.json"
NORMALIZATION_VERSION = "1.0"


def _parse_tags(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [p.strip() for p in inner.split(",") if p.strip()]
    return [p.strip() for p in value.split(",") if p.strip()]


def _parse_metadata_block(text: str) -> tuple[dict[str, str], str]:
    """Return metadata dict and raw note body."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "# Tacit Capture":
        raise ValueError("file must start with '# Tacit Capture'")

    meta: dict[str, str] = {}
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.strip() == "## Raw note":
            body = "\n".join(lines[i + 1 :]).lstrip("\n")
            return meta, body
        if ":" in line and not line.strip().startswith("#"):
            key, _, rest = line.partition(":")
            k = key.strip().lower().replace(" ", "_")
            meta[k] = rest.strip()
        i += 1
    raise ValueError("missing '## Raw note' section")


def _normalize_timestamp(ts: str) -> str:
    ts = ts.strip()
    if not ts:
        raise ValueError("empty timestamp")
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _build_id(utc_compact: str, source: str, lane: str, raw_text: str) -> str:
    # utc_compact: YYYYMMDDTHHMMSSZ
    digest = hashlib.sha256(f"{source}\n{lane}\n{raw_text}".encode("utf-8")).hexdigest()[:12]
    return f"tacit_{utc_compact}_{digest}"


def _utc_compact_from_iso(iso_z: str) -> str:
    """iso_z ends with Z."""
    dt = datetime.fromisoformat(iso_z.replace("Z", "+00:00"))
    dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y%m%dT%H%M%SZ")


def parse_and_normalize(
    raw_markdown: str,
    *,
    provenance_path: str,
) -> dict[str, Any]:
    meta, raw_text = _parse_metadata_block(raw_markdown)
    content_sha256 = hashlib.sha256(raw_markdown.encode("utf-8")).hexdigest()

    lane = meta.get("lane", "").strip()
    if not lane:
        raise ValueError("metadata 'lane' is required")

    ts_raw = meta.get("timestamp", "").strip()
    if not ts_raw:
        raise ValueError("metadata 'timestamp' is required")

    iso_z = _normalize_timestamp(ts_raw)
    utc_compact = _utc_compact_from_iso(iso_z)

    source = (meta.get("source") or "unknown").strip()
    conf = (meta.get("confidence") or "medium").strip().lower()
    if conf not in ("low", "medium", "high"):
        raise ValueError("confidence must be low, medium, or high")

    priv = (meta.get("privacy") or "private").strip().lower()
    if priv not in ("private", "shareable"):
        raise ValueError("privacy must be private or shareable")

    dest_raw = (meta.get("intended_destination") or "unknown").strip()
    candidate_destinations = [p.strip() for p in dest_raw.split("|") if p.strip()]

    tags = _parse_tags(meta.get("tags") or "")

    tacit_id = _build_id(utc_compact, source, lane, raw_text)

    record: dict[str, Any] = {
        "id": tacit_id,
        "timestamp": iso_z,
        "source": source,
        "lane": lane,
        "raw_text": raw_text,
        "tags": tags,
        "candidate_destinations": candidate_destinations,
        "confidence": conf,
        "privacy": priv,
        "provenance_path": provenance_path,
        "normalization_version": NORMALIZATION_VERSION,
        "content_sha256": content_sha256,
    }
    return record


def _validate_schema(record: dict[str, Any]) -> list[str]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return ["jsonschema not installed; skipping schema validation"]
    if not SCHEMA_PATH.is_file():
        return [f"missing schema {SCHEMA_PATH}"]
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(record), key=lambda e: e.path)
    return [str(e.message) for e in errors]


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize tacit capture markdown to JSON.")
    ap.add_argument("--input", "-i", type=Path, required=True, help="Input .md path")
    ap.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=None,
        help="Directory for normalized JSON (default: <repo>/runtime/tacit/normalized)",
    )
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (for default paths and relative provenance)",
    )
    ap.add_argument(
        "--append-index",
        action="store_true",
        help="Append one line to runtime/tacit/index.jsonl under repo root",
    )
    ap.add_argument(
        "--stdout",
        action="store_true",
        help="Print JSON to stdout instead of writing file",
    )
    args = ap.parse_args()

    root = args.repo_root.resolve()
    inp = args.input.resolve()
    raw = inp.read_text(encoding="utf-8")

    try:
        rel = str(inp.relative_to(root))
    except ValueError:
        rel = str(inp)

    try:
        record = parse_and_normalize(raw, provenance_path=rel)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    val_errs = _validate_schema(record)
    if val_errs and not val_errs[0].startswith("jsonschema not installed"):
        for m in val_errs:
            print(f"schema: {m}", file=sys.stderr)
        return 3
    if val_errs:
        print(val_errs[0], file=sys.stderr)

    out_dir = (args.output_dir or (root / "runtime" / "tacit" / "normalized")).resolve()
    if args.stdout:
        print(json.dumps(record, indent=2, ensure_ascii=False))
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{record['id']}.json"
    out_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)

    if args.append_index:
        idx_path = root / "runtime" / "tacit" / "index.jsonl"
        idx_path.parent.mkdir(parents=True, exist_ok=True)
        line = {
            "id": record["id"],
            "provenance_path": record["provenance_path"],
            "content_sha256": record["content_sha256"],
            "timestamp": record["timestamp"],
        }
        with idx_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
        print(f"appended {idx_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
