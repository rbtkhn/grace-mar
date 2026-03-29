"""Tests for scripts/suggest_morning_forks.py deterministic ranking."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import suggest_morning_forks as smf  # noqa: E402


def test_build_fork_scores_returns_sorted_desc():
    rows = smf.build_fork_scores("grace-mar")
    assert len(rows) >= 4
    scores = [r[0] for r in rows]
    assert scores == sorted(scores, reverse=True)


def test_each_fork_has_id_title_why():
    for sc, fid, title, why in smf.build_fork_scores("grace-mar"):
        assert fid
        assert title
        assert why
        assert isinstance(sc, float)


def test_format_markdown_contains_user_and_commands():
    ranked = smf.build_fork_scores("grace-mar")
    md = smf.format_markdown(ranked, top=3, user_id="grace-mar")
    assert "grace-mar" in md
    assert "harness_warmup.py" in md
    assert "log_operator_choice.py" in md
