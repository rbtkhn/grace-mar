#!/usr/bin/env python3
"""Tests for Phase 1: Seed Registry — schema, emit, summary, status transitions."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


class TestSchema:
    @pytest.fixture
    def schema(self):
        return json.loads((ROOT / "schema-registry" / "seed-claim.v1.json").read_text())

    def test_required_fields(self, schema):
        expected = {
            "seed_id", "user_slug", "claim_text", "category", "source_events",
            "first_seen", "last_seen", "observation_count", "recurrence_score",
            "contradiction_count", "confidence", "status", "promotion_readiness",
            "sensitivity",
        }
        assert expected == set(schema["required"])

    def test_status_enum(self, schema):
        statuses = set(schema["properties"]["status"]["enum"])
        assert "observed" in statuses
        assert "promoted" in statuses
        assert "expired" in statuses
        assert len(statuses) == 9

    def test_category_enum(self, schema):
        cats = set(schema["properties"]["category"]["enum"])
        assert "identity" in cats
        assert "curiosity" in cats
        assert len(cats) == 7

    def test_sensitivity_enum(self, schema):
        sens = set(schema["properties"]["sensitivity"]["enum"])
        assert sens == {"standard", "elevated", "high"}


class TestEmit:
    @pytest.fixture
    def registry(self, tmp_path, monkeypatch):
        monkeypatch.setattr("emit_seed_claim.REPO_ROOT", tmp_path)
        user_dir = tmp_path / "users" / "test"
        user_dir.mkdir(parents=True)
        return user_dir / "seed-registry.jsonl"

    def test_new_claim(self, registry, monkeypatch):
        from emit_seed_claim import emit_seed_claim
        monkeypatch.setattr("emit_seed_claim.REPO_ROOT", registry.parent.parent.parent)
        row = emit_seed_claim(
            "test", claim_text="likes trains", category="curiosity",
            source_events=["session-001"],
        )
        assert row["observation_count"] == 1
        assert row["status"] == "observed"
        assert row["seed_id"].startswith("seed-")
        assert registry.exists()

    def test_observe_increments(self, registry, monkeypatch):
        from emit_seed_claim import emit_seed_claim
        monkeypatch.setattr("emit_seed_claim.REPO_ROOT", registry.parent.parent.parent)
        row1 = emit_seed_claim(
            "test", claim_text="likes trains", category="curiosity",
            source_events=["session-001"],
        )
        sid = row1["seed_id"]
        row2 = emit_seed_claim(
            "test", seed_id=sid, observe=True, source_events=["session-002"],
        )
        assert row2["observation_count"] == 2
        assert row2["recurrence_score"] > row1["recurrence_score"]

    def test_set_status(self, registry, monkeypatch):
        from emit_seed_claim import emit_seed_claim
        monkeypatch.setattr("emit_seed_claim.REPO_ROOT", registry.parent.parent.parent)
        row = emit_seed_claim(
            "test", claim_text="likes math", category="pedagogy",
            source_events=["s1"],
        )
        updated = emit_seed_claim(
            "test", seed_id=row["seed_id"], status="weak_signal",
        )
        assert updated["status"] == "weak_signal"

    def test_contradiction_ref(self, registry, monkeypatch):
        from emit_seed_claim import emit_seed_claim
        monkeypatch.setattr("emit_seed_claim.REPO_ROOT", registry.parent.parent.parent)
        row = emit_seed_claim(
            "test", claim_text="wants to be pilot", category="identity",
            source_events=["s1"],
        )
        updated = emit_seed_claim(
            "test", seed_id=row["seed_id"], observe=True,
            source_events=["s2"], contradiction_ref="seed-other",
        )
        assert updated["contradiction_count"] == 1
        assert "seed-other" in updated["contradiction_refs"]
        assert updated["confidence"] < row["confidence"] or updated["confidence"] == 0

    def test_missing_claim_text_raises(self, registry, monkeypatch):
        from emit_seed_claim import emit_seed_claim
        monkeypatch.setattr("emit_seed_claim.REPO_ROOT", registry.parent.parent.parent)
        with pytest.raises(ValueError, match="claim_text"):
            emit_seed_claim("test", category="curiosity", source_events=["s1"])

    def test_invalid_category_raises(self, registry, monkeypatch):
        from emit_seed_claim import emit_seed_claim
        monkeypatch.setattr("emit_seed_claim.REPO_ROOT", registry.parent.parent.parent)
        with pytest.raises(ValueError, match="category"):
            emit_seed_claim(
                "test", claim_text="test", category="invalid",
                source_events=["s1"],
            )


class TestRecurrenceScore:
    def test_single_observation(self):
        from emit_seed_claim import compute_recurrence_score
        score = compute_recurrence_score(1, "2026-01-01T00:00:00Z", "2026-01-01T00:00:00Z")
        assert 0 < score < 0.3

    def test_multiple_observations_higher(self):
        from emit_seed_claim import compute_recurrence_score
        s1 = compute_recurrence_score(1, "2026-01-01T00:00:00Z", "2026-01-01T00:00:00Z")
        s3 = compute_recurrence_score(3, "2026-01-01T00:00:00Z", "2026-01-15T00:00:00Z", 3)
        assert s3 > s1

    def test_time_span_matters(self):
        from emit_seed_claim import compute_recurrence_score
        short = compute_recurrence_score(3, "2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z", 3)
        long = compute_recurrence_score(3, "2026-01-01T00:00:00Z", "2026-01-30T00:00:00Z", 3)
        assert long > short


class TestSummary:
    @pytest.fixture
    def populated(self, tmp_path, monkeypatch):
        monkeypatch.setattr("seed_registry_summary.REPO_ROOT", tmp_path)
        user_dir = tmp_path / "users" / "test"
        user_dir.mkdir(parents=True)
        reg = user_dir / "seed-registry.jsonl"
        claims = [
            {"seed_id": "seed-a", "user_slug": "test", "claim_text": "likes A",
             "category": "curiosity", "source_events": ["s1"], "first_seen": "2026-01-01T00:00:00Z",
             "last_seen": "2026-01-01T00:00:00Z", "observation_count": 1,
             "recurrence_score": 0.15, "contradiction_count": 0, "contradiction_refs": [],
             "confidence": 0.15, "status": "observed", "promotion_readiness": 0.15,
             "sensitivity": "standard"},
            {"seed_id": "seed-b", "user_slug": "test", "claim_text": "likes B",
             "category": "identity", "source_events": ["s1", "s2", "s3"], "first_seen": "2026-01-01T00:00:00Z",
             "last_seen": "2026-01-20T00:00:00Z", "observation_count": 3,
             "recurrence_score": 0.65, "contradiction_count": 0, "contradiction_refs": [],
             "confidence": 0.65, "status": "candidate", "promotion_readiness": 0.65,
             "sensitivity": "elevated"},
            {"seed_id": "seed-c", "user_slug": "test", "claim_text": "done C",
             "category": "preference", "source_events": ["s1"], "first_seen": "2026-01-01T00:00:00Z",
             "last_seen": "2026-01-01T00:00:00Z", "observation_count": 1,
             "recurrence_score": 0.15, "contradiction_count": 0, "contradiction_refs": [],
             "confidence": 0.15, "status": "promoted", "promotion_readiness": 0.15,
             "sensitivity": "standard"},
        ]
        with reg.open("w") as f:
            for c in claims:
                f.write(json.dumps(c) + "\n")
        return reg

    def test_load_excludes_terminal(self, populated):
        from seed_registry_summary import load_latest, _filter
        latest = load_latest("test")
        active = _filter(latest)
        ids = {c["seed_id"] for c in active}
        assert "seed-c" not in ids
        assert "seed-a" in ids

    def test_filter_by_status(self, populated):
        from seed_registry_summary import load_latest, _filter
        latest = load_latest("test")
        observed = _filter(latest, status="observed")
        assert len(observed) == 1
        assert observed[0]["seed_id"] == "seed-a"

    def test_ready_filter(self, populated):
        from seed_registry_summary import load_latest, _filter
        latest = load_latest("test")
        ready = _filter(latest, ready=True, readiness_threshold=0.6)
        assert len(ready) == 1
        assert ready[0]["seed_id"] == "seed-b"
