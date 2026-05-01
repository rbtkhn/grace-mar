#!/usr/bin/env python3
"""Backfill John Mearsheimer site pages into strategy-notebook raw-input/.

Thin wrapper around ``backfill_author_page_raw_input.py`` with Mearsheimer defaults.
Treat the public site as a discovery index, not a completeness mandate.
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

from backfill_author_page_raw_input import DEFAULT_RAW_ROOT, run

DEFAULT_AUTHOR_URL = "https://www.mearsheimer.com/"
DEFAULT_DOMAIN = "mearsheimer.com"
DEFAULT_PUBLICATION = "mearsheimer.com"
DEFAULT_THREAD = "mearsheimer"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--author-url", default=DEFAULT_AUTHOR_URL)
    ap.add_argument("--domain", default=DEFAULT_DOMAIN)
    ap.add_argument("--publication", default=DEFAULT_PUBLICATION)
    ap.add_argument("--root", type=Path, default=DEFAULT_RAW_ROOT)
    ap.add_argument("--ingest-date", type=str, default=None, help="YYYY-MM-DD ingest_date in frontmatter")
    ap.add_argument("--thread", type=str, default=DEFAULT_THREAD)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=50)
    args = ap.parse_args()

    ingest = (
        datetime.strptime(args.ingest_date, "%Y-%m-%d").date()
        if args.ingest_date
        else date.today()
    )

    return run(
        author_url=args.author_url,
        domain=args.domain,
        path_shape="any-article",
        publication=args.publication,
        raw_root=args.root,
        ingest_date=ingest,
        thread=args.thread,
        apply=args.apply,
        limit=max(1, min(args.limit, 100)),
    )


if __name__ == "__main__":
    raise SystemExit(main())
