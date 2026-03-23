#!/usr/bin/env python3
"""Query predictions table in work_jiang_metrics.sqlite (JSONL is canonical source)."""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = ROOT / "research" / "external" / "work-jiang" / "registry" / "work_jiang_metrics.sqlite"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--status", help="resolution_status filter")
    parser.add_argument("--video-id", dest="video_id", help="video_id filter")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--json", action="store_true", help="Print full payload JSON per line")
    args = parser.parse_args()

    if not args.db.exists():
        print("Run: python3 scripts/work_jiang/rebuild_registry_db.py", file=sys.stderr)
        return 1

    conn = sqlite3.connect(str(args.db))
    conn.row_factory = sqlite3.Row
    q = "SELECT prediction_id, video_id, resolution_status, payload FROM predictions WHERE 1=1"
    params: list = []
    if args.status:
        q += " AND resolution_status = ?"
        params.append(args.status)
    if args.video_id:
        q += " AND video_id = ?"
        params.append(args.video_id)
    q += f" LIMIT {max(1, args.limit)}"
    rows = conn.execute(q, params).fetchall()
    conn.close()

    for r in rows:
        if args.json:
            print(r["payload"])
        else:
            print(f"{r['prediction_id']}\t{r['video_id']}\t{r['resolution_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
