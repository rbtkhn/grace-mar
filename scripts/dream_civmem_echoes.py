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

ANALOGY_CANDIDATE_LABEL = (
    "Analogy candidate only — not evidence, not recommendation, not Record."
)

# Query-side only; index uses its own tokenization in build_civmem_inrepo_index.
STOPWORDS = frozenset(
    {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "as", "by",
        "with", "from", "into", "through", "during", "before", "after", "above", "below",
        "between", "under", "again", "further", "then", "once", "here", "there", "when",
        "where", "why", "how", "all", "each", "few", "more", "most", "other", "some", "such",
        "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "can", "will",
        "just", "don", "should", "now", "this", "that", "these", "those", "is", "are", "was",
        "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "doing",
        "would", "could", "may", "might", "must", "shall",
    }
)

_MIN_TOKEN_LEN = 2
_INTERESTING_MIN_LEN = 5


def _load_civmem_budget() -> dict[str, Any]:
    try:
        from context_budget import get_bool, get_int, load_context_budget
    except ImportError:
        from scripts.context_budget import get_bool, get_int, load_context_budget  # type: ignore

    return load_context_budget("dream")


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _normalize_tokens(tokens: list[str]) -> list[str]:
    out: list[str] = []
    for t in tokens:
        if len(t) < _MIN_TOKEN_LEN or t in STOPWORDS:
            continue
        out.append(t)
    return out


def _extract_interesting_query_tokens(query: str) -> list[str]:
    return [t for t in _normalize_tokens(_tokenize(query)) if len(t) >= _INTERESTING_MIN_LEN]


def _looks_specific(path: str, snippet: str, interesting_query_tokens: list[str]) -> bool:
    if not interesting_query_tokens:
        return True
    blob = f"{path} {snippet}".lower()
    toks = set(_normalize_tokens(_tokenize(blob)))
    return any(t in toks for t in interesting_query_tokens)


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
    limit: int | None = None,
    min_overlap: int | None = None,
    query_limit: int | None = None,
    snippet_max: int = 200,
    require_specificity: bool | None = None,
    dream_budget: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], bool]:
    """
    Return (echoes, index_missing). echoes empty if index missing or query empty.
    Default cap is one echo; overlap must be >= min_overlap (integer token count from index).
    """
    from build_civmem_inrepo_index import query_inrepo_civmem

    budget = dream_budget if dream_budget is not None else _load_civmem_budget()
    try:
        from context_budget import get_bool, get_int
    except ImportError:
        from scripts.context_budget import get_bool, get_int  # type: ignore

    eff_limit = limit if limit is not None else get_int(budget, "max_civ_mem_echoes", 1)
    eff_min_overlap = min_overlap if min_overlap is not None else get_int(budget, "min_civ_mem_overlap", 4)
    eff_query_limit = query_limit if query_limit is not None else get_int(budget, "civmem_query_limit", 24)
    eff_require = require_specificity if require_specificity is not None else get_bool(
        budget, "require_specific_civ_mem_token", False
    )

    if not CIVMEM_INDEX_PATH.is_file():
        return [], True

    q = build_civmem_query_from_digest(digest, max_chars=800)
    if not q.strip():
        q = excerpt_self_memory_short_term(self_memory_text, max_chars=400)
    q = " ".join(q.split())[:800]
    if not q.strip():
        return [], False

    interesting = _extract_interesting_query_tokens(q)
    raw = query_inrepo_civmem(q, limit=eff_query_limit)
    echoes: list[dict[str, Any]] = []
    for row in raw:
        path = str(row.get("path", "") or "")
        try:
            rel = str(Path(path).relative_to(REPO_ROOT))
        except ValueError:
            rel = path
        overlap = int(row.get("overlap", 0) or 0)
        if overlap < eff_min_overlap:
            continue
        snip = str(row.get("snippet", "") or "")[:snippet_max]
        spec_ok = _looks_specific(rel, snip, interesting)
        if eff_require and interesting and not spec_ok:
            continue
        score = float(overlap) + (2.0 if spec_ok else 0.0)
        echoes.append(
            {
                "path": rel,
                "overlap": overlap,
                "snippet_preview": snip,
                "analogy_label": ANALOGY_CANDIDATE_LABEL,
                "specificity_pass": spec_ok,
                "score": score,
            }
        )
        if len(echoes) >= eff_limit:
            break
    return echoes, False
