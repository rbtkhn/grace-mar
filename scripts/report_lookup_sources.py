#!/usr/bin/env python3
"""
Report lookup source distribution (library vs CMC vs full) from dyad:lookup events.

Supports capability-dissipation awareness: which sources actually satisfy lookups.
See docs/implementable-insights.md §8.

Usage:
    python scripts/report_lookup_sources.py [--user grace-mar] [--days 30] [--json]
"""

import argparse
import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER = "grace-mar"
DEFAULT_DAYS = 30


def _parse_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().strip().splitlines():
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return rows


def _ts_in_window(ts_str: str, cutoff: datetime) -> bool:
    if not ts_str:
        return False
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        if dt.tzinfo:
            dt = dt.replace(tzinfo=None)
        return dt >= cutoff
    except (ValueError, TypeError):
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Report lookup source distribution from dyad:lookup events"
    )
    parser.add_argument("--user", "-u", default=DEFAULT_USER, help="User id")
    parser.add_argument("--days", "-d", type=int, default=DEFAULT_DAYS, help="Days to include")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    profile_dir = REPO_ROOT / "users" / args.user
    events_path = profile_dir / "pipeline-events.jsonl"
    cutoff = datetime.now() - timedelta(days=args.days)

    counts: Counter[str] = Counter()
    total = 0
    for row in _parse_jsonl(events_path):
        if row.get("event") != "dyad:lookup":
            continue
        if not _ts_in_window(row.get("ts", ""), cutoff):
            continue
        total += 1
        lookup_source = row.get("lookup_source", "unknown")
        counts[lookup_source] += 1

    if args.json:
        out = {
            "user": args.user,
            "days": args.days,
            "total_lookups": total,
            "by_source": dict(counts),
        }
        print(json.dumps(out, indent=2))
    else:
        print(f"Lookup source distribution — {args.user}, last {args.days} days")
        print("=" * 50)
        print(f"Total dyad:lookup events: {total}")
        if total == 0:
            print("(No lookups in window; lookup_source added 2026-02)")
            return
        for src in ("library", "cmc", "full", "unknown"):
            n = counts.get(src, 0)
            pct = 100.0 * n / total if total else 0
            print(f"  {src:12} {n:4} ({pct:5.1f}%)")
        for src, n in sorted(counts.items()):
            if src not in ("library", "cmc", "full", "unknown"):
                pct = 100.0 * n / total if total else 0
                print(f"  {src:12} {n:4} ({pct:5.1f}%)")


if __name__ == "__main__":
    main()
