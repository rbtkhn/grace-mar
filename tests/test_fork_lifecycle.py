"""Tests for fork lifecycle (fork_state, lineage, drift, transitions)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from grace_mar.fork_lineage import append_lineage_event, read_lineage_tail  # noqa: E402
from grace_mar.fork_state import (  # noqa: E402
    can_transition,
    ensure_fork_state,
    fork_state_path,
    load_fork_state,
    transition_fork_phase,
)
from grace_mar.drift import compute_drift_report  # noqa: E402


def test_can_transition_seed_to_interact():
    assert can_transition("seed", "interact")
    assert not can_transition("seed", "snapshotted")


def test_ensure_fork_state_roundtrip(tmp_path, monkeypatch):
    # Use tmp repo layout: tmp_path/users/u/
    root = tmp_path
    uid = "test-fork"
    monkeypatch.chdir(root)
    # grace_mar paths use REPO_ROOT from package - we need to pass root to functions
    # Tests call with tmp_path as synthetic repo root
    st = ensure_fork_state(root, uid)
    assert st["phase"] == "seed"
    assert fork_state_path(root, uid).is_file()
    st2 = load_fork_state(root, uid)
    assert st2["fork_id"] == uid


def test_lineage_append(tmp_path):
    root = tmp_path
    uid = "lf-test"
    (root / "users" / uid).mkdir(parents=True)
    append_lineage_event(root, uid, {"event": "test", "x": 1})
    tail = read_lineage_tail(root, uid, max_lines=5)
    assert tail and tail[-1]["event"] == "test"


def test_transition_updates_phase(tmp_path):
    root = tmp_path
    uid = "tr-test"
    ensure_fork_state(root, uid)
    transition_fork_phase(root, uid, "interact")
    st = load_fork_state(root, uid)
    assert st["phase"] == "interact"


def test_drift_report_writes(tmp_path):
    root = tmp_path
    uid = "dr-test"
    ud = root / "users" / uid
    ud.mkdir(parents=True)
    (ud / "recursion-gate.md").write_text("## Candidates\n\n## Processed\n", encoding="utf-8")
    p = compute_drift_report(root, uid)
    assert p.is_file()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert "drift_score" in data
