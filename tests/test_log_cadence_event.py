"""Tests for scripts/log_cadence_event.py — cadence event append logic."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from log_cadence_event import ANCHOR, HEADER, KINDS, append_cadence_event, resolve_cursor_model


@pytest.fixture(autouse=True)
def _clear_cursor_model_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CURSOR_MODEL", raising=False)


@pytest.fixture()
def events_file(tmp_path: Path) -> Path:
    """Pre-seeded events file with header and anchor."""
    p = tmp_path / "work-cadence-events.md"
    p.write_text(HEADER, encoding="utf-8")
    return p


def test_append_one_event(events_file: Path) -> None:
    append_cadence_event(
        "dream", "grace-mar", ok=True, mode="default",
        kv={"integrity": "pass"}, events_path=events_file,
    )
    text = events_file.read_text(encoding="utf-8")
    assert "— dream (grace-mar) ok=true mode=default cursor_model=unknown integrity=pass" in text
    assert text.count("— dream") == 1


def test_append_two_events_order(events_file: Path) -> None:
    append_cadence_event(
        "coffee", "grace-mar", ok=True, mode="work-start",
        events_path=events_file,
    )
    append_cadence_event(
        "dream", "grace-mar", ok=True, mode="strict",
        kv={"governance": "pass"}, events_path=events_file,
    )
    text = events_file.read_text(encoding="utf-8")
    assert "cursor_model=unknown" in text
    coffee_pos = text.index("— coffee")
    dream_pos = text.index("— dream")
    assert coffee_pos < dream_pos, "Events should appear in append order (oldest first)"


def test_missing_file_creates_with_header(tmp_path: Path) -> None:
    p = tmp_path / "subdir" / "events.md"
    assert not p.exists()
    append_cadence_event(
        "bridge", "grace-mar", ok=True,
        kv={"refs": "abc1234"}, events_path=p,
    )
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert ANCHOR in text
    assert "— bridge (grace-mar) ok=true cursor_model=unknown refs=abc1234" in text


def test_invalid_kind_raises() -> None:
    with pytest.raises(ValueError, match="kind must be one of"):
        append_cadence_event("nap", "grace-mar", events_path=Path("/dev/null"))


def test_ok_false_recorded(events_file: Path) -> None:
    append_cadence_event(
        "dream", "grace-mar", ok=False, mode="strict",
        events_path=events_file,
    )
    text = events_file.read_text(encoding="utf-8")
    assert "ok=false" in text


def test_append_harvest_event(events_file: Path) -> None:
    append_cadence_event(
        "harvest",
        "grace-mar",
        ok=True,
        mode="default",
        kv={"packet": "chat"},
        events_path=events_file,
    )
    text = events_file.read_text(encoding="utf-8")
    assert "— harvest (grace-mar) ok=true mode=default cursor_model=unknown packet=chat" in text


def test_resolve_cursor_model_env(monkeypatch: pytest.MonkeyPatch) -> None:
    assert resolve_cursor_model() == "unknown"
    monkeypatch.setenv("CURSOR_MODEL", "  Test Model  ")
    assert resolve_cursor_model() == "Test Model"


def test_cursor_model_explicit_overrides_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CURSOR_MODEL", "from-env")
    assert resolve_cursor_model(explicit="from-arg") == "from-arg"


def test_append_cursor_model_spaces_become_underscores(events_file: Path) -> None:
    append_cadence_event(
        "coffee",
        "grace-mar",
        ok=True,
        mode="minimal",
        cursor_model="A B Model",
        events_path=events_file,
    )
    text = events_file.read_text(encoding="utf-8")
    assert "cursor_model=A_B_Model" in text
