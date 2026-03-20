"""
Correlate pipeline JSONL rows for replay (e.g. staged → applied parent_event_id).

See docs/harness-replay-spec.md.
"""

from __future__ import annotations

import json
from pathlib import Path


def _read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            out.append(row)
    return out


def find_staged_event_id_for_candidate(events_path: Path, candidate_id: str) -> str | None:
    """
    Return event_id of the latest `staged` row for this candidate_id, if any.
    Older ledger lines may lack event_id — returns None then.
    """
    cid = candidate_id.strip().upper()
    rows = _read_jsonl(events_path)
    matches = [
        r
        for r in rows
        if str(r.get("candidate_id") or "").upper() == cid
        and str(r.get("event") or "").lower() == "staged"
    ]
    if not matches:
        return None
    matches.sort(key=lambda r: str(r.get("ts") or ""))
    last = matches[-1]
    eid = last.get("event_id")
    return str(eid) if eid else None
