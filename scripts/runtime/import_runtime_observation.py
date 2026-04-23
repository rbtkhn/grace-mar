#!/usr/bin/env python3
"""Import a JSON payload from a runtime into runtime-complements/inbox + receipt (membrane v1).

Stdlib only. Does not touch users/, recursion-gate, or bot/prompt.
"""

from __future__ import annotations

import argparse
import json
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INBOX = REPO_ROOT / "runtime" / "runtime-complements" / "inbox"
RECEIPTS = REPO_ROOT / "runtime" / "runtime-complements" / "receipts"

SCHEMA_VERSION = "1.0.0"
SOURCE_ENUM = ("letta", "mem0", "openmemory", "thoth", "other")
TYPE_TO_MODE: dict[str, str] = {
    "session_summary": "session_summary",
    "quick_recall": "quick_recall",
    "approval_pattern": "approval_pattern",
}


def _ts_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _ts_iso_z() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _rel_posix(p: Path) -> str:
    return p.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def infer_import_mode(payload: dict[str, Any]) -> str:
    t = str(payload.get("type", "")).lower()
    if t in TYPE_TO_MODE:
        return TYPE_TO_MODE[t]
    if t:
        return "other"
    return "observation"


def normalize_source(cli: str) -> str:
    s = (cli or "other").strip().lower()
    return s if s in SOURCE_ENUM else "other"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Import a runtime JSON observation into inbox + write a v1 receipt."
    )
    ap.add_argument(
        "--source",
        required=True,
        help=f"Source runtime (one of: {', '.join(SOURCE_ENUM)}; unknown maps to 'other').",
    )
    ap.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to input JSON (repo-relative or absolute).",
    )
    args = ap.parse_args()

    src_runtime = normalize_source(args.source)
    in_path = args.input
    if not in_path.is_absolute():
        in_path = (REPO_ROOT / in_path).resolve()
    if not in_path.is_file():
        print(f"error: input is not a file: {in_path}", file=sys.stderr)
        return 1
    try:
        raw = in_path.read_text(encoding="utf-8", errors="strict")
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 1
    if not isinstance(payload, dict):
        print("error: JSON must be an object at top level", file=sys.stderr)
        return 2

    INBOX.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    ts = _ts_compact()
    import_id = f"import_{ts}_{secrets.token_hex(4)}"
    receipt_id = f"rcr_{ts}_{secrets.token_hex(6)}"
    in_rel = _rel_posix(in_path)
    imode = infer_import_mode(payload)
    session_id: str | None = None
    c = payload.get("conversation_id")
    if isinstance(c, str) and c.strip():
        session_id = c.strip()

    inbox_name = f"runtime-complement-inbox_{ts}_{import_id}.json"
    inbox_path = INBOX / inbox_name
    wrapped: dict[str, Any] = {
        "import_id": import_id,
        "imported_at": _ts_iso_z(),
        "source_runtime": src_runtime,
        "original_input_file": in_rel,
        "payload": payload,
        "status": "runtime_only",
        "human_review_required": True,
    }
    inbox_path.write_text(
        json.dumps(wrapped, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    in_rel_inbox = _rel_posix(inbox_path)

    receipt_stem = f"runtime-complement-receipt_{ts}_{receipt_id}"
    receipt_path = RECEIPTS / f"{receipt_stem}.json"
    gat = _ts_iso_z()
    rel_receipt = _rel_posix(receipt_path)
    receipt_obj: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "receipt_id": receipt_id,
        "generated_at": gat,
        "source_runtime": src_runtime,
        "import_mode": imode,
        "input_file": in_rel,
        "output_files": [in_rel_inbox, rel_receipt],
        "canonical_surfaces_touched": False,
        "promotion_status": "runtime_only",
        "human_review_required": True,
        "notes": "Imported to runtime-complements inbox; no canonical surface writes.",
    }
    if session_id is not None:
        receipt_obj["source_session_id"] = session_id
    receipt_path.write_text(
        json.dumps(receipt_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(in_rel_inbox)
    print(rel_receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
