#!/usr/bin/env python3
"""
cadence-dream.py — consolidated dream runner for companion-self instances.

End-of-day consolidation in one command.  Runs good-night-brief.py with
appropriate flags, then reports git status so the operator sees uncommitted
work before closing the day.

The night brief writes daily-handoff/night-handoff.json — the artifact
that cadence-coffee.py (via good-morning-brief.py) picks up tomorrow.

After the brief, this runner merges worktree triage (worktreeState,
worktreeAdvice) into night-handoff.json when the handoff exists.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent


def _run(argv: list[str]) -> int:
    print(f"\n{'=' * 60}\n$ {' '.join(argv)}\n{'=' * 60}\n", flush=True)
    r = subprocess.run(argv, cwd=str(_REPO))
    return r.returncode


def _git_summary() -> str:
    """Uncommitted-work snapshot for end-of-day awareness."""
    status = subprocess.run(
        ["git", "status", "-sb"],
        cwd=str(_REPO),
        capture_output=True,
        text=True,
    )
    diff_stat = subprocess.run(
        ["git", "diff", "--stat"],
        cwd=str(_REPO),
        capture_output=True,
        text=True,
    )
    out = status.stdout.strip()
    if diff_stat.stdout.strip():
        out += "\n\nUnstaged changes:\n" + diff_stat.stdout.strip()
    return out


def _classify_worktree(status_out: str, diff_out: str) -> tuple[str, str]:
    """Return (worktreeState, worktreeAdvice). Read-only triage; no commits."""
    combined = f"{status_out}\n{diff_out}".lower()
    if "unmerged" in combined or "both modified" in combined:
        return (
            "risky residue",
            "Merge or conflict state — inspect before continuing; do not assume clean pull.",
        )
    lines = [ln.strip() for ln in status_out.splitlines() if ln.strip()]
    body = [ln for ln in lines if not ln.startswith("## ")]
    if not body:
        return "clean", "leave"
    diff_len = len(diff_out)
    if diff_len > 4000 or len(body) > 12:
        return (
            "risky residue",
            "Large or wide diff — inspect tomorrow first; consider bridge when closing session.",
        )
    return (
        "light residue",
        "leave or commit before sleep (operator choice); bridge seals when you close the session.",
    )


def _merge_worktree_into_handoff(user_id: str) -> None:
    handoff_path = _REPO / "users" / user_id / "daily-handoff" / "night-handoff.json"
    if not handoff_path.is_file():
        return
    try:
        data = json.loads(handoff_path.read_text(encoding="utf-8"))
    except Exception:
        return
    status = subprocess.run(
        ["git", "status", "-sb"],
        cwd=str(_REPO),
        capture_output=True,
        text=True,
    )
    diff_stat = subprocess.run(
        ["git", "diff", "--stat"],
        cwd=str(_REPO),
        capture_output=True,
        text=True,
    )
    state, advice = _classify_worktree(status.stdout or "", diff_stat.stdout or "")
    data["worktreeState"] = state
    data["worktreeAdvice"] = advice
    handoff_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Dream — consolidated night cadence runner for companion-self instances."
    )
    p.add_argument(
        "--user",
        required=True,
        help="Instance user id (users/<id>/)",
    )
    p.add_argument(
        "--mode",
        "-m",
        choices=("minimal", "standard", "reflective"),
        default="standard",
        help="Dream mode (default: standard)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Run night brief without writing closeout or handoff",
    )
    p.add_argument(
        "--suggest-gate",
        action="store_true",
        help="Include gated candidate suggestions in the night brief",
    )
    args = p.parse_args()
    user = args.user
    py = sys.executable

    night_cmd = [py, "scripts/good-night-brief.py", "--user", user, "--mode", args.mode]
    if not args.dry_run:
        night_cmd.append("--write-closeout")
    if args.suggest_gate:
        night_cmd.append("--suggest-gate")

    code = _run(night_cmd)
    if code != 0:
        return code

    if not args.dry_run:
        _merge_worktree_into_handoff(user)

    print(f"\n{'=' * 60}\n$ git status (end-of-day)\n{'=' * 60}\n", flush=True)
    print(_git_summary())

    return 0


if __name__ == "__main__":
    sys.exit(main())
