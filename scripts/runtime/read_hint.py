#!/usr/bin/env python3
"""
Soft hints before re-reading a path or topic: surface relevant runtime observations.

Suggestion-only — does not block reads or mutate files. See docs/runtime/read-hints.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_RUNTIME_DIR = Path(__file__).resolve().parent
if str(_RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(_RUNTIME_DIR))

from observation_store import load_all  # noqa: E402
from lane_search import filter_rows, rank_hits, format_ts_display  # noqa: E402
from search_scoring import ts_sort_key  # noqa: E402


def _haystack(obs: dict) -> str:
    parts = [
        obs.get("title") or "",
        obs.get("summary") or "",
        obs.get("source_path") or "",
        " ".join(obs.get("tags") or []),
        " ".join(obs.get("source_refs") or []),
    ]
    return " ".join(parts).lower()


def _path_matches(obs: dict, path_norm: str) -> bool:
    sp = (obs.get("source_path") or "").strip().lower()
    if not path_norm:
        return True
    if path_norm in sp or sp.endswith(path_norm) or path_norm.endswith(sp):
        return True
    hay = _haystack(obs)
    return path_norm in hay


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Hint: runtime observations may already cover this path or topic (soft; does not block reads)."
    )
    parser.add_argument("--lane", help="Prefer this lane (exact match)")
    parser.add_argument("--path", help="File path as in observation source_path or mentioned in text")
    parser.add_argument("--query", "-q", default="", help="Topic keywords (all terms must appear in haystack)")
    parser.add_argument("--limit", type=int, default=5, help="Max observations to list (default 5)")
    args = parser.parse_args()

    path_arg = (args.path or "").strip()
    query = (args.query or "").strip()

    if not path_arg and not query:
        print("error: provide --path and/or --query", file=sys.stderr)
        return 2

    rows = load_all()
    lane_eq = args.lane.strip() if args.lane else None
    pool = filter_rows(
        rows,
        lane_eq=lane_eq,
        source_kind=None,
        since=None,
        until=None,
        required_tags=[],
    )

    path_norm = path_arg.lower().replace("\\", "/")

    if query:
        sub = [r for r in pool if (not path_arg) or _path_matches(r, path_norm)]
        ranked = rank_hits(
            sub,
            query=query,
            bonus_tags=[],
            require_positive_match=True,
        )
        hits = [row for _s, row in ranked[: args.limit]]
    else:
        matched = [r for r in pool if _path_matches(r, path_norm)]
        matched.sort(key=lambda r: -ts_sort_key(r))
        hits = matched[: args.limit]

    label = path_arg or f"topic: {query}"
    print(f"Read hint: {label}\n")

    if not hits:
        print("No relevant runtime observations found. Direct read is reasonable.")
        print("\nYou may still open the file or notebook directly.")
        return 0

    print(f"Grace-Mar already has {len(hits)} relevant runtime observation(s) in the current filter.")
    print(f"Most recent: {format_ts_display(hits[0].get('timestamp'))}")
    print("Top items:")
    for h in hits:
        oid = h.get("obs_id", "?")
        title = (h.get("title") or "")[:120]
        print(f"- {oid} | {title}")

    anchor = hits[0].get("obs_id", "")
    lane_s = args.lane or (hits[0].get("lane") or "work-strategy")
    q_for_brief = query or path_arg or ""

    print("\nSuggested next step:")
    print(f"  python3 scripts/runtime/lane_timeline.py --anchor {anchor} --before 2 --after 2")
    if query:
        print(
            f'  python3 scripts/runtime/memory_brief.py --lane {lane_s} --query "{query}" --limit 5'
        )
    else:
        print(
            f'  python3 scripts/runtime/memory_brief.py --lane {lane_s} --query "{path_arg}" --limit 5'
        )

    print("\nYou may still read the file directly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
