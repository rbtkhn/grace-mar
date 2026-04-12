"""generate_scenarios — factorial matrix expansion (BUILD-AI-GAP-005)."""

from __future__ import annotations

from scripts.work_dev.generate_scenarios import build_matrix


def test_handback_tail_stress_openclaw_eight_stressors() -> None:
    """handback_tail_stress.yaml: 1 runtime × 8 stressor dimension values."""
    rows = build_matrix(scenario_filter="handback_tail", runtimes=["openclaw"])
    assert len(rows) == 8
    stressor_tags = []
    for r in rows:
        assert r.scenario_id == "handback_tail_stress"
        assert r.runtime == "openclaw"
        assert "handback_analysis" in r.required_checks
        assert r.values.get("base_task") == "stage_openclaw_handback"
        s = r.values.get("stressor")
        assert s is not None
        stressor_tags.append(str(s))
    assert sorted(stressor_tags) == [
        "V-01_minimize",
        "V-02_authority",
        "V-03_time_pressure",
        "V-04_structured_conflict",
        "V-05_tool_failure",
        "V-06_hedging",
        "V-07_contradictory_prior",
        "V-08_ood_tail",
    ]
