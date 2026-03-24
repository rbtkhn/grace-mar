#!/usr/bin/env python3
"""
Promote approved content from review-queue/ to canonical locations.

Usage:
    python3 scripts/work_jiang/promote_from_review_queue.py ch07 --dry-run
    python3 scripts/work_jiang/promote_from_review_queue.py ch07 --approve
    python3 scripts/work_jiang/promote_from_review_queue.py --list
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORK_JIANG = REPO_ROOT / "research" / "external" / "work-jiang"
REVIEW_QUEUE = WORK_JIANG / "review-queue"
ARCHIVE = REVIEW_QUEUE / "archive"

PROMOTION_MAP = {
    "draft.md": lambda scope: f"chapters/{scope}/draft.md",
    "outline.md": lambda scope: f"chapters/{scope}/outline.md",
    "notes.md": lambda scope: f"chapters/{scope}/notes.md",
    "predictions.json": lambda scope: f"prediction-tracking/staging/{scope}-predictions.json",
}


sys.path.insert(0, str(Path(__file__).resolve().parent))


def list_pending() -> None:
    if not REVIEW_QUEUE.exists():
        print("No review-queue directory found.")
        return
    scopes = sorted(
        d.name for d in REVIEW_QUEUE.iterdir()
        if d.is_dir() and d.name not in ("archive", ".git")
    )
    if not scopes:
        print("Review queue is empty.")
        return
    for scope in scopes:
        files = sorted(f.name for f in (REVIEW_QUEUE / scope).iterdir() if f.is_file())
        print(f"  {scope}/  ({len(files)} file(s)): {', '.join(files)}")


def promote(scope: str, dry_run: bool = False) -> None:
    scope_dir = REVIEW_QUEUE / scope
    if not scope_dir.exists() or not scope_dir.is_dir():
        print(f"No review-queue entry for '{scope}'", file=sys.stderr)
        sys.exit(1)

    files = [f for f in scope_dir.iterdir() if f.is_file()]
    if not files:
        print(f"No files in review-queue/{scope}/")
        return

    promoted = 0
    for f in files:
        target_fn = PROMOTION_MAP.get(f.name)
        if target_fn:
            dest = WORK_JIANG / target_fn(scope)
        else:
            dest = WORK_JIANG / "chapters" / scope / f.name

        if dry_run:
            print(f"  [dry-run] {f.name} → {dest.relative_to(WORK_JIANG)}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
            print(f"  promoted: {f.name} → {dest.relative_to(WORK_JIANG)}")
        promoted += 1

    if not dry_run:
        archive_dir = ARCHIVE / scope
        archive_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            shutil.move(str(f), str(archive_dir / f.name))
        scope_dir.rmdir()

        try:
            from emit_task_event import append_task_event
            for task_prefix in ("draft", "analysis", "predictions"):
                task_id = f"{task_prefix}-{scope}"
                try:
                    append_task_event(task_id, "merged", note="promoted from review-queue")
                except Exception:
                    pass
        except ImportError:
            pass

        print(f"\n{promoted} file(s) promoted; originals archived to review-queue/archive/{scope}/")
    else:
        print(f"\n{promoted} file(s) would be promoted (dry-run).")


def main() -> None:
    parser = argparse.ArgumentParser(description="Promote review-queue content to canonical.")
    parser.add_argument("scope", nargs="?", help="Scope directory to promote (e.g. ch07)")
    parser.add_argument("--approve", action="store_true", help="Actually promote (default is dry-run)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--list", action="store_true", help="List pending items")
    args = parser.parse_args()

    if args.list:
        list_pending()
        return

    if not args.scope:
        print("Scope is required (e.g. ch07). Use --list to see pending.", file=sys.stderr)
        sys.exit(1)

    promote(args.scope, dry_run=not args.approve)


if __name__ == "__main__":
    main()
