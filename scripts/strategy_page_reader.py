"""Discover and parse strategy pages from expert thread files.

Pages are marker-fenced blocks within thread files::

    <!-- strategy-page:start id="..." date="..." watch="..." -->
    ### Page: ...
    ...
    <!-- strategy-page:end -->

This module is a reusable library (not a CLI). It is imported by
``strategy_watch.py``, ``strategy_page.py``, ``strategy_weave.py``,
and other scripts.

WORK only; not Record.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PAGE_MARKER_RE = re.compile(
    r'<!--\s*strategy-page:start'
    r'\s+id="(?P<id>[^"]+)"'
    r'\s+date="(?P<date>[^"]*)"'
    r'\s+watch="(?P<watch>[^"]*)"'
    r'\s*-->',
)
PAGE_END_RE = re.compile(r'<!--\s*strategy-page:end\s*-->')


@dataclass
class PageBlock:
    id: str
    date: str
    watch: str
    expert_id: str
    content: str
    source_path: Path = field(default_factory=lambda: Path())

    def to_dict(self) -> dict:
        d: dict = {
            "id": self.id,
            "date": self.date,
            "watch": self.watch,
            "expert_id": self.expert_id,
            "content": self.content,
        }
        if self.source_path != Path():
            d["source_path"] = str(self.source_path)
        return d


def discover_pages(thread_path: Path, expert_id: str = "") -> list[PageBlock]:
    """Find all page blocks in a single thread file."""
    if not thread_path.is_file():
        return []

    text = thread_path.read_text(encoding="utf-8")
    pages: list[PageBlock] = []
    pos = 0

    while pos < len(text):
        m = PAGE_MARKER_RE.search(text, pos)
        if not m:
            break
        end_m = PAGE_END_RE.search(text, m.end())
        if not end_m:
            break
        content = text[m.end():end_m.start()].strip()
        pages.append(PageBlock(
            id=m.group("id"),
            date=m.group("date"),
            watch=m.group("watch"),
            expert_id=expert_id,
            content=content,
            source_path=thread_path,
        ))
        pos = end_m.end()

    return pages


def discover_all_pages(notebook_dir: Path) -> dict[str, list[PageBlock]]:
    """Scan all expert thread files and return ``{expert_id: [pages]}``."""
    from strategy_expert_corpus import CANONICAL_EXPERT_IDS, expert_thread_paths_for_discovery

    result: dict[str, list[PageBlock]] = {}
    for expert_id in CANONICAL_EXPERT_IDS:
        combined: list[PageBlock] = []
        for thread_path in expert_thread_paths_for_discovery(notebook_dir, expert_id):
            combined.extend(discover_pages(thread_path, expert_id=expert_id))
        if combined:
            result[expert_id] = combined
    return result


def pages_for_watch(notebook_dir: Path, watch_id: str) -> dict[str, list[PageBlock]]:
    """Return only pages matching a specific ``watch=`` tag."""
    all_pages = discover_all_pages(notebook_dir)
    filtered: dict[str, list[PageBlock]] = {}
    for expert_id, pages in all_pages.items():
        matching = [p for p in pages if p.watch == watch_id]
        if matching:
            filtered[expert_id] = matching
    return filtered


def all_watch_ids(notebook_dir: Path) -> list[str]:
    """Return sorted unique watch IDs across all pages."""
    watches: set[str] = set()
    for pages in discover_all_pages(notebook_dir).values():
        for p in pages:
            if p.watch:
                watches.add(p.watch)
    return sorted(watches)
