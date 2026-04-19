"""Unit tests for workflow_depth_control heuristics (deterministic)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
PREP = REPO / "scripts" / "prepared_context"
if str(PREP) not in sys.path:
    sys.path.insert(0, str(PREP))

from workflow_depth_control import (  # noqa: E402
    auto_decide_format,
    count_contradiction_refs,
    depth_to_mode_and_max_obs,
)


def test_depth_to_mode_and_max_obs() -> None:
    assert depth_to_mode_and_max_obs("shallow") == ("compact", 30)
    assert depth_to_mode_and_max_obs("normal") == ("medium", 30)
    assert depth_to_mode_and_max_obs("deep") == ("deep", 30)
    assert depth_to_mode_and_max_obs("exhaustive") == ("deep", 48)


def test_count_contradiction_refs() -> None:
    rows = [
        {"contradiction_refs": ["a", "b"]},
        {"contradiction_refs": None},
        {"contradiction_refs": ["c"]},
    ]
    assert count_contradiction_refs(rows) == 3


def test_auto_no_hits_escalates() -> None:
    mode, reason, phases = auto_decide_format(
        query="iran",
        pool_rows=[],
        compact_scores={
            "total_candidates": 0,
            "utilization": 0.0,
            "coverage": 0.0,
        },
    )
    assert mode == "medium"
    assert reason == "no_ranked_hits_escalate"
    assert any("escalate" in p.get("summary", "").lower() for p in phases)


def test_auto_sufficient_signal_compact() -> None:
    mode, reason, _ = auto_decide_format(
        query="x",
        pool_rows=[{"obs_id": "1"}],
        compact_scores={
            "total_candidates": 10,
            "utilization": 0.4,
            "coverage": 0.3,
        },
    )
    assert mode == "compact"
    assert reason == "sufficient_signal"


def test_auto_contradiction_escalates() -> None:
    pool = [{"contradiction_refs": ["a", "b", "c", "d"]}]
    mode, reason, _ = auto_decide_format(
        query="",
        pool_rows=pool,
        compact_scores={
            "total_candidates": 5,
            "utilization": 0.1,
            "coverage": 0.2,
        },
    )
    assert mode == "medium"
    assert reason == "high_contradiction_density"
