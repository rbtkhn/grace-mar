#!/usr/bin/env python3
"""Scaffold ``### Pages / Work Product`` indexes in expert thread files.

WORK only; not Record.

Default mode is a dry run that prints the entries that should exist. ``--apply``
inserts a missing section or appends missing entries without editing page bodies
or existing thread prose.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_strategy_page_thread_links import (  # noqa: E402
    NOTEBOOK_DIR,
    THREAD_MARKER_START,
    PageInfo,
    clean_inline,
    discover_pages,
    expected_thread_file,
    human_layer,
    month_segment,
    page_is_indexed,
    pages_work_product_section,
    repo_rel,
)


def relative_link(from_file: Path, to_file: Path) -> str:
    return Path(
        Path(".").joinpath(
            *Path(
                to_file.resolve().relative_to(from_file.parent.resolve())
            ).parts
        )
    ).as_posix()


def rel_link_portable(from_file: Path, to_file: Path) -> str:
    try:
        import os

        return Path(os.path.relpath(to_file.resolve(), from_file.parent.resolve())).as_posix()
    except ValueError:
        return repo_rel(to_file)


def entry_for(page: PageInfo, thread_file: Path) -> str:
    role = clean_inline(page.fields.get("thread_role", "")) or "carry-forward"
    delta = clean_inline(page.fields.get("continuity_delta", "")) or "TODO: name this page's continuity delta."
    title = page.title.replace("[", "(").replace("]", ")")
    href = rel_link_portable(thread_file, page.path)
    return (
        f"- {page.date} - [{title}]({href})\n"
        f"  role: {role}\n"
        f"  delta: {delta}"
    )


def section_for(entries: list[str]) -> str:
    return "### Pages / Work Product\n\n" + "\n".join(entries).rstrip() + "\n"


def find_month_heading(text: str, month: str) -> re.Match[str] | None:
    return re.search(rf"^##\s+{re.escape(month)}\s*$", human_layer(text), re.MULTILINE)


def insert_or_append(thread_file: Path, month: str, entries: list[str]) -> str:
    text = thread_file.read_text(encoding="utf-8", errors="replace")
    human = human_layer(text)
    machine = text[len(human):] if len(human) < len(text) else ""
    segment = month_segment(text, month)
    existing_section = pages_work_product_section(segment)
    add = "\n".join(entries).rstrip() + "\n"

    if existing_section:
        section_start = human.find(existing_section)
        if section_start < 0:
            return text
        insert_at = section_start + len(existing_section)
        return human[:insert_at].rstrip() + "\n" + add + human[insert_at:] + machine

    new_section = "\n" + section_for(entries)
    heading = find_month_heading(text, month)
    if heading:
        insert_at = heading.end()
        return human[:insert_at] + "\n" + new_section + human[insert_at:] + machine

    # Monthly files may begin with the machine marker and no human month heading yet.
    prefix = f"## {month}\n\n" + section_for(entries) + "\n"
    return prefix + text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--notebook-dir", type=Path, default=NOTEBOOK_DIR)
    ap.add_argument("--expert-id", default="", help="Limit to one expert id.")
    ap.add_argument("--year-month", default="", help="Limit to YYYY-MM.")
    ap.add_argument("--apply", action="store_true", help="Write missing thread index sections/entries.")
    args = ap.parse_args()

    if args.year_month and not re.fullmatch(r"\d{4}-\d{2}", args.year_month):
        print("error: --year-month must be YYYY-MM", file=sys.stderr)
        return 2

    notebook = args.notebook_dir.resolve()
    pending: dict[Path, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    pages = discover_pages(notebook, args.expert_id, args.year_month)
    for page in pages:
        thread_file = expected_thread_file(page, notebook)
        indexed, _has_section = page_is_indexed(page, thread_file)
        if indexed:
            continue
        pending[thread_file][page.month].append(entry_for(page, thread_file))

    if not pending:
        print("ok: no missing page-thread index entries found")
        return 0

    for thread_file in sorted(pending):
        print()
        print(f"## {repo_rel(thread_file)}")
        for month, entries in sorted(pending[thread_file].items()):
            print()
            print(f"### {month}")
            print(section_for(entries).rstrip())

    if not args.apply:
        print()
        print("dry-run only; rerun with --apply to update thread files")
        return 0

    for thread_file, by_month in pending.items():
        if not thread_file.is_file():
            print(f"warning: missing thread file, skipped: {repo_rel(thread_file)}", file=sys.stderr)
            continue
        text = thread_file.read_text(encoding="utf-8", errors="replace")
        for month, entries in sorted(by_month.items()):
            text = insert_or_append(thread_file, month, entries)
            thread_file.write_text(text, encoding="utf-8")
        print(f"updated {repo_rel(thread_file)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
