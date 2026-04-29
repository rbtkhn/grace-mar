"""Smoke tests for scripts/recommend_route.py (advisory route receipt)."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module():
    root = Path(__file__).resolve().parents[1]
    path = root / "scripts" / "recommend_route.py"
    spec = importlib.util.spec_from_file_location("recommend_route", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod, root


def _config(mod, root):
    return mod.load_config(root / "config" / "route_recommendation.json")


def test_coding_vs_research_shapes():
    mod, root = _load_module()
    cfg = _config(mod, root)
    d = mod.infer_recommendation(
        "Refactor this Python utility and compare two architecture options.",
        cfg,
        None,
    )
    assert d["task_shape"] == "coding"
    assert d["confidence"] in ("high", "medium")

    d2 = mod.infer_recommendation(
        "Read these sources, synthesize the market picture, and draft a memo for the strategy inbox.",
        cfg,
        None,
    )
    assert d2["task_shape"] == "research_to_artifact"


def test_governance_requires_gate_review():
    mod, root = _load_module()
    cfg = _config(mod, root)
    d = mod.infer_recommendation("Should this candidate become durable knowledge?", cfg, None)
    assert d["task_shape"] == "governance_review"
    assert d["requires_gate_review"] is True


def test_unclear_vague_fallback():
    mod, root = _load_module()
    cfg = _config(mod, root)
    d = mod.infer_recommendation("Do something smart with this.", cfg, None)
    assert d["task_shape"] == "unclear"
    assert d["confidence"] == "low"
    assert "clarify" in d["suggested_next_step"].lower() or "sentence" in d["suggested_next_step"].lower()


def test_render_receipt_includes_yaml_and_sections():
    mod, root = _load_module()
    cfg = _config(mod, root)
    d = mod.infer_recommendation(
        "Set up a recurring weekly digest across tools.", cfg, None
    )
    assert d["task_shape"] == "recurring_workflow"
    body = mod.render_receipt_markdown(d, "2026-01-01T00:00:00+00:00")
    assert "---" in body and "kind: route-recommendation" in body
    assert "# Route Recommendation" in body
    assert "Governance note" in body


def test_forbidden_under_users_returns_true():
    """Staging derived receipts under ``users/*`` is forbidden."""
    mod, repo = _load_module()
    under_users = repo / "users" / "grace-mar" / "hypothetical-route-receipt.md"
    assert mod.is_forbidden_record_path(under_users, repo) is True



def test_work_strategy_lane_hint_boosts_scores():
    mod, root = _load_module()
    cfg = _config(mod, root)
    blob = "Synthesize summaries from transcripts into notebook prose."
    a = mod.score_shapes(blob, cfg, None)["research_to_artifact"]
    b = mod.score_shapes(blob, cfg, "work-strategy")["research_to_artifact"]
    assert b >= a

