#!/usr/bin/env python3
"""Print-only suggestions for civ_mem_routing_focus.yaml from routing-decisions.jsonl.

Reads profile counts over the last N days and emits a commented YAML snippet for
operator review (does not write files).

Usage:
  python3 scripts/suggest_routing_focus.py
  python3 scripts/suggest_routing_focus.py --days 14 --jsonl artifacts/skill-work/work-civ-mem/routing-decisions.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSONL = (
    REPO_ROOT / "artifacts" / "skill-work" / "work-civ-mem" / "routing-decisions.jsonl"
)


def _rel_repo(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def _parse_ts(s: str) -> datetime | None:
    try:
        raw = s.strip()
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--days",
        type=int,
        default=14,
        help="Include rows with ts within this many days (UTC)",
    )
    ap.add_argument(
        "--jsonl",
        type=Path,
        default=DEFAULT_JSONL,
        help="Path to routing-decisions.jsonl",
    )
    args = ap.parse_args()

    path = args.jsonl
    if not path.is_file():
        print(f"# No file at {path} — run route_civ_mem_topic.py with --log-decision first.", file=sys.stderr)
        print("# generated_from: (empty)")
        return 0

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    profiles: Counter[str] = Counter()
    n = 0
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = _parse_ts(row.get("ts", ""))
            if ts is None or ts < cutoff:
                continue
            n += 1
            p = row.get("profile")
            if p:
                profiles[str(p)] += 1

    modal = profiles.most_common(1)[0][0] if profiles else None
    until = datetime.now(timezone.utc) + timedelta(days=args.days)
    until_s = until.date().isoformat()
    since = datetime.now(timezone.utc).date().isoformat()

    lines = [
        "# --- suggested routing focus (paste into config/civ_mem_routing_focus.yaml after review) ---",
        f"# generated_from: {_rel_repo(path)}",
        f"# days: {args.days}",
        f"# rows_in_window: {n}",
        f"# modal_profile: {modal}",
        f"# suggested_valid_until_note: set valid_until to ~{until_s} for a matching forward window (UTC)",
        f"# date_range_utc: last {args.days} days ending {since}",
        "#",
        "focus_version: 1",
        f'valid_from: "{since}"',
        f'valid_until: "{until_s}"',
        "profile_overlap_bonus:",
    ]

    all_profiles = sorted(profiles.keys()) or ["latin_catholic_sphere", "mediterranean_islam_christian_encounter"]
    for pid in all_profiles:
        bonus = 1 if modal and pid == modal and profiles else 0
        lines.append(f"  {pid}: {bonus}")

    lines.append("sticky_keywords: []")
    lines.append("# --- end suggestion ---")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
