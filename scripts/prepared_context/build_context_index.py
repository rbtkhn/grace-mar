#!/usr/bin/env python3
"""
Emit a compact Markdown index of runtime observations for prepared-context (layer 1).

Does not read full notebooks by default — index-first discipline.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_RT = REPO_ROOT / "scripts" / "runtime"
if str(_RT) not in sys.path:
    sys.path.insert(0, str(_RT))

from observation_store import load_all  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build compact observation index (Markdown).")
    parser.add_argument("--lane", help="Filter by lane substring")
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()

    rows = load_all()
    lane_sub = (args.lane or "").strip().lower()
    filtered: list[dict] = []
    for row in rows:
        if lane_sub and lane_sub not in (row.get("lane") or "").lower():
            continue
        filtered.append(row)
    filtered.sort(key=lambda r: r.get("timestamp") or "")
    filtered = filtered[-args.limit :]

    print("# Runtime observation index (prepared context — layer 1)\n")
    print("_Runtime memory — not approved Record truth._\n")
    for row in filtered:
        oid = row.get("obs_id", "?")
        ts = row.get("timestamp", "")
        lane = row.get("lane", "")
        title = row.get("title", "")
        summ = (row.get("summary") or "")[:240]
        print(f"- **{oid}** — `{lane}` — {ts}\n  - {title}\n  - {summ}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
