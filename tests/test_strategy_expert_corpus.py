"""Tests for scripts/strategy_expert_corpus.py."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from scripts.strategy_expert_corpus import (
    CANONICAL_EXPERT_IDS,
    extract_thread_ingests,
    rebuild_threads,
    render_thread_extraction,
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


def test_render_thread_extraction_includes_transcript_and_knots() -> None:
    text = render_thread_extraction(
        "john-mearsheimer",
        transcript_lines=["- `transcript line`"],
        knot_refs=[
            {
                "path": "chapters/k.md",
                "date": "2026-04-13",
                "knot_label": "weave",
                "note": "test",
            }
        ],
    )
    assert "Segment 2" in text
    assert "transcript line" in text
    assert "k.md" in text


def test_rebuild_threads_returns_one_path_per_canonical_expert(tmp_path: Path) -> None:
    knot = tmp_path / "knot-index.yaml"
    knot.write_text("knots: []\n", encoding="utf-8")
    paths = rebuild_threads(out_dir=tmp_path, knot_index_path=knot, dry_run=True)
    assert len(paths) == len(CANONICAL_EXPERT_IDS)
    assert all(p.name.startswith("strategy-expert-") for p in paths)
