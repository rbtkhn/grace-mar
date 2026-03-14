#!/usr/bin/env python3
"""
Generate a compact daily operator warmup for Grace-Mar.

This is an operator workflow surface. It summarizes continuity state,
WAP status, repo integrity, and local worktree noise without changing
the Record or processing the gate.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

try:
    from harness_warmup import _last_activity_oneliner, _pending_candidates, _read, _session_lines_tail
    from work_american_politics_ops import get_wap_snapshot
except ImportError:
    from scripts.harness_warmup import _last_activity_oneliner, _pending_candidates, _read, _session_lines_tail
    from scripts.work_american_politics_ops import get_wap_snapshot

REPO_ROOT = Path(__file__).resolve().parent.parent
USERS_DIR = REPO_ROOT / "users"


def _git_status_lines() -> list[str]:
    proc = subprocess.run(
        ["git", "status", "--short"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return [f"git status failed: {proc.stderr.strip() or 'unknown error'}"]
    return [line for line in proc.stdout.splitlines() if line.strip()]


def _integrity_errors(user_id: str) -> list[str]:
    proc = subprocess.run(
        ["python3", "scripts/validate-integrity.py", "--user", user_id, "--json"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode not in {0, 1}:
        return [f"integrity validator failed to run: {proc.stderr.strip() or 'unknown error'}"]
    try:
        payload = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        return ["integrity validator returned invalid JSON"]
    errors = payload.get("errors")
    if not isinstance(errors, list):
        return ["integrity validator returned malformed payload"]
    return [str(item) for item in errors]


def _priority_list(
    *,
    pending_all: list[tuple[str, str]],
    pending_wap: list[tuple[str, str]],
    integrity_errors: list[str],
    wap_snapshot: dict[str, object],
    dirty_files: list[str],
) -> list[str]:
    priorities: list[str] = []
    if integrity_errors:
        priorities.append("Fix integrity failures before export or merge work.")
    if pending_all:
        priorities.append(
            f"Review {len(pending_all)} pending gate candidate(s) in `users/grace-mar/recursion-gate.md` before they go stale."
        )
    if pending_wap:
        priorities.append("Handle live WAP gate items before creating more territory continuity.")

    blockers = wap_snapshot.get("territory_blockers") or []
    if blockers:
        first = blockers[0]
        if isinstance(first, dict) and first.get("action"):
            priorities.append(str(first["action"]))

    next_actions = wap_snapshot.get("next_actions") or []
    for action in next_actions:
        if isinstance(action, str):
            priorities.append(action)

    if dirty_files and not priorities:
        priorities.append("Clean up or commit current local changes before starting a new work block.")

    deduped: list[str] = []
    seen: set[str] = set()
    for item in priorities:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)

    if not deduped:
        deduped.append("No urgent blockers detected. Pick the next highest-value WAP or architecture task.")
    return deduped[:3]


def build_operator_daily_warmup(user_id: str = "grace-mar") -> str:
    user_dir = USERS_DIR / user_id
    recursion_gate = _read(user_dir / "recursion-gate.md")
    evidence = _read(user_dir / "self-evidence.md")
    session = _read(user_dir / "session-log.md")

    pending_all = _pending_candidates(recursion_gate, "all")
    pending_wap = _pending_candidates(recursion_gate, "wap")
    pending_companion = _pending_candidates(recursion_gate, "companion")
    last_activity = _last_activity_oneliner(evidence) or "_none parsed_"
    session_tail = _session_lines_tail(session, 3)
    wap_snapshot = get_wap_snapshot(user_id)
    integrity_errors = _integrity_errors(user_id)
    dirty_files = _git_status_lines()
    content_counts = (wap_snapshot.get("content_queue") or {}).get("status_counts") or {}
    brief_counts = (wap_snapshot.get("brief_readiness") or {}).get("status_counts") or {}
    primary_label = ((wap_snapshot.get("campaign_status") or {}).get("primary_date")) or "unknown"
    days_until_primary = ((wap_snapshot.get("campaign_status") or {}).get("days_until_primary"))
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# Daily operator warmup",
        "",
        f"- Generated: {ts}",
        f"- User: `{user_id}`",
        f"- Gate pending: {len(pending_all)} total ({len(pending_wap)} WAP, {len(pending_companion)} companion)",
        f"- Last activity: {last_activity}",
        f"- Integrity: {'PASS' if not integrity_errors else f'FAIL ({len(integrity_errors)} issue(s))'}",
        f"- Worktree: {'clean' if not dirty_files else f'{len(dirty_files)} changed file(s)'}",
        "",
        "## Top priorities",
        "",
    ]
    for item in _priority_list(
        pending_all=pending_all,
        pending_wap=pending_wap,
        integrity_errors=integrity_errors,
        wap_snapshot=wap_snapshot,
        dirty_files=dirty_files,
    ):
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## WAP snapshot",
            "",
            f"- Primary date: {primary_label} ({days_until_primary} day(s) remaining)",
            f"- Territory blockers: {len(wap_snapshot.get('territory_blockers') or [])}",
            f"- Brief readiness: ready={brief_counts.get('ready', 0)}, watch={brief_counts.get('watch', 0)}, needs_refresh={brief_counts.get('needs_refresh', 0)}",
            f"- Content queue: idea={content_counts.get('idea', 0)}, draft={content_counts.get('draft', 0)}, review={content_counts.get('review', 0)}, posted={content_counts.get('posted', 0)}",
            "",
            "## Repo health",
            "",
        ]
    )

    if integrity_errors:
        for err in integrity_errors[:5]:
            lines.append(f"- {err}")
        if len(integrity_errors) > 5:
            lines.append(f"- ... and {len(integrity_errors) - 5} more integrity issue(s)")
    else:
        lines.append("- Integrity validator passed.")

    lines.extend(["", "## Local changes", ""])
    if dirty_files:
        for path in dirty_files[:8]:
            lines.append(f"- `{path}`")
        if len(dirty_files) > 8:
            lines.append(f"- ... and {len(dirty_files) - 8} more")
    else:
        lines.append("- Worktree clean.")

    lines.extend(["", "## Session tail", ""])
    if session_tail:
        for item in session_tail:
            lines.append(f"- {item}")
    else:
        lines.append("- `users/grace-mar/session-log.md` tail unavailable.")

    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            "- Read-only summary only. Do not merge Record changes without companion approval.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a daily operator warmup for Grace-Mar.")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    args = parser.parse_args()
    print(build_operator_daily_warmup(user_id=args.user))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
