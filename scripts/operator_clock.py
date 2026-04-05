#!/usr/bin/env python3
"""
Single-line authoritative UTC clock for operator threads.

Mitigates mixed dates across user_info, script output, and external docs by giving
one paste-friendly instant. See docs/date-time-conventions.md (ISO UTC).
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone


def main() -> int:
    p = argparse.ArgumentParser(
        description="Print one ISO-8601 UTC timestamp line (operator session clock)."
    )
    p.add_argument(
        "--date-only",
        action="store_true",
        help="Print YYYY-MM-DD only (calendar day in UTC).",
    )
    args = p.parse_args()
    now = datetime.now(timezone.utc)
    if args.date_only:
        print(now.strftime("%Y-%m-%d"))
    else:
        print(now.strftime("%Y-%m-%dT%H:%M:%SZ"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
