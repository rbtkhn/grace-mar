#!/usr/bin/env python3
"""Generate shelf tables (Theology, Physics/biology, History, Computer Science) from self-library.md YAML.
Use --in-place to replace the Current entries table in each section."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

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

SHELF_SECTIONS = ["Theology", "Physics/biology", "History", "Computer Science"]


def _classify_shelf(scope_list: list[str], lane: str) -> str | None:
    scopes_lower = [s.lower() for s in scope_list]
    for tag, shelf in SCOPE_TO_SHELF:
        if tag in scopes_lower or any(tag in s for s in scopes_lower):
            return shelf
    return None


def _load_entries(path: Path) -> list[dict]:
    """Load all LIB entries (active and deprecated) with id, title, scope, notes, lane, status."""
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
        notes_m = re.search(r'notes:\s*["\']([^"\']*)["\']', block)
        lane_m = re.search(r"lane:\s*[\"']?(\w+)", block)
        status_m = re.search(r"status:\s*(\w+)", block)
        if not title_m:
            continue
        scope_raw = scope_m.group(1) if scope_m else ""
        scopes = [s.strip().strip("'\"") for s in scope_raw.split(",") if s.strip()]
        notes = (notes_m.group(1) if notes_m else "").strip()
        lane = (lane_m.group(1) or "canon").lower()
        status = status_m.group(1) if status_m else "active"
        entries.append(
            {
                "id": lib_id,
                "title": title_m.group(1),
                "scope": scopes,
                "notes": notes,
                "lane": lane,
                "status": status,
            }
        )
    return entries


def _shelf_for_entry(e: dict) -> str | None:
    return _classify_shelf(e["scope"], e["lane"])


def _escape_table_cell(s: str) -> str:
    """Escape pipe and newlines for markdown table."""
    return s.replace("|", "\\|").replace("\n", " ").strip()


def _format_description(notes: str, scope: list[str]) -> str:
    if notes:
        return _escape_table_cell(notes[:500])
    if scope:
        return "Scope: " + ", ".join(scope[:8])
    return ""


def build_theology_table(entries: list[dict]) -> str:
    theology = [e for e in entries if _shelf_for_entry(e) == "Theology"]
    theology.sort(key=lambda e: int(e["id"].replace("LIB-", "")))
    lines = [
        "**Current entries (Theology shelf):**",
        "",
        "| ID | Title | Description |",
        "|----|--------|-------------|",
    ]
    for e in theology:
        desc = _format_description(e["notes"], e["scope"])
        lines.append(f"| **{e['id']}** | {_escape_table_cell(e['title'])} | {desc} |")
    return "\n".join(lines)


def _build_shelf_table(shelf: str, entries: list[dict], section_heading: str) -> str:
    """section_heading e.g. 'Current entries (examples):' or 'Current entries:'"""
    shelf_entries = [e for e in entries if _shelf_for_entry(e) == shelf]
    shelf_entries.sort(key=lambda e: int(e["id"].replace("LIB-", "")))
    if not shelf_entries:
        return f"**{section_heading}** None yet. Add LIB rows with `scope` including the relevant tags as approved."
    lines = [
        f"**{section_heading}**",
        "",
        "| ID | Title | Description |",
        "|----|--------|-------------|",
    ]
    for e in shelf_entries:
        desc = _format_description(e["notes"], e["scope"])
        lines.append(f"| **{e['id']}** | {_escape_table_cell(e['title'])} | {desc} |")
    return "\n".join(lines)


def build_physics_table(entries: list[dict]) -> str:
    return _build_shelf_table(
        "Physics/biology", entries, "Current entries (examples):"
    )


def build_history_table(entries: list[dict]) -> str:
    return _build_shelf_table("History", entries, "Current entries (examples):")


def build_cs_table(entries: list[dict]) -> str:
    return _build_shelf_table("Computer Science", entries, "Current entries:")


def _replace_in_section(
    content: str,
    section_header: str,
    marker: str,
    new_block: str,
    stop_before: str | None = None,
) -> str:
    """Replace content after marker in the given ## section until stop_before or next --- or ##."""
    escaped = re.escape(section_header)
    stop = (r"\n\n" + re.escape(stop_before)) if stop_before else r"(?:\n\n---|\n## )"
    pattern = re.compile(
        r"(## "
        + escaped
        + r"\n.*?"
        + re.escape(marker)
        + r")\s*.*?(?="
        + stop
        + r")",
        re.DOTALL,
    )
    table_body = "\n".join(new_block.split("\n")[2:]) if "\n| " in new_block else new_block
    new_content, n = pattern.subn(r"\1\n\n" + table_body, content, count=1)
    if n == 0:
        return content
    return new_content


def main() -> int:
    p = argparse.ArgumentParser(
        description="Generate shelf tables from self-library.md"
    )
    p.add_argument("-u", "--user", default="grace-mar")
    p.add_argument(
        "-i",
        "--in-place",
        action="store_true",
        help="Replace Current entries tables in self-library.md",
    )
    args = p.parse_args()
    lib_path = REPO_ROOT / "users" / args.user / "self-library.md"
    entries = _load_entries(lib_path)
    theology_table = build_theology_table(entries)
    physics_table = build_physics_table(entries)
    history_table = build_history_table(entries)
    cs_table = build_cs_table(entries)
    if not args.in_place:
        print("## Theology\n")
        print(theology_table)
        print("\n## Physics, chemistry & biology\n")
        print(physics_table)
        print("\n## History\n")
        print(history_table)
        print("\n## Computer Science\n")
        print(cs_table)
        return 0
    content = lib_path.read_text(encoding="utf-8")
    content = _replace_in_section(
        content,
        "Theology",
        "**Current entries (Theology shelf):**",
        theology_table,
        stop_before="**Paths:**",
    )
    content = _replace_in_section(
        content,
        "Physics, chemistry & biology",
        "**Current entries (examples):**",
        physics_table,
    )
    content = _replace_in_section(
        content,
        "History",
        "**Current entries (examples):**",
        history_table,
    )
    content = _replace_in_section(
        content,
        "Computer Science",
        "**Current entries:**",
        cs_table,
    )
    lib_path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
