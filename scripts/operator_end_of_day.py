#!/usr/bin/env python3
"""
Operator end-of-day stack — run auto_dream then operator_handoff_check in one paste.

Night-side counterpart to operator_reentry_stack.py (morning).  Dream handles
memory normalization, integrity, governance, and contradiction digest; handoff
check captures gate state, commits, worktree noise, and the re-entry prompt
for tomorrow's coffee.

Strategy notebook (LIB-0153): this script does not edit chapters/YYYY-MM/days.md.
When an agent runs the full `dream` ritual, follow `.cursor/skills/dream/SKILL.md`
§ Strategy notebook — end-of-day production closeout for that calendar day's page
(read STATUS + days.md, stub / condense note / gap).

Xavier journal (LIB-0154): this script does not run `xavier_journal_ob1_digest.py`.
Full `dream` includes § Xavier journal — generate the day file with `--write` (network).

Usage:
    python3 scripts/operator_end_of_day.py -u grace-mar
    python3 scripts/operator_end_of_day.py -u grace-mar --strict   # strict dream mode
    python3 scripts/operator_end_of_day.py -u grace-mar --dry-run  # inspect without writing
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent


def _run(argv: list[str]) -> int:
    print(f"\n{'=' * 60}\n$ {' '.join(argv)}\n{'=' * 60}\n", flush=True)
    r = subprocess.run(argv, cwd=str(_REPO))
    return r.returncode


def main() -> int:
    p = argparse.ArgumentParser(
        description=(
            "Run auto_dream + operator_handoff_check (read-only night-close stack). "
            "Full dream ritual also includes strategy-notebook closeout and "
            "xavier-journal digest generation per .cursor/skills/dream/SKILL.md "
            "(not run by this script)."
        )
    )
    p.add_argument("-u", "--user", default="grace-mar", help="User id (default grace-mar)")
    p.add_argument(
        "--strict",
        action="store_true",
        help="Pass --strict to auto_dream.py",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Pass --dry-run to auto_dream.py (no writes)",
    )
    p.add_argument(
        "--cursor-model",
        default=None,
        help="Forwarded to auto_dream.py for agent_surface + cadence line",
    )
    args = p.parse_args()
    user = args.user
    py = sys.executable

    dream_cmd = [py, "scripts/auto_dream.py", "-u", user]
    if args.strict:
        dream_cmd.append("--strict")
    if args.dry_run:
        dream_cmd.append("--dry-run")
    if args.cursor_model and args.cursor_model.strip():
        dream_cmd.extend(["--cursor-model", args.cursor_model.strip()])

    steps: list[list[str]] = [
        dream_cmd,
        [py, "scripts/operator_handoff_check.py", "-u", user],
    ]

    for argv in steps:
        code = _run(argv)
        if code != 0:
            return code
    return 0


if __name__ == "__main__":
    sys.exit(main())
