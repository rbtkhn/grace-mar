#!/usr/bin/env python3
"""Summarize retrieval-miss records from runtime/retrieval-misses/index.jsonl.

Outputs counts by failure_class and retrieval_surface. Optional --since filter.
Non-canonical; see runtime/retrieval-misses/README.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any

_RUNTIME_DIR = Path(__file__).resolve().parent
if str(_RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(_RUNTIME_DIR))

import ledger_paths  # noqa: E402

MISS_FILE = ledger_paths.retrieval_misses_jsonl()


def load_records(since: date | None = None) -> list[dict[str, Any]]:
    if not MISS_FILE.exists():
        return []
    records: list[dict[str, Any]] = []
    for line_no, raw in enumerate(MISS_FILE.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError:
            print(f"warning: skipping malformed line {line_no}", file=sys.stderr)
            continue
        if since:
            ts_str = rec.get("timestamp", "")
            try:
                ts_date = datetime.fromisoformat(ts_str.replace("Z", "+00:00")).date()
            except (ValueError, AttributeError):
                continue
            if ts_date < since:
                continue
        records.append(rec)
    return records


def print_table(title: str, counter: Counter[str]) -> None:
    if not counter:
        print(f"\n{title}: (none)")
        return
    label_width = max(len(k) for k in counter)
    total = sum(counter.values())
    print(f"\n{title} ({total} total)")
    print("-" * (label_width + 10))
    for key, count in counter.most_common():
        print(f"  {key:<{label_width}}  {count:>5}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize Grace-Mar retrieval misses.")
    parser.add_argument("--since", help="Only include records on or after YYYY-MM-DD")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of table")
    args = parser.parse_args()

    since: date | None = None
    if args.since:
        try:
            since = date.fromisoformat(args.since)
        except ValueError:
            print(f"error: invalid date format: {args.since} (expected YYYY-MM-DD)", file=sys.stderr)
            return 2

    records = load_records(since)

    if not records:
        if not MISS_FILE.exists():
            print(f"No ledger file found at {MISS_FILE}")
        else:
            print("No matching records.")
        return 0

    by_class: Counter[str] = Counter()
    by_surface: Counter[str] = Counter()
    for rec in records:
        by_class[rec.get("failure_class", "unknown")] += 1
        by_surface[rec.get("retrieval_surface", "unknown")] += 1

    if args.json:
        out = {
            "total": len(records),
            "by_failure_class": dict(by_class.most_common()),
            "by_retrieval_surface": dict(by_surface.most_common()),
        }
        if since:
            out["since"] = since.isoformat()
        print(json.dumps(out, indent=2))
    else:
        header = f"Retrieval-miss summary — {len(records)} records"
        if since:
            header += f" (since {since.isoformat()})"
        print(header)
        print_table("By failure class", by_class)
        print_table("By retrieval surface", by_surface)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
