"""Tests for grace_mar.merge.boundary_classifier and persisted boundary-classification v1."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from grace_mar.merge.boundary_classifier import (
    build_boundary_classification,
    infer_surface_from_proposal_class,
    review_surface_token_to_classifier_tuple,
    suggested_reclassify_proposal_class,
    write_boundary_classification,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schema-registry" / "boundary-classification.v1.json"


@pytest.fixture
def schema():
    with SCHEMA_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def test_infer_surface_civ_mem():
    assert infer_surface_from_proposal_class("CIV_MEM_ADD") == ("self_library", "civ_mem")


def test_suggested_reclassify_revise():
    pc = suggested_reclassify_proposal_class("self_library", None, "SELF_KNOWLEDGE_REVISE")
    assert pc == "SELF_LIBRARY_REVISE"


def test_build_boundary_classification_validates(schema):
    row = {
        "id": "CANDIDATE-0999",
        "status": "pending",
        "proposal_class": "SELF_KNOWLEDGE_ADD",
        "summary": "x",
        "boundary_review": {
            "target_surface": "SELF-KNOWLEDGE",
            "suggested_surface": "SELF-LIBRARY",
            "misfiled_warning": "Misfiled?",
            "hint_reasons": ["LIB-0001"],
            "confidence": "low",
        },
    }
    doc = build_boundary_classification(row, user_slug="grace-mar")
    jsonschema.Draft202012Validator(schema).validate(doc)
    assert doc["boundaryStatus"] == "misaligned"
    assert doc["proposalClassSuggested"] == "SELF_LIBRARY_ADD"


def test_write_boundary_classification_creates_file(tmp_path: Path, schema):
    (tmp_path / "users" / "test-user" / "review-queue").mkdir(parents=True)
    row = {
        "id": "CANDIDATE-0888",
        "status": "pending",
        "proposal_class": "SELF_KNOWLEDGE_ADD",
        "summary": "topic",
        "boundary_review": {
            "target_surface": "SELF-KNOWLEDGE",
            "suggested_surface": "SELF-KNOWLEDGE",
            "misfiled_warning": None,
            "hint_reasons": [],
            "confidence": "high",
        },
    }
    path = write_boundary_classification("test-user", row, tmp_path)
    assert path is not None
    assert path.is_file()
    data = json.loads(path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(data)


def test_review_surface_token_to_classifier_tuple():
    assert review_surface_token_to_classifier_tuple("civ_mem") == ("self_library", "civ_mem")
    assert review_surface_token_to_classifier_tuple("self") == ("self_knowledge", None)


def test_combined_suggested_surface_maps_to_civ_mem():
    """Heuristic may return 'CIV-MEM / SELF-LIBRARY' from identity_library_boundary_rules."""
    row = {
        "id": "CANDIDATE-0777",
        "status": "pending",
        "proposal_class": "SELF_KNOWLEDGE_ADD",
        "summary": "s",
        "boundary_review": {
            "target_surface": "SELF-KNOWLEDGE",
            "suggested_surface": "CIV-MEM / SELF-LIBRARY",
            "misfiled_warning": "warn",
            "hint_reasons": ["path"],
            "confidence": "medium",
        },
    }
    doc = build_boundary_classification(row, user_slug="grace-mar")
    assert doc["surfaceSuggested"] == "self_library"
    assert doc["subsurfaceSuggested"] == "civ_mem"
