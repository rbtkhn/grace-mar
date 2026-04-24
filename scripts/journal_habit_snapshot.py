#!/usr/bin/env python3
"""
Journal habit snapshot — filename-based rhythm only.

Scans dev-journal (*-day-*.md) and cici-notebook (YYYY-MM-DD.md) for calendar
dates in filenames; prints active days in a rolling window and staleness.

Does not parse frontmatter or prose. See docs/skill-work/journal-metrics-habit.md.
"""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEV_JOURNAL = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "dev-journal"
CICI_JOURNAL = REPO_ROOT / "docs" / "skill-work" / "work-cici" / "cici-notebook"

DEV_FILENAME = re.compile(r"(\d{4}-\d{2}-\d{2})-day-\d+\.md$")
XAV_FILENAME = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")

SKIP_ROOT_MD = frozenset({"README.md", "SYNTHESIS-SOURCES.md"})


def _parse_dates_journal(root: Path, pattern: re.Pattern[str]) -> list[date]:
    if not root.is_dir():
        return []
    out: list[date] = []
    for p in root.iterdir():
        if not p.is_file() or p.suffix != ".md" or p.name in SKIP_ROOT_MD:
            continue
        m = pattern.match(p.name)
        if not m:
            continue
        y, mo, d = (int(x) for x in m.group(1).split("-"))
        out.append(date(y, mo, d))
    return sorted(out)


def _count_active(dates: list[date], today: date, window: int) -> int:
    if window < 1:
        return 0
    start = today - timedelta(days=window - 1)
    return sum(1 for d in dates if start <= d <= today)


def _staleness_days(dates: list[date], today: date) -> int | None:
    if not dates:
        return None
    # Future-dated filenames (timezone drift, typo) clamp to 0 — not negative.
    return max(0, (today - max(dates)).days)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Journal habit snapshot: active days + staleness (filename dates only)"
    )
    parser.add_argument(
        "--window",
        type=int,
        default=14,
        metavar="N",
        help="Rolling window in days (default 14)",
    )
    parser.add_argument(
        "--utc",
        action="store_true",
        help="Use UTC calendar date for 'today'",
    )
    args = parser.parse_args()
    today = datetime.now(timezone.utc).date() if args.utc else date.today()

    dev_dates = _parse_dates_journal(DEV_JOURNAL, DEV_FILENAME)
    cici_dates = _parse_dates_journal(CICI_JOURNAL, XAV_FILENAME)
    w = args.window

    print(f"# Journal habit snapshot (today={today}, window={w}d)\n")
    for label, dates in (
        ("dev-journal", dev_dates),
        ("cici-notebook", cici_dates),
    ):
        active = _count_active(dates, today, w)
        stale = _staleness_days(dates, today)
        last = max(dates) if dates else None
        print(f"## {label}")
        print(f"- Active days in last {w}d: **{active}**")
        print(f"- Last entry date (from filename): {last or '—'}")
        if stale is None:
            print("- Staleness (days since last entry): — (no entries)")
        else:
            print(f"- Staleness (days since last entry): **{stale}**")
        print()

    print(
        "Phase 0 / optional YAML: docs/skill-work/journal-metrics-habit.md",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
