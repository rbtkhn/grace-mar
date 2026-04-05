#!/usr/bin/env python3
"""
Operational snapshot for bridge \"Since last bridge\" deltas.

Writes users/<id>/daily-handoff/last-bridge-state.json after a successful
bridge (post-push). Not Record truth. Optional --print-delta emits markdown
bullets comparing previous state to current on-disk/git snapshot.

Usage:
  python3 scripts/bridge_last_state.py -u grace-mar --write
  python3 scripts/bridge_last_state.py -u grace-mar --print-delta
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER = os.getenv("GRACE_MAR_USER_ID", "grace-mar")
STATE_NAME = "last-bridge-state.json"
TERRITORY_GLOB = "docs/skill-work/work-*/work-*-history.md"
TERRITORY_RECENCY_DAYS = 7


def _read_text(path: Path) -> str:
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return ""


def _pending_count(gate_text: str) -> int:
    """Count CANDIDATE-* blocks with status: pending (Candidates section only)."""
    in_processed = False
    ids: list[str] = []
    current_id: str | None = None
    for line in gate_text.splitlines():
        if line.strip().startswith("## Processed"):
            in_processed = True
        if in_processed:
            continue
        m = re.match(r"###\s+(CANDIDATE-\d+)", line)
        if m:
            current_id = m.group(1)
        if current_id and re.search(r"status:\s*pending", line):
            ids.append(current_id)
            current_id = None
    return len(ids)


def _gate_fingerprint(gate_path: Path) -> str:
    if not gate_path.is_file():
        return "0"
    st = gate_path.stat()
    raw = f"{st.st_mtime_ns}:{st.st_size}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _git_head(repo: Path) -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(repo),
            capture_output=True,
            text=True,
            timeout=30,
        )
        return (r.stdout or "").strip() or "unknown"
    except (OSError, subprocess.TimeoutExpired):
        return "unknown"


def _git_status_sb(repo: Path) -> str:
    try:
        r = subprocess.run(
            ["git", "status", "-sb"],
            cwd=str(repo),
            capture_output=True,
            text=True,
            timeout=30,
        )
        return (r.stdout or "").strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def _git_diff_stat(repo: Path) -> str:
    try:
        r = subprocess.run(
            ["git", "diff", "--stat"],
            cwd=str(repo),
            capture_output=True,
            text=True,
            timeout=60,
        )
        return r.stdout or ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def classify_worktree_risk(status_out: str, diff_out: str) -> str:
    """Return safe | inspect | conflict-prone (bridge preflight)."""
    combined = f"{status_out}\n{diff_out}".lower()
    if "unmerged" in combined or "both modified" in combined:
        return "conflict-prone"
    lines = [ln.strip() for ln in status_out.splitlines() if ln.strip()]
    body = [ln for ln in lines if not ln.startswith("## ")]
    if not body:
        return "safe"
    diff_len = len(diff_out)
    if diff_len > 4000 or len(body) > 12:
        return "conflict-prone"
    return "inspect"


def _active_territories(repo_root: Path, days: int = TERRITORY_RECENCY_DAYS) -> list[str]:
    """Territory folder names with a history entry in the last N days (aligns with bridge continuity harness)."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    cutoff_str = cutoff.strftime("%Y-%m-%d")
    active: list[str] = []
    for path in sorted(repo_root.glob(TERRITORY_GLOB)):
        territory = path.parent.name
        text = _read_text(path)
        for m in re.finditer(r"##\s+(\d{4}-\d{2}-\d{2})", text):
            if m.group(1) >= cutoff_str:
                active.append(territory)
                break
    return sorted(set(active))


def _resolve_companion_self(repo_root: Path) -> Path | None:
    env = os.environ.get("GRACE_MAR_COMPANION_SELF", "").strip()
    if env:
        p = Path(env).expanduser().resolve()
        if p.is_dir() and (p / ".git").exists():
            return p
    sibling = (repo_root.parent / "companion-self").resolve()
    if sibling.is_dir() and (sibling / ".git").exists():
        return sibling
    return None


def capture_state(repo_root: Path, user_id: str) -> dict[str, Any]:
    users_dir = repo_root / "users" / user_id
    handoff_dir = users_dir / "daily-handoff"
    gate_path = users_dir / "recursion-gate.md"
    gate_text = _read_text(gate_path)
    companion = _resolve_companion_self(repo_root)

    gm_status = _git_status_sb(repo_root)
    gm_diff = _git_diff_stat(repo_root)
    out: dict[str, Any] = {
        "runIso": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "user": user_id,
        "graceMarHead": _git_head(repo_root),
        "graceMarWorktreeRisk": classify_worktree_risk(gm_status, gm_diff),
        "gatePendingCount": _pending_count(gate_text),
        "gateFingerprint": _gate_fingerprint(gate_path),
        "territoriesActive": _active_territories(repo_root),
    }
    if companion:
        cs_status = _git_status_sb(companion)
        cs_diff = _git_diff_stat(companion)
        out["companionSelfHead"] = _git_head(companion)
        out["companionSelfWorktreeRisk"] = classify_worktree_risk(cs_status, cs_diff)
    else:
        out["companionSelfHead"] = ""
        out["companionSelfWorktreeRisk"] = ""
    return out


def _read_state(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def build_delta_lines(prev: dict[str, Any], cur: dict[str, Any]) -> list[str]:
    if not prev:
        return ["First bridge state in this workspace — no prior delta."]
    out: list[str] = []
    if prev.get("graceMarHead") != cur.get("graceMarHead"):
        out.append("grace-mar HEAD changed since last bridge.")
    if prev.get("companionSelfHead") and cur.get("companionSelfHead"):
        if prev.get("companionSelfHead") != cur.get("companionSelfHead"):
            out.append("companion-self HEAD changed since last bridge.")
    if prev.get("gatePendingCount") != cur.get("gatePendingCount"):
        out.append(
            f"Gate pending count changed ({prev.get('gatePendingCount')} → {cur.get('gatePendingCount')})."
        )
    elif prev.get("gateFingerprint") != cur.get("gateFingerprint"):
        out.append("Gate file changed (fingerprint) since last bridge.")
    pt, ct = prev.get("territoriesActive"), cur.get("territoriesActive")
    if isinstance(pt, list) and isinstance(ct, list) and set(pt) != set(ct):
        out.append("Active territory set changed since last bridge.")
    if prev.get("graceMarWorktreeRisk") != cur.get("graceMarWorktreeRisk"):
        out.append(
            f"grace-mar worktree risk class changed ({prev.get('graceMarWorktreeRisk')} → {cur.get('graceMarWorktreeRisk')})."
        )
    return out[:4] if out else ["No material delta since last bridge."]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default=DEFAULT_USER, help="Instance user id")
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: grace-mar root)",
    )
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "--write",
        action="store_true",
        help="Write last-bridge-state.json after successful bridge",
    )
    g.add_argument(
        "--print-delta",
        action="store_true",
        help="Print markdown bullets for Since last bridge section",
    )
    args = ap.parse_args()
    user = args.user.strip()
    repo_root = args.repo_root.resolve()
    users_dir = repo_root / "users" / user
    handoff_dir = users_dir / "daily-handoff"
    state_path = handoff_dir / STATE_NAME

    cur = capture_state(repo_root, user)

    if args.print_delta:
        prev = _read_state(state_path)
        for line in build_delta_lines(prev, cur):
            print(f"- {line}")
        return 0

    handoff_dir.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(cur, indent=2) + "\n", encoding="utf-8")
    print(state_path.relative_to(repo_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
