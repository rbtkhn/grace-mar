"""Tests for reflection cycle (no OpenAI calls)."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_filter_review_candidates_signal_type():
    from scripts.recursion_gate_review import filter_review_candidates

    rows = [
        {"id": "CANDIDATE-0001", "status": "pending", "signal_type": "reflection-cycle"},
        {"id": "CANDIDATE-0002", "status": "pending", "signal_type": "operator_paste"},
    ]
    out = filter_review_candidates(rows, status="pending", signal_type="reflection-cycle")
    assert len(out) == 1
    assert out[0]["id"] == "CANDIDATE-0001"


def test_collect_bundle_has_slices():
    from grace_mar.reflection.collect import collect_bundle

    b = collect_bundle(
        user_id="grace-mar",
        repo_root=REPO_ROOT,
        lookback_days=14,
        transcript_tail_chars=5000,
        max_jsonl_lines=50,
        max_processed_chars=20_000,
        negative_examples_max_chars=2000,
    )
    assert b.user_id == "grace-mar"
    assert len(b.slices) >= 1
    ctx = b.as_prompt_context(50_000)
    assert "users/grace-mar" in ctx or len(ctx) == 0


def test_build_reflection_candidate_block_shape():
    from grace_mar.reflection.format_gate import build_reflection_candidate_block

    prop = {
        "summary": "Test reflection proposal",
        "suggested_entry": "Suggested line for IX",
        "mind_category": "knowledge",
        "profile_target": "IX-A. KNOWLEDGE",
        "prompt_section": "YOUR KNOWLEDGE",
        "prompt_addition": "none",
        "source_exchange": "Operator narrative.",
        "evidence_citations": [
            "users/grace-mar/session-transcript.md:lines 10-20",
            "users/grace-mar/pipeline-events.jsonl:tail",
        ],
        "rationale": "Because excerpts show pattern X.",
        "confidence": 0.75,
        "priority_score": 80,
        "reflection_axis": "record",
        "risk_level": "low",
        "impact_level": "medium",
        "channel_key": "reflection-cycle",
        "signal_type": "reflection-cycle",
    }
    block = build_reflection_candidate_block(
        candidate_id="CANDIDATE-0999",
        reflection_cycle_id="REFLECT-20990101-001",
        timestamp="2099-01-01 12:00:00",
        title_summary="Test",
        proposal=prop,
        full_analysis_rel="reflection-proposals/REFLECT-20990101-001.md",
    )
    assert "CANDIDATE-0999" in block
    assert "reflection_cycle_id: REFLECT-20990101-001" in block
    assert "signal_type: reflection-cycle" in block
    assert "status: pending" in block


def test_run_reflection_engine_dry_run():
    from grace_mar.reflection.collect import collect_bundle
    from grace_mar.reflection.engine import run_reflection_engine

    b = collect_bundle(
        user_id="grace-mar",
        repo_root=REPO_ROOT,
        lookback_days=7,
        transcript_tail_chars=2000,
        max_jsonl_lines=20,
        max_processed_chars=5000,
        negative_examples_max_chars=500,
    )
    r = run_reflection_engine(b, dry_run=True, max_proposals=5)
    assert r.proposals
    assert len(r.proposals[0].get("evidence_citations") or []) >= 2


def test_allow_high_risk_empty_gate_ok(tmp_path: Path):
    from grace_mar.reflection.rate_limit import allow_high_risk_proposal

    profile = tmp_path / "u"
    profile.mkdir()
    (profile / "recursion-gate.md").write_text("## Candidates\n## Processed\n", encoding="utf-8")
    ok, msg = allow_high_risk_proposal(profile_dir=profile, force=False)
    assert ok
    assert msg == "ok"
