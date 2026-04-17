#!/usr/bin/env python3
"""
Verify `daily-strategy-inbox.md` **Accumulator for:** date matches an expected calendar day.

Default expected date: today in the local timezone of the machine running this script.
Use `--date YYYY-MM-DD` when the operator's calendar day differs (e.g. CI in UTC vs US local).

Exit 0 = match; 1 = mismatch or parse error; 2 = file missing.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_INBOX = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "strategy-notebook"
    / "daily-strategy-inbox.md"
)

ACCUM_RE = re.compile(
    r"^\*\*Accumulator for:\*\*\s*(\d{4}-\d{2}-\d{2})\b",
    re.MULTILINE,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--inbox",
        type=Path,
        default=DEFAULT_INBOX,
        help="Path to daily-strategy-inbox.md",
    )
    ap.add_argument(
        "--date",
        dest="expect",
        metavar="YYYY-MM-DD",
        default=None,
        help="Expected calendar day (default: today local)",
    )
    args = ap.parse_args()
    inbox = args.inbox
    if not inbox.is_file():
        print(f"verify_strategy_inbox_accumulator: no file {inbox}", file=sys.stderr)
        return 2
    text = inbox.read_text(encoding="utf-8", errors="replace")
    m = ACCUM_RE.search(text)
    if not m:
        print(
            "verify_strategy_inbox_accumulator: could not parse **Accumulator for:** line",
            file=sys.stderr,
        )
        return 1
    found = m.group(1)
    if args.expect:
        try:
            expected = date.fromisoformat(args.expect)
        except ValueError:
            print(
                f"verify_strategy_inbox_accumulator: bad --date {args.expect!r}",
                file=sys.stderr,
            )
            return 1
    else:
        expected = date.today()
    expected_s = expected.isoformat()
    if found != expected_s:
        print(
            f"verify_strategy_inbox_accumulator: Accumulator for is {found!r}, "
            f"expected {expected_s!r} (pass --date {expected_s} to assert operator day).",
            file=sys.stderr,
        )
        return 1
    print(f"verify_strategy_inbox_accumulator: ok — Accumulator for: {found}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
