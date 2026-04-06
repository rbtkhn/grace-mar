#!/usr/bin/env python3
"""
Tests for the Record Diff Queue: schema extension, renderer, adapter, and CLI wiring.

Covers both template-portable (schema, renderer, demo data) and instance-specific
(gate adapter, --from-gate CLI) components.
"""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


# ---------------------------------------------------------------------------
# Schema validation tests
# ---------------------------------------------------------------------------

class TestIdentityDiffSchema:
    """Validate the extended identity-diff v1 schema accepts new fields."""

    @pytest.fixture
    def schema(self):
        return json.loads((ROOT / "schema-registry" / "identity-diff.v1.json").read_text())

    def test_schema_has_recommended_action(self, schema):
        assert "recommendedAction" in schema["properties"]
        ra = schema["properties"]["recommendedAction"]
        assert ra["type"] == "string"
        assert set(ra["enum"]) == {"accept", "reject", "defer", "merge_partially"}

    def test_schema_has_why_it_matters(self, schema):
        assert "whyItMatters" in schema["properties"]
        wim = schema["properties"]["whyItMatters"]
        assert wim["type"] == "string"
        assert wim.get("minLength") == 1

    def test_new_fields_are_optional(self, schema):
        required = schema["required"]
        assert "recommendedAction" not in required
        assert "whyItMatters" not in required

    def test_existing_required_fields_unchanged(self, schema):
        expected = {"schemaVersion", "diffId", "userSlug", "category", "before", "after", "changeSummary", "evidenceRefs"}
        assert expected == set(schema["required"])


# ---------------------------------------------------------------------------
# Demo data tests
# ---------------------------------------------------------------------------

class TestDemoData:
    """Validate demo diffs conform to the extended schema."""

    @pytest.fixture
    def diff_001(self):
        return json.loads((ROOT / "users" / "demo" / "review-queue" / "diffs" / "diff-001.json").read_text())

    @pytest.fixture
    def diff_002(self):
        return json.loads((ROOT / "users" / "demo" / "review-queue" / "diffs" / "diff-002.json").read_text())

    def test_diff_001_has_new_fields(self, diff_001):
        assert diff_001["recommendedAction"] == "accept"
        assert "whyItMatters" in diff_001
        assert len(diff_001["whyItMatters"]) > 0

    def test_diff_002_exists_and_valid(self, diff_002):
        assert diff_002["schemaVersion"] == "1.0.0"
        assert diff_002["diffId"] == "diff-002"
        assert diff_002["category"] == "curiosity"
        assert len(diff_002["evidenceRefs"]) >= 1

    def test_diff_002_has_conflict_note(self, diff_002):
        assert "conflictNote" in diff_002
        assert len(diff_002["conflictNote"]) > 0

    def test_diff_002_recommended_action(self, diff_002):
        assert diff_002["recommendedAction"] == "defer"


# ---------------------------------------------------------------------------
# Renderer tests
# ---------------------------------------------------------------------------

class TestRenderer:
    """Test render_record_diff_queue.py logic."""

    @pytest.fixture
    def sample_diff(self):
        return {
            "schemaVersion": "1.0.0",
            "diffId": "diff-test-001",
            "userSlug": "test-user",
            "category": "curiosity",
            "before": {"topic": "space", "depth": "surface"},
            "after": {"topic": "space", "depth": "active"},
            "changeSummary": "Upgrade space interest to active curiosity.",
            "evidenceRefs": ["session-001"],
            "confidenceDelta": {"before": 0.3, "after": 0.8},
            "conflictNote": "Contradicts earlier disinterest signal.",
            "recommendedAction": "accept",
            "whyItMatters": "First sustained STEM curiosity.",
        }

    def test_render_card_contains_all_fields(self, sample_diff):
        from render_record_diff_queue import render_card

        card = render_card(sample_diff)
        assert "diff-test-001" in card
        assert "curiosity" in card
        assert "test-user" in card
        assert "space" in card
        assert "Upgrade space interest" in card
        assert "First sustained STEM curiosity" in card
        assert "session-001" in card
        assert "0.3" in card
        assert "0.8" in card
        assert "Contradicts earlier disinterest" in card
        assert "Accept" in card

    def test_render_card_without_optional_fields(self):
        from render_record_diff_queue import render_card

        minimal = {
            "schemaVersion": "1.0.0",
            "diffId": "diff-minimal",
            "userSlug": "test",
            "category": "identity",
            "before": {"state": "none"},
            "after": {"state": "new"},
            "changeSummary": "A minimal diff.",
            "evidenceRefs": ["ref-1"],
        }
        card = render_card(minimal)
        assert "diff-minimal" in card
        assert "A minimal diff" in card
        assert "Why It Matters" not in card
        assert "Recommended Action" not in card

    def test_render_queue_sorts_by_confidence_delta(self):
        from render_record_diff_queue import render_queue

        d1 = {
            "schemaVersion": "1.0.0", "diffId": "diff-small",
            "userSlug": "t", "category": "identity",
            "before": {}, "after": {}, "changeSummary": "small",
            "evidenceRefs": ["r"], "confidenceDelta": {"before": 0.5, "after": 0.6},
        }
        d2 = {
            "schemaVersion": "1.0.0", "diffId": "diff-large",
            "userSlug": "t", "category": "identity",
            "before": {}, "after": {}, "changeSummary": "large",
            "evidenceRefs": ["r"], "confidenceDelta": {"before": 0.1, "after": 0.9},
        }
        md = render_queue([d1, d2])
        pos_large = md.index("diff-large")
        pos_small = md.index("diff-small")
        assert pos_large < pos_small, "Higher confidence delta should appear first"

    def test_render_queue_header(self):
        from render_record_diff_queue import render_queue

        d = {
            "schemaVersion": "1.0.0", "diffId": "diff-x",
            "userSlug": "t", "category": "identity",
            "before": {}, "after": {}, "changeSummary": "x",
            "evidenceRefs": ["r"],
        }
        md = render_queue([d])
        assert md.startswith("# Record Diff Queue")
        assert "1 pending change(s)" in md

    def test_collect_diffs_from_demo_dir(self):
        from render_record_diff_queue import collect_diffs

        diffs = collect_diffs(["users/demo/review-queue/diffs/"])
        assert len(diffs) >= 2
        ids = {d["diffId"] for d in diffs}
        assert "diff-001" in ids
        assert "diff-002" in ids


# ---------------------------------------------------------------------------
# Gate adapter tests
# ---------------------------------------------------------------------------

class TestGateAdapter:
    """Test gate_to_diff_adapter.py conversion logic."""

    SAMPLE_YAML = textwrap.dedent("""\
        status: pending
        timestamp: 2026-04-01
        channel_key: operator:cursor
        source: test exchange
        mind_category: curiosity
        signal_type: we_did
        priority_score: 4
        summary: Discovered interest in volcanoes through a science activity.
        profile_target: IX-B. CURIOSITY
        suggested_entry: "Volcanoes — active curiosity from science activity, three follow-up questions."
        prompt_section: YOUR CURIOSITY
        prompt_addition: You're curious about volcanoes.
        suggested_followup: Try a volcano experiment next session.
    """)

    def test_candidate_to_diff_produces_valid_structure(self):
        from gate_to_diff_adapter import candidate_to_diff

        diff = candidate_to_diff("CANDIDATE-9999", "Test candidate", self.SAMPLE_YAML, "")
        assert diff["schemaVersion"] == "1.0.0"
        assert diff["diffId"] == "diff-gate-CANDIDATE-9999"
        assert diff["category"] == "curiosity"
        assert "Volcanoes" in diff["after"]["entry"]
        assert diff["changeSummary"] == "Discovered interest in volcanoes through a science activity."
        assert len(diff["evidenceRefs"]) >= 1
        assert diff["confidenceDelta"]["after"] == 0.9  # priority 4 -> 0.5 + 0.4
        assert diff["whyItMatters"] == "Try a volcano experiment next session."

    def test_non_pending_candidate_returns_empty(self):
        from gate_to_diff_adapter import candidate_to_diff

        yaml = self.SAMPLE_YAML.replace("status: pending", "status: approved")
        diff = candidate_to_diff("CANDIDATE-0001", "Approved", yaml, "")
        assert diff == {}

    def test_quick_merge_sets_accept(self):
        from gate_to_diff_adapter import candidate_to_diff

        yaml = self.SAMPLE_YAML + "ready_for_quick_merge: true\n"
        diff = candidate_to_diff("CANDIDATE-0002", "Quick", yaml, "")
        assert diff.get("recommendedAction") == "accept"

    def test_conflict_detected_mapped(self):
        from gate_to_diff_adapter import candidate_to_diff

        yaml = self.SAMPLE_YAML + "conflicts_detected: Contradicts previous disinterest.\n"
        diff = candidate_to_diff("CANDIDATE-0003", "Conflict", yaml, "")
        assert diff.get("conflictNote") == "Contradicts previous disinterest."

    def test_conflict_none_not_mapped(self):
        from gate_to_diff_adapter import candidate_to_diff

        yaml = self.SAMPLE_YAML + "conflicts_detected: none\n"
        diff = candidate_to_diff("CANDIDATE-0004", "No conflict", yaml, "")
        assert "conflictNote" not in diff


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------

class TestCLI:
    """Integration tests for the renderer CLI."""

    def test_renderer_on_demo_data(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "render_record_diff_queue.py"),
             "users/demo/review-queue/diffs/"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode == 0
        assert "Record Diff Queue" in result.stdout
        assert "diff-001" in result.stdout
        assert "diff-002" in result.stdout

    def test_renderer_json_mode(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "render_record_diff_queue.py"),
             "--json", "users/demo/review-queue/diffs/"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_renderer_output_file(self, tmp_path):
        out = tmp_path / "queue.md"
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "render_record_diff_queue.py"),
             "--output", str(out), "users/demo/review-queue/diffs/"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode == 0
        assert out.exists()
        content = out.read_text()
        assert "Record Diff Queue" in content

    def test_adapter_cli(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "gate_to_diff_adapter.py"),
             "-u", "grace-mar"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode == 0

    def test_renderer_from_gate(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "render_record_diff_queue.py"),
             "--from-gate", "-u", "grace-mar"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        # May return 0 (with diffs) or 1 (no pending candidates) — both are valid
        assert result.returncode in (0, 1)

    def test_renderer_no_args_errors(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "render_record_diff_queue.py")],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode != 0
