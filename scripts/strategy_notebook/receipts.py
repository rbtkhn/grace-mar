"""Append-only JSONL receipts for strategy-notebook script runs.

See docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-TRACE-CONTRACT.md
WORK only; not Record.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class PageOperation(str, Enum):
    """Governed labels for scripted or proposed page mutations (v1)."""

    NOOP = "NOOP"
    APPEND = "APPEND"
    REFINE = "REFINE"
    SPLIT = "SPLIT"
    MERGE = "MERGE"
    CONTRADICT = "CONTRADICT"
    DEPRECATE = "DEPRECATE"


@dataclass
class NotebookReceipt:
    ts: str
    entrypoint: str
    page_operation: str
    status: str  # ok | failed | dry_run
    sources_read: list[str] = field(default_factory=list)
    outputs_touched: list[str] = field(default_factory=list)
    decision: str = ""
    model: str | None = None
    provider: str | None = None
    token_count: int | None = None
    cost_usd: float | None = None
    warning_flags: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_receipt_log_path(repo_root: Path) -> Path:
    """Default gitignored JSONL path under artifacts/work-strategy/strategy-notebook/receipts/."""
    return (
        repo_root
        / "artifacts"
        / "work-strategy"
        / "strategy-notebook"
        / "receipts"
        / "strategy-notebook-receipts.jsonl"
    )


def append_receipt(
    repo_root: Path,
    receipt: NotebookReceipt,
    *,
    log_path: Path | None = None,
) -> Path:
    """Append one JSON line to the receipt log. Creates parent directories."""
    dest = log_path or default_receipt_log_path(repo_root)
    dest.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(receipt.to_json_dict(), ensure_ascii=False, sort_keys=True)
    with dest.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return dest


def rel_posix(repo_root: Path, p: Path) -> str:
    """Best-effort repo-relative POSIX path for receipts."""
    try:
        return p.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return str(p)
