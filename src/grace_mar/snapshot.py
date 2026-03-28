"""
Snapshot manifests under users/<fork_id>/snapshots/<tag>.json
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from grace_mar.fork_lineage import append_lineage_event
from grace_mar.fork_state import (
    can_transition,
    load_fork_state,
    snapshots_base,
    write_fork_state,
)
from grace_mar.drift import compute_drift_report


def _sha256_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_head(repo_root: Path) -> str:
    try:
        r = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return ""


def _pending_blocking(gate_text: str) -> bool:
    return bool(re.search(r"status:\s*pending", gate_text, re.IGNORECASE))


def create_snapshot(
    repo_root: Path,
    fork_id: str,
    tag: str,
    *,
    skip_git_tag: bool = False,
    skip_integrity: bool = False,
) -> Path:
    profile = repo_root / "users" / fork_id
    gate_text = (profile / "recursion-gate.md").read_text(encoding="utf-8") if (profile / "recursion-gate.md").is_file() else ""

    if _pending_blocking(gate_text):
        raise RuntimeError("Cannot snapshot: pending candidates in recursion-gate (blocking)")

    compute_drift_report(repo_root, fork_id)
    drift_path = profile / "drift-report.json"
    drift_data = json.loads(drift_path.read_text(encoding="utf-8")) if drift_path.is_file() else {}
    drift_score = float(drift_data.get("drift_score", 0.0))

    st = load_fork_state(repo_root, fork_id) or {}
    policies = st.get("policies") or {}
    threshold = float(policies.get("snapshot_drift_threshold", 0.45))
    phase = str(st.get("phase") or "interact")

    if drift_score > threshold:
        raise RuntimeError(f"Drift {drift_score} above threshold {threshold}; snapshot blocked")

    if not skip_integrity:
        r = subprocess.run(
            [sys.executable, str(repo_root / "scripts" / "validate-integrity.py"), "--user", fork_id, "--json"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if r.returncode != 0:
            raise RuntimeError(f"validate-integrity failed: {r.stderr or r.stdout[:500]}")

    _scripts = repo_root / "scripts"
    if str(_scripts) not in sys.path:
        sys.path.insert(0, str(_scripts))
    from repo_io import resolve_surface_markdown_path  # noqa: E402

    skills_resolved = resolve_surface_markdown_path(profile, "self_skills")
    record_files = {
        "self.md": profile / "self.md",
        "self-archive.md": profile / "self-archive.md",
        "self-library.md": profile / "self-library.md",
        "self-skills.md": skills_resolved,
    }
    checksums: dict[str, str] = {}
    for name, p in record_files.items():
        checksums[name] = _sha256_file(p) if p.is_file() else ""

    git_commit = _git_head(repo_root)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    manifest: dict[str, Any] = {
        "tag": tag,
        "fork_id": fork_id,
        "git_commit": git_commit,
        "created_at": now,
        "drift_score": drift_score,
        "phase": "snapshotted",
        "session_range": {
            "from": str(st.get("last_session_id") or ""),
            "to": str(st.get("last_session_id") or ""),
        },
        "record_checksums": checksums,
    }

    snap_dir = snapshots_base(repo_root, fork_id)
    snap_dir.mkdir(parents=True, exist_ok=True)
    out_path = snap_dir / f"{tag}.json"
    out_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    append_lineage_event(
        repo_root,
        fork_id,
        {"event": "snapshot_created", "tag": tag, "git_commit": git_commit[:40]},
    )

    st = load_fork_state(repo_root, fork_id)
    if st:
        st["last_snapshot_tag"] = tag
        counters = st.setdefault("counters", {})
        counters["snapshot_count"] = int(counters.get("snapshot_count", 0)) + 1
        st["counters"] = counters
        if can_transition(str(st.get("phase") or "interact"), "snapshotted"):
            st["phase"] = "snapshotted"
        write_fork_state(repo_root, fork_id, st)

    if not skip_git_tag:
        subprocess.run(
            ["git", "-C", str(repo_root), "tag", "-a", tag, "-m", f"snapshot {fork_id} {tag}"],
            capture_output=True,
            text=True,
            timeout=30,
        )

    return out_path
