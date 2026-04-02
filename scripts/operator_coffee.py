#!/usr/bin/env python3
"""
Consolidated coffee Step 1 — single entry point for all warmup modes.

Replaces the need for the agent (or operator) to choose between
operator_daily_warmup, harness_warmup, operator_handoff_check, and
operator_reentry_stack depending on context.  Mode selects the right
combination; all four underlying scripts are preserved and still callable
individually.

Modes
-----
  work-start  Full work-start coffee: daily warmup + harness warmup + branch snapshot
  light       Lighter pass: daily warmup + compact harness + one-line branch
  minimal     Minimal pass: compact harness only (no daily warmup unless --include-warmup)
  closeout    Night closeout: handoff check (gate, PH closeout, commits, worktree)
  reentry     Cold-thread stack: handoff + daily warmup + harness (same as operator_reentry_stack)

Usage
-----
    python3 scripts/operator_coffee.py -u grace-mar                     # default: work-start
    python3 scripts/operator_coffee.py -u grace-mar --mode light
    python3 scripts/operator_coffee.py -u grace-mar --mode closeout
    python3 scripts/operator_coffee.py -u grace-mar --mode reentry --compact
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
MODES = ("work-start", "light", "minimal", "closeout", "reentry")


def _run(argv: list[str], *, label: str | None = None) -> int:
    display = label or " ".join(argv)
    print(f"\n{'=' * 60}\n$ {display}\n{'=' * 60}\n", flush=True)
    r = subprocess.run(argv, cwd=str(_REPO))
    return r.returncode


def _branch_snapshot() -> str:
    """One plain-language block: branch hygiene status."""
    status = subprocess.run(
        ["git", "status", "-sb"], cwd=str(_REPO),
        capture_output=True, text=True,
    )
    branches = subprocess.run(
        ["git", "branch", "-vv"], cwd=str(_REPO),
        capture_output=True, text=True,
    )
    status_out = status.stdout.strip()
    branch_out = branches.stdout.strip()
    non_main = [
        line.strip() for line in branch_out.splitlines()
        if line.strip() and not line.strip().startswith("* main")
        and not line.strip().startswith("main")
    ]
    if not non_main:
        return "Branch hygiene: clean (main only)."
    return (
        f"Branch snapshot:\n{status_out}\n\n"
        f"Branches:\n{branch_out}\n\n"
        f"Non-main branches: {len(non_main)} — review per git-branch-hygiene.md."
    )


def main() -> int:
    p = argparse.ArgumentParser(
        description="Consolidated coffee Step 1 — single entry point for all warmup modes."
    )
    p.add_argument("-u", "--user", default="grace-mar", help="User id (default: grace-mar)")
    p.add_argument(
        "--mode", "-m",
        choices=MODES,
        default="work-start",
        help="Warmup mode (default: work-start)",
    )
    p.add_argument(
        "--compact",
        action="store_true",
        help="Pass --compact to harness_warmup.py",
    )
    p.add_argument(
        "--include-warmup",
        action="store_true",
        help="In minimal mode, also run operator_daily_warmup",
    )
    args = p.parse_args()
    user = args.user
    py = sys.executable

    from gate_block_parser import sweep_rejected_to_processed
    gate_path = _REPO / "users" / user / "recursion-gate.md"
    swept = sweep_rejected_to_processed(gate_path)
    if swept:
        print(f"Gate cleanup: moved {len(swept)} rejected candidate(s) to Processed: {', '.join(swept)}")

    warmup = [py, "scripts/operator_daily_warmup.py", "-u", user]
    harness = [py, "scripts/harness_warmup.py", "-u", user]
    harness_compact = [py, "scripts/harness_warmup.py", "-u", user, "--compact"]
    handoff = [py, "scripts/operator_handoff_check.py", "-u", user]

    steps: list[list[str]] = []

    if args.mode == "work-start":
        steps = [warmup, harness_compact if args.compact else harness]
    elif args.mode == "light":
        steps = [warmup, harness_compact]
    elif args.mode == "minimal":
        if args.include_warmup:
            steps.append(warmup)
        steps.append(harness_compact)
    elif args.mode == "closeout":
        steps = [handoff]
    elif args.mode == "reentry":
        steps = [handoff, warmup, harness_compact if args.compact else harness]

    for argv in steps:
        code = _run(argv)
        if code != 0:
            return code

    if args.mode != "closeout":
        print(f"\n{'=' * 60}\n$ git branch snapshot\n{'=' * 60}\n", flush=True)
        print(_branch_snapshot())

    try:
        from log_cadence_event import append_cadence_event
        append_cadence_event("coffee", user, ok=True, mode=args.mode)
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
