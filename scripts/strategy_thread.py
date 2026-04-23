#!/usr/bin/env python3
"""Operator command **``thread``**: triage inbox + extract for thread distillation.

After **``thread:<expert_id>``** paste-ready lines are in
``docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md``,
run (from repo root)::

    bin/thread

or::

    python3 scripts/strategy_thread.py

This runs **two automatic steps**:

1. **Triage** (``strategy_expert_transcript.py``) — routes ``thread:`` lines
   from the inbox to per-expert transcript files (append-only, 7-day prune),
   and appends lines derived from ``raw-input/**`` markdown with
   ``kind: rss-item`` + ``thread:`` in YAML (see ``fetch-sources.json`` /
   ``fetch_strategy_raw_input.py``).
2. **Extraction** (``strategy_expert_corpus.py``) — reads each expert's
   transcript + existing ``strategy-page`` blocks (+ optional legacy index rows),
   writes raw material to thread files between script markers.

After extraction, prints **page-candidate suggestions** when cross-expert
material or tension-bearing content is detected.

**Batch-analysis snapshot** has moved to ``strategy_weave.py`` — run
``weave`` to refresh it.

**Not** **``weave``**: **``thread``** updates transcript and thread files
only; it does **not** perform integrated analysis or write pages.

WORK-only; not Record.

Spec: ``docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md``
§ *Thread (terminology)*.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts"))

DEFAULT_INBOX = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md"
)
DEFAULT_OUT_DIR = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
)
DEFAULT_KNOT_INDEX = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook/knot-index.yaml"
)


def _suggest_page_candidates(out_dir: Path) -> list[str]:
    """Detect cross-expert page opportunities from pages already in threads."""
    from strategy_page_reader import discover_all_pages

    all_pages = discover_all_pages(out_dir)
    page_experts: dict[str, list[str]] = defaultdict(list)
    for expert_id, pages in all_pages.items():
        for p in pages:
            page_experts[p.id].append(expert_id)

    suggestions: list[str] = []
    for page_id, experts in page_experts.items():
        if len(experts) >= 2:
            watch = ""
            for ep_list in all_pages.values():
                for p in ep_list:
                    if p.id == page_id and p.watch:
                        watch = p.watch
                        break
                if watch:
                    break
            cmd = f"page {' '.join(sorted(experts))}"
            if watch:
                cmd += f" --watch {watch}"
            suggestions.append(
                f"page candidate: '{page_id}' spans {', '.join(sorted(experts))} → `{cmd}`"
            )
    return suggestions


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR)
    p.add_argument("--knot-index", type=Path, default=DEFAULT_KNOT_INDEX)
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--today", help="Override today (YYYY-MM-DD)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    from datetime import datetime
    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else None

    # Step 1: Triage inbox → transcript files (append + prune)
    print("--- Step 1: Triage (inbox → transcripts) ---")
    from strategy_expert_transcript import triage_to_transcripts
    transcript_paths = triage_to_transcripts(
        inbox_path=args.inbox,
        out_dir=args.out,
        keep_days=max(1, args.days),
        today=today,
        dry_run=args.dry_run,
    )
    for path in transcript_paths:
        print(f"  transcript: {path.relative_to(REPO_ROOT)}")

    # Step 2: Extract transcript + knots + pages → thread files
    print("--- Step 2: Extraction (transcripts + pages → threads) ---")
    from strategy_expert_corpus import rebuild_threads
    thread_paths = rebuild_threads(
        out_dir=args.out,
        knot_index_path=args.knot_index,
        dry_run=args.dry_run,
    )
    for path in thread_paths:
        print(f"  thread: {path.relative_to(REPO_ROOT)}")

    # Page-candidate suggestions
    suggestions = _suggest_page_candidates(args.out)
    if suggestions:
        print("--- Page candidates ---")
        for s in suggestions:
            print(f"  {s}")

    mode = "dry-run" if args.dry_run else "write"
    print(
        f"\nDone ({mode}): {len(transcript_paths)} transcripts, "
        f"{len(thread_paths)} threads"
    )
    if suggestions:
        print(f"  {len(suggestions)} page candidate(s) detected — run weave + page to act on them")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
