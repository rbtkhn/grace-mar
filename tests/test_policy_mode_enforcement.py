"""Tests for policy-mode enforcement — fail-fast on unknown modes, staging gating."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts" / "runtime"))

from policy_mode_config import (
    DEFAULT_MODE,
    UnknownPolicyModeError,
    load_defaults,
    resolve_mode,
    staging_decision,
)


# ── resolve_mode strict behavior ────────────────────────────────────

def test_resolve_mode_known_mode() -> None:
    """Known modes resolve without error in strict and non-strict."""
    defaults = load_defaults()
    for mode_name in defaults:
        assert resolve_mode(mode_name, defaults) == mode_name
        assert resolve_mode(mode_name, defaults, strict=True) == mode_name


def test_resolve_mode_empty_returns_default() -> None:
    """Empty mode resolves to operator_only in both modes."""
    defaults = load_defaults()
    assert resolve_mode(None, defaults) == DEFAULT_MODE
    assert resolve_mode("", defaults) == DEFAULT_MODE
    assert resolve_mode(None, defaults, strict=True) == DEFAULT_MODE


def test_resolve_mode_unknown_nonstrict_falls_back() -> None:
    """Non-strict mode silently falls back to operator_only."""
    defaults = load_defaults()
    assert resolve_mode("totally_bogus_mode", defaults) == DEFAULT_MODE


def test_resolve_mode_unknown_strict_raises() -> None:
    """Strict mode raises UnknownPolicyModeError on unknown mode name."""
    defaults = load_defaults()
    with pytest.raises(UnknownPolicyModeError) as exc_info:
        resolve_mode("totally_bogus_mode", defaults, strict=True)
    assert "totally_bogus_mode" in str(exc_info.value)
    assert "Valid modes" in str(exc_info.value)


# ── staging_decision behavior ────────────────────────────────────────

def test_staging_decision_operator_only_allows() -> None:
    """operator_only mode allows staging."""
    defaults = load_defaults()
    verb, _ = staging_decision("operator_only", "SELF", defaults)
    assert verb == "allowed"


def test_staging_decision_blocked_mode() -> None:
    """If candidate_staging is blocked, verb must be 'blocked'."""
    fake = {"test_blocked": {"candidate_staging": "blocked"}}
    verb, reason = staging_decision("test_blocked", "SELF", fake)
    assert verb == "blocked"
    assert "blocked" in reason.lower()


def test_staging_decision_hold_by_default() -> None:
    """hold_by_default mode returns hold_hint."""
    defaults = load_defaults()
    if "high_risk_abstention" in defaults:
        verb, _ = staging_decision("high_risk_abstention", "EVIDENCE", defaults)
        assert verb in ("hold_hint", "warn", "blocked")


def test_staging_decision_identity_bound_self_warns() -> None:
    """identity_bound mode warns on SELF target."""
    defaults = load_defaults()
    if "identity_bound" in defaults:
        verb, reason = staging_decision("identity_bound", "SELF", defaults)
        assert verb == "warn"
        assert "policy-ack" in reason.lower() or "strict self guard" in reason.lower()


# ── precheck_gate_staging fails on unknown policy mode ───────────────

def test_precheck_fails_on_unknown_policy_mode(tmp_path: Path) -> None:
    """precheck_gate_staging.py should exit 2 for unknown policy modes."""
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    seed = REPO_ROOT / "tests" / "fixtures" / "observations-seed.jsonl"
    (obs_dir / "index.jsonl").write_text(
        seed.read_text(encoding="utf-8"), encoding="utf-8"
    )
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "runtime" / "precheck_gate_staging.py"),
            "--id", "obs_bench_001",
            "--policy-mode", "totally_invalid_mode",
        ],
        env=env, capture_output=True, text=True,
    )
    assert r.returncode == 2, f"expected exit 2 for unknown mode, got {r.returncode}: {r.stderr}"
    assert "unknown policy mode" in r.stderr.lower() or "Unknown policy mode" in r.stderr


def test_precheck_outputs_policy_mode_in_receipt(tmp_path: Path) -> None:
    """precheck_gate_staging.py should print policy_mode in stderr."""
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    seed = REPO_ROOT / "tests" / "fixtures" / "observations-seed.jsonl"
    (obs_dir / "index.jsonl").write_text(
        seed.read_text(encoding="utf-8"), encoding="utf-8"
    )
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "runtime" / "precheck_gate_staging.py"),
            "--id", "obs_bench_001",
            "--policy-mode", "operator_only",
        ],
        env=env, capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    assert "policy_mode: operator_only" in r.stderr
    assert "staging_decision:" in r.stderr


# ── stage_candidate_from_observations fails on unknown mode ──────────

def test_stage_candidate_fails_on_unknown_policy_mode(tmp_path: Path) -> None:
    """stage_candidate_from_observations.py should exit 2 for unknown policy modes."""
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    seed = REPO_ROOT / "tests" / "fixtures" / "observations-seed.jsonl"
    (obs_dir / "index.jsonl").write_text(
        seed.read_text(encoding="utf-8"), encoding="utf-8"
    )
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "runtime" / "stage_candidate_from_observations.py"),
            "--lane", "work-strategy",
            "--id", "obs_bench_001",
            "--candidate-type", "other",
            "--target-surface", "OTHER",
            "--summary", "test",
            "--proposed-change", "test",
            "--policy-mode", "totally_invalid_mode",
            "--dry-run",
        ],
        env=env, capture_output=True, text=True,
    )
    assert r.returncode == 2, f"expected exit 2 for unknown mode, got {r.returncode}: {r.stderr}"
    assert "unknown policy mode" in r.stderr.lower() or "Unknown policy mode" in r.stderr
