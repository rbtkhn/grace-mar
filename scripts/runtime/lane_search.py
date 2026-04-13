#!/usr/bin/env python3
"""Compact search over runtime/observations/index.jsonl (index-first retrieval)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_RUNTIME_DIR = Path(__file__).resolve().parent
if str(_RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(_RUNTIME_DIR))

from observation_store import load_all  # noqa: E402
from search_scoring import parse_cli_datetime, parse_obs_timestamp, score_observation, ts_sort_key  # noqa: E402


def format_ts_display(raw: str | None) -> str:
    if not raw:
        return "?"
    dt = parse_obs_timestamp(raw)
    if dt is None:
        return raw
    if dt.tzinfo is None:
        from datetime import timezone as tz

        dt = dt.replace(tzinfo=tz.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _passes_since_until(obs: dict, since: datetime | None, until: datetime | None) -> bool:
    dt = parse_obs_timestamp(obs.get("timestamp"))
    if dt is None:
        return since is None and until is None
    if dt.tzinfo is None:
        from datetime import timezone as tz

        dt = dt.replace(tzinfo=tz.utc)
    if since is not None and dt < since:
        return False
    if until is not None and dt > until:
        return False
    return True


def _has_all_tags(obs: dict, required: list[str]) -> bool:
    if not required:
        return True
    obs_tags = [t.lower() for t in (obs.get("tags") or [])]
    return all(any(req.lower() == ot for ot in obs_tags) for req in required)


def filter_rows(
    rows: list[dict],
    *,
    lane_eq: str | None,
    source_kind: str | None,
    since,
    until,
    required_tags: list[str],
) -> list[dict]:
    out: list[dict] = []
    for r in rows:
        if lane_eq is not None and r.get("lane") != lane_eq:
            continue
        if source_kind and r.get("source_kind") != source_kind:
            continue
        if not _passes_since_until(r, since, until):
            continue
        if not _has_all_tags(r, required_tags):
            continue
        out.append(r)
    return out


def compact_json_obj(score: float, obs: dict) -> dict:
    summ = (obs.get("summary") or "").replace("\n", " ").strip()
    if len(summ) > 500:
        summ = summ[:497] + "…"
    d = {
        "score": round(score, 4),
        "obs_id": obs.get("obs_id"),
        "timestamp": obs.get("timestamp"),
        "lane": obs.get("lane"),
        "source_kind": obs.get("source_kind"),
        "title": obs.get("title"),
        "summary": summ,
        "confidence": obs.get("confidence"),
    }
    return d


def compact_timeline_obj(obs: dict) -> dict:
    """Compact row for lane_timeline JSON (no score; no notes)."""
    summ = (obs.get("summary") or "").replace("\n", " ").strip()
    if len(summ) > 500:
        summ = summ[:497] + "…"
    return {
        "obs_id": obs.get("obs_id"),
        "timestamp": obs.get("timestamp"),
        "lane": obs.get("lane"),
        "source_kind": obs.get("source_kind"),
        "title": obs.get("title"),
        "summary": summ,
        "confidence": obs.get("confidence"),
    }


def rank_hits(
    rows: list[dict],
    *,
    query: str,
    bonus_tags: list[str],
    require_positive_match: bool,
) -> list[tuple[float, dict]]:
    hits: list[tuple[float, dict]] = []
    q = query.strip()
    tags_for_score = list(bonus_tags)

    for row in rows:
        s = score_observation(row, query, bonus_tags=tags_for_score)
        if require_positive_match and s <= 0.0:
            continue
        hits.append((s, row))

    hits.sort(key=lambda h: (-h[0], -ts_sort_key(h[1])))
    return hits


def top_hits_for_timeline(
    rows: list[dict],
    *,
    lane: str | None,
    query: str,
    source_kind: str | None,
    since,
    until,
    required_tags: list[str],
    pick: int,
) -> tuple[dict | None, str | None]:
    """Return (anchor_obs, error_message). pick is 1-based."""
    pool = filter_rows(
        rows,
        lane_eq=lane,
        source_kind=source_kind,
        since=since,
        until=until,
        required_tags=required_tags,
    )
    ranked = rank_hits(
        pool,
        query=query,
        bonus_tags=required_tags,
        require_positive_match=bool(query.strip() or required_tags),
    )
    if not ranked:
        return None, "no search results for timeline"
    if pick < 1 or pick > len(ranked):
        return None, f"--pick must be 1..{len(ranked)}"
    return ranked[pick - 1][1], None


def main() -> int:
    parser = argparse.ArgumentParser(description="Search runtime observations (compact index).")
    parser.add_argument("--query", "-q", default="", help="Search query (keyword / phrase)")
    parser.add_argument("--lane", help="Restrict to exact lane string (optional)")
    parser.add_argument("--source-kind", dest="source_kind", help="Filter by source_kind")
    parser.add_argument("--tag", action="append", default=[], help="Tag filter (repeatable; AND)")
    parser.add_argument("--since", help="ISO date-time lower bound (inclusive)")
    parser.add_argument("--until", help="ISO date-time upper bound (inclusive)")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true", help="Single JSON array of compact hits")
    args = parser.parse_args()

    since = parse_cli_datetime(args.since)
    until = parse_cli_datetime(args.until)
    req_tags = [t for t in args.tag if t.strip()]

    rows = load_all()
    lane_eq = args.lane.strip() if args.lane else None
    pool = filter_rows(
        rows,
        lane_eq=lane_eq,
        source_kind=args.source_kind,
        since=since,
        until=until,
        required_tags=req_tags,
    )

    q = args.query.strip()
    require_positive = bool(q or req_tags)
    hits = rank_hits(pool, query=args.query, bonus_tags=req_tags, require_positive_match=require_positive)
    hits = hits[: args.limit]

    if args.json:
        out = [compact_json_obj(s, o) for s, o in hits]
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    for score, obs in hits:
        oid = obs.get("obs_id", "?")
        ts = format_ts_display(obs.get("timestamp"))
        lane = obs.get("lane", "?")
        sk = obs.get("source_kind", "?")
        title = obs.get("title", "")
        summ = (obs.get("summary") or "").replace("\n", " ").strip()
        conf = obs.get("confidence")
        conf_s = f" | conf={conf:g}" if isinstance(conf, (int, float)) else ""
        print(f"{oid} | {ts} | {lane} | {sk} | {title}{conf_s}")
        print(f"  {summ}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
