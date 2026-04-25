#!/usr/bin/env python3
"""Remove strategy raw-input date folders older than N days (default 7).

Scans ``docs/skill-work/work-strategy/strategy-notebook/raw-input/`` for
subdirectories named ``YYYY-MM-DD`` (by convention **pub_date** / air day — see
``raw-input/README.md`` § Layout) and deletes those strictly before the cutoff
date (local timezone). Non-date dirs (e.g. ``_aired-pending``) are skipped.

If ``.pruning-suspended`` exists under the raw-input root, ``--apply`` refuses
unless ``--override`` is passed (operator-initiated prune). Dry-run is
always allowed.

WORK-only; not Record.

Usage:
  python3 scripts/prune_strategy_raw_input.py --dry-run
  python3 scripts/prune_strategy_raw_input.py --apply
  python3 scripts/prune_strategy_raw_input.py --apply --override   # when suspended
"""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_ROOT = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/raw-input"
)

_RE_DATE_DIR = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help=f"raw-input root (default: {DEFAULT_ROOT.relative_to(REPO_ROOT)})",
    )
    p.add_argument(
        "--days",
        type=int,
        default=7,
        help="Keep folders for this many calendar days including today (default: 7)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print paths that would be removed; do not delete",
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="Actually remove old date directories",
    )
    p.add_argument(
        "--override",
        action="store_true",
        help="Required for --apply when raw-input/.pruning-suspended exists",
    )
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    if args.dry_run and args.apply:
        raise SystemExit("Use only one of --dry-run or --apply")
    if not args.dry_run and not args.apply:
        args.dry_run = True

    root: Path = args.root.resolve()
    if not root.is_dir():
        print(f"raw-input root missing or not a directory: {root}")
        return 1

    suspend_marker = root / ".pruning-suspended"
    if args.apply and suspend_marker.is_file() and not args.override:
        print(
            "Raw-input pruning is suspended (marker file present):\n"
            f"  {suspend_marker.relative_to(REPO_ROOT)}\n"
            "Pass --override with --apply to delete old folders, or remove the marker file.\n"
            "Dry-run is unchanged; run without --apply to preview."
        )
        return 1

    today = date.today()
    # Match strategy_expert_transcript.py: keep sections where d > cutoff,
    # cutoff = today - keep_days (default 7). Same calendar window as expert transcripts.
    cutoff = today - timedelta(days=args.days)

    candidates: list[tuple[date, Path]] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        name = child.name
        if not _RE_DATE_DIR.match(name):
            continue
        y, m, d = int(name[0:4]), int(name[5:7]), int(name[8:10])
        folder_date = date(y, m, d)
        if folder_date <= cutoff:
            candidates.append((folder_date, child))

    if not candidates:
        print(
            f"No date folders to prune under {root} "
            f"(remove when folder_date <= {cutoff}; --days {args.days})"
        )
        return 0

    for folder_date, path in sorted(candidates, key=lambda x: x[0]):
        rel = path.relative_to(REPO_ROOT)
        if args.apply:
            shutil.rmtree(path)
            print(f"removed {rel}")
        else:
            print(f"would remove {rel} (date {folder_date} <= cutoff {cutoff})")

    if args.dry_run:
        print("(dry-run; pass --apply to delete)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
