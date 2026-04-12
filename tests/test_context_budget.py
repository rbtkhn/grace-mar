"""Tests for scripts/context_budget.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import context_budget as cb  # noqa: E402


def test_load_context_budget_missing_returns_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cb, "BUDGETS_DIR", tmp_path)
    assert cb.load_context_budget("nope") == {}


def test_load_context_budget_bad_json_returns_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cb, "BUDGETS_DIR", tmp_path)
    (tmp_path / "x.json").write_text("{not json", encoding="utf-8")
    assert cb.load_context_budget("x") == {}


def test_load_daily_brief_budget_from_repo() -> None:
    path = REPO / "config" / "context_budgets" / "daily_brief.json"
    assert path.is_file()
    raw = cb.load_context_budget("daily_brief")
    assert isinstance(raw, dict)
    assert cb.get_bool(raw, "append_cel_footer", False) is True


def test_load_session_brief_budget_from_repo() -> None:
    """session_brief.json exists and loads (CEL budgets)."""
    path = REPO / "config" / "context_budgets" / "session_brief.json"
    assert path.is_file()
    raw = cb.load_context_budget("session_brief")
    assert isinstance(raw, dict)
    assert cb.get_int(raw, "max_pending_ids_listed", 99) >= 1


def test_get_int_and_get_bool() -> None:
    d = {"a": 3, "b": "7", "c": True, "d": "yes", "e": "off"}
    assert cb.get_int(d, "a", 0) == 3
    assert cb.get_int(d, "b", 0) == 7
    assert cb.get_int(d, "c", 99) == 99
    assert cb.get_int(d, "missing", 12) == 12
    assert cb.get_bool(d, "c", False) is True
    assert cb.get_bool(d, "d", False) is True
    assert cb.get_bool(d, "e", True) is False
