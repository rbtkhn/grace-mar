#!/usr/bin/env python3
"""Operator command **``thread``**: triage inbox + extract for thread distillation.

After **``thread:<expert_id>``** paste-ready lines are in
``docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md``,
run (from repo root)::

    bin/thread

or::

    python3 scripts/strategy_thread.py

This runs **three automatic steps**:

1. **Triage** (``strategy_expert_transcript.py``) — routes ``thread:`` lines
   from the inbox to per-expert ``-transcript.md`` files (append-only, 7-day
   prune). Internal infrastructure; not a separate operator command.
2. **Extraction** (``strategy_expert_corpus.py``) — reads each expert's
   transcript + relevant knots, writes raw material to ``-thread.md`` between
   script markers. The assistant then refines this into a curated analytical
   thread.
3. **Batch-analysis snapshot** (``parse_batch_analysis.py``) — parses
   ``batch-analysis`` lines from the inbox and writes a JSON snapshot to
   ``artifacts/skill-work/work-strategy/batch-analysis-snapshot.json``.

**Not** **``weave``**: **``thread``** updates transcript and thread files
only; it does **not** merge into ``days.md`` or knot pages.

WORK-only; not Record.

Spec: ``docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md``
§ *Thread (terminology)*.
"""

from __future__ import annotations

import argparse
import sys
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

    # Step 2: Extract transcript + knots → thread files
    print("--- Step 2: Extraction (transcripts + knots → threads) ---")
    from strategy_expert_corpus import rebuild_threads
    thread_paths = rebuild_threads(
        out_dir=args.out,
        knot_index_path=args.knot_index,
        dry_run=args.dry_run,
    )
    for path in thread_paths:
        print(f"  thread: {path.relative_to(REPO_ROOT)}")

    # Step 3: Refresh batch-analysis snapshot
    print("--- Step 3: Batch-analysis snapshot ---")
    from parse_batch_analysis import parse_inbox, build_snapshot
    import json
    batch_refs = parse_inbox(args.inbox)
    snapshot = build_snapshot(batch_refs)
    batch_out = REPO_ROOT / "artifacts/skill-work/work-strategy/batch-analysis-snapshot.json"
    if args.dry_run:
        print(f"  dry-run: {len(batch_refs)} batch-analysis refs (not written)")
    else:
        batch_out.parent.mkdir(parents=True, exist_ok=True)
        batch_out.write_text(
            json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"  snapshot: {batch_out.relative_to(REPO_ROOT)} ({len(batch_refs)} refs)")

    mode = "dry-run" if args.dry_run else "write"
    print(
        f"\nDone ({mode}): {len(transcript_paths)} transcripts, "
        f"{len(thread_paths)} threads, {len(batch_refs)} batch-analysis refs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
