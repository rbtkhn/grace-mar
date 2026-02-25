#!/usr/bin/env python3
"""
Boundary coverage — entity and IX counts from SELF.md.

Parses users/[id]/SELF.md and reports:
- Entity counts per category (movies, books, places, foods, activities, etc.)
- IX-A / IX-B / IX-C entry counts (post-seed growth dimensions)

Use for visibility into what's inside the knowledge boundary. Run occasionally or in CI.

Usage:
  python3 scripts/boundary_coverage.py
  python3 scripts/boundary_coverage.py -u grace-mar
  python3 scripts/boundary_coverage.py --json   # machine-readable
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
USERS_DIR = REPO_ROOT / "users"


def _count_entries(content: str, prefix: str) -> int:
    """Count entries with id: PREFIX-XXXX (e.g. LEARN-, CUR-, PER-)."""
    pattern = rf"id:\s*{re.escape(prefix)}"
    return len(re.findall(pattern, content))


def _count_list_items_after_key(content: str, key: str, keys_before_next: list[str]) -> int:
    """Count YAML list items under key until next key in keys_before_next."""
    lines = content.split("\n")
    in_block = False
    count = 0
    for line in lines:
        if re.match(rf"^{key}\s*:", line):
            in_block = True
            continue
        if in_block:
            if any(re.match(rf"^{k}\s*:", line) for k in keys_before_next):
                break
            if re.match(r"^-\s+", line) or re.match(r"^\s{2,}-\s+", line):
                count += 1
    return count


def _extract_favorites(content: str) -> dict[str, int]:
    """Extract entity counts from Favorites and Extended sections."""
    counts: dict[str, int] = {}
    # Favorites block: movies, food, books, places, games
    fav_section = re.search(
        r"### Favorites\s*\n\n?```yaml\s*\n(.*?)```",
        content,
        re.DOTALL,
    )
    if fav_section:
        block = fav_section.group(1)
        keys_order = ["movies", "food", "books", "places", "games"]
        for i, key in enumerate(keys_order):
            next_keys = keys_order[i + 1 :] if i + 1 < len(keys_order) else []
            next_keys.extend(["people", "activities", "foods", "music", "favorite_gemstone"])
            counts[key] = _count_list_items_after_key(block, key, next_keys)

    # Extended block: activities, music, people
    ext_section = re.search(
        r"### Extended.*?```yaml\s*\n(.*?)```",
        content,
        re.DOTALL,
    )
    if ext_section:
        block = ext_section.group(1)
        for key in ["activities", "music", "people"]:
            counts[key] = _count_list_items_after_key(
                block, key, ["people", "activities", "foods", "music", "favorite_gemstone"]
            )

    return counts


def run(user_id: str = "grace-mar", json_out: bool = False) -> dict:
    """Compute boundary coverage for user. Returns dict of counts."""
    self_path = USERS_DIR / user_id / "SELF.md"
    if not self_path.exists():
        raise SystemExit(f"SELF.md not found: {self_path}")

    content = self_path.read_text()

    ix_a = _count_entries(content, "LEARN-")
    ix_b = _count_entries(content, "CUR-")
    ix_c = _count_entries(content, "PER-")

    favorites = _extract_favorites(content)
    total_entities = sum(favorites.values())

    result = {
        "user_id": user_id,
        "self_path": str(self_path),
        "entities": favorites,
        "entity_total": total_entities,
        "IX-A": ix_a,
        "IX-B": ix_b,
        "IX-C": ix_c,
        "IX_total": ix_a + ix_b + ix_c,
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="Boundary coverage from SELF.md")
    parser.add_argument("-u", "--user", default="grace-mar", help="User id (default: grace-mar)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    try:
        result = run(user_id=args.user, json_out=args.json)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        import json
        print(json.dumps(result, indent=2))
        return

    # Human-readable
    print("Boundary coverage —", result["user_id"])
    print("SELF:", result["self_path"])
    print()
    print("Entities (favorites + extended)")
    print("-" * 40)
    for k, v in sorted(result["entities"].items()):
        if v > 0:
            print(f"  {k}: {v}")
    print(f"  total: {result['entity_total']}")
    print()
    print("IX (post-seed growth)")
    print("-" * 40)
    print(f"  IX-A (Knowledge):  {result['IX-A']}")
    print(f"  IX-B (Curiosity):  {result['IX-B']}")
    print(f"  IX-C (Personality): {result['IX-C']}")
    print(f"  total:             {result['IX_total']}")


if __name__ == "__main__":
    main()
