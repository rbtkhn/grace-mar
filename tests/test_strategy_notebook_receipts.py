"""Tests for strategy-notebook JSONL receipts (WORK only)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_notebook.receipts import (  # noqa: E402
    NotebookReceipt,
    PageOperation,
    append_receipt,
    default_receipt_log_path,
    rel_posix,
)


def test_page_operation_values() -> None:
    vals = {e.value for e in PageOperation}
    assert "NOOP" in vals and "APPEND" in vals
    assert len(vals) == len(PageOperation)


def test_notebook_receipt_round_trip_json() -> None:
    r = NotebookReceipt(
        ts="2026-04-16T12:00:00Z",
        entrypoint="test",
        page_operation=PageOperation.APPEND.value,
        status="ok",
        sources_read=["docs/a.md"],
        outputs_touched=["artifacts/x.jsonl"],
        decision="test run",
        details={"k": "v"},
    )
    d = r.to_json_dict()
    line = json.dumps(d, ensure_ascii=False, sort_keys=True)
    back = json.loads(line)
    assert back["entrypoint"] == "test"
    assert back["page_operation"] == "APPEND"
    assert back["details"] == {"k": "v"}


def test_append_receipt_creates_line(tmp_path: Path) -> None:
    log = tmp_path / "r.jsonl"
    r = NotebookReceipt(
        ts="2026-04-16T12:00:01Z",
        entrypoint="unit",
        page_operation=PageOperation.NOOP.value,
        status="ok",
    )
    p = append_receipt(tmp_path, r, log_path=log)
    assert p == log
    lines = log.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    row = json.loads(lines[0])
    assert row["status"] == "ok"


def test_default_receipt_log_path_under_artifacts() -> None:
    p = default_receipt_log_path(REPO_ROOT)
    assert "artifacts/work-strategy/strategy-notebook/receipts" in p.as_posix()


def test_rel_posix_inside_repo(tmp_path: Path) -> None:
    # minimal fake repo root
    f = tmp_path / "a" / "b.txt"
    f.parent.mkdir(parents=True)
    f.write_text("x", encoding="utf-8")
    assert rel_posix(tmp_path, f) == "a/b.txt"
