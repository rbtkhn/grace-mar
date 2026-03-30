#!/usr/bin/env python3
"""
Operator re-entry stack — run handoff check, daily warmup, and harness warmup in one paste.

Handoff and daily warmup overlap somewhat (gate counts, dirty paths); this is for convenience.

Usage:
    python3 scripts/operator_reentry_stack.py -u grace-mar
    python3 scripts/operator_reentry_stack.py -u grace-mar --compact   # short harness block only
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
    p = argparse.ArgumentParser(description="Run operator handoff + daily warmup + harness warmup (read-only).")
    p.add_argument("-u", "--user", default="grace-mar", help="User id (default grace-mar)")
    p.add_argument(
        "--compact",
        action="store_true",
        help="Pass --compact to harness_warmup.py only",
    )
    args = p.parse_args()
    user = args.user
    py = sys.executable

    steps: list[list[str]] = [
        [py, "scripts/operator_handoff_check.py", "-u", user],
        [py, "scripts/operator_daily_warmup.py", "-u", user],
    ]
    hw = [py, "scripts/harness_warmup.py", "-u", user]
    if args.compact:
        hw.append("--compact")
    steps.append(hw)

    for argv in steps:
        code = _run(argv)
        if code != 0:
            return code
    return 0


if __name__ == "__main__":
    sys.exit(main())
