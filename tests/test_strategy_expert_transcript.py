"""Tests for scripts/strategy_expert_transcript.py (triage + 7-day prune)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from scripts.strategy_expert_transcript import canonical_transcript_header, triage_to_transcripts


def _minimal_inbox() -> str:
    """No thread: lines — triage adds nothing; existing transcript sections are only pruned."""
    return """# scratch
**Accumulator for:** 2026-01-20 _(clock)_

_(Append below this line.)_
"""


def test_prune_drops_sections_older_than_keep_days_window(tmp_path: Path) -> None:
    """With today=2026-01-20 and keep_days=7, cutoff is 2026-01-13; keep dates > cutoff only."""
    expert = "test-prune-expert"
    out_dir = tmp_path / "notebook"
    out_dir.mkdir()
    inbox = tmp_path / "inbox.md"
    inbox.write_text(_minimal_inbox(), encoding="utf-8")

    transcript = out_dir / f"strategy-expert-{expert}-transcript.md"
    transcript.write_text(
        canonical_transcript_header(expert)
        + "\n"
        + "## 2025-12-01\n"
        + "- stale\n"
        + "\n"
        + "## 2026-01-19\n"
        + "- recent\n",
        encoding="utf-8",
    )

    triage_to_transcripts(
        inbox_path=inbox,
        out_dir=out_dir,
        keep_days=7,
        today=date(2026, 1, 20),
        dry_run=False,
        expert_ids=frozenset({expert}),
    )

    text = transcript.read_text(encoding="utf-8")
    assert "2025-12-01" not in text
    assert "stale" not in text
    assert "## 2026-01-19" in text
    assert "recent" in text


def test_prune_exact_cutoff_date_is_removed(tmp_path: Path) -> None:
    """Section dated exactly (today - keep_days) is not kept: d > cutoff is strict."""
    expert = "test-prune-expert"
    out_dir = tmp_path / "notebook"
    out_dir.mkdir()
    inbox = tmp_path / "inbox.md"
    inbox.write_text(_minimal_inbox(), encoding="utf-8")

    transcript = out_dir / f"strategy-expert-{expert}-transcript.md"
    # today 2026-01-20, keep_days=7 -> cutoff 2026-01-13; 2026-01-13 should drop
    transcript.write_text(
        canonical_transcript_header(expert)
        + "\n"
        + "## 2026-01-13\n"
        + "- on cutoff boundary\n"
        + "\n"
        + "## 2026-01-14\n"
        + "- first day inside window\n",
        encoding="utf-8",
    )

    triage_to_transcripts(
        inbox_path=inbox,
        out_dir=out_dir,
        keep_days=7,
        today=date(2026, 1, 20),
        dry_run=False,
        expert_ids=frozenset({expert}),
    )

    text = transcript.read_text(encoding="utf-8")
    assert "2026-01-13" not in text
    assert "on cutoff boundary" not in text
    assert "## 2026-01-14" in text
    assert "first day inside window" in text
