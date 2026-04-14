"""Tests for scripts/strategy_expert_corpus.py."""

from __future__ import annotations

from datetime import date

from scripts.strategy_expert_corpus import (
    CANONICAL_EXPERT_IDS,
    extract_thread_ingests,
    render_expert_file,
    rebuild_corpus,
)


def test_extract_respects_bundle_and_thread() -> None:
    inbox = """
**Accumulator for:** 2026-04-14 _(clock)_

_(Append below this line.)_

<!-- brief-handoff-bundle: 2026-04-12 -->

- X | cold: test // hook | https://example.com | verify:x | thread:john-mearsheimer
"""
    out = extract_thread_ingests(inbox, today=date(2026, 4, 14))
    assert "john-mearsheimer" in out
    d = date(2026, 4, 12)
    assert d in out["john-mearsheimer"]
    assert any("john-mearsheimer" in line for line in out["john-mearsheimer"][d])


def test_ignores_unknown_thread_slug() -> None:
    inbox = """
**Accumulator for:** 2026-04-14 _(clock)_

_(Append below this line.)_

- foo | verify:x | thread:someone-not-indexed
"""
    out = extract_thread_ingests(inbox, today=date(2026, 4, 14))
    assert not out


def test_render_prunes_old_dates() -> None:
    today = date(2026, 4, 14)
    by_date = {
        date(2026, 4, 1): ["- old"],
        date(2026, 4, 13): ["- new"],
    }
    text = render_expert_file(
        "john-mearsheimer",
        by_date,
        keep_days=7,
        today=today,
    )
    assert "2026-04-01" not in text
    assert "2026-04-13" in text
    assert "- new" in text


def test_rebuild_corpus_writes_all_indexed_experts(tmp_path) -> None:
    inbox = tmp_path / "inbox.md"
    inbox.write_text(
        """**Accumulator for:** 2026-04-14 _(clock)_

_(Append below this line.)_

- x | thread:daniel-davis
""",
        encoding="utf-8",
    )
    out = tmp_path / "corpus"
    paths = rebuild_corpus(
        inbox_path=inbox,
        out_dir=out,
        keep_days=7,
        today=date(2026, 4, 14),
        dry_run=False,
    )
    assert len(paths) == len(CANONICAL_EXPERT_IDS)
    assert (out / "daniel-davis.md").read_text(encoding="utf-8").count("daniel-davis") >= 2
