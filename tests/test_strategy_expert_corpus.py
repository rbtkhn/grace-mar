"""Tests for scripts/strategy_expert_corpus.py."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from scripts.strategy_expert_corpus import (
    CANONICAL_EXPERT_IDS,
    collect_inbox_raw_input_pointers,
    extract_thread_ingests,
    month_thread_paths_by_month,
    parse_transcript_by_month,
    rebuild_threads,
    render_thread_extraction,
)

def test_extract_respects_bundle_and_thread() -> None:
    inbox = """
**Accumulator for:** 2026-04-14 _(clock)_

_(Append below this line.)_

<!-- brief-handoff-bundle: 2026-04-12 -->

- X | cold: test // hook | https://example.com | verify:x | thread:mearsheimer
"""
    out = extract_thread_ingests(inbox, today=date(2026, 4, 14))
    assert "mearsheimer" in out
    d = date(2026, 4, 12)
    assert d in out["mearsheimer"]
    assert any("mearsheimer" in line for line in out["mearsheimer"][d])


def test_multiline_thread_ingest_includes_paragraphs_until_next_bullet() -> None:
    inbox = """
**Accumulator for:** 2026-04-14 _(clock)_

_(Append below this line.)_

- YT | cold: opener // hook | https://example.com | thread:mearsheimer
Second paragraph of quote without a leading dash.

- X | other | thread:ritter
"""
    out = extract_thread_ingests(inbox, today=date(2026, 4, 14))
    d = date(2026, 4, 14)
    block = out["mearsheimer"][d][0]
    assert "Second paragraph" in block
    assert "ritter" not in block


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
        "mearsheimer",
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
    assert "start HTML comment" in text
    assert "transcript line" in text
    assert "k.md" in text


def test_render_thread_extraction_includes_raw_input_pointers() -> None:
    text = render_thread_extraction(
        "davis",
        transcript_lines=[],
        knot_refs=[],
        page_blocks=[],
        raw_input_lane_lines=["- [a.md](raw-input/2026-04-24/a.md)"],
    )
    assert "Recent raw-input" in text
    assert "raw-input/2026-04-24/a.md" in text
    assert "_(No transcript, raw-input lane, or page material" not in text


def test_render_thread_extraction_raw_input_lane_suffices_without_transcript() -> None:
    """Empty rolling transcript is OK when the lane lists on-disk / inbox raw-input (phase-4 gate)."""
    text = render_thread_extraction(
        "davis",
        transcript_lines=[],
        knot_refs=[],
        page_blocks=[],
        raw_input_lane_lines=["- [b.md](raw-input/2026-04-24/b.md) _on-disk_"],
    )
    assert "Union of" in text or "de-duped" in text
    assert "_(No transcript, raw-input lane, or page material" not in text


def test_collect_inbox_raw_input_pointers_respects_thread_tag_and_month(
    tmp_path: Path,
) -> None:
    inbox = tmp_path / "daily-strategy-inbox.md"
    ri = tmp_path / "raw-input" / "2026-04-20"
    ri.mkdir(parents=True)
    (ri / "foo.md").write_text("x", encoding="utf-8")
    inbox.write_text(
        "- x | [raw](raw-input/2026-04-20/foo.md) | thread:ritter\n"
        "- y | [raw](raw-input/2026-03-01/bar.md) | thread:ritter\n",
        encoding="utf-8",
    )
    all_ptrs = collect_inbox_raw_input_pointers(
        tmp_path, "ritter", inbox_path=inbox, month_filter_ym=None
    )
    assert any("foo.md" in p for p in all_ptrs)
    assert any("bar.md" in p for p in all_ptrs)

    april = collect_inbox_raw_input_pointers(
        tmp_path, "ritter", inbox_path=inbox, month_filter_ym="2026-04"
    )
    assert any("foo.md" in p for p in april)
    assert not any("bar.md" in p for p in april)


def test_rebuild_threads_returns_one_path_per_canonical_expert(tmp_path: Path) -> None:
    knot = tmp_path / "knot-index.yaml"
    knot.write_text("knots: []\n", encoding="utf-8")
    paths = rebuild_threads(out_dir=tmp_path, knot_index_path=knot, dry_run=True)
    assert len(paths) == len(CANONICAL_EXPERT_IDS)
    assert all(p.name == "thread.md" for p in paths)


def test_rebuild_threads_monthly_extra_paths_for_expert_with_month_files(tmp_path: Path) -> None:
    knot = tmp_path / "knot-index.yaml"
    knot.write_text("knots: []\n", encoding="utf-8")
    nb = tmp_path
    eid = "pape"
    d = nb / "experts" / eid
    d.mkdir(parents=True)
    (d / f"{eid}-thread-2026-04.md").write_text(
        "# Expert thread\n\n## 2026-04\n\n"
        "<!-- strategy-expert-thread:start -->\n"
        "x\n<!-- strategy-expert-thread:end -->\n",
        encoding="utf-8",
    )
    (d / "transcript.md").write_text(
        "# t\n\n"
        "<!-- Triage appends new date sections below. Do not add content above this line. -->\n\n"
        "## 2026-04-14\n- line a\n",
        encoding="utf-8",
    )
    for other in CANONICAL_EXPERT_IDS:
        if other == eid:
            continue
        od = nb / "experts" / other
        od.mkdir(parents=True)
        (od / "thread.md").write_text(
            "<!-- strategy-expert-thread:start -->\n"
            "<!-- strategy-expert-thread:end -->\n",
            encoding="utf-8",
        )

    paths = rebuild_threads(out_dir=nb, knot_index_path=knot, dry_run=True)
    assert len(paths) == len(CANONICAL_EXPERT_IDS)
    month_re = re.compile(r"-thread-\d{4}-\d{2}\.md$")
    pape_monthly = [p for p in paths if p.parent.name == eid and month_re.search(p.name)]
    assert len(pape_monthly) == 1
    assert not any(p.name == "thread.md" for p in paths if p.parent.name == eid)
    assert month_thread_paths_by_month(nb, eid) == {"2026-04": d / f"{eid}-thread-2026-04.md"}
    by_m = parse_transcript_by_month(d / "transcript.md")
    assert "2026-04" in by_m
    assert any("line a" in ln for ln in by_m["2026-04"])
