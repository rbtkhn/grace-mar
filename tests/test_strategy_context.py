"""Tests for scripts/strategy_context.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
PY = sys.executable
SCRIPT = REPO / "scripts" / "strategy_context.py"


def test_extract_day_block_and_open():
    from scripts.strategy_context import (
        extract_day_block,
        extract_h3_section,
        open_bullet_lines,
    )

    md = """## 2026-04-01

### Chronicle
- x

### Foresight
- First open
- Second **bold**

## 2026-04-02
### Foresight
- other
"""
    block = extract_day_block(md, "2026-04-01")
    assert block is not None
    open_body = extract_h3_section(block, "Foresight")
    bullets = open_bullet_lines(open_body, limit=5)
    assert bullets[0] == "First open"
    assert "bold" in bullets[1]


def test_truncate_words():
    from scripts.strategy_context import truncate_words

    s = " ".join([f"w{i}" for i in range(200)])
    out = truncate_words(s, 10)
    assert len(out.split()) <= 10
    assert out.endswith("…")


def test_count_expert_rows_sample():
    from scripts.strategy_context import count_expert_table_rows

    sample = """
| expert_id | Anchor |
|------------|--------|
| `foo-bar` | Name |
| `baz` | Other |
"""
    assert count_expert_table_rows(sample) == 2


def test_strategy_context_smoke_compact():
    r = subprocess.run(
        [
            PY,
            str(SCRIPT),
            "-u",
            "grace-mar",
            "--date",
            "2026-04-13",
            "--compact",
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    assert "daily-strategy-inbox.md" in r.stdout
    assert "2026-04-13" in r.stdout


def test_meta_excerpt_sample():
    from scripts.strategy_context import meta_excerpt

    assert "not found" in meta_excerpt(Path("/nonexistent/meta.md"))


def test_minds_excerpt_month_fallback():
    from scripts.strategy_context import minds_excerpt

    out = minds_excerpt("2099-01-01")
    assert "2099-01" in out or "missing" in out.lower()


def test_strategy_context_compact_meta_minds():
    r = subprocess.run(
        [
            PY,
            str(SCRIPT),
            "-u",
            "grace-mar",
            "--date",
            "2026-04-13",
            "--compact",
            "--meta",
            "--minds",
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    assert "meta.md" in r.stdout
    assert "minds/outputs" in r.stdout


def test_strategy_context_paragraph_word_cap():
    r = subprocess.run(
        [
            PY,
            str(SCRIPT),
            "-u",
            "grace-mar",
            "--date",
            "2026-04-13",
            "--max-words",
            "80",
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    n = len(r.stdout.split())
    assert n <= 85


def test_parse_work_choice_strategy_events_filters():
    from scripts.strategy_context import parse_work_choice_strategy_events

    transcript = """
### [WORK-choice] 2026-04-14T10:00:00Z
- context: WORK
- picked: A — build

### [WORK-choice] 2026-04-13T12:00:00Z
- context: COFFEE
- picked: C
- note: unrelated

### [WORK-choice] 2026-04-12T08:00:00Z
- context: WORK
- picked: B — steward

### [WORK-choice] 2026-04-11T07:00:00Z
- context: HOME
- picked: weave batch
"""
    events = parse_work_choice_strategy_events(transcript)
    ts_sorted = [e.ts.isoformat() for e in events]
    assert "2026-04-14" in ts_sorted[0]
    assert "2026-04-12" in ts_sorted[1]
    assert "2026-04-11" in ts_sorted[2]
    assert all(e.kind == "WORK-choice" for e in events)
    assert len(events) == 3


def test_parse_fold_jsonl_events(tmp_path):
    from scripts.strategy_context import parse_fold_jsonl_events

    p = tmp_path / "strategy-fold-events.jsonl"
    p.write_text(
        '{"ts": "2026-01-02T03:04:05Z", "notebook_date": "2026-01-02", '
        '"fold_kind": "manual", "note": "hello"}\n'
        "not json\n"
        '{"bad": "row"}\n',
        encoding="utf-8",
    )
    events = parse_fold_jsonl_events(p)
    assert len(events) == 1
    assert events[0].kind == "fold"
    assert "manual" in events[0].summary
    assert "hello" in events[0].summary


def test_merge_history_events_sort_and_take():
    from datetime import datetime, timezone

    from scripts.strategy_context import HistoryEvent, merge_history_events

    e1 = HistoryEvent(
        ts=datetime(2026, 1, 1, tzinfo=timezone.utc), kind="a", summary="x"
    )
    e2 = HistoryEvent(
        ts=datetime(2026, 1, 3, tzinfo=timezone.utc), kind="b", summary="y"
    )
    e3 = HistoryEvent(
        ts=datetime(2026, 1, 2, tzinfo=timezone.utc), kind="c", summary="z"
    )
    merged = merge_history_events(
        fold_events=[e1], wc_events=[e2], git_events=[e3], take=2
    )
    assert [m.kind for m in merged] == ["b", "c"]


def test_format_history_section_empty_and_nonempty():
    from datetime import datetime, timezone

    from scripts.strategy_context import HistoryEvent, format_history_section

    assert format_history_section([]) == ""
    ev = HistoryEvent(
        ts=datetime(2026, 4, 16, 12, 0, tzinfo=timezone.utc),
        kind="fold",
        summary="fold manual — 2026-04-16",
    )
    block = format_history_section([ev])
    assert "### Recent strategy activity (lightweight)" in block
    assert "Indicative only" in block
    assert "fold" in block


def test_strategy_context_recent_smoke():
    r = subprocess.run(
        [
            PY,
            str(SCRIPT),
            "-u",
            "grace-mar",
            "--date",
            "2026-04-13",
            "--recent",
            "3",
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    assert "Notebook 2026-04-13" in r.stdout
    # Recent activity section only appears when events exist for the date window
    if "### Recent strategy activity (lightweight)" in r.stdout:
        assert "WORK-choice" in r.stdout or "git" in r.stdout
