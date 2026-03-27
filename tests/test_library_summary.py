"""Tests for bot.core._library_summary ordering (lane + lookup_priority)."""

import re
from unittest.mock import patch

import bot.core as core


def _titles_from_summary(summary: str) -> list[str]:
    titles = []
    for ln in summary.strip().split("\n"):
        m = re.match(r"- \[[^/]+/[^]]+\] (.+): ", ln)
        if m:
            titles.append(m.group(1))
    return titles


def test_library_summary_lookup_priority_order_within_lane():
    """preferred < high < medium < low < none within the same lane; title tie-breaks last."""
    fake = [
        {"title": "Zebra Book", "scope": ["x"], "volume": None, "lane": "reference", "lookup_priority": "high"},
        {"title": "Alpha Book", "scope": ["x"], "volume": None, "lane": "reference", "lookup_priority": "preferred"},
        {"title": "Beta Book", "scope": ["x"], "volume": None, "lane": "reference", "lookup_priority": "low"},
        {"title": "Gamma Book", "scope": ["x"], "volume": None, "lane": "reference", "lookup_priority": "medium"},
        {"title": "Delta Book", "scope": ["x"], "volume": None, "lane": "reference", "lookup_priority": "none"},
    ]
    with patch.object(core, "_load_library", return_value=fake):
        summary = core._library_summary()
    assert _titles_from_summary(summary) == [
        "Alpha Book",
        "Zebra Book",
        "Gamma Book",
        "Beta Book",
        "Delta Book",
    ]


def test_library_summary_lane_sorts_before_lookup_priority():
    """reference (any priority) before canon before influence; lane dominates over preferred."""
    fake = [
        {"title": "Canon Preferred", "scope": [], "volume": None, "lane": "canon", "lookup_priority": "preferred"},
        {"title": "Ref High", "scope": [], "volume": None, "lane": "reference", "lookup_priority": "high"},
        {"title": "Influence Low", "scope": [], "volume": None, "lane": "influence", "lookup_priority": "low"},
    ]
    with patch.object(core, "_load_library", return_value=fake):
        summary = core._library_summary()
    assert _titles_from_summary(summary) == ["Ref High", "Canon Preferred", "Influence Low"]
