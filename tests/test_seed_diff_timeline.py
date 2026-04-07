#!/usr/bin/env python3
"""Tests for Phase 4: Seed Diff View and Seed Timeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def _make_claim(**overrides):
    base = {
        "seed_id": "seed-tl-001",
        "user_slug": "test",
        "claim_text": "reads chapter books",
        "category": "pedagogy",
        "source_events": ["session-001", "session-002"],
        "first_seen": "2026-01-10T00:00:00+00:00",
        "last_seen": "2026-01-25T00:00:00+00:00",
        "observation_count": 2,
        "recurrence_score": 0.45,
        "contradiction_count": 0,
        "contradiction_refs": [],
        "confidence": 0.45,
        "status": "recurring",
        "promotion_readiness": 0.45,
        "sensitivity": "standard",
    }
    base.update(overrides)
    return base


class TestSeedDiff:
    def test_diff_structure(self):
        from emit_seed_diff import build_seed_diff
        claim = _make_claim()
        diff = build_seed_diff(claim, "observed", "recurring")
        assert diff["category"] == "seed_transition"
        assert diff["sourceType"] == "seed"
        assert diff["before"]["status"] == "observed"
        assert diff["after"]["status"] == "recurring"

    def test_diff_has_required_fields(self):
        from emit_seed_diff import build_seed_diff
        claim = _make_claim()
        diff = build_seed_diff(claim, "observed", "recurring")
        assert "schemaVersion" in diff
        assert "diffId" in diff
        assert "changeSummary" in diff
        assert "confidenceDelta" in diff
        assert "recommendedAction" in diff
        assert "whyItMatters" in diff

    def test_candidate_recommends_accept(self):
        from emit_seed_diff import build_seed_diff
        claim = _make_claim(status="candidate")
        diff = build_seed_diff(claim, "recurring", "candidate")
        assert diff["recommendedAction"] == "accept"

    def test_weak_signal_recommends_defer(self):
        from emit_seed_diff import build_seed_diff
        claim = _make_claim(status="weak_signal")
        diff = build_seed_diff(claim, "observed", "weak_signal")
        assert diff["recommendedAction"] == "defer"

    def test_write_diff(self, tmp_path, monkeypatch):
        from emit_seed_diff import build_seed_diff, write_diff
        monkeypatch.setattr("emit_seed_diff.REPO_ROOT", tmp_path)
        user_dir = tmp_path / "users" / "test"
        user_dir.mkdir(parents=True)
        claim = _make_claim()
        diff = build_seed_diff(claim, "observed", "recurring")
        path = write_diff("test", diff)
        assert path.exists()
        loaded = json.loads(path.read_text())
        assert loaded["diffId"] == diff["diffId"]


class TestSchemaExtension:
    def test_seed_transition_in_category(self):
        schema = json.loads(
            (ROOT / "schema-registry" / "identity-diff.v1.json").read_text()
        )
        cats = schema["properties"]["category"]["enum"]
        assert "seed_transition" in cats

    def test_source_type_field(self):
        schema = json.loads(
            (ROOT / "schema-registry" / "identity-diff.v1.json").read_text()
        )
        assert "sourceType" in schema["properties"]
        assert "seed" in schema["properties"]["sourceType"]["enum"]


class TestTimeline:
    @pytest.fixture
    def registry_with_history(self, tmp_path, monkeypatch):
        monkeypatch.setattr("seed_timeline.REPO_ROOT", tmp_path)
        user_dir = tmp_path / "users" / "test"
        user_dir.mkdir(parents=True)
        reg = user_dir / "seed-registry.jsonl"
        snapshots = [
            {"seed_id": "seed-tl-001", "user_slug": "test",
             "claim_text": "reads chapter books", "category": "pedagogy",
             "source_events": ["session-001"], "first_seen": "2026-01-10T00:00:00+00:00",
             "last_seen": "2026-01-10T00:00:00+00:00", "observation_count": 1,
             "recurrence_score": 0.15, "contradiction_count": 0, "contradiction_refs": [],
             "confidence": 0.15, "status": "observed", "promotion_readiness": 0.15,
             "sensitivity": "standard"},
            {"seed_id": "seed-tl-001", "user_slug": "test",
             "claim_text": "reads chapter books", "category": "pedagogy",
             "source_events": ["session-001", "session-002"],
             "first_seen": "2026-01-10T00:00:00+00:00",
             "last_seen": "2026-01-20T00:00:00+00:00", "observation_count": 2,
             "recurrence_score": 0.40, "contradiction_count": 0, "contradiction_refs": [],
             "confidence": 0.40, "status": "weak_signal", "promotion_readiness": 0.40,
             "sensitivity": "standard"},
            {"seed_id": "seed-tl-001", "user_slug": "test",
             "claim_text": "reads chapter books", "category": "pedagogy",
             "source_events": ["session-001", "session-002", "session-003"],
             "first_seen": "2026-01-10T00:00:00+00:00",
             "last_seen": "2026-02-05T00:00:00+00:00", "observation_count": 3,
             "recurrence_score": 0.55, "contradiction_count": 0, "contradiction_refs": [],
             "confidence": 0.55, "status": "recurring", "promotion_readiness": 0.55,
             "sensitivity": "standard"},
        ]
        with reg.open("w") as f:
            for s in snapshots:
                f.write(json.dumps(s) + "\n")
        return reg

    def test_timeline_events(self, registry_with_history):
        from seed_timeline import _load_all_snapshots, build_timeline
        all_snaps = _load_all_snapshots("test")
        events = build_timeline(all_snaps["seed-tl-001"])
        event_types = [e["event"] for e in events]
        assert "first_observed" in event_types
        assert "status_change" in event_types
        assert "new_observation" in event_types

    def test_status_changes_captured(self, registry_with_history):
        from seed_timeline import _load_all_snapshots, build_timeline
        all_snaps = _load_all_snapshots("test")
        events = build_timeline(all_snaps["seed-tl-001"])
        status_changes = [e for e in events if e["event"] == "status_change"]
        assert len(status_changes) == 2
        assert "observed -> weak_signal" in status_changes[0]["detail"]
        assert "weak_signal -> recurring" in status_changes[1]["detail"]

    def test_empty_registry(self, tmp_path, monkeypatch):
        monkeypatch.setattr("seed_timeline.REPO_ROOT", tmp_path)
        from seed_timeline import _load_all_snapshots
        assert _load_all_snapshots("nonexistent") == {}
