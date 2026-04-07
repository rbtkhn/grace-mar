#!/usr/bin/env python3
"""Tests for Phase 5: Seed Phase Doctrine — doc exists, manifest field, cross-references."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


class TestDoctrine:
    def test_doctrine_doc_exists(self):
        assert (ROOT / "docs" / "seed-phase-doctrine.md").exists()

    def test_doctrine_has_seven_principles(self):
        text = (ROOT / "docs" / "seed-phase-doctrine.md").read_text()
        for i in range(1, 8):
            assert f"### {i}." in text, f"Principle {i} not found"

    def test_doctrine_cross_references(self):
        text = (ROOT / "docs" / "seed-phase-doctrine.md").read_text()
        assert "seed-phase.md" in text
        assert "seed-registry.md" in text
        assert "AGENTS.md" in text
        assert "change-review.md" in text


class TestManifestSchema:
    @pytest.fixture
    def manifest_schema(self):
        path = ROOT / "schema-registry" / "seed-phase-manifest.v1.json"
        return json.loads(path.read_text())

    def test_doctrine_version_field(self, manifest_schema):
        props = manifest_schema["properties"]
        assert "doctrine_version" in props
        assert props["doctrine_version"]["type"] == "string"

    def test_doctrine_version_not_required(self, manifest_schema):
        assert "doctrine_version" not in manifest_schema.get("required", [])


class TestSeedPhaseWiring:
    def test_seed_phase_references_doctrine(self):
        text = (ROOT / "docs" / "seed-phase.md").read_text()
        assert "seed-phase-doctrine.md" in text

    def test_seed_phase_references_registry(self):
        text = (ROOT / "docs" / "seed-phase.md").read_text()
        assert "seed-registry.md" in text or "Seed Registry" in text

    def test_seed_phase_references_nursery(self):
        text = (ROOT / "docs" / "seed-phase.md").read_text()
        assert "seed-nursery.md" in text or "Nursery" in text

    def test_seed_phase_references_timeline(self):
        text = (ROOT / "docs" / "seed-phase.md").read_text()
        assert "seed-timeline.md" in text or "Timeline" in text


class TestAllDocsExist:
    @pytest.mark.parametrize("doc", [
        "seed-registry.md",
        "seed-promotion-thresholds.md",
        "seed-nursery.md",
        "seed-timeline.md",
        "seed-phase-doctrine.md",
    ])
    def test_doc_exists(self, doc):
        assert (ROOT / "docs" / doc).exists(), f"Missing doc: {doc}"

    @pytest.mark.parametrize("schema", [
        "seed-claim.v1.json",
    ])
    def test_schema_exists(self, schema):
        assert (ROOT / "schema-registry" / schema).exists(), f"Missing schema: {schema}"

    @pytest.mark.parametrize("script", [
        "emit_seed_claim.py",
        "seed_registry_summary.py",
        "evaluate_seed_promotion.py",
        "seed_to_gate.py",
        "seed_nursery_report.py",
        "emit_seed_diff.py",
        "seed_timeline.py",
    ])
    def test_script_exists(self, script):
        assert (ROOT / "scripts" / script).exists(), f"Missing script: {script}"
