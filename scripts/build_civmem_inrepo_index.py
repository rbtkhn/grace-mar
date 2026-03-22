#!/usr/bin/env python3
"""
Build search index over docs/civilization-memory for in-repo CMC lookup.

Enables the bot to answer civ-mem–scoped questions when the external
civilization_memory repo is not present. Index is written to
docs/civilization-memory/.cache/inrepo_index.json.

Usage:
  python scripts/build_civmem_inrepo_index.py build
  python scripts/build_civmem_inrepo_index.py query "Rome and aqueducts" [--limit 5]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CIVMEM_DIR = REPO_ROOT / "docs" / "civilization-memory"
CACHE_DIR = CIVMEM_DIR / ".cache"
INDEX_PATH = CACHE_DIR / "inrepo_index.json"
SKIP_DIRS = {".git", "node_modules", ".cache", ".skeleton"}

# Stopwords for query scoring (subset of lookup_cmc _FTS_STOPWORDS)
_STOPWORDS = frozenset(
    "the and for are but not you all can had her was one our out day get has him his how man new now old see way who"
    .split()
)


def _tokenize(text: str) -> set[str]:
    """Lowercase tokens 3+ chars, drop stopwords."""
    tokens = re.findall(r"[a-z0-9]{3,}", text.lower())
    return set(t for t in tokens if t not in _STOPWORDS)


def _first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()[:200]
    return ""


def _body_snippet(text: str, max_chars: int = 500) -> str:
    """First paragraph or first max_chars of body after first heading."""
    lines = text.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("# "):
            start = i + 1
            break
    body = " ".join(lines[start:]).replace("\n", " ").strip()
    body = re.sub(r"\s+", " ", body)
    return body[:max_chars] if body else ""


def build_index() -> dict:
    """Scan docs/civilization-memory for .md files; return index dict."""
    entries = []
    for path in sorted(CIVMEM_DIR.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        rel = path.relative_to(CIVMEM_DIR)
        title = _first_heading(content)
        snippet = _body_snippet(content)
        if not snippet and not title:
            snippet = content.replace("\n", " ")[:400]
        entries.append({
            "path": str(rel),
            "title": title,
            "snippet": snippet,
        })
    return {"version": 1, "entries": entries}


def query_index(index: dict, question: str, limit: int = 5) -> list[str]:
    """
    Score entries by term overlap with question; return list of snippet strings.
    """
    rows = query_index_entries(index, question, limit=limit)
    return [r["snippet"] for r in rows if r.get("snippet", "").strip()]


def query_index_entries(index: dict, question: str, limit: int = 5) -> list[dict[str, object]]:
    """
    Score entries by term overlap with question; return ranked rows with path for provenance.
    """
    q_tokens = _tokenize(question)
    if not q_tokens:
        return []
    scored: list[tuple[int, str, str]] = []
    for e in index.get("entries", []):
        text = (e.get("title", "") + " " + e.get("snippet", "")).lower()
        doc_tokens = _tokenize(text)
        overlap = len(q_tokens & doc_tokens)
        if overlap > 0:
            path = str(e.get("path", "") or "")
            snip = str(e.get("snippet", "") or "")
            scored.append((overlap, path, snip))
    scored.sort(key=lambda x: -x[0])
    out: list[dict[str, object]] = []
    for o, path, snip in scored[:limit]:
        out.append({"overlap": o, "path": path, "snippet": snip[:600]})
    return out


def query_inrepo_civmem(question: str, *, limit: int = 3) -> list[dict[str, object]]:
    """
    Load the on-disk inrepo index (if present) and return ranked matches.
    Used by daily brief / operator tools — not Voice truth; historical depth only.
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
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        index = build_index()
        INDEX_PATH.write_text(json.dumps(index, indent=2), encoding="utf-8")
        print(f"Indexed {len(index['entries'])} docs -> {INDEX_PATH}", file=sys.stderr)
        return 0
    if cmd == "query":
        if not INDEX_PATH.is_file():
            print("Run 'build' first.", file=sys.stderr)
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
