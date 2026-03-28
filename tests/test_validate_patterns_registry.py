"""Tests for scripts/work_jiang/validate_patterns_registry.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def vp_mod():
    path = REPO_ROOT / "scripts" / "work_jiang" / "validate_patterns_registry.py"
    spec = importlib.util.spec_from_file_location("validate_patterns_registry", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_validate_recurrence_exceeds_total_cases(vp_mod):
    patterns = [
        {
            "pattern_id": "pat-0999",
            "name": "Bad recurrence",
            "definition": "x" * 50,
            "observable_signatures": ["a"],
            "linked_prediction_ids": [],
            "dependencies": [],
            "performance": {
                "signatures_matched": 2,
                "total_cases": 2,
                "narrative": "n" * 25,
                "recurrence": {
                    "lecture_occurrences": 2,
                    "analog_occurrences": 1,
                    "frequency_qualifier": "high",
                },
            },
        }
    ]
    errors, _ = vp_mod.validate_patterns(patterns, {"jiang-GS01-001"})
    assert any("cannot exceed total_cases" in e for e in errors)


def test_validate_signatures_exceed_total(vp_mod):
    patterns = [
        {
            "pattern_id": "pat-0998",
            "name": "Bad sig",
            "definition": "y" * 50,
            "observable_signatures": ["a"],
            "performance": {
                "signatures_matched": 5,
                "total_cases": 3,
                "narrative": "n" * 25,
            },
        }
    ]
    errors, _ = vp_mod.validate_patterns(patterns, set())
    assert any("signatures_matched" in e and "total_cases" in e for e in errors)


def test_validate_dependency_unknown(vp_mod):
    patterns = [
        {
            "pattern_id": "pat-0997",
            "name": "Dangling dep",
            "definition": "z" * 50,
            "observable_signatures": ["b"],
            "dependencies": ["pat-0001"],
            "performance": {
                "signatures_matched": 0,
                "total_cases": 1,
                "narrative": "n" * 25,
            },
        }
    ]
    errors, _ = vp_mod.validate_patterns(patterns, set())
    assert any("dependency" in e for e in errors)
