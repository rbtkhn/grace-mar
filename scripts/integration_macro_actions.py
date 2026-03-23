#!/usr/bin/env python3
"""
Stateless helper: suggest branch names and merge order for parallel macro-actions.

Does not modify git state or the Record. See docs/skill-work/work-dev/PARALLEL-MACRO-ACTIONS.md
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone


def _slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\-.]+", "-", s, flags=re.UNICODE)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "session"


def cmd_branches(args: argparse.Namespace) -> int:
    slug = _slug(args.session)
    prefix = args.prefix.strip().rstrip("/")
    n = max(1, int(args.slots))
    day = datetime.now(timezone.utc).strftime("%Y%m%d")
    print(f"# Parallel macro-actions: {slug}")
    print(f"# Date tag: {day}  (informational; branches use session + slot only)")
    print(f"# Merge order: agent-1 → agent-{n} → integration branch / main")
    print()
    for i in range(1, n + 1):
        name = f"{prefix}/{slug}-agent-{i}"
        print(f"  {i}. {name}")
    print()
    print("Suggested git (run from repo root, after committing or stashing):")
    print(f"  git fetch origin && git checkout main && git pull")
    for i in range(1, n + 1):
        name = f"{prefix}/{slug}-agent-{i}"
        print(f"  git checkout -b {name}")
        print(f"  # … work scoped to non-overlapping paths …")
        print(f"  git push -u origin {name}")
        print()
    return 0


def cmd_checklist(args: argparse.Namespace) -> int:
    slug = _slug(args.session)
    prefix = args.prefix.strip().rstrip("/")
    n = max(1, int(args.slots))
    lines = [
        f"## Macro-session: `{slug}`",
        "",
        "- [ ] Non-overlapping path ownership agreed (list paths per agent).",
        "- [ ] Branches:",
    ]
    for i in range(1, n + 1):
        lines.append(f"  - [ ] `{prefix}/{slug}-agent-{i}`")
    lines.extend(
        [
            "- [ ] Merge order: **1 → 2 → … → n** into integration or `main` (rebase if needed).",
            "- [ ] RECURSION-GATE / pipeline: stage on branch; **merge Record only via** `process_approved_candidates.py` **after approval**.",
            "- [ ] No simultaneous edits to gated files (`self.md`, `self-evidence.md`, `recursion-gate.md`, `bot/prompt.py`) without single-owner sequencing.",
            "",
        ]
    )
    print("\n".join(lines))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Suggest parallel macro-action branch names (stateless).")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("branches", help="Print suggested branch names and rough git steps")
    b.add_argument("--session", "-s", required=True, help="Session label (slugified for branch names)")
    b.add_argument("--slots", "-n", type=int, default=2, help="Number of parallel agents (default: 2)")
    b.add_argument("--prefix", default="macro", help="Branch prefix (default: macro)")
    b.set_defaults(func=cmd_branches)

    c = sub.add_parser("checklist", help="Print a markdown checklist for paste into a PR or doc")
    c.add_argument("--session", "-s", required=True, help="Session label")
    c.add_argument("--slots", "-n", type=int, default=2, help="Number of parallel agents (default: 2)")
    c.add_argument("--prefix", default="macro", help="Branch prefix (default: macro)")
    c.set_defaults(func=cmd_checklist)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
