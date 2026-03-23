"""
Heuristic drift scoring — users/<fork_id>/drift-report.json
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from grace_mar.fork_state import drift_report_path, load_fork_state, write_fork_state


def _pending_count(gate_text: str) -> int:
    n = 0
    for m in re.finditer(
        r"### (CANDIDATE-\d+).*?```yaml\s*\n(.*?)```", gate_text, re.DOTALL | re.IGNORECASE
    ):
        blk = m.group(2)
        if re.search(r"^\s*status:\s*pending\s*$", blk, re.MULTILINE | re.IGNORECASE):
            n += 1
    return n


def _real_world_pending(gate_text: str) -> int:
    n = 0
    for m in re.finditer(
        r"### (CANDIDATE-\d+).*?```yaml\s*\n(.*?)```", gate_text, re.DOTALL | re.IGNORECASE
    ):
        blk = m.group(2)
        if re.search(r"^\s*status:\s*pending\s*$", blk, re.MULTILINE | re.IGNORECASE) and re.search(
            r"lineage_class:\s*real_world_update", blk, re.IGNORECASE
        ):
            n += 1
    return n


def _days_since_last_merge(merge_receipts: Path) -> float | None:
    if not merge_receipts.is_file():
        return None
    lines = [ln for ln in merge_receipts.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        return None
    try:
        last = json.loads(lines[-1])
        at = str(last.get("approved_at") or "")
        # ISO date
        if "T" in at:
            raw = at.replace("Z", "+00:00")
            dt = datetime.fromisoformat(raw)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            delta = datetime.now(timezone.utc) - dt
            return max(0.0, delta.total_seconds() / 86400.0)
    except (json.JSONDecodeError, ValueError, OSError):
        pass
    return None


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def compute_drift_report(repo_root: Path, fork_id: str) -> Path:
    profile = repo_root / "users" / fork_id
    gate_path = profile / "recursion-gate.md"
    gate_text = gate_path.read_text(encoding="utf-8") if gate_path.is_file() else ""

    pending = _pending_count(gate_text)
    rw = _real_world_pending(gate_text)
    days = _days_since_last_merge(profile / "merge-receipts.jsonl")

    # Component proxies 0..1
    identity_drift = _clamp01(0.08 * pending + 0.12 * rw)
    interest_drift = _clamp01(0.05 * pending)
    skill_drift = _clamp01(0.04 * rw)
    library_drift = _clamp01(0.02 * pending)

    stale_merge = 0.0
    if days is not None:
        stale_merge = _clamp01(min(1.0, (days / 90.0) * 0.4))

    drift_score = _clamp01(
        0.28 * identity_drift
        + 0.22 * interest_drift
        + 0.18 * skill_drift
        + 0.12 * library_drift
        + 0.20 * stale_merge
    )

    if drift_score < 0.20:
        status = "expected_evolution"
    elif drift_score <= 0.45:
        status = "review_recommended"
    else:
        status = "snapshot_blocked"

    signals: list[dict[str, Any]] = []
    if rw:
        signals.append({"kind": "unmerged_real_world_update", "count": rw})
    if days is not None and days > 30:
        signals.append({"kind": "days_since_merge", "days": round(days, 1)})

    report: dict[str, Any] = {
        "fork_id": fork_id,
        "computed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "drift_score": round(drift_score, 4),
        "components": {
            "identity_drift": round(identity_drift, 4),
            "interest_drift": round(interest_drift, 4),
            "skill_drift": round(skill_drift, 4),
            "library_drift": round(library_drift, 4),
            "stale_merge_proxy": round(stale_merge, 4),
        },
        "signals": signals,
        "status": status,
        "pending_candidates": pending,
    }

    out = drift_report_path(repo_root, fork_id)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    st = load_fork_state(repo_root, fork_id)
    if st:
        st["drift_score"] = float(report["drift_score"])
        write_fork_state(repo_root, fork_id, st)

    return out
