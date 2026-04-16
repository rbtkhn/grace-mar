"""Tests for backfill month-window scaffolding (scripts/backfill_expert_thread.py)."""

from __future__ import annotations

from datetime import date

from scripts.backfill_expert_thread import Evidence, months_spanning_range, render_backfill_block


def test_months_spanning_range_q1() -> None:
    assert months_spanning_range(date(2026, 1, 1), date(2026, 3, 31)) == [
        "2026-01",
        "2026-02",
        "2026-03",
    ]


def test_months_spanning_range_single_month() -> None:
    assert months_spanning_range(date(2026, 3, 5), date(2026, 3, 28)) == ["2026-03"]


def test_render_backfill_empty_evidence_emits_month_shells() -> None:
    block = render_backfill_block("scott-ritter", date(2026, 1, 1), date(2026, 3, 31), [])
    assert "### 2026-01" in block
    assert "### 2026-02" in block
    assert "### 2026-03" in block
    assert block.count("_No eligible evidence for this month._") == 3
    assert "No eligible evidence found in the requested window" not in block


def test_render_backfill_one_bullet_in_february() -> None:
    ev = [
        Evidence(
            event_date="2026-02-10",
            source_type="days",
            path="chapters/2026-02/days.md",
            title="",
            summary="Test line.",
            anchors=[],
            confidence="high",
        )
    ]
    block = render_backfill_block("x", date(2026, 1, 1), date(2026, 3, 31), ev)
    assert "### 2026-01" in block and "_No eligible evidence for this month._" in block
    assert "### 2026-02" in block and "Test line." in block
    assert "### 2026-03" in block
