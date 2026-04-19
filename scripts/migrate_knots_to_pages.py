#!/usr/bin/env python3
"""One-time migration: (1) move flat expert files into per-expert folders,
(2) convert standalone knot files into page blocks inside thread files.

Usage::

    python3 scripts/migrate_knots_to_pages.py --dry-run          # preview both phases
    python3 scripts/migrate_knots_to_pages.py                    # run both phases
    python3 scripts/migrate_knots_to_pages.py --phase folder     # folder restructure only
    python3 scripts/migrate_knots_to_pages.py --phase pages      # knots-to-pages only

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_expert_corpus import (
    CANONICAL_EXPERT_IDS,
    THREAD_MARKER_START,
    _EXPERT_IDS_SET,
    expert_paths,
)

NOTEBOOK_DIR = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
)
DEFAULT_KNOT_INDEX = NOTEBOOK_DIR / "knot-index.yaml"
DEFAULT_KNOT_CONNECTIONS = NOTEBOOK_DIR / "knot-connections.yaml"

_RE_EXPERT_THREADS = re.compile(
    r"\*\*Expert threads?:\*\*\s*(.+)", re.IGNORECASE
)
_RE_MONTH = re.compile(r"^##\s+(\d{4}-\d{2})\s*$")

PAGE_MARKER_START = '<!-- strategy-page:start id="{id}" date="{date}" watch="{watch}" -->'
PAGE_MARKER_END = "<!-- strategy-page:end -->"


# ---------------------------------------------------------------------------
# Phase 1 — folder restructure
# ---------------------------------------------------------------------------

_FILE_SUFFIXES = {
    "": "profile.md",
    "-thread": "thread.md",
    "-transcript": "transcript.md",
    "-mind": "mind.md",
}


def _display_path(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def phase_folder(dry_run: bool) -> list[str]:
    """Move flat expert files into ``experts/<id>/`` directories."""
    actions: list[str] = []
    for expert_id in CANONICAL_EXPERT_IDS:
        dest_dir = NOTEBOOK_DIR / "experts" / expert_id
        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)

        for suffix, target_name in _FILE_SUFFIXES.items():
            src = NOTEBOOK_DIR / f"strategy-expert-{expert_id}{suffix}.md"
            dst = dest_dir / target_name
            if not src.is_file():
                continue
            if dst.is_file():
                actions.append(f"skip (already exists): {_display_path(dst)}")
                continue
            label = "would move" if dry_run else "moved"
            actions.append(f"{label}: {_display_path(src)} → {_display_path(dst)}")
            if not dry_run:
                shutil.move(str(src), str(dst))

    return actions


# ---------------------------------------------------------------------------
# Phase 2 — knots to pages
# ---------------------------------------------------------------------------

def _load_knot_index(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data.get("knots", []) if data else []


def _load_connections(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data.get("connections", []) if data else []


def _watches_for_knot(knot_path_str: str, connections: list[dict]) -> list[str]:
    """Extract shared-watch tags from knot-connections.yaml warrant lists."""
    watches: list[str] = []
    for conn in connections:
        if conn.get("from") == knot_path_str or conn.get("to") == knot_path_str:
            for w in conn.get("warrant", []):
                if w.startswith("shared-watch:"):
                    tag = w.split(":", 1)[1]
                    if tag not in watches:
                        watches.append(tag)
    return watches


def _experts_from_knot(knot: dict, knot_content: str) -> list[str]:
    """Determine which canonical experts this knot involves."""
    experts: list[str] = []
    for c in knot.get("clusters", []) or []:
        if c in _EXPERT_IDS_SET and c not in experts:
            experts.append(c)
    m = _RE_EXPERT_THREADS.search(knot_content)
    if m:
        for slug in re.split(r"[,;\s]+", m.group(1)):
            slug = slug.strip().strip("`").strip(".")
            if slug in _EXPERT_IDS_SET and slug not in experts:
                experts.append(slug)
    return sorted(experts)


def _build_page_block(
    knot_label: str,
    knot_date: str,
    watches: list[str],
    experts: list[str],
    expert_id: str,
    source_basename: str,
    content: str,
) -> str:
    """Render a single page block for insertion into a thread file."""
    watch_str = watches[0] if watches else ""
    also_in = [e for e in experts if e != expert_id]

    marker_start = PAGE_MARKER_START.format(
        id=knot_label, date=knot_date, watch=watch_str
    )
    lines = [
        marker_start,
        f"### Page: {knot_label}",
        "",
        f"**Date:** {knot_date}",
    ]
    if watch_str:
        lines.append(f"**Watch:** {watch_str}")
    lines.append(f"**Source knot:** {source_basename}")
    if also_in:
        lines.append(f"**Also in:** {', '.join(also_in)}")
    lines.append("")
    lines.append(content.strip())
    lines.append(PAGE_MARKER_END)
    return "\n".join(lines)


def _insert_page_into_thread(thread_path: Path, month: str, page_block: str, dry_run: bool) -> str:
    """Insert a page block under the ``## YYYY-MM`` chapter in a thread file.

    Returns an action description string.
    """
    if not thread_path.is_file():
        return f"skip (thread file missing): {thread_path}"

    text = thread_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    month_heading = f"## {month}"
    insert_idx: int | None = None

    for i, line in enumerate(lines):
        if line.strip() == month_heading:
            j = i + 1
            while j < len(lines):
                ln = lines[j].strip()
                if ln == THREAD_MARKER_START:
                    insert_idx = j
                    break
                if _RE_MONTH.match(lines[j]):
                    insert_idx = j
                    break
                j += 1
            else:
                insert_idx = len(lines)
            break

    if insert_idx is None:
        if THREAD_MARKER_START in text:
            marker_idx = next(
                i for i, ln in enumerate(lines) if ln.strip() == THREAD_MARKER_START
            )
            new_lines = lines[:marker_idx] + [
                "", month_heading, "", page_block, ""
            ] + lines[marker_idx:]
        else:
            new_lines = lines + ["", month_heading, "", page_block, ""]
    else:
        new_lines = lines[:insert_idx] + [page_block, ""] + lines[insert_idx:]

    label = "would insert" if dry_run else "inserted"
    if not dry_run:
        thread_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return f"{label} page into {thread_path.relative_to(REPO_ROOT)} under {month_heading}"


def phase_pages(dry_run: bool) -> list[str]:
    """Read knot-index + knot files, insert page blocks into thread files."""
    knots = _load_knot_index(DEFAULT_KNOT_INDEX)
    connections = _load_connections(DEFAULT_KNOT_CONNECTIONS)
    actions: list[str] = []

    for knot in knots:
        knot_path_str = knot.get("path", "")
        knot_path = REPO_ROOT / knot_path_str
        knot_date = knot.get("date", "unknown")
        knot_label = knot.get("knot_label", "")
        month = knot_date[:7] if len(knot_date) >= 7 else "unknown"

        if not knot_path.is_file():
            actions.append(f"skip (knot file missing): {knot_path_str}")
            continue

        content = knot_path.read_text(encoding="utf-8")
        experts = _experts_from_knot(knot, content)
        watches = _watches_for_knot(knot_path_str, connections)

        if not experts:
            actions.append(f"skip (no canonical experts): {knot_label} ({knot_path_str})")
            continue

        for expert_id in experts:
            thread_path = expert_paths(expert_id, NOTEBOOK_DIR)["thread"]
            page_block = _build_page_block(
                knot_label=knot_label,
                knot_date=knot_date,
                watches=watches,
                experts=experts,
                expert_id=expert_id,
                source_basename=knot_path.name,
                content=content,
            )
            action = _insert_page_into_thread(thread_path, month, page_block, dry_run)
            actions.append(action)

    return actions


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing",
    )
    ap.add_argument(
        "--phase",
        choices=["folder", "pages"],
        default=None,
        help="Run only one phase (default: both)",
    )
    args = ap.parse_args()

    run_folder = args.phase in (None, "folder")
    run_pages = args.phase in (None, "pages")

    if run_folder:
        print("--- Phase 1: Expert folder restructure ---")
        for action in phase_folder(args.dry_run):
            print(f"  {action}")

    if run_pages:
        print("--- Phase 2: Knots to pages ---")
        for action in phase_pages(args.dry_run):
            print(f"  {action}")

    mode = "dry-run" if args.dry_run else "applied"
    print(f"\nDone ({mode}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
