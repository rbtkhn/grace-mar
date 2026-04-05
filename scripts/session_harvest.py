#!/usr/bin/env python3
"""
Thin checklist + optional template for the session harvest ritual.

Does not author insights — the agent fills narrative from the visible thread.
See .cursor/skills/harvest/SKILL.md and docs/skill-work/work-cadence/harvest-packet-contract.md.

Usage:
  python3 scripts/session_harvest.py -u demo
  python3 scripts/session_harvest.py -u demo --mode strategic --emit-template
  python3 scripts/session_harvest.py -u demo --log --mode default
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_SCRIPT = REPO_ROOT / "scripts" / "log_cadence_event.py"
MODES = ("default", "technical", "strategic", "minimal")

# Common instance territory histories (optional; marked missing if absent).
TERRITORY_HISTORIES = [
    "docs/skill-work/work-coffee/work-coffee-history.md",
    "docs/skill-work/work-dream/work-dream-history.md",
    "docs/skill-work/work-politics/work-politics-history.md",
    "docs/skill-work/work-dev/work-dev-history.md",
]


def _optional_second_repo() -> Path | None:
    """If set, show git status for a sibling instance repo (multi-root workflows)."""
    env = os.environ.get("GRACE_MAR_INSTANCE_ROOT", "").strip()
    if env:
        p = Path(env).expanduser().resolve()
        if p.is_dir() and (p / ".git").exists():
            return p
    return None


def _run_git(cwd: Path, *args: str) -> str:
    try:
        r = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=60,
        )
        out = (r.stdout or "").strip()
        err = (r.stderr or "").strip()
        if r.returncode != 0:
            return f"(git exit {r.returncode}) {err or out or 'no output'}"
        return out or "(empty)"
    except FileNotFoundError:
        return "(git not found)"
    except subprocess.TimeoutExpired:
        return "(git timeout)"


def _checklist(user_id: str) -> list[tuple[str, bool]]:
    uid = user_id.strip()
    rows: list[tuple[str, bool]] = []
    base = REPO_ROOT / "users" / uid
    for rel in (
        "self-memory.md",
        "recursion-gate.md",
        "recursion-gate.json",
        "daily-handoff/night-handoff.json",
        "last-dream.json",
        "session-transcript.md",
    ):
        p = base / rel
        rows.append((str(p.relative_to(REPO_ROOT)), p.is_file()))
    for rel in TERRITORY_HISTORIES:
        p = REPO_ROOT / rel
        rows.append((rel, p.is_file()))
    return rows


def _emit_template(mode: str) -> None:
    print(
        f"""# Session Harvest Packet — (date)

## Use this packet for

## Current session purpose

_(mode: {mode})_

## Main outcomes

## Strongest insights

## Decisions / directions chosen

## Important developments

## Artifacts / files / modules / products

## Risks / tensions / critiques

## Open questions

## Recommended next steps

## Suggested asks for the receiving agent

## Executive compression

## Agent surface
- **Cursor model:** (fill from Cursor model picker / chat header)

Paste this into the target agent session as context for analysis; do not treat it as a fresh-session initializer.
"""
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "-u",
        "--user",
        default=os.getenv("COMPANION_USER_ID", "demo"),
        help="Instance user id (default: COMPANION_USER_ID or demo)",
    )
    ap.add_argument(
        "--mode",
        choices=MODES,
        default="default",
        help="Harvest emphasis (echoed in template and cadence log)",
    )
    ap.add_argument("--emit-template", action="store_true", help="Print markdown skeleton to stdout")
    ap.add_argument(
        "--log",
        action="store_true",
        help="Append work-cadence-events.md line via log_cadence_event.py --kind harvest",
    )
    args = ap.parse_args()

    if args.emit_template:
        _emit_template(args.mode)

    print("## Session harvest — on-disk checklist\n")
    print(f"- **repo:** `{REPO_ROOT}`")
    print(f"- **user:** `{args.user}`\n")
    for rel, ok in _checklist(args.user):
        mark = "yes" if ok else "missing"
        print(f"- `{rel}` — {mark}")

    print("\n### git (this repo)\n")
    print("```")
    print(_run_git(REPO_ROOT, "status", "-sb"))
    print("```\n")
    print("```")
    print(_run_git(REPO_ROOT, "log", "--oneline", "-10"))
    print("```")

    second = _optional_second_repo()
    if second is not None:
        print("\n### git (GRACE_MAR_INSTANCE_ROOT)\n")
        print(f"`{second}`\n")
        print("```")
        print(_run_git(second, "status", "-sb"))
        print("```")
    else:
        print("\n### Second repo\n")
        print(
            "(optional) Set `GRACE_MAR_INSTANCE_ROOT` to an instance git root "
            "for an extra one-line `git status` in multi-root workflows.\n"
        )

    if args.log:
        cmd = [
            sys.executable,
            str(LOG_SCRIPT),
            "--kind",
            "harvest",
            "-u",
            args.user.strip(),
            "--ok",
            "--mode",
            args.mode,
            "--kv",
            "source=session_harvest",
        ]
        r = subprocess.run(cmd, cwd=str(REPO_ROOT))
        return r.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
