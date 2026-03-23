"""
Append-only fork lineage ledger: users/<fork_id>/fork-lineage.jsonl
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from grace_mar.fork_state import lineage_path


def _utc_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_lineage_event(repo_root: Path, fork_id: str, event: dict[str, Any]) -> dict[str, Any]:
    """Append one JSON object line. Adds ts if missing."""
    path = lineage_path(repo_root, fork_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = dict(event)
    if "ts" not in row:
        row["ts"] = _utc_ts()
    line = json.dumps(row, ensure_ascii=True) + "\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)
    return row


def read_lineage_tail(repo_root: Path, fork_id: str, max_lines: int = 500) -> list[dict[str, Any]]:
    path = lineage_path(repo_root, fork_id)
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[dict[str, Any]] = []
    for ln in lines[-max_lines:]:
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return out
