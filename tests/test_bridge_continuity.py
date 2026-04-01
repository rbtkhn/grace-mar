"""Pytest wrapper for the bridge continuity fidelity harness."""

import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def _load_harness():
    spec = importlib.util.spec_from_file_location(
        "bridge_continuity_harness",
        REPO_ROOT / "scripts" / "test_bridge_continuity.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_harness = _load_harness()
run_harness = _harness.run_harness

PASS_THRESHOLD = 0.8


def test_bridge_round_trip_overall():
    result = run_harness(REPO_ROOT, "grace-mar")
    assert result["overall_score"] >= PASS_THRESHOLD, (
        f"Bridge continuity {result['overall_score']:.1%} < {PASS_THRESHOLD:.0%} threshold. "
        f"Failing dimensions: "
        + ", ".join(d["name"] for d in result["dimensions"] if not d["passed"])
    )


def test_bridge_gate_fidelity():
    result = run_harness(REPO_ROOT, "grace-mar")
    gate = next(d for d in result["dimensions"] if d["name"] == "gate")
    assert gate["passed"], f"Gate fidelity failed: {gate['detail']}"


def test_bridge_dream_fidelity():
    result = run_harness(REPO_ROOT, "grace-mar")
    dream = next(d for d in result["dimensions"] if d["name"] == "dream")
    assert dream["passed"], f"Dream fidelity failed: {dream['detail']}"


def test_bridge_territory_recall():
    result = run_harness(REPO_ROOT, "grace-mar")
    terr = next(d for d in result["dimensions"] if d["name"] == "territories")
    assert terr["passed"], f"Territory recall failed: {terr['detail']}"


def test_bridge_commit_preservation():
    result = run_harness(REPO_ROOT, "grace-mar")
    commits = next(d for d in result["dimensions"] if d["name"] == "commits")
    assert commits["passed"], f"Commit preservation failed: {commits['detail']}"
