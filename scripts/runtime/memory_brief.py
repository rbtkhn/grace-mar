#!/usr/bin/env python3
"""
One bounded runtime memory brief: search → timeline → compact expansion.

Does not auto-stage gate candidates; output is runtime-only. See docs/runtime/read-hints.md.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

_RUNTIME_DIR = Path(__file__).resolve().parent
if str(_RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(_RUNTIME_DIR))

from expand_observations import expanded_row  # noqa: E402
from lane_search import filter_rows, rank_hits, format_ts_display  # noqa: E402
from lane_timeline import build_timeline_window  # noqa: E402
from observation_store import by_id, load_all  # noqa: E402


def _takeaway_line(obs: dict, max_len: int = 220) -> str:
    oid = obs.get("obs_id", "?")
    summ = (obs.get("summary") or "").replace("\n", " ").strip()
    if len(summ) > max_len:
        summ = summ[: max_len - 1] + "…"
    return f"{summ} [{oid}]"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Memory brief: lane-scoped search, timeline slice, bounded expansion (runtime-only). "
        "Use --lane/--query or positional: LANE [QUERY ...].",
    )
    parser.add_argument(
        "positional",
        nargs="*",
        metavar="LANE",
        help="Optional: lane and optional query words (backward-compatible; do not combine with --lane)",
    )
    parser.add_argument("--lane", default=None, help="Lane to search (exact string)")
    parser.add_argument("--query", "-q", default=None, help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Top compact hits (default 5)")
    parser.add_argument("--expand", type=int, default=3, help="How many hits to expand (default 3)")
    parser.add_argument("--timeline-before", type=int, default=2, help="Rows before anchor")
    parser.add_argument("--timeline-after", type=int, default=2, help="Rows after anchor")
    parser.add_argument(
        "--cross-lane",
        action="store_true",
        help="Search all lanes; timeline pool uses global order when set (same as lane_timeline --cross-lane)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Write Markdown to this path (default: stdout only)",
    )
    args = parser.parse_args()

    if args.lane is not None and args.positional:
        parser.error("use either --lane/--query or positional LANE [QUERY], not both")

    if args.lane is not None:
        lane = args.lane.strip()
        query = (args.query if args.query is not None else "").strip()
    elif args.positional:
        lane = args.positional[0].strip()
        query = " ".join(args.positional[1:]).strip()
    else:
        parser.error("provide --lane (and optional --query) or: LANE [QUERY ...]")

    rows = load_all()
    lane_eq = None if args.cross_lane else lane
    pool = filter_rows(
        rows,
        lane_eq=lane_eq,
        source_kind=None,
        since=None,
        until=None,
        required_tags=[],
    )

    ranked = rank_hits(
        pool,
        query=query,
        bonus_tags=[],
        require_positive_match=bool(query.strip()),
    )
    hits = ranked[: args.limit]
    if not hits:
        print("No relevant observations found for this lane and query.", file=sys.stderr)
        return 1

    anchor = hits[0][1]
    window, werr = build_timeline_window(
        rows,
        anchor,
        before=args.timeline_before,
        after=args.timeline_after,
        cross_lane=args.cross_lane,
    )
    if werr or window is None:
        print(f"error: timeline: {werr or 'failed'}", file=sys.stderr)
        return 2

    expand_n = max(0, min(args.expand, len(hits)))
    expanded_raw: list[dict] = []
    seen: set[str] = set()
    for i in range(expand_n):
        oid = hits[i][1].get("obs_id")
        if not oid or oid in seen:
            continue
        seen.add(str(oid))
        raw = by_id(str(oid))
        if raw:
            expanded_raw.append(expanded_row(raw))

    built = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    q = query

    lines: list[str] = [
        "# Memory Brief",
        "",
        "Status: Runtime-only",
        f"Lane: {lane}",
        f"Built: {built}",
        f"Query: {q}",
        "",
        "## Best Matches",
    ]
    for _s, row in hits:
        oid = row.get("obs_id", "?")
        title = row.get("title", "")
        lines.append(f"- {oid} | {title}")

    lines.extend(["", "## Timeline Context"])
    for row in window:
        ts = format_ts_display(row.get("timestamp"))
        oid = row.get("obs_id", "?")
        title = row.get("title", "")
        lines.append(f"- {ts} | {oid} | {title}")

    lines.extend(["", "## Expanded Takeaways"])
    for row in expanded_raw:
        lines.append(f"- {_takeaway_line(row)}")

    high_conf = sum(
        1
        for _s, row in hits
        if isinstance(row.get("confidence"), (int, float)) and float(row["confidence"]) >= 0.8
    )
    lines.extend(
        [
            "",
            "## Recommended Next Move",
            "- Use this brief as runtime prepared context for the next operator or agent step.",
            "- Consider `stage_candidate_from_observations.py` only after contradiction review if a durable Record or work-surface change is justified.",
        ]
    )
    if high_conf >= 2:
        lines.append(
            f"- Soft signal: {high_conf} match(es) with confidence ≥ 0.8 — review contradictions before staging."
        )

    lines.extend(
        [
            "",
            "Boundary:",
            "This is runtime context only.",
            "It does not update SELF, SELF-LIBRARY, SKILLS, EVIDENCE, or recursion-gate.md.",
        ]
    )
    content = "\n".join(lines) + "\n"

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(content, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
