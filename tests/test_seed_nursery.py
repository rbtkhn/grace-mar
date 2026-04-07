#!/usr/bin/env python3
"""Tests for Phase 3: Weak Signal Nursery — report generation, explanations."""

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
        "seed_id": "seed-nurs-001",
        "user_slug": "test",
        "claim_text": "enjoys painting",
        "category": "expression",
        "source_events": ["session-001"],
        "first_seen": "2026-01-10T00:00:00Z",
        "last_seen": "2026-01-10T00:00:00Z",
        "observation_count": 1,
        "recurrence_score": 0.15,
        "contradiction_count": 0,
        "contradiction_refs": [],
        "confidence": 0.15,
        "status": "observed",
        "promotion_readiness": 0.15,
        "sensitivity": "standard",
    }
    base.update(overrides)
    return base


class TestNurseryCard:
    def test_still_seed_has_reasons(self, rules):
        from seed_nursery_report import nursery_card
        claim = _make_claim()
        card = nursery_card(claim, rules)
        assert len(card["still_seed_because"]) > 0
        assert any("recurrence" in r or "observation" in r for r in card["still_seed_because"])

    def test_would_mature_has_guidance(self, rules):
        from seed_nursery_report import nursery_card
        claim = _make_claim()
        card = nursery_card(claim, rules)
        assert len(card["would_mature_with"]) > 0

    def test_falsification_always_present(self, rules):
        from seed_nursery_report import nursery_card
        claim = _make_claim()
        card = nursery_card(claim, rules)
        assert len(card["would_falsify_with"]) >= 1

    def test_contradiction_shows_refs(self, rules):
        from seed_nursery_report import nursery_card
        claim = _make_claim(
            contradiction_count=1,
            contradiction_refs=["seed-other"],
            notes="contradicts other claim",
        )
        card = nursery_card(claim, rules)
        assert any("seed-other" in r for r in card["would_falsify_with"])
        assert any("contradiction" in r for r in card["still_seed_because"])

    def test_observed_does_not_affect_behavior(self, rules):
        from seed_nursery_report import nursery_card
        claim = _make_claim(status="observed")
        card = nursery_card(claim, rules)
        assert card["affects_behavior"] is False

    def test_recurring_may_affect_behavior(self, rules):
        from seed_nursery_report import nursery_card
        claim = _make_claim(status="recurring")
        card = nursery_card(claim, rules)
        assert card["affects_behavior"] is True

    def test_review_date_computed(self, rules):
        from seed_nursery_report import nursery_card
        claim = _make_claim()
        card = nursery_card(claim, rules)
        assert card["review_by"] != "unknown"

    def test_expiry_date_used_if_present(self, rules):
        from seed_nursery_report import nursery_card
        claim = _make_claim(expiry_review_date="2026-06-01")
        card = nursery_card(claim, rules)
        assert card["review_by"] == "2026-06-01"

    def test_ready_claim_says_ready(self, rules):
        from seed_nursery_report import nursery_card
        claim = _make_claim(
            observation_count=5,
            source_events=["session-001", "session-002", "session-003"],
            first_seen="2026-01-01T00:00:00Z",
            last_seen="2026-02-01T00:00:00Z",
            recurrence_score=0.8,
            confidence=0.8,
            status="candidate",
        )
        card = nursery_card(claim, rules)
        assert any("ready" in r or "meets all" in r for r in card["still_seed_because"])

    def test_elevated_sensitivity_mentions_operator(self, rules):
        from seed_nursery_report import nursery_card
        claim = _make_claim(sensitivity="elevated", category="identity")
        card = nursery_card(claim, rules)
        assert any("operator" in r for r in card["still_seed_because"] + card["would_mature_with"])
