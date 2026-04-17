#!/usr/bin/env python3
"""Replace the human-readable header in each ``strategy-expert-<id>-transcript.md``

with :func:`strategy_expert_transcript.canonical_transcript_header` (matches triage output
for new files). Body below ``TRIAGE_MARKER`` is unchanged.

WORK only; not Record.

Usage::

    python3 scripts/refresh_strategy_expert_transcript_headers.py
    python3 scripts/refresh_strategy_expert_transcript_headers.py --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_expert_transcript import TRIAGE_MARKER, canonical_transcript_header

NOTEBOOK = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
RE_TRANSCRIPT = re.compile(r"^strategy-expert-(.+)-transcript\.md$")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="Print paths only; do not write")
    args = p.parse_args()

    paths = sorted(NOTEBOOK.glob("strategy-expert-*-transcript.md"))
    updated = 0
    for path in paths:
        m = RE_TRANSCRIPT.match(path.name)
        if not m:
            continue
        expert_id = m.group(1)
        text = path.read_text(encoding="utf-8")
        idx = text.find(TRIAGE_MARKER)
        if idx == -1:
            print(f"skip (no triage marker): {path.relative_to(REPO_ROOT)}", flush=True)
            continue
        body = text[idx + len(TRIAGE_MARKER) :]
        new_text = canonical_transcript_header(expert_id) + body
        if new_text == text:
            continue
        if args.dry_run:
            print(f"would update: {path.relative_to(REPO_ROOT)}", flush=True)
        else:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated: {path.relative_to(REPO_ROOT)}", flush=True)
        updated += 1
    print(f"Done. {'Would update' if args.dry_run else 'Updated'} {updated} file(s).", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
