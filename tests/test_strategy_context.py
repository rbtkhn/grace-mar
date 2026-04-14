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

### Signal
- x

### Open
- First open
- Second **bold**

## 2026-04-02
### Open
- other
"""
    block = extract_day_block(md, "2026-04-01")
    assert block is not None
    open_body = extract_h3_section(block, "Open")
    bullets = open_bullet_lines(open_body, limit=5)
    assert bullets[0] == "First open"
    assert "bold" in bullets[1]


def test_truncate_words():
    from scripts.strategy_context import truncate_words

    s = " ".join([f"w{i}" for i in range(200)])
    out = truncate_words(s, 10)
    assert len(out.split()) <= 10
    assert out.endswith("…")


def test_count_analyst_rows_sample():
    from scripts.strategy_context import count_analyst_table_rows

    sample = """
| analyst_id | Anchor |
|------------|--------|
| `foo-bar` | Name |
| `baz` | Other |
"""
    assert count_analyst_table_rows(sample) == 2


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
