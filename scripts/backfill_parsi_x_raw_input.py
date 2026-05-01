#!/usr/bin/env python3
"""Backfill Trita Parsi X posts into strategy-notebook raw-input/.

Thin wrapper around ``backfill_x_profile_raw_input.py`` with Parsi defaults.
WORK only; not Record.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from backfill_x_profile_raw_input import DEFAULT_RAW_ROOT, run

DEFAULT_PROFILE_URL = "https://x.com/tparsi"
DEFAULT_THREAD = "parsi"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--profile-url", default=DEFAULT_PROFILE_URL)
    ap.add_argument("--root", type=Path, default=DEFAULT_RAW_ROOT)
    ap.add_argument("--ingest-date", type=str, default=None, help="YYYY-MM-DD ingest_date in frontmatter")
    ap.add_argument("--thread", type=str, default=DEFAULT_THREAD)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--status-url", action="append", default=[], help="Explicit status URL to capture")
    args = ap.parse_args()

    ingest = (
        datetime.strptime(args.ingest_date, "%Y-%m-%d").date()
        if args.ingest_date
        else date.today()
    )

    return run(
        profile_url=args.profile_url,
        raw_root=args.root,
        ingest_date=ingest,
        thread=args.thread,
        apply=args.apply,
        status_urls=args.status_url,
    )


if __name__ == "__main__":
    raise SystemExit(main())
