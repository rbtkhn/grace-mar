"""Tests for personality conflict detection (demo / regression)."""

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "bot"))

from conflict_check import check_conflicts, format_conflicts_for_yaml  # noqa: E402


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
