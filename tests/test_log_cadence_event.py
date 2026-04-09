"""Tests for scripts/log_cadence_event.py — cadence event append logic."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
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


def test_append_thanks_event(events_file: Path) -> None:
    append_cadence_event(
        "thanks",
        "grace-mar",
        ok=True,
        kv={"park": "gate-review-later"},
        events_path=events_file,
    )
    text = events_file.read_text(encoding="utf-8")
    assert (
        "— thanks (grace-mar) ok=true cursor_model=unknown park=gate-review-later" in text
    )


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


def test_dedupe_skips_second_same_kind_user_within_window(
    events_file: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    events_file.write_text(
        HEADER
        + "- **2026-01-15 12:00 UTC** — coffee (grace-mar) ok=true mode=work-start cursor_model=unknown\n",
        encoding="utf-8",
    )
    append_cadence_event(
        "coffee",
        "grace-mar",
        ok=True,
        mode="work-start",
        events_path=events_file,
        dedupe_seconds=60,
        now=datetime(2026, 1, 15, 12, 0, 30, tzinfo=timezone.utc),
    )
    text = events_file.read_text(encoding="utf-8")
    assert text.count("— coffee") == 1
    err = capsys.readouterr().err
    assert "cadence dedupe: skipped duplicate coffee (grace-mar)" in err


def test_dedupe_allows_after_window(events_file: Path) -> None:
    events_file.write_text(
        HEADER
        + "- **2026-01-15 12:00 UTC** — coffee (grace-mar) ok=true mode=work-start cursor_model=unknown\n",
        encoding="utf-8",
    )
    append_cadence_event(
        "coffee",
        "grace-mar",
        ok=True,
        mode="work-start",
        events_path=events_file,
        dedupe_seconds=60,
        now=datetime(2026, 1, 15, 12, 2, 0, tzinfo=timezone.utc),
    )
    text = events_file.read_text(encoding="utf-8")
    assert text.count("— coffee") == 2


def test_dedupe_disabled_allows_back_to_back(events_file: Path) -> None:
    t = datetime(2026, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
    append_cadence_event(
        "coffee", "grace-mar", ok=True, mode="work-start",
        events_path=events_file, dedupe_seconds=None, now=t,
    )
    append_cadence_event(
        "coffee", "grace-mar", ok=True, mode="work-start",
        events_path=events_file, dedupe_seconds=None, now=t,
    )
    text = events_file.read_text(encoding="utf-8")
    assert text.count("— coffee") == 2


def test_dedupe_different_kind_not_skipped(events_file: Path) -> None:
    t = datetime(2026, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
    append_cadence_event("coffee", "grace-mar", ok=True, mode="work-start", events_path=events_file, now=t)
    append_cadence_event("dream", "grace-mar", ok=True, mode="default", events_path=events_file, now=t)
    text = events_file.read_text(encoding="utf-8")
    assert "— coffee" in text and "— dream" in text
