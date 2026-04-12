"""Tests for since-previous-dream catch-up window (dream_catchup)."""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path

from scripts.dream_catchup import (
    catch_up_local_dates,
    missing_strategy_notebook_days,
    parse_strategy_notebook_day_headers,
    read_previous_dream_generated_at,
    strategy_notebook_month_paths,
)


def test_catch_up_first_dream_today_only() -> None:
    now = datetime(2026, 4, 11, 6, 0, 0, tzinfo=timezone.utc)
    got = catch_up_local_dates(previous_dream_utc=None, now_utc=now, tz_name="UTC")
    assert got == [date(2026, 4, 11)]


def test_catch_up_same_local_day_empty() -> None:
    prev = datetime(2026, 4, 11, 8, 0, 0, tzinfo=timezone.utc)
    now = datetime(2026, 4, 11, 22, 0, 0, tzinfo=timezone.utc)
    got = catch_up_local_dates(previous_dream_utc=prev, now_utc=now, tz_name="UTC")
    assert got == []


def test_catch_up_overnight_two_days() -> None:
    prev = datetime(2026, 4, 9, 23, 0, 0, tzinfo=timezone.utc)
    now = datetime(2026, 4, 11, 6, 0, 0, tzinfo=timezone.utc)
    got = catch_up_local_dates(previous_dream_utc=prev, now_utc=now, tz_name="UTC")
    assert got == [date(2026, 4, 10), date(2026, 4, 11)]


def test_parse_day_headers() -> None:
    text = """# x\n\n## 2026-04-10\n\nfoo\n\n## 2026-04-11\n\nbar\n"""
    assert parse_strategy_notebook_day_headers(text) == {"2026-04-10", "2026-04-11"}


def test_strategy_notebook_month_paths_span() -> None:
    root = Path("/repo")
    paths = strategy_notebook_month_paths(root, date(2026, 3, 30), date(2026, 4, 2))
    assert len(paths) == 2
    assert paths[0].name == "days.md"
    assert "2026-03" in str(paths[0])
    assert "2026-04" in str(paths[1])


def test_missing_strategy_notebook_days(tmp_path: Path) -> None:
    ch = tmp_path / "docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04"
    ch.mkdir(parents=True)
    (ch / "days.md").write_text("## 2026-04-10\n\nx\n", encoding="utf-8")
    want = [date(2026, 4, 10), date(2026, 4, 11)]
    miss = missing_strategy_notebook_days(tmp_path, want)
    assert miss == ["2026-04-11"]


def test_read_previous_dream_generated_at(tmp_path: Path) -> None:
    users = tmp_path / "users" / "u1"
    users.mkdir(parents=True)
    (users / "last-dream.json").write_text(
        '{"generated_at": "2026-04-10T12:00:00+00:00"}\n', encoding="utf-8"
    )
    got = read_previous_dream_generated_at(tmp_path / "users", "u1")
    assert got is not None
    assert got.isoformat().startswith("2026-04-10T12:00:00")

