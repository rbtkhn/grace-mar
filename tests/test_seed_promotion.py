#!/usr/bin/env python3
"""Tests for Phase 2: Promotion Threshold Engine — rule evaluation, edge cases, contradiction blocking."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


@pytest.fixture
def rules():
    return json.loads((ROOT / "config" / "seed-promotion-rules.json").read_text())


def _make_claim(**overrides):
    base = {
        "seed_id": "seed-test-001",
        "user_slug": "test",
        "claim_text": "test claim",
        "category": "curiosity",
        "source_events": ["session-001", "session-002"],
        "first_seen": "2026-01-01T00:00:00Z",
        "last_seen": "2026-01-15T00:00:00Z",
        "observation_count": 3,
        "recurrence_score": 0.65,
        "contradiction_count": 0,
        "contradiction_refs": [],
        "confidence": 0.65,
        "status": "recurring",
        "promotion_readiness": 0.65,
        "sensitivity": "standard",
    }
    base.update(overrides)
    return base


class TestEvaluateClaim:
    def test_ready_claim(self, rules):
        from evaluate_seed_promotion import evaluate_claim
        claim = _make_claim()
        result = evaluate_claim(claim, rules)
        assert result["verdict"] == "ready"
        assert len(result["blockers"]) == 0

    def test_insufficient_observations(self, rules):
        from evaluate_seed_promotion import evaluate_claim
        claim = _make_claim(observation_count=1, source_events=["session-001"],
                            recurrence_score=0.15)
        result = evaluate_claim(claim, rules)
        assert result["verdict"] != "ready"
        assert any("observations" in b for b in result["blockers"] + result["approaching"])

    def test_insufficient_time_span(self, rules):
        from evaluate_seed_promotion import evaluate_claim
        claim = _make_claim(
            first_seen="2026-01-01T00:00:00Z",
            last_seen="2026-01-02T00:00:00Z",
        )
        result = evaluate_claim(claim, rules)
        assert result["verdict"] == "blocked"
        assert any("time_span" in b for b in result["blockers"])

    def test_contradiction_blocks(self, rules):
        from evaluate_seed_promotion import evaluate_claim
        claim = _make_claim(contradiction_count=1, contradiction_refs=["seed-other"])
        result = evaluate_claim(claim, rules)
        assert result["verdict"] == "blocked"
        assert any("contradiction" in b for b in result["blockers"])

    def test_elevated_sensitivity_stricter(self, rules):
        from evaluate_seed_promotion import evaluate_claim
        claim = _make_claim(sensitivity="elevated", observation_count=2,
                            source_events=["session-001", "session-002"])
        result = evaluate_claim(claim, rules)
        assert result["verdict"] != "ready"

    def test_identity_category_upgrades_sensitivity(self, rules):
        from evaluate_seed_promotion import evaluate_claim
        claim = _make_claim(category="identity", sensitivity="standard",
                            observation_count=2)
        result = evaluate_claim(claim, rules)
        assert any("observations" in b or "operator" in b
                    for b in result["blockers"] + result["approaching"])

    def test_safety_category_is_high(self, rules):
        from evaluate_seed_promotion import evaluate_claim
        claim = _make_claim(category="safety", sensitivity="standard",
                            observation_count=4)
        result = evaluate_claim(claim, rules)
        assert any("operator approval" in b for b in result["blockers"])

    def test_approaching_one_away(self, rules):
        from evaluate_seed_promotion import evaluate_claim
        claim = _make_claim(
            observation_count=1,
            source_events=["session-001"],
            first_seen="2026-01-01T00:00:00Z",
            last_seen="2026-01-15T00:00:00Z",
            recurrence_score=0.55,
        )
        result = evaluate_claim(claim, rules)
        assert any("approaching" in r for r in [result["verdict"]]
                    ) or len(result["approaching"]) > 0


class TestRulesConfig:
    def test_rules_file_exists(self):
        path = ROOT / "config" / "seed-promotion-rules.json"
        assert path.exists()

    def test_rules_valid_json(self, rules):
        assert "defaults" in rules
        assert "sensitivity_overrides" in rules
        assert "category_overrides" in rules

    def test_defaults_present(self, rules):
        d = rules["defaults"]
        assert d["min_observations"] >= 1
        assert d["min_sessions"] >= 1
        assert d["min_time_span_days"] >= 1
        assert 0 < d["recurrence_score_threshold"] <= 1.0
