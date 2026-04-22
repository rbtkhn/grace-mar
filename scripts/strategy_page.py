#!/usr/bin/env python3
"""Compose a new page for named experts and insert it into their thread files.

The **page** command is the Ship-lane complement to **weave** (Think lane).
It creates a marker-fenced page block in each named expert's thread file
under the current ``## YYYY-MM`` chapter.

Usage::

    python3 scripts/strategy_page.py davis barnes
    python3 scripts/strategy_page.py davis barnes --watch hormuz
    python3 scripts/strategy_page.py pape --id zero-sum-hormuz
    python3 scripts/strategy_page.py davis barnes --dry-run

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_expert_corpus import (
    CANONICAL_EXPERT_IDS,
    THREAD_MARKER_START,
    _EXPERT_IDS_SET,
    thread_path_for_page_month,
)
from strategy_page_reader import discover_pages

DEFAULT_INBOX = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md"
)
DEFAULT_NOTEBOOK = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
)

PAGE_MARKER_START = '<!-- strategy-page:start id="{id}" date="{date}" watch="{watch}" -->'
PAGE_MARKER_END = "<!-- strategy-page:end -->"

_RE_MONTH_H2 = re.compile(r"^##\s+(\d{4}-\d{2})\s*$")


# ---------------------------------------------------------------------------
# Inbox material extraction
# ---------------------------------------------------------------------------

def _gather_inbox_material(
    experts: list[str],
    inbox_path: Path,
) -> list[str]:
    """Extract inbox lines tagged with ``thread:<expert>`` or batch-analysis
    lines referencing any of the named experts."""
    if not inbox_path.is_file():
        return []
    text = inbox_path.read_text(encoding="utf-8")
    relevant: list[str] = []
    for line in text.splitlines():
        lower = line.lower()
        for eid in experts:
            if f"thread:{eid}" in lower:
                relevant.append(line.rstrip())
                break
        else:
            if "batch-analysis" in lower:
                for eid in experts:
                    if eid in lower:
                        relevant.append(line.rstrip())
                        break
    return relevant


# ---------------------------------------------------------------------------
# Page block construction
# ---------------------------------------------------------------------------

def build_page_block(
    page_id: str,
    page_date: str,
    watch: str,
    experts: list[str],
    current_expert: str,
    inbox_lines: list[str],
) -> str:
    """Render a page block ready for insertion."""
    also_in = [e for e in experts if e != current_expert]

    marker = PAGE_MARKER_START.format(id=page_id, date=page_date, watch=watch)
    lines = [marker, f"### Page: {page_id}", ""]
    lines.append(f"**Date:** {page_date}")
    if watch:
        lines.append(f"**Watch:** {watch}")
    if also_in:
        lines.append(f"**Also in:** {', '.join(also_in)}")
    lines.append("")

    if inbox_lines:
        lines.append("**Inbox material:**")
        lines.append("")
        for il in inbox_lines[:20]:
            lines.append(il)
        lines.append("")

    lines.append("_(Operator/assistant: refine this page content.)_")
    lines.append(PAGE_MARKER_END)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Thread file insertion
# ---------------------------------------------------------------------------

def insert_page(thread_path: Path, month: str, page_block: str, dry_run: bool) -> str:
    """Insert a page block under ``## YYYY-MM`` in a thread file."""
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
                if _RE_MONTH_H2.match(lines[j]):
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
    return f"{label} page '{month_heading}' in {thread_path}"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "experts",
        nargs="+",
        help="Expert IDs to include in this page",
    )
    ap.add_argument("--watch", default="", help="Watch tag for this page")
    ap.add_argument("--id", dest="page_id", default="", help="Explicit page slug")
    ap.add_argument(
        "--date",
        default="",
        help="Page date (YYYY-MM-DD); defaults to today",
    )
    ap.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    ap.add_argument("--notebook", type=Path, default=DEFAULT_NOTEBOOK)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    expert_ids = [e.lower().strip() for e in args.experts]
    for eid in expert_ids:
        if eid not in _EXPERT_IDS_SET:
            print(f"error: unknown expert ID: {eid}", file=sys.stderr)
            print(f"valid IDs: {', '.join(CANONICAL_EXPERT_IDS)}", file=sys.stderr)
            return 1

    page_date = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    month = page_date[:7]

    if args.page_id:
        page_id = args.page_id
    else:
        page_id = "-".join(expert_ids) + "-" + page_date

    inbox_lines = _gather_inbox_material(expert_ids, args.inbox)

    for eid in expert_ids:
        page_block = build_page_block(
            page_id=page_id,
            page_date=page_date,
            watch=args.watch,
            experts=expert_ids,
            current_expert=eid,
            inbox_lines=inbox_lines,
        )
        thread_path = thread_path_for_page_month(args.notebook, eid, month)
        result = insert_page(thread_path, month, page_block, args.dry_run)
        print(f"  {result}")

    if args.dry_run:
        print(f"\nDry run: page '{page_id}' for {', '.join(expert_ids)} (not written)")
    else:
        print(f"\nCreated page '{page_id}' for {', '.join(expert_ids)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
