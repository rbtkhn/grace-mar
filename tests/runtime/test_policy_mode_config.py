"""Tests for scripts/runtime/policy_mode_config.py."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MOD = REPO_ROOT / "scripts" / "runtime" / "policy_mode_config.py"


@pytest.fixture()
def policy_mod():
    import importlib.util

    spec = importlib.util.spec_from_file_location("policy_mode_config", MOD)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(m)
    return m


def test_resolve_mode_unknown_falls_back(policy_mod):
    d = policy_mod.load_defaults()
    assert policy_mod.resolve_mode("not_a_real_mode", d) == "operator_only"


def test_resolve_mode_known(policy_mod):
    d = policy_mod.load_defaults()
    assert policy_mod.resolve_mode("reference_only", d) == "reference_only"


def test_staging_decision_reference_only_blocked(policy_mod):
    d = policy_mod.load_defaults()
    verb, _reason = policy_mod.staging_decision("reference_only", "SELF", d)
    assert verb == "blocked"
    verb2, _ = policy_mod.staging_decision("reference_only", "SKILLS", d)
    assert verb2 == "blocked"


def test_staging_decision_operator_allowed(policy_mod):
    d = policy_mod.load_defaults()
    verb, _ = policy_mod.staging_decision("operator_only", "SELF", d)
    assert verb == "allowed"


def test_staging_decision_identity_bound_self_warns(policy_mod):
    d = policy_mod.load_defaults()
    verb, _ = policy_mod.staging_decision("identity_bound", "SELF", d)
    assert verb == "warn"
    verb2, _ = policy_mod.staging_decision("identity_bound", "EVIDENCE", d)
    assert verb2 == "allowed"


def test_staging_decision_high_risk_hold(policy_mod):
    d = policy_mod.load_defaults()
    verb, _ = policy_mod.staging_decision("high_risk_abstention", "EVIDENCE", d)
    assert verb == "hold_hint"


def test_load_defaults_skips_schema_version(tmp_path: Path, policy_mod):
    p = tmp_path / "defaults.json"
    p.write_text(
        json.dumps(
            {
                "schemaVersion": "1.0",
                "operator_only": {"candidate_staging": "allowed"},
                "reference_only": {"candidate_staging": "blocked"},
            }
        ),
        encoding="utf-8",
    )
    d = policy_mod.load_defaults(p)
    assert "schemaVersion" not in d
    assert "operator_only" in d
