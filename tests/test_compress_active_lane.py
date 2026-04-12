"""Active lane compression — paths and payload shape."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def test_work_strategy_lane_payload():
    import compress_active_lane

    p = compress_active_lane.build_active_lane_payload("work-strategy", "grace-mar", REPO)
    assert p["lane"] == "work-strategy"
    assert "current_objective" in p
    assert "relevant_source_paths" in p
    paths = p["relevant_source_paths"]
    assert any("docs/skill-work/work-strategy/" in x for x in paths)
    assert any("users/grace-mar/self-work.md" in x for x in paths)

    md = compress_active_lane.build_active_lane_markdown(p)
    assert "work-strategy" in md
    assert "docs/skill-work/work-strategy" in md


def test_unknown_lane_errors():
    import compress_active_lane

    with pytest.raises(FileNotFoundError):
        compress_active_lane.build_active_lane_payload("work-nonexistent-lane-xyz", "grace-mar", REPO)
