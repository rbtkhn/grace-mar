"""Unit tests for workflow_depth_control heuristics (deterministic)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
PREP = REPO / "scripts" / "prepared_context"
if str(PREP) not in sys.path:
    sys.path.insert(0, str(PREP))

from workflow_depth_control import (  # noqa: E402
    THRESHOLD_ANCHOR_DRIFT_RISK,
    THRESHOLD_DUPLICATE_EVIDENCE_RATIO,
    THRESHOLD_MARGINAL_SUPPORT_GAIN,
    THRESHOLD_POOL_MIN_FOR_DIMINISHING,
    auto_decide_format,
    count_contradiction_refs,
    depth_to_mode_and_max_obs,
)


def _unpack(res: tuple):
    mode, reason, phases, guard = res
    return mode, reason, phases, guard


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
    mode, reason, phases, guard = _unpack(
        auto_decide_format(
            query="iran",
            pool_rows=[],
            compact_scores={
                "total_candidates": 0,
                "utilization": 0.0,
                "coverage": 0.0,
            },
        )
    )
    assert mode == "medium"
    assert reason == "no_ranked_hits_escalate"
    assert any("escalate" in p.get("summary", "").lower() for p in phases)
    assert any(p.get("phase") == "phase_2_quality_guard" for p in phases)
    assert "guard_summary" in guard


def test_auto_sufficient_signal_compact() -> None:
    mode, reason, _, guard = _unpack(
        auto_decide_format(
            query="x",
            pool_rows=[{"obs_id": "1"}],
            compact_scores={
                "total_candidates": 10,
                "utilization": 0.4,
                "coverage": 0.3,
            },
        )
    )
    assert mode == "compact"
    assert reason == "sufficient_signal"
    assert guard.get("guard_summary") is not None


def test_auto_contradiction_escalates() -> None:
    pool = [{"contradiction_refs": ["a", "b", "c", "d"]}]
    mode, reason, _, _ = _unpack(
        auto_decide_format(
            query="",
            pool_rows=pool,
            compact_scores={
                "total_candidates": 5,
                "utilization": 0.1,
                "coverage": 0.2,
            },
        )
    )
    assert mode == "medium"
    assert reason == "high_contradiction_density"


def test_duplicate_evidence_bloom_halts_low_util_escalation() -> None:
    """Most pool rows repeat the same title as compact-selected evidence."""
    selected = [{"obs_id": "sel1", "title": "Duplicate Bloom Topic", "source_refs": []}]
    pool_rows = [
        {"obs_id": f"p{i}", "title": "Duplicate Bloom Topic", "source_refs": [], "summary": f"s{i}"}
        for i in range(8)
    ]
    mode, reason, phases, guard = _unpack(
        auto_decide_format(
            query="q",
            pool_rows=pool_rows,
            compact_scores={
                "total_candidates": 8,
                "utilization": 0.1,
                "coverage": 0.2,
                "chars_included": 100,
            },
            task_anchor="review duplicate bloom",
            compact_included_rows=selected,
        )
    )
    assert mode == "compact"
    assert reason == "duplicate_evidence_bloom"
    qg = next(p for p in phases if p.get("phase") == "phase_2_quality_guard")
    assert qg["halt_continue"] == "halt"
    assert qg["recommended_stop_reason"] == "duplicate_evidence_bloom"
    assert qg["signal"] == "duplicate_evidence_ratio"
    assert float(qg["signal_value"]) >= THRESHOLD_DUPLICATE_EVIDENCE_RATIO
    assert guard["stop_signal"] == "duplicate_evidence_ratio"
    assert guard["guard_veto"] is True
    assert "new_total_items" in guard["guard_summary"]


def test_diminishing_returns_halts_low_util_escalation() -> None:
    """Pool is large but almost all obs_ids already in compact selection; only four pool rows repeat selected titles so duplicate ratio stays below bloom threshold."""
    selected = [{"obs_id": f"o{i}", "title": f"SelTitle{i}", "source_refs": []} for i in range(7)]
    pool_rows = []
    for i in range(8):
        if i < 4:
            title = f"SelTitle{i}"
        else:
            title = f"PoolOnlyTitle{i}xyz"
        pool_rows.append({"obs_id": f"o{i}", "title": title, "source_refs": [f"ref/{i}"]})
    mode, reason, phases, guard = _unpack(
        auto_decide_format(
            query="q",
            pool_rows=pool_rows,
            compact_scores={
                "total_candidates": 8,
                "utilization": 0.1,
                "coverage": 0.15,
                "chars_included": 50,
            },
            task_anchor="marginal gain test",
            compact_included_rows=selected,
        )
    )
    assert mode == "compact"
    assert reason == "diminishing_returns"
    qg = next(p for p in phases if p.get("phase") == "phase_2_quality_guard")
    assert qg["recommended_stop_reason"] == "diminishing_returns"
    assert qg["signal"] == "marginal_support_gain"
    assert len(pool_rows) >= THRESHOLD_POOL_MIN_FOR_DIMINISHING
    assert float(qg["signal_value"]) <= THRESHOLD_MARGINAL_SUPPORT_GAIN
    assert guard["stop_signal"] == "marginal_support_gain"


def test_anchor_drift_risk_halts_low_util_escalation() -> None:
    """Narrow anchor tokens vs generic pool text → high drift (dup ratio and marginal stay below other thresholds)."""
    pool_rows = []
    for i in range(8):
        row = {
            "obs_id": f"g{i}",
            "title": f"Shared title dup {i % 4}" if i < 4 else f"Unique title chunk {i}",
            "summary": "general meeting observation status update notes" if i >= 4 else "shared line",
            "source_refs": [f"ref/only{i}"],
        }
        pool_rows.append(row)
    selected = [dict(pool_rows[0])]
    mode, reason, phases, guard = _unpack(
        auto_decide_format(
            query="q",
            pool_rows=pool_rows,
            compact_scores={
                "total_candidates": 8,
                "utilization": 0.1,
                "coverage": 0.12,
                "chars_included": 40,
            },
            task_anchor="cryptography lattice protocol quantum resistance specification uniqueword",
            compact_included_rows=selected,
        )
    )
    assert mode == "compact"
    assert reason == "anchor_drift_risk"
    qg = next(p for p in phases if p.get("phase") == "phase_2_quality_guard")
    assert qg["signal"] == "anchor_drift_risk"
    assert float(qg["signal_value"]) >= THRESHOLD_ANCHOR_DRIFT_RISK
    assert guard["stop_signal"] == "anchor_drift_risk"


def test_healthy_low_util_still_escalates_to_medium() -> None:
    """Distinct pool rows, anchor words overlap pool, marginal support not depleted."""
    pool_rows = [
        {
            "obs_id": f"h{i}",
            "title": f"Strategy lattice review {i}",
            "summary": "cryptography protocol analysis quantum resistance",
            "source_refs": [f"unique/ref/{i}"],
        }
        for i in range(8)
    ]
    selected = [{"obs_id": "h0", "title": "Strategy lattice review 0", "summary": "cryptography", "source_refs": ["unique/ref/0"]}]
    mode, reason, phases, guard = _unpack(
        auto_decide_format(
            query="q",
            pool_rows=pool_rows,
            compact_scores={
                "total_candidates": 8,
                "utilization": 0.1,
                "coverage": 0.18,
                "chars_included": 200,
            },
            task_anchor="cryptography lattice protocol quantum",
            compact_included_rows=selected,
        )
    )
    assert mode == "medium"
    assert reason == "low_utilization_escalate"
    qg = next(p for p in phases if p.get("phase") == "phase_2_quality_guard")
    assert qg["halt_continue"] == "continue"
    assert qg["recommended_stop_reason"] == ""
    assert guard.get("guard_veto") is not True
    assert "stop_signal" in guard


def test_guard_receipt_has_expected_keys() -> None:
    _, _, _, guard = _unpack(
        auto_decide_format(
            query="q",
            pool_rows=[{"obs_id": f"p{i}", "title": "Dup", "source_refs": []} for i in range(8)],
            compact_scores={"total_candidates": 8, "utilization": 0.1, "coverage": 0.2, "chars_included": 1},
            task_anchor="x",
            compact_included_rows=[{"obs_id": "s", "title": "Dup", "source_refs": []}],
        )
    )
    assert "guard_summary" in guard
    assert isinstance(guard["guard_summary"], dict)


def test_governance_module_has_no_record_write_paths() -> None:
    """PR 4: workflow_depth_control stays a prepared-context helper — no gate/SELF paths."""
    src = (PREP / "workflow_depth_control.py").read_text(encoding="utf-8")
    assert "self.md" not in src
    assert "recursion-gate.md" not in src
    assert "process_approved_candidates" not in src
