"""Tests for scripts/menu_choice_evolution.py aggregation."""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import menu_choice_evolution as mce  # noqa: E402


def _ts(days_ago: int) -> str:
    dt = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def test_parse_blocks_counts_recent():
    raw = f"""
### [WORK-choice] {_ts(2)}
- context: WORK
- picked: A

### [WORK-choice] {_ts(2)}
- context: WORK
- picked: B

### [WORK-choice] {_ts(40)}
- context: WORK
- picked: Z
"""
    since = datetime.now(timezone.utc) - timedelta(days=30)
    rows = mce.parse_blocks(raw, since=since)
    picks = [r["picked"] for r in rows]
    assert "A" in picks and "B" in picks
    assert "Z" not in picks
