#!/usr/bin/env python3
"""Chronological window around a runtime observation (search → timeline retrieval)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_RUNTIME_DIR = Path(__file__).resolve().parent
if str(_RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(_RUNTIME_DIR))

from observation_store import load_all  # noqa: E402
from lane_search import (  # noqa: E402
    compact_timeline_obj,
    format_ts_display,
    top_hits_for_timeline,
)
from search_scoring import parse_cli_datetime, ts_sort_key  # noqa: E402


def _timeline_pool(rows: list[dict], anchor: dict, *, cross_lane: bool) -> list[dict]:
    if cross_lane:
        pool = list(rows)
    else:
        lane = anchor.get("lane")
        pool = [r for r in rows if r.get("lane") == lane]
    pool.sort(key=lambda r: ts_sort_key(r))
    return pool


def _window_for_anchor(pool: list[dict], anchor_id: str, before: int, after: int) -> tuple[list[dict] | None, str | None]:
    ids = [r.get("obs_id") for r in pool]
    try:
        idx = ids.index(anchor_id)
    except ValueError:
        return None, f"anchor not in timeline pool: {anchor_id}"
    start = max(0, idx - before)
    end = min(len(pool), idx + after + 1)
    return pool[start:end], None


def build_timeline_window(
    rows: list[dict],
    anchor: dict,
    *,
    before: int,
    after: int,
    cross_lane: bool = False,
) -> tuple[list[dict] | None, str | None]:
    """Chronological window around anchor (same pool rules as CLI)."""
    pool = _timeline_pool(rows, anchor, cross_lane=cross_lane)
    aid = anchor.get("obs_id")
    if not isinstance(aid, str):
        return None, "anchor missing obs_id"
    return _window_for_anchor(pool, aid, before, after)


def main() -> int:
    parser = argparse.ArgumentParser(description="Timeline window around a runtime observation.")
    parser.add_argument("--anchor", help="Center on this obs_id")
    parser.add_argument("--query", "-q", default="", help="Resolve anchor via lane-search (top hit unless --pick)")
    parser.add_argument("--lane", help="With --query: restrict search to this lane (optional; omit = all lanes)")
    parser.add_argument("--pick", type=int, default=1, help="1-based rank when resolving via --query (default 1)")
    parser.add_argument("--before", type=int, default=2, help="Rows before anchor (same-lane pool by default)")
    parser.add_argument("--after", type=int, default=2, help="Rows after anchor (same-lane pool by default)")
    parser.add_argument("--source-kind", dest="source_kind", help="With --query: filter source_kind before ranking")
    parser.add_argument("--tag", action="append", default=[], help="With --query: tag filter (repeatable; AND)")
    parser.add_argument("--since", help="With --query: ISO lower bound (inclusive)")
    parser.add_argument("--until", help="With --query: ISO upper bound (inclusive)")
    parser.add_argument(
        "--cross-lane",
        action="store_true",
        help="Use global chronological order across lanes (default: anchor lane only)",
    )
    parser.add_argument("--json", action="store_true", help="JSON array of compact rows (no notes)")
    args = parser.parse_args()

    anchor_id = (args.anchor or "").strip()
    q = args.query.strip()
    if anchor_id and q:
        print("error: pass only one of --anchor or --query", file=sys.stderr)
        return 2
    if not anchor_id and not q:
        print("error: provide --anchor or --query", file=sys.stderr)
        return 2

    rows = load_all()
    since = parse_cli_datetime(args.since)
    until = parse_cli_datetime(args.until)
    req_tags = [t for t in args.tag if t.strip()]
    lane_eq = args.lane.strip() if args.lane else None

    anchor: dict | None = None
    if anchor_id:
        for r in rows:
            if r.get("obs_id") == anchor_id:
                anchor = r
                break
        if anchor is None:
            print(f"error: anchor not found: {anchor_id}", file=sys.stderr)
            return 2
    else:
        anchor, err = top_hits_for_timeline(
            rows,
            lane=lane_eq,
            query=args.query,
            source_kind=args.source_kind,
            since=since,
            until=until,
            required_tags=req_tags,
            pick=args.pick,
        )
        if err or anchor is None:
            print(f"error: {err or 'could not resolve anchor'}", file=sys.stderr)
            return 2

    window, werr = build_timeline_window(
        rows,
        anchor,
        before=args.before,
        after=args.after,
        cross_lane=args.cross_lane,
    )
    if werr or window is None:
        print(f"error: {werr or 'timeline window failed'}", file=sys.stderr)
        return 2

    if args.json:
        out = [compact_timeline_obj(r) for r in window]
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    for row in window:
        ts = format_ts_display(row.get("timestamp"))
        oid = row.get("obs_id", "?")
        sk = row.get("source_kind", "?")
        lane = row.get("lane", "?")
        title = row.get("title", "")
        summ = (row.get("summary") or "").replace("\n", " ").strip()
        print(f"[{ts}] {oid} | {sk} | {lane} | {title}")
        print(f"  {summ}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
