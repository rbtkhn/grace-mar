#!/usr/bin/env python3
"""Backfill Jeffrey Sachs article pages into strategy-notebook raw-input/.

Thin wrapper around ``backfill_author_page_raw_input.py`` for Sachs' public
articles / op-eds surface on jeffsachs.org.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from backfill_author_page_raw_input import DEFAULT_RAW_ROOT, run

DEFAULT_AUTHOR_URL = "https://www.jeffsachs.org/newspaper-articles"
DEFAULT_DOMAIN = "jeffsachs.org"
DEFAULT_THREAD = "sachs"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--author-url", default=DEFAULT_AUTHOR_URL)
    ap.add_argument("--domain", default=DEFAULT_DOMAIN)
    ap.add_argument("--path-shape", default="any-article")
    ap.add_argument("--publication", default="jeffsachs.org")
    ap.add_argument("--root", type=Path, default=DEFAULT_RAW_ROOT)
    ap.add_argument("--ingest-date", type=str, default=None, help="YYYY-MM-DD ingest_date in frontmatter")
    ap.add_argument("--thread", type=str, default=DEFAULT_THREAD)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--exclude-prefix", action="append", default=[])
    args = ap.parse_args()

    ingest = (
        datetime.strptime(args.ingest_date, "%Y-%m-%d").date()
        if args.ingest_date
        else date.today()
    )

    return run(
        author_url=args.author_url,
        domain=args.domain,
        path_shape=args.path_shape,
        publication=args.publication,
        raw_root=args.root,
        ingest_date=ingest,
        thread=args.thread,
        apply=args.apply,
        limit=max(1, min(args.limit, 100)),
        exclude_prefixes=args.exclude_prefix,
    )


if __name__ == "__main__":
    raise SystemExit(main())
