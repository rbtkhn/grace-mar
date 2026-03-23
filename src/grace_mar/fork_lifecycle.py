"""
Phase transitions, session manifest paths, and high-level lifecycle helpers.
"""

from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from grace_mar.fork_lineage import append_lineage_event
from grace_mar.fork_state import (
    can_transition,
    ensure_fork_state,
    fork_state_path,
    load_fork_state,
    sessions_base,
    snapshots_base,
    transition_fork_phase,
    write_fork_state,
)


def _today_ymd() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def _session_id_for_today(repo_root: Path, fork_id: str) -> str:
    st = ensure_fork_state(repo_root, fork_id)
    counters = st.setdefault("counters", {})
    seq = int(counters.get("session_seq", 0)) + 1
    counters["session_seq"] = seq
    st["counters"] = counters
    write_fork_state(repo_root, fork_id, st)
    return f"SES-{_today_ymd()}-{seq:03d}"


def session_manifest_path(repo_root: Path, fork_id: str, session_id: str) -> Path:
    # SES-YYYYMMDD-NNN -> users/.../sessions/YYYY/MM/session-SES-....json
    m = re.match(r"SES-(\d{4})(\d{2})(\d{2})-", session_id)
    if not m:
        y, mo, d = _today_ymd()[:4], _today_ymd()[4:6], _today_ymd()[6:8]
    else:
        y, mo, d = m.group(1), m.group(2), m.group(3)
    return sessions_base(repo_root, fork_id) / y / mo / f"session-{session_id}.json"


def begin_session(
    repo_root: Path,
    fork_id: str,
    *,
    channel: str = "operator",
) -> dict[str, Any]:
    st = ensure_fork_state(repo_root, fork_id)
    phase = str(st.get("phase") or "seed")
    if phase == "seed":
        st = transition_fork_phase(repo_root, fork_id, "interact", state=st)
        phase = "interact"
    if phase not in ("interact", "diverge", "snapshotted"):
        raise RuntimeError(f"cannot start session in phase {phase}")

    session_id = _session_id_for_today(repo_root, fork_id)
    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest: dict[str, Any] = {
        "session_id": session_id,
        "fork_id": fork_id,
        "started_at": started,
        "ended_at": "",
        "phase_at_start": phase,
        "phase_at_end": "",
        "channel": channel,
        "candidate_ids": [],
        "approved_candidate_ids": [],
        "rejected_candidate_ids": [],
        "merge_receipt_id": "",
        "git_commit": "",
        "runtime_bundle_id": "",
        "drift_score_after": None,
    }
    path = session_manifest_path(repo_root, fork_id, session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    st = load_fork_state(repo_root, fork_id) or st
    st["last_session_id"] = session_id
    counters = st.setdefault("counters", {})
    counters["session_count"] = int(counters.get("session_count", 0)) + 1
    st["counters"] = counters
    write_fork_state(repo_root, fork_id, st)

    append_lineage_event(
        repo_root,
        fork_id,
        {"event": "session_started", "session_id": session_id, "phase": phase},
    )
    return manifest


def end_session(
    repo_root: Path,
    fork_id: str,
    session_id: str,
    *,
    drift_score_after: float | None = None,
    git_commit: str = "",
) -> dict[str, Any]:
    path = session_manifest_path(repo_root, fork_id, session_id)
    if not path.is_file():
        raise FileNotFoundError(f"session manifest not found: {path}")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    ended = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest["ended_at"] = ended
    manifest["phase_at_end"] = str((load_fork_state(repo_root, fork_id) or {}).get("phase") or "")
    if drift_score_after is not None:
        manifest["drift_score_after"] = drift_score_after
    if git_commit:
        manifest["git_commit"] = git_commit
    else:
        manifest["git_commit"] = _git_head(repo_root)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    append_lineage_event(
        repo_root,
        fork_id,
        {
            "event": "session_committed",
            "session_id": session_id,
            "git_commit": manifest.get("git_commit") or "",
        },
    )
    st = load_fork_state(repo_root, fork_id) or ensure_fork_state(repo_root, fork_id)
    st["last_session_commit"] = str(manifest.get("git_commit") or "")
    if drift_score_after is not None:
        st["drift_score"] = float(drift_score_after)
    write_fork_state(repo_root, fork_id, st)
    return manifest


def _git_head(repo_root: Path) -> str:
    try:
        r = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if r.returncode == 0:
            return r.stdout.strip()[:40]
    except (OSError, subprocess.SubprocessError):
        pass
    return ""


def merge_checkpoint(
    repo_root: Path,
    fork_id: str,
    receipt: dict[str, Any],
) -> dict[str, Any]:
    """Record merge checkpoint: lineage + optional phase transition merge_pending -> interact."""
    st = load_fork_state(repo_root, fork_id) or ensure_fork_state(repo_root, fork_id)
    phase_before = str(st.get("phase") or "interact")
    receipt_id = str(receipt.get("receipt_id") or receipt.get("merge_receipt_id") or "")
    if phase_before == "merge_pending" and can_transition("merge_pending", "interact"):
        st = transition_fork_phase(repo_root, fork_id, "interact", state=st)
    counters = st.setdefault("counters", {})
    counters["merge_count"] = int(counters.get("merge_count", 0)) + 1
    st["counters"] = counters
    write_fork_state(repo_root, fork_id, st)
    phase_after = str(st.get("phase") or "")
    append_lineage_event(
        repo_root,
        fork_id,
        {
            "event": "merge_applied",
            "merge_receipt_id": receipt_id,
            "phase_before": phase_before,
            "phase_after": phase_after,
        },
    )
    return st
