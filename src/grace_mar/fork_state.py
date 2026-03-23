"""
Durable fork lifecycle state: users/<fork_id>/fork_state.json
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Phases (spec): seed, interact, diverge, merge_pending, snapshotted
VALID_PHASES = frozenset({"seed", "interact", "diverge", "merge_pending", "snapshotted"})

DEFAULT_POLICIES: dict[str, Any] = {
    "allow_divergence": True,
    "merge_requires_human": True,
    "max_unreviewed_sessions": 25,
    "snapshot_drift_threshold": 0.45,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fork_state_path(repo_root: Path, fork_id: str) -> Path:
    return repo_root / "users" / fork_id / "fork_state.json"


def load_fork_state(repo_root: Path, fork_id: str) -> dict[str, Any] | None:
    path = fork_state_path(repo_root, fork_id)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def write_fork_state(repo_root: Path, fork_id: str, state: dict[str, Any]) -> None:
    path = fork_state_path(repo_root, fork_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    state = dict(state)
    state["fork_id"] = fork_id
    state["updated_at"] = _utc_now()
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def default_fork_state(fork_id: str, *, seed_commit: str = "") -> dict[str, Any]:
    now = _utc_now()
    return {
        "fork_id": fork_id,
        "phase": "seed",
        "seed_commit": seed_commit,
        "last_session_id": "",
        "last_session_commit": "",
        "last_snapshot_tag": "",
        "drift_score": 0.0,
        "created_at": now,
        "updated_at": now,
        "counters": {
            "session_count": 0,
            "merge_count": 0,
            "snapshot_count": 0,
            "session_seq": 0,
        },
        "policies": dict(DEFAULT_POLICIES),
    }


def ensure_fork_state(repo_root: Path, fork_id: str) -> dict[str, Any]:
    existing = load_fork_state(repo_root, fork_id)
    if existing:
        return existing
    state = default_fork_state(fork_id)
    write_fork_state(repo_root, fork_id, state)
    return state


# (from_phase, to_phase) — spec §1 Invariant D
_ALLOWED_TRANSITIONS: frozenset[tuple[str, str]] = frozenset(
    {
        ("seed", "interact"),
        ("interact", "diverge"),
        ("interact", "merge_pending"),
        ("interact", "snapshotted"),
        ("diverge", "merge_pending"),
        ("diverge", "snapshotted"),
        ("merge_pending", "interact"),
        ("snapshotted", "interact"),
    }
)


def can_transition(from_phase: str, to_phase: str) -> bool:
    return (from_phase, to_phase) in _ALLOWED_TRANSITIONS


def transition_fork_phase(
    repo_root: Path,
    fork_id: str,
    to_phase: str,
    *,
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if to_phase not in VALID_PHASES:
        raise ValueError(f"invalid phase: {to_phase}")
    st = state if state is not None else load_fork_state(repo_root, fork_id)
    if not st:
        st = ensure_fork_state(repo_root, fork_id)
    cur = str(st.get("phase") or "seed")
    if cur not in VALID_PHASES:
        cur = "seed"
    if not can_transition(cur, to_phase):
        raise ValueError(f"illegal phase transition: {cur} -> {to_phase}")
    st["phase"] = to_phase
    write_fork_state(repo_root, fork_id, st)
    return st


def sessions_base(repo_root: Path, fork_id: str) -> Path:
    return repo_root / "users" / fork_id / "sessions"


def snapshots_base(repo_root: Path, fork_id: str) -> Path:
    return repo_root / "users" / fork_id / "snapshots"


def lineage_path(repo_root: Path, fork_id: str) -> Path:
    return repo_root / "users" / fork_id / "fork-lineage.jsonl"


def drift_report_path(repo_root: Path, fork_id: str) -> Path:
    return repo_root / "users" / fork_id / "drift-report.json"
