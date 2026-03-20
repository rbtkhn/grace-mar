"""Tests for personality conflict detection (demo / regression)."""

# Import via package path only. Do not prepend REPO/bot to sys.path — that makes
# `import bot` load bot/bot.py as a top-level module and breaks `from .core` in bot/bot.py
# for later tests (e.g. test_voice importing bot.prompt).

import pytest

from bot.conflict_check import check_conflicts, format_conflicts_for_yaml


def test_personality_non_personality_skipped():
    yaml = "mind_category: knowledge\nsummary: likes dinosaurs\nsuggested_entry: T-Rex"
    assert check_conflicts(yaml) == []


def test_format_empty():
    assert format_conflicts_for_yaml([]) == ""


def test_dependent_vs_independent_when_profile_has_independent():
    """grace-mar self.md seed includes trait: independent."""
    yaml = """
mind_category: personality
summary: Student was dependent on teacher cues today
suggested_entry: "Dependent in structured class"
""".strip()
    hits = check_conflicts(yaml)
    pairs = [tuple(h["pair"]) for h in hits]
    assert ("dependent", "independent") in pairs or ("independent", "dependent") in pairs
