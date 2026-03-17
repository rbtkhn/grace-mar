#!/usr/bin/env python3
"""Reorder self-library.md Entries block by shelf (Theology, Physics, History, CS, then Reference/Canon/Influence).
Preserves exact block content. No ID renumbering. Output is written to stdout for inspection or replacement."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Shelf order: thematic first, then by lane. Each entry maps to one shelf (first match wins).
SHELF_ORDER = [
    "Theology",
    "Physics/biology",
    "History",
    "Computer Science",
    "Reference",
    "Canon",
    "Influence",
]

SCOPE_TO_SHELF = [
    ("theology", "Theology"),
    ("physics", "Physics/biology"),
    ("chemistry", "Physics/biology"),
    ("biology", "Physics/biology"),
    ("science", "Physics/biology"),
    ("history", "History"),
    ("world history", "History"),
    ("computer_science", "Computer Science"),
    ("programming", "Computer Science"),
    ("software", "Computer Science"),
    ("algorithms", "Computer Science"),
    ("AI", "Computer Science"),
    ("systems", "Computer Science"),
]

LANE_TO_SHELF = {
    "reference": "Reference",
    "canon": "Canon",
    "influence": "Influence",
}


def _classify_shelf(block: str) -> str:
    scope_m = re.search(r"scope:\s*\[([^\]]*)\]", block)
    scope_raw = scope_m.group(1) if scope_m else ""
    scopes = [s.strip().strip("'\"").lower() for s in scope_raw.split(",") if s.strip()]
    for tag, shelf in SCOPE_TO_SHELF:
        if tag in scopes or any(tag in s for s in scopes):
            return shelf
    lane_m = re.search(r"lane:\s*[\"']?(\w+)", block)
    lane = (lane_m.group(1) or "canon").lower()
    return LANE_TO_SHELF.get(lane, "Canon")


def _lib_id_num(block: str) -> int:
    m = re.search(r"id:\s+LIB-(\d+)", block)
    return int(m.group(1)) if m else 0


def extract_entries_block(content: str) -> str | None:
    m = re.search(r"^```yaml\s*\nentries:\s*\n(.*?)^```", content, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else None


def _strip_trailing_section_comment(block: str) -> str:
    """Remove trailing blank lines and section comments (  # --- ... )."""
    lines = block.rstrip().split("\n")
    while lines:
        last = lines[-1].strip()
        if not last or re.match(r"^\s*#\s*---", last):
            lines.pop()
        else:
            break
    return "\n".join(lines).rstrip()


def parse_blocks(entries_body: str) -> list[tuple[str, str]]:
    """Return list of (raw_block, shelf)."""
    blocks = re.findall(
        r"(  - id: LIB-\d+.*?)(?=  - id: LIB-\d+|$)",
        entries_body,
        re.DOTALL,
    )
    out = []
    for raw in blocks:
        raw = _strip_trailing_section_comment(raw)
        if not raw:
            continue
        shelf = _classify_shelf(raw)
        out.append((raw, shelf))
    return out


def reorder(blocks_with_shelf: list[tuple[str, str]]) -> list[tuple[str, str]]:
    order_idx = {s: i for i, s in enumerate(SHELF_ORDER)}
    key = lambda x: (order_idx.get(x[1], 99), _lib_id_num(x[0]))
    return sorted(blocks_with_shelf, key=key)


def emit_entries(ordered: list[tuple[str, str]]) -> str:
    lines = ["entries:"]
    prev_shelf = None
    for raw, shelf in ordered:
        if prev_shelf is not None and prev_shelf != shelf:
            lines.append("")
            lines.append(f"  # --- {shelf} ---")
            lines.append("")
        prev_shelf = shelf
        lines.append(raw)
    return "\n".join(lines)


def main() -> int:
    import sys
    p = argparse.ArgumentParser(description="Reorder self-library Entries by shelf")
    p.add_argument("-u", "--user", default="grace-mar")
    p.add_argument("-o", "--out", help="Write result to file (default: stdout)")
    p.add_argument("-i", "--in-place", action="store_true", help="Replace Entries section in self-library.md")
    args = p.parse_args()
    lib_path = REPO_ROOT / "users" / args.user / "self-library.md"
    content = lib_path.read_text(encoding="utf-8")
    entries_body = extract_entries_block(content)
    if not entries_body:
        print("Could not find ```yaml entries: ... ``` block", file=sys.stderr)
        return 1
    blocks = parse_blocks(entries_body)
    ordered = reorder(blocks)
    new_entries = emit_entries(ordered)
    yaml_block = f"```yaml\n{new_entries}\n```"
    if args.in_place:
        # Replace from "## Entries" through closing ``` with new section
        pattern = re.compile(
            r"(## Entries\s*\n\n)```yaml\s*\nentries:.*?^```",
            re.DOTALL | re.MULTILINE,
        )
        new_content = pattern.sub(r"\1" + yaml_block, content)
        if new_content == content:
            print("No match for Entries section", file=sys.stderr)
            return 1
        lib_path.write_text(new_content, encoding="utf-8")
        return 0
    if args.out:
        Path(args.out).write_text(yaml_block, encoding="utf-8")
    else:
        print(yaml_block)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
