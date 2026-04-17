"""Tests for scripts/import_working_identity_candidates.py normalization logic."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from import_working_identity_candidates import (  # noqa: E402
    LAYER_TO_SURFACE,
    extract_candidates,
    normalize_item,
)


def test_normalize_string_item():
    result = normalize_item(
        "Prefers concise summaries",
        layer_type="behavioral_calibration",
        source_tool="ChatGPT",
    )
    assert result["claim"] == "Prefers concise summaries"
    assert result["confidence"] == "medium"
    assert result["durability_class"] == "recurring"
    assert result["sensitivity_class"] == "review_required"
    assert result["portability_class"] == "cross_tool"
    assert result["proposed_target_surface"] == "SELF"
    assert result["source_type"] == "external_ai_extract"
    assert result["source_tool"] == "ChatGPT"
    assert result["supporting_examples"] == []
    assert result["review_status"] == "pending"


def test_normalize_object_item():
    raw = {
        "claim": "Uses compare / validate / authorize structure",
        "confidence": "high",
        "durability": "stable",
        "examples": ["PR review pattern", "Gate review pass"],
    }
    result = normalize_item(
        raw,
        layer_type="workflow_calibration",
        source_tool="Claude",
    )
    assert result["claim"] == "Uses compare / validate / authorize structure"
    assert result["confidence"] == "high"
    assert result["durability_class"] == "stable"
    assert result["proposed_target_surface"] == "SKILLS"
    assert result["supporting_examples"] == ["PR review pattern", "Gate review pass"]


def test_normalize_empty_claim_returns_empty():
    result = normalize_item("", layer_type="domain_encoding", source_tool="x")
    assert result == {}

    result = normalize_item(
        {"claim": "", "confidence": "high"},
        layer_type="domain_encoding",
        source_tool="x",
    )
    assert result == {}


def test_normalize_invalid_confidence_defaults_medium():
    result = normalize_item(
        {"claim": "test", "confidence": "very_high"},
        layer_type="behavioral_calibration",
        source_tool="x",
    )
    assert result["confidence"] == "medium"


def test_normalize_invalid_durability_defaults_recurring():
    result = normalize_item(
        {"claim": "test", "durability": "permanent"},
        layer_type="behavioral_calibration",
        source_tool="x",
    )
    assert result["durability_class"] == "recurring"


def test_layer_to_surface_mapping():
    assert LAYER_TO_SURFACE["domain_encoding"] == "SELF-LIBRARY"
    assert LAYER_TO_SURFACE["workflow_calibration"] == "SKILLS"
    assert LAYER_TO_SURFACE["behavioral_calibration"] == "SELF"
    assert LAYER_TO_SURFACE["artifact_rationale"] == "EVIDENCE"


def test_extract_candidates_full():
    data = {
        "domain_encoding": [
            {"claim": "Knows repo governance", "confidence": "high", "durability": "stable", "examples": []},
        ],
        "workflow_calibration": [
            "Prefers proposal-first workflow",
        ],
        "behavioral_calibration": [
            {"claim": "Short prompts, expects full output", "confidence": "high", "durability": "stable", "examples": ["a", "b"]},
        ],
        "artifact_rationale": [],
        "candidate_examples": [],
        "sensitivity_flags": [
            {"claim": "May reference internal project names", "confidence": "low", "durability": "ephemeral", "examples": []},
        ],
        "merge_targets": ["SELF", "SKILLS"],
    }
    candidates = extract_candidates(data, source_tool="TestTool")
    assert len(candidates) == 4

    assert candidates[0]["layer_type"] == "domain_encoding"
    assert candidates[0]["proposed_target_surface"] == "SELF-LIBRARY"

    assert candidates[1]["layer_type"] == "workflow_calibration"
    assert candidates[1]["claim"] == "Prefers proposal-first workflow"

    assert candidates[2]["layer_type"] == "behavioral_calibration"
    assert candidates[2]["supporting_examples"] == ["a", "b"]

    # sensitivity_flags item
    assert candidates[3]["sensitivity_class"] == "review_required"
    assert candidates[3]["claim"] == "May reference internal project names"


def test_extract_candidates_empty_sections():
    data = {
        "domain_encoding": [],
        "workflow_calibration": [],
        "behavioral_calibration": [],
        "artifact_rationale": [],
    }
    candidates = extract_candidates(data, source_tool="x")
    assert candidates == []


def test_extract_candidates_missing_sections():
    data = {"domain_encoding": [{"claim": "test", "confidence": "low"}]}
    candidates = extract_candidates(data, source_tool="x")
    assert len(candidates) == 1
    assert candidates[0]["claim"] == "test"
    assert candidates[0]["confidence"] == "low"
