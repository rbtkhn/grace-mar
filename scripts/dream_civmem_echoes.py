#!/usr/bin/env python3
"""Bounded civ-mem token overlap for dream handoff — query only, no index build."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

CIVMEM_INDEX_PATH = REPO_ROOT / "docs" / "civilization-memory" / ".cache" / "inrepo_index.json"

CIVMEM_DISCLAIMER = (
    "Analogical / historical depth from in-repo civ-mem (token overlap); "
    "not current truth, not Voice knowledge, not part of the Record."
)


def excerpt_self_memory_short_term(memory_text: str, *, max_chars: int = 400) -> str:
    """First ~max_chars from Short-term section, or head of file."""
    if not memory_text.strip():
        return ""
    m = re.search(r"^## Short-term\s*$", memory_text, re.MULTILINE)
    if not m:
        return " ".join(memory_text.split())[:max_chars]
    start = m.end()
    rest = memory_text[start:]
    m2 = re.search(r"^## \S", rest, re.MULTILINE)
    body = rest[: m2.start()] if m2 else rest
    collapsed = " ".join(body.split())
    return collapsed[:max_chars]


def build_civmem_query_from_digest(digest: dict[str, Any], *, max_chars: int = 800) -> str:
    parts: list[str] = []
    total = 0
    for entry in digest.get("entries") or []:
        if entry.get("relationship_type") == "reinforcement":
            continue
        title = str(entry.get("title") or "").strip()
        summary = str(entry.get("summary") or "").strip()[:220]
        why = entry.get("why_flagged")
        why_s = ""
        if isinstance(why, list) and why:
            why_s = str(why[0])[:120]
        chunk = f"{title} {summary} {why_s}".strip()
        if not chunk:
            continue
        if total + len(chunk) + 1 > max_chars:
            remain = max_chars - total - 1
            if remain > 20:
                parts.append(chunk[:remain])
            break
        parts.append(chunk)
        total += len(chunk) + 1
    return " ".join(parts)[:max_chars]


def compute_civmem_echoes(
    *,
    digest: dict[str, Any],
    self_memory_text: str,
    limit: int = 3,
    snippet_max: int = 200,
) -> tuple[list[dict[str, Any]], bool]:
    """
    Return (echoes, index_missing). echoes empty if index missing or query empty.
    """
    from build_civmem_inrepo_index import query_inrepo_civmem

    if not CIVMEM_INDEX_PATH.is_file():
        return [], True

    q = build_civmem_query_from_digest(digest, max_chars=800)
    if not q.strip():
        q = excerpt_self_memory_short_term(self_memory_text, max_chars=400)
    q = " ".join(q.split())[:800]
    if not q.strip():
        return [], False

    raw = query_inrepo_civmem(q, limit=limit)
    echoes: list[dict[str, Any]] = []
    for row in raw:
        path = str(row.get("path", "") or "")
        try:
            rel = str(Path(path).relative_to(REPO_ROOT))
        except ValueError:
            rel = path
        overlap = int(row.get("overlap", 0) or 0)
        snip = str(row.get("snippet", "") or "")[:snippet_max]
        echoes.append(
            {
                "path": rel,
                "overlap": overlap,
                "snippet_preview": snip,
            }
        )
    return echoes, False
