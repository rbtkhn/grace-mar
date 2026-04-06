"""Readiness JSON expectations for demo and fixtures."""

from __future__ import annotations

import json
from pathlib import Path

from tests.conftest import REPO_ROOT, copy_fixture


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_demo_readiness_is_activation_eligible() -> None:
    readiness = load_json(REPO_ROOT / "users" / "demo" / "seed-phase" / "seed_readiness.json")
    decision = readiness["readiness"]["decision"]
    assert decision in {"pass", "conditional_pass"}


def test_valid_minimal_fixture_has_expected_readiness(tmp_seed_dir) -> None:
    copy_fixture("valid-minimal", tmp_seed_dir)
    readiness = load_json(tmp_seed_dir / "seed_readiness.json")
    assert readiness["readiness"]["decision"] in {"pass", "conditional_pass"}


def test_invalid_readiness_threshold_fixture_not_ready(tmp_seed_dir) -> None:
    copy_fixture("invalid-readiness-threshold", tmp_seed_dir)
    readiness = load_json(tmp_seed_dir / "seed_readiness.json")
    assert readiness["readiness"]["decision"] == "fail"
