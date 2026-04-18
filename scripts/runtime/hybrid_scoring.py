"""Shared scoring primitives for hybrid retrieval across non-canonical surfaces.

Combines lexical relevance, an optional semantic hook (stub in v1), and
recency influence into a single weighted score.  Stdlib-only.

Non-canonical; does not touch Record or recursion-gate.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


# ── stop-words (shared with search_evidence) ──────────────────────────

STOP_WORDS = frozenset(
    "a an the is are was were be been being have has had do does did will would "
    "shall should may might can could of in to for on with at by from as into "
    "through during before after above below between out off over under again "
    "further then once here there when where why how all each every both few "
    "more most other some such no nor not only own same so than too very and "
    "but or if while that this these those it its he she they them their his "
    "her my your we our what which who whom".split()
)


# ── default weight triple ─────────────────────────────────────────────

DEFAULT_WEIGHTS = (0.80, 0.15, 0.05)  # lexical, semantic, recency


# ── result container ──────────────────────────────────────────────────

@dataclass
class HybridResult:
    path: str
    label: str
    retrieval_surface: str
    lexical_score: float
    semantic_score: float
    recency_score: float
    final_score: float
    matched_terms: list[str] = field(default_factory=list)
    snippet: str = ""
    meta: dict[str, Any] = field(default_factory=dict)


# ── tokeniser ─────────────────────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


# ── lexical helpers ───────────────────────────────────────────────────

def tfidf_cosine(query_tokens: list[str], doc_tokens: list[str], idf: dict[str, float]) -> float:
    """TF-IDF cosine between *query_tokens* and *doc_tokens* using pre-built IDF."""
    if not query_tokens or not doc_tokens:
        return 0.0
    q_tf = Counter(query_tokens)
    d_tf = Counter(doc_tokens)
    q_total = len(query_tokens) or 1
    d_total = len(doc_tokens) or 1

    q_vec: dict[str, float] = {t: (c / q_total) * idf.get(t, 1.0) for t, c in q_tf.items()}
    d_vec: dict[str, float] = {t: (c / d_total) * idf.get(t, 1.0) for t, c in d_tf.items()}

    common = set(q_vec) & set(d_vec)
    if not common:
        return 0.0
    dot = sum(q_vec[k] * d_vec[k] for k in common)
    mag_q = math.sqrt(sum(v * v for v in q_vec.values()))
    mag_d = math.sqrt(sum(v * v for v in d_vec.values()))
    if mag_q == 0 or mag_d == 0:
        return 0.0
    return dot / (mag_q * mag_d)


def build_idf(all_doc_tokens: list[list[str]]) -> dict[str, float]:
    n = len(all_doc_tokens)
    if n == 0:
        return {}
    df: Counter[str] = Counter()
    for tokens in all_doc_tokens:
        df.update(set(tokens))
    return {term: math.log((n + 1) / (count + 1)) + 1.0 for term, count in df.items()}


def term_overlap_score(query_tokens: list[str], doc_tokens: list[str]) -> float:
    """Simple normalised term overlap (fallback when corpus is too small for TF-IDF)."""
    if not query_tokens:
        return 0.0
    doc_set = set(doc_tokens)
    hits = sum(1 for t in query_tokens if t in doc_set)
    return hits / len(query_tokens)


def normalize_scores(scores: list[float]) -> list[float]:
    """Min-max normalise a list of raw scores to 0-1."""
    if not scores:
        return scores
    lo, hi = min(scores), max(scores)
    span = hi - lo
    if span == 0:
        return [1.0 if hi > 0 else 0.0 for _ in scores]
    return [(s - lo) / span for s in scores]


# ── semantic hook (stub in v1) ────────────────────────────────────────

def semantic_score(query: str, text: str) -> float:
    """Return a 0-1 semantic similarity score.

    v1: always returns 0.0 — no embedding model is available in stdlib.
    When a lightweight embedding backend is added, implement here.
    """
    return 0.0


def semantic_available() -> bool:
    """Whether semantic scoring is active (not just stubbed)."""
    return False


# ── recency ───────────────────────────────────────────────────────────

def recency_from_iso(ts_str: str | None, *, now: datetime | None = None) -> float:
    """0-1 linear decay over 7 days from an ISO timestamp string."""
    if not ts_str or not isinstance(ts_str, str):
        return 0.0
    t = ts_str.strip()
    if t.endswith("Z"):
        t = t[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(t)
    except ValueError:
        return 0.0
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    now = now or datetime.now(timezone.utc)
    age = (now - dt).total_seconds()
    if age < 0:
        return 1.0
    week = 7 * 24 * 3600
    return max(0.0, 1.0 - age / week)


def recency_from_mtime(mtime: float, *, now: datetime | None = None) -> float:
    """0-1 linear decay over 7 days from a file mtime (epoch seconds)."""
    now = now or datetime.now(timezone.utc)
    age = now.timestamp() - mtime
    if age < 0:
        return 1.0
    week = 7 * 24 * 3600
    return max(0.0, 1.0 - age / week)


# ── score combination ─────────────────────────────────────────────────

def combine_scores(
    lexical: float,
    semantic: float,
    recency: float,
    *,
    weights: tuple[float, float, float] = DEFAULT_WEIGHTS,
    semantic_active: bool = False,
) -> float:
    """Weighted sum with automatic redistribution when semantic is unavailable."""
    w_lex, w_sem, w_rec = weights
    if not semantic_active:
        w_lex += w_sem
        w_sem = 0.0
    return w_lex * lexical + w_sem * semantic + w_rec * recency
