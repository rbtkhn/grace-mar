#!/usr/bin/env python3
"""
Thin checklist + optional template for the session harvest ritual.

Does not author insights — the agent fills narrative from the visible thread.
See .cursor/skills/harvest/SKILL.md and docs/skill-work/work-cadence/harvest-packet-contract.md.

Usage:
  python3 scripts/session_harvest.py -u grace-mar
  python3 scripts/session_harvest.py -u grace-mar --mode strategic --emit-template
  python3 scripts/session_harvest.py -u grace-mar --log --mode default
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

TERRITORY_HISTORIES = [
    "docs/skill-work/work-coffee/work-coffee-history.md",
    "docs/skill-work/work-dream/work-dream-history.md",
    "docs/skill-work/work-politics/work-politics-history.md",
    "docs/skill-work/work-dev/work-dev-history.md",
]


def _default_companion_self_root() -> Path:
    env = os.environ.get("GRACE_MAR_COMPANION_SELF", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return REPO_ROOT / "companion-self"


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
    for name in ("self-memory.md", "recursion-gate.md", "last-dream.json", "session-transcript.md"):
        p = base / name
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
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", "grace-mar"), help="Instance user id")
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
    ap.add_argument(
        "--cursor-model",
        default=None,
        help="With --log: forwarded to log_cadence_event (else CURSOR_MODEL env)",
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

    print("\n### git (grace-mar)\n")
    print("```")
    print(_run_git(REPO_ROOT, "status", "-sb"))
    print("```\n")
    print("```")
    print(_run_git(REPO_ROOT, "log", "--oneline", "-10"))
    print("```")

    cs = _default_companion_self_root()
    if cs.is_dir() and (cs / ".git").exists():
        print("\n### git (companion-self)\n")
        print(f"`{cs}`\n")
        print("```")
        print(_run_git(cs, "status", "-sb"))
        print("```")
    else:
        print("\n### companion-self\n")
        print(f"(not present or not a git repo: `{cs}`)\n")

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
        if args.cursor_model and args.cursor_model.strip():
            cmd.extend(["--cursor-model", args.cursor_model.strip()])
        r = subprocess.run(cmd, cwd=str(REPO_ROOT))
        return r.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
