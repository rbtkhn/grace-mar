#!/usr/bin/env python3
"""
Seed month-scale human narrative segments in an expert thread file.

Purpose
-------
- Add human-maintained segment headings above the machine thread markers
- Designed for month-scale expert-thread segments like:
    ## 2026-01
    ## 2026-02
    ## 2026-03
- Never touches the machine extraction block

Typical use
-----------
python3 scripts/seed_expert_thread_segments.py \
  --expert-id daniel-davis \
  --segments 2026-01,2026-02,2026-03 \
  --dry-run

python3 scripts/seed_expert_thread_segments.py \
  --expert-id daniel-davis \
  --segments 2026-01,2026-02,2026-03 \
  --apply
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def display_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def build_stub(seg: str) -> str:
    return "\n".join(
        [
            f"## {seg}",
            "- [strength: medium] Core stance / through-line for this segment.",
            "- [strength: medium] Main mechanism or causal claim.",
            "- [strength: low] Main unresolved ambiguity / open question.",
            "- [strength: medium] Main divergence or tension versus another expert.",
            "",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--expert-id", required=True)
    ap.add_argument("--segments", required=True, help="Comma-separated YYYY-MM values")
    ap.add_argument("--thread-path", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if not args.dry_run and not args.apply:
        print(
            "Specify --dry-run (print updated thread to stdout) or --apply (write file).",
            file=sys.stderr,
        )
        return 2

    expert_id = args.expert_id.strip()
    segments = [s.strip() for s in args.segments.split(",") if s.strip()]
    thread_path = (
        Path(args.thread_path) if args.thread_path else NOTEBOOK_DIR / f"strategy-expert-{expert_id}-thread.md"
    )

    if not thread_path.exists():
        raise SystemExit(f"Thread file not found: {thread_path}")

    text = read_text(thread_path)

    if THREAD_MARKER_START in text:
        human, machine = text.split(THREAD_MARKER_START, 1)
        machine = THREAD_MARKER_START + machine
    else:
        human, machine = text, ""

    human = human.rstrip() + "\n\n"

    for seg in segments:
        if re.search(rf"^##\s+{re.escape(seg)}\s*$", human, re.MULTILINE):
            continue
        human += build_stub(seg)

    updated = human.rstrip() + "\n\n"
    if machine:
        updated += machine.lstrip("\n")
    else:
        updated = updated.rstrip() + "\n"

    if args.dry_run:
        print(updated)
        if args.apply:
            thread_path.write_text(updated, encoding="utf-8")
            print(f"Wrote {display_path(thread_path)}", file=sys.stderr)
        return 0

    thread_path.write_text(updated, encoding="utf-8")
    print(f"Seeded segments in {display_path(thread_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
