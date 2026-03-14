#!/usr/bin/env python3
"""Summarize self-library.md by scope tags (shelf keywords) and lookup_priority."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_entries(path: Path) -> list[dict]:
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")
    entries = []
    for m in re.finditer(
        r"-\s+id:\s+(LIB-\d+)(.*?)(?=-\s+id:\s+LIB-|\Z)", content, re.DOTALL
    ):
        lib_id = m.group(1)
        block = m.group(2)
        title_m = re.search(r'title:\s*["\']([^"\']+)["\']', block)
        scope_m = re.search(r"scope:\s*\[([^\]]*)\]", block)
        status_m = re.search(r"status:\s*(\w+)", block)
        priority_m = re.search(r"lookup_priority:\s*[\"']?(\w+)", block)
        lane_m = re.search(r"lane:\s*[\"']?(\w+)", block)
        if status_m and status_m.group(1) != "active":
            continue
        if not title_m:
            continue
        scope_raw = scope_m.group(1) if scope_m else ""
        scopes = [s.strip().strip("'\"") for s in scope_raw.split(",") if s.strip()]
        entries.append(
            {
                "id": lib_id,
                "title": title_m.group(1)[:60],
                "scope": scopes,
                "lookup_priority": priority_m.group(1) if priority_m else "low",
                "lane": lane_m.group(1) if lane_m else "canon",
            }
        )
    return entries


SHELF_KEYWORDS = [
    "theology",
    "physics",
    "chemistry",
    "biology",
    "history",
    "world history",
    "science",
    "geography",
    "mythology",
    "ballet",
]


def main() -> int:
    p = argparse.ArgumentParser(description="Library shelf summary")
    p.add_argument("-u", "--user", default="grace-mar")
    args = p.parse_args()
    lib_path = REPO_ROOT / "users" / args.user / "self-library.md"
    entries = load_entries(lib_path)
    print(f"Active entries: {len(entries)}  ({lib_path.relative_to(REPO_ROOT)})")
    print()
    pri = Counter(e["lookup_priority"] for e in entries)
    print("lookup_priority:", dict(pri.most_common()))
    lane = Counter(e["lane"] for e in entries)
    print("lane:", dict(lane.most_common()))
    print()
    print("Shelf keyword → entries (id + title):")
    for kw in SHELF_KEYWORDS:
        hits = [e for e in entries if any(kw.lower() == s.lower() for s in e["scope"])]
        if not hits:
            continue
        print(f"  [{kw}] ({len(hits)})")
        for e in hits[:8]:
            print(f"    {e['id']} [{e['lookup_priority']}] {e['title']}")
        if len(hits) > 8:
            print(f"    … +{len(hits) - 8} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
