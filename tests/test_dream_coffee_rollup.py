"""Tests for dream coffee rollup and related handoff helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from dream_coffee_rollup import parse_coffee_cadence_lines, rollup_coffee_24h
from dream_civmem_echoes import (
    CIVMEM_DISCLAIMER,
    build_civmem_query_from_digest,
    compute_civmem_echoes,
    excerpt_self_memory_short_term,
)
from dream_execution_paths import build_execution_paths


def test_parse_coffee_cadence_lines_filters_user_and_window() -> None:
    md = """
_(Append below this line.)_
- **2026-04-02 10:00 UTC** — coffee (grace-mar) ok=true mode=work-start
- **2026-04-02 11:00 UTC** — coffee (other-user) ok=true mode=work-start
- **2026-04-02 12:00 UTC** — coffee (grace-mar) ok=false mode=closeout
- **2026-04-01 09:00 UTC** — coffee (grace-mar) ok=true mode=minimal
"""
    ws = datetime(2026, 4, 2, 9, 0, tzinfo=timezone.utc)
    we = datetime(2026, 4, 2, 15, 0, tzinfo=timezone.utc)
    runs = parse_coffee_cadence_lines(md, user_id="grace-mar", window_start=ws, window_end=we)
    assert len(runs) == 2
    assert runs[0]["mode"] == "work-start"
    assert runs[0]["ok"] is True
    assert runs[1]["mode"] == "closeout"
    assert runs[1]["ok"] is False


def test_rollup_coffee_24h_counts_modes(tmp_path: Path) -> None:
    md = """- **2026-04-02 14:00 UTC** — coffee (grace-mar) ok=true mode=work-start
- **2026-04-02 15:00 UTC** — coffee (grace-mar) ok=true mode=light
"""
    p = tmp_path / "cadence.md"
    p.write_text(md, encoding="utf-8")
    now = datetime(2026, 4, 2, 16, 0, tzinfo=timezone.utc)
    r = rollup_coffee_24h(user_id="grace-mar", now_utc=now, events_path=p, max_runs=20)
    assert r["count"] == 2
    assert r["by_mode"]["work-start"] == 1
    assert r["by_mode"]["light"] == 1
    assert r["first_ts"] is not None
    assert r["span_hours"] is not None


def test_rollup_missing_file_note() -> None:
    p = Path(__file__).resolve().parent / "nonexistent_cadence_xyz.md"
    r = rollup_coffee_24h(user_id="grace-mar", events_path=p)
    assert r["count"] == 0
    assert r["note"] == "no cadence file"


def test_malformed_line_skipped() -> None:
    md = """- **2026-04-02 10:00 UTC** — coffee (grace-mar) ok=true mode=work-start
not a valid line
- **2026-04-02 11:00 UTC** — bridge (grace-mar) ok=true
"""
    ws = datetime(2026, 4, 2, 9, 0, tzinfo=timezone.utc)
    we = datetime(2026, 4, 2, 15, 0, tzinfo=timezone.utc)
    runs = parse_coffee_cadence_lines(md, user_id="grace-mar", window_start=ws, window_end=we)
    assert len(runs) == 1


def test_excerpt_self_memory_short_term() -> None:
    text = "## Short-term\n\nhello world\nmore\n\n## Medium-term\n\nx"
    ex = excerpt_self_memory_short_term(text, max_chars=100)
    assert "hello" in ex
    assert "Medium-term" not in ex


def test_build_civmem_query_from_digest_skips_reinforcement() -> None:
    d = {
        "entries": [
            {"title": "Alpha", "summary": "one", "relationship_type": "reinforcement"},
            {"title": "Beta", "summary": "two", "relationship_type": "contradiction", "why_flagged": ["x"]},
        ]
    }
    q = build_civmem_query_from_digest(d, max_chars=500)
    assert "Beta" in q
    assert "Alpha" not in q


def test_compute_civmem_echoes_index_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    import dream_civmem_echoes as dce

    monkeypatch.setattr(dce, "CIVMEM_INDEX_PATH", Path("/nonexistent/inrepo_index.json"))
    echoes, missing = compute_civmem_echoes(
        digest={"entries": [{"title": "t", "summary": "s", "relationship_type": "duplicate"}]},
        self_memory_text="",
    )
    assert missing is True
    assert echoes == []


def test_build_execution_paths_three_and_suggested() -> None:
    now = datetime(2026, 1, 1, 22, 0, tzinfo=timezone.utc)
    paths, idx = build_execution_paths(
        user_id="grace-mar",
        now_utc=now,
        integrity_ok=True,
        governance_ok=True,
        reviewable_count=0,
        contradiction_count=0,
        coffee_count_24h=10,
    )
    assert len(paths) == 3
    assert paths[0]["id"] == "today_field"
    assert "reentry_heavy" in paths[0]["signals_used"]
    # tomorrow Jan 2 -> tm_yday 2 -> (2-1)%3 == 1
    assert idx == 1


def test_build_execution_paths_integrity_fail() -> None:
    paths, _ = build_execution_paths(
        user_id="grace-mar",
        now_utc=datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc),
        integrity_ok=False,
        governance_ok=True,
        reviewable_count=0,
        contradiction_count=0,
        coffee_count_24h=0,
    )
    build_path = next(p for p in paths if p["id"] == "build")
    assert "integrity_fail" in build_path["signals_used"]


def test_civmem_disclaimer_nonempty() -> None:
    assert "Record" in CIVMEM_DISCLAIMER
