#!/usr/bin/env python3
"""
Build search index over research/repos/civilization_memory (upstream CMC checkout).

Parallel to build_civmem_inrepo_index.py, which indexes only docs/civilization-memory
(satellite essays). This script indexes the full local checkout when present.

Writes: research/repos/civilization_memory/.cache/upstream_index.json

Usage:
  python scripts/build_civmem_upstream_index.py build
  python scripts/build_civmem_upstream_index.py query "Rome aqueducts" [--limit 5]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from build_civmem_inrepo_index import build_markdown_index, query_index, query_index_entries

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_DIR = REPO_ROOT / "research" / "repos" / "civilization_memory"
CACHE_DIR = UPSTREAM_DIR / ".cache"
INDEX_PATH = CACHE_DIR / "upstream_index.json"


def query_upstream_civmem(question: str, *, limit: int = 3) -> list[dict[str, object]]:
    """
    Load upstream index if present; return ranked match rows with path + snippet.
    """
    if not INDEX_PATH.is_file():
        return []
    try:
        index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return query_index_entries(index, question, limit=limit)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        return 1
    cmd = sys.argv[1].lower()
    if cmd == "build":
        if not UPSTREAM_DIR.is_dir():
            print(
                f"Upstream checkout missing: {UPSTREAM_DIR}",
                file=sys.stderr,
            )
            return 1
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        index = build_markdown_index(UPSTREAM_DIR)
        INDEX_PATH.write_text(json.dumps(index, indent=2), encoding="utf-8")
        print(f"Indexed {len(index['entries'])} docs -> {INDEX_PATH}", file=sys.stderr)
        return 0
    if cmd == "query":
        if not INDEX_PATH.is_file():
            print("Run 'build' first (upstream checkout must exist).", file=sys.stderr)
            return 1
        question = sys.argv[2] if len(sys.argv) > 2 else ""
        limit = 5
        if "--limit" in sys.argv:
            i = sys.argv.index("--limit")
            if i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
        index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        snippets = query_index(index, question, limit=limit)
        for s in snippets:
            print(s[:400] + ("..." if len(s) > 400 else ""))
            print("---")
        return 0
    print("Usage: build | query \"...\" [--limit N]", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
