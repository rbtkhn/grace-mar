#!/usr/bin/env python3
"""Rebuild work_jiang_metrics.sqlite from canonical JSONL registries."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

_SCRIPTS_WJ = Path(__file__).resolve().parent
if str(_SCRIPTS_WJ) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_WJ))

from registry_db import DEFAULT_DB, rebuild_from_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--db",
        type=Path,
        default=None,
        help=f"SQLite path (default: {DEFAULT_DB})",
    )
    parser.add_argument("--predictions", type=Path, default=None)
    parser.add_argument("--divergences", type=Path, default=None)
    parser.add_argument("--patterns", type=Path, default=None)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 0 if DB file exists and has tables (no rebuild)",
    )
    args = parser.parse_args()

    if args.check:
        db = args.db or DEFAULT_DB
        if not db.exists():
            print("MISSING_DB")
            return 1
        import sqlite3

        c = sqlite3.connect(str(db))
        cur = c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name IN "
            "('predictions','divergences','patterns')"
        )
        rows = {r[0] for r in cur.fetchall()}
        c.close()
        if not {"predictions", "divergences"}.issubset(rows):
            print("INCOMPLETE_SCHEMA")
            return 1
        if "patterns" not in rows:
            print("INCOMPLETE_SCHEMA")
            return 1
        print("OK")
        return 0

    rebuild_from_jsonl(
        predictions_path=args.predictions,
        divergences_path=args.divergences,
        patterns_path=args.patterns,
        db_path=args.db,
    )
    print(f"Rebuilt {args.db or DEFAULT_DB}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
