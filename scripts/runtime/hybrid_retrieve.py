#!/usr/bin/env python3
"""Hybrid retrieval across non-canonical surfaces.

Combines lexical scoring, an optional semantic hook (stub in v1), and
recency influence.  Dispatches to the appropriate data source per surface.

Non-canonical; does not touch Record or recursion-gate.
See docs/hybrid-retrieval.md.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_RUNTIME_DIR = Path(__file__).resolve().parent
_SCRIPTS_DIR = _RUNTIME_DIR.parent
REPO_ROOT = _RUNTIME_DIR.parent.parent

for _p in (_RUNTIME_DIR, _SCRIPTS_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import chunk_store  # noqa: E402
import hybrid_scoring as hs  # noqa: E402
import ledger_paths  # noqa: E402

SURFACES = frozenset({
    "prepared_context",
    "evidence_lookup",
    "artifact_lookup",
    "notebook_lookup",
})

DEFAULT_USER = os.getenv("GRACE_MAR_USER_ID", "grace-mar")
USERS_DIR = REPO_ROOT / "users"
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
NOTEBOOK_CHAPTERS = REPO_ROOT / "docs" / "skill-work" / "work-strategy" / "strategy-notebook" / "chapters"


# ── surface: prepared_context ─────────────────────────────────────────

def _search_prepared_context(
    query: str,
    top_k: int,
    use_recency: bool,
    weights: tuple[float, float, float],
) -> list[hs.HybridResult]:
    from observation_store import load_all  # noqa: E402
    from search_scoring import score_observation  # noqa: E402

    rows = load_all()
    if not rows:
        return []

    query_tokens = hs.tokenize(query)
    raw_scores: list[tuple[float, dict]] = []
    for row in rows:
        s = score_observation(row, query, bonus_tags=[])
        if s > 0:
            raw_scores.append((s, row))

    if not raw_scores:
        return []

    lexical_vals = [s for s, _ in raw_scores]
    normed = hs.normalize_scores(lexical_vals)

    sem_active = hs.semantic_available()
    results: list[hs.HybridResult] = []
    for (raw_lex, row), norm_lex in zip(raw_scores, normed):
        rec = hs.recency_from_iso(row.get("timestamp")) if use_recency else 0.0
        sem = hs.semantic_score(query, (row.get("title") or "") + " " + (row.get("summary") or ""))
        final = hs.combine_scores(norm_lex, sem, rec, weights=weights, semantic_active=sem_active)

        title = (row.get("title") or "").strip()
        summary = (row.get("summary") or "").replace("\n", " ").strip()
        matched = [t for t in query_tokens if t in (title + " " + summary).lower()]

        results.append(hs.HybridResult(
            path=f"runtime/observations/{row.get('obs_id', '?')}",
            label=title or row.get("obs_id", "?"),
            retrieval_surface="prepared_context",
            lexical_score=norm_lex,
            semantic_score=sem,
            recency_score=rec,
            final_score=final,
            matched_terms=sorted(set(matched)),
            snippet=summary[:200] if summary else "",
            meta={"obs_id": row.get("obs_id"), "lane": row.get("lane")},
        ))

    results.sort(key=lambda r: -r.final_score)
    return results[:top_k]


# ── surface: evidence_lookup ──────────────────────────────────────────

def _search_evidence(
    query: str,
    top_k: int,
    use_recency: bool,
    weights: tuple[float, float, float],
) -> list[hs.HybridResult]:
    from search_evidence import SearchResult, parse_evidence, search  # noqa: E402

    user = DEFAULT_USER
    archive = USERS_DIR / user / "self-archive.md"
    if not archive.exists():
        return []

    entries = parse_evidence(archive)
    if not entries:
        return []

    hits: list[SearchResult] = search(query, entries, top=max(top_k * 3, 30))
    if not hits:
        return []

    lexical_vals = [h.score for h in hits]
    normed = hs.normalize_scores(lexical_vals)

    sem_active = hs.semantic_available()
    results: list[hs.HybridResult] = []
    for hit, norm_lex in zip(hits, normed):
        rec = 0.0
        if use_recency and hit.entry.date:
            rec = hs.recency_from_iso(hit.entry.date + "T00:00:00Z")

        sem = hs.semantic_score(query, hit.entry.text)
        final = hs.combine_scores(norm_lex, sem, rec, weights=weights, semantic_active=sem_active)

        results.append(hs.HybridResult(
            path=f"users/{user}/self-archive.md:{hit.entry.line_start}-{hit.entry.line_end}",
            label=f"{hit.entry.entry_id} — {hit.entry.title}",
            retrieval_surface="evidence_lookup",
            lexical_score=norm_lex,
            semantic_score=sem,
            recency_score=rec,
            final_score=final,
            matched_terms=hit.matched_terms,
            snippet=hit.entry.text[:200].replace("\n", " "),
            meta={"entry_id": hit.entry.entry_id, "entry_type": hit.entry.entry_type, "date": hit.entry.date},
        ))

    results.sort(key=lambda r: -r.final_score)
    return results[:top_k]


# ── surface: artifact_lookup / notebook_lookup ────────────────────────

def _score_chunks(
    chunks: list[dict],
    query: str,
    query_tokens: list[str],
    idf: dict[str, float],
    surface: str,
    use_recency: bool,
    weights: tuple[float, float, float],
) -> list[hs.HybridResult]:
    """Score pre-generated chunk records and return HybridResults."""
    sem_active = hs.semantic_available()
    scored: list[tuple[float, dict]] = []
    for chk in chunks:
        tokens = hs.tokenize(chk.get("content", ""))
        s = hs.tfidf_cosine(query_tokens, tokens, idf)
        if s > 0:
            scored.append((s, chk))

    if not scored:
        return []

    lexical_vals = [s for s, _ in scored]
    normed = hs.normalize_scores(lexical_vals)

    results: list[hs.HybridResult] = []
    for (raw_lex, chk), norm_lex in zip(scored, normed):
        rec = 0.0
        if use_recency and chk.get("generated_at"):
            rec = hs.recency_from_iso(chk["generated_at"])

        content = chk.get("content", "")
        sem = hs.semantic_score(query, content[:2000])
        final = hs.combine_scores(norm_lex, sem, rec, weights=weights, semantic_active=sem_active)

        src_path = chk.get("source_path", "?")
        start = chk.get("start_line", "?")
        end = chk.get("end_line", "?")
        section = chk.get("section_hint", "")

        chunk_tokens = set(hs.tokenize(content))
        matched = sorted(t for t in query_tokens if t in chunk_tokens)

        snippet = content[:300].replace("\n", " ").strip()
        if len(content) > 300:
            snippet = snippet[:297] + "..."

        results.append(hs.HybridResult(
            path=f"{src_path}:{start}-{end}",
            label=section or chk.get("chunk_id", "?"),
            retrieval_surface=surface,
            lexical_score=norm_lex,
            semantic_score=sem,
            recency_score=rec,
            final_score=final,
            matched_terms=matched,
            snippet=snippet,
            meta={
                "chunk_id": chk.get("chunk_id"),
                "chunk_index": chk.get("chunk_index"),
                "total_chunks": chk.get("total_chunks"),
                "section_hint": section,
                "source_path": src_path,
                "filename": Path(src_path).name,
            },
        ))

    return results


def _scan_md_files(
    base_dir: Path,
    query: str,
    top_k: int,
    surface: str,
    use_recency: bool,
    weights: tuple[float, float, float],
) -> list[hs.HybridResult]:
    """Token-overlap search over .md/.json files under *base_dir*.

    When chunk indexes are available for a surface, large files are scored
    at chunk granularity instead of whole-file. Small/un-chunked files use
    the original whole-file path.
    """
    if not base_dir.is_dir():
        return []

    chunked_paths = chunk_store.chunked_source_paths(surface)
    all_chunks = chunk_store.load_chunks(surface) if chunked_paths else []

    skip = {".git", "node_modules", ".cache", "__pycache__"}
    docs: list[tuple[Path, str, list[str]]] = []
    for p in sorted(base_dir.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix not in (".md", ".json", ".yaml", ".yml"):
            continue
        if any(part in skip for part in p.parts):
            continue
        try:
            rel = str(p.relative_to(REPO_ROOT))
        except ValueError:
            rel = str(p)
        if rel in chunked_paths:
            continue  # handled via chunk scoring below
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        tokens = hs.tokenize(text)
        if tokens:
            docs.append((p, text, tokens))

    query_tokens = hs.tokenize(query)
    if not query_tokens:
        return []

    all_token_lists: list[list[str]] = [t for _, _, t in docs]
    for chk in all_chunks:
        all_token_lists.append(hs.tokenize(chk.get("content", "")))
    all_token_lists.append(query_tokens)
    idf = hs.build_idf(all_token_lists)

    # Score whole-file docs (un-chunked)
    results: list[hs.HybridResult] = []
    if docs:
        scored: list[tuple[float, Path, str, list[str]]] = []
        for p, text, tokens in docs:
            s = hs.tfidf_cosine(query_tokens, tokens, idf)
            if s > 0:
                scored.append((s, p, text, tokens))

        if scored:
            lexical_vals = [s for s, _, _, _ in scored]
            normed = hs.normalize_scores(lexical_vals)

            sem_active = hs.semantic_available()
            for (raw_lex, p, text, tokens), norm_lex in zip(scored, normed):
                rec = 0.0
                if use_recency:
                    try:
                        rec = hs.recency_from_mtime(p.stat().st_mtime)
                    except OSError:
                        pass

                sem = hs.semantic_score(query, text[:2000])
                final = hs.combine_scores(norm_lex, sem, rec, weights=weights, semantic_active=sem_active)

                try:
                    rel = str(p.relative_to(REPO_ROOT))
                except ValueError:
                    rel = str(p)

                heading = ""
                for line in text.splitlines()[:10]:
                    if line.startswith("# "):
                        heading = line[2:].strip()[:120]
                        break

                doc_set = set(tokens)
                matched = sorted(t for t in query_tokens if t in doc_set)

                snippet_text = text[:300].replace("\n", " ").strip()
                if len(text) > 300:
                    snippet_text = snippet_text[:297] + "..."

                results.append(hs.HybridResult(
                    path=rel,
                    label=heading or p.name,
                    retrieval_surface=surface,
                    lexical_score=norm_lex,
                    semantic_score=sem,
                    recency_score=rec,
                    final_score=final,
                    matched_terms=matched,
                    snippet=snippet_text,
                    meta={"filename": p.name},
                ))

    # Score chunk records
    if all_chunks:
        chunk_results = _score_chunks(
            all_chunks, query, query_tokens, idf, surface, use_recency, weights,
        )
        results.extend(chunk_results)

    results.sort(key=lambda r: -r.final_score)
    return results[:top_k]


def _search_artifacts(
    query: str, top_k: int, use_recency: bool, weights: tuple[float, float, float],
) -> list[hs.HybridResult]:
    return _scan_md_files(ARTIFACTS_DIR, query, top_k, "artifact_lookup", use_recency, weights)


def _search_notebook(
    query: str, top_k: int, use_recency: bool, weights: tuple[float, float, float],
) -> list[hs.HybridResult]:
    return _scan_md_files(NOTEBOOK_CHAPTERS, query, top_k, "notebook_lookup", use_recency, weights)


# ── dispatch ──────────────────────────────────────────────────────────

_DISPATCH: dict[str, Any] = {
    "prepared_context": _search_prepared_context,
    "evidence_lookup": _search_evidence,
    "artifact_lookup": _search_artifacts,
    "notebook_lookup": _search_notebook,
}


def retrieve(
    surface: str,
    query: str,
    *,
    top_k: int = 5,
    use_recency: bool = True,
    weights: tuple[float, float, float] = hs.DEFAULT_WEIGHTS,
) -> list[hs.HybridResult]:
    fn = _DISPATCH.get(surface)
    if fn is None:
        raise ValueError(f"unsupported surface: {surface}. allowed: {', '.join(sorted(SURFACES))}")
    return fn(query, top_k, use_recency, weights)


# ── miss-ledger integration ──────────────────────────────────────────

def _log_miss(surface: str, query: str, top_k: int, result_count: int) -> None:
    logger = _RUNTIME_DIR / "log_retrieval_miss.py"
    if not logger.exists():
        print("warning: log_retrieval_miss.py not found; skipping miss log", file=sys.stderr)
        return
    notes = f"hybrid_retrieve returned {result_count}/{top_k} results"
    cmd = [
        sys.executable, str(logger),
        "--surface", surface,
        "--query", query[:500],
        "--failure-class", "unknown",
        "--notes", notes,
        "--recorded-by", "hybrid_retrieve",
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"miss logged for surface={surface}", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"warning: miss log failed: {e.stderr}", file=sys.stderr)


# ── CLI ───────────────────────────────────────────────────────────────

def _format_text(results: list[hs.HybridResult], query: str, surface: str) -> str:
    if not results:
        return f'No results for "{query}" on {surface}.'
    lines = [f'Hybrid retrieval: "{query}" on {surface} — {len(results)} result(s)\n']
    for rank, r in enumerate(results, 1):
        lines.append(f"  [{rank}] {r.label}")
        lines.append(f"      path: {r.path}")
        lines.append(f"      final={r.final_score:.4f}  lex={r.lexical_score:.4f}  "
                      f"sem={r.semantic_score:.4f}  rec={r.recency_score:.4f}")
        if r.matched_terms:
            lines.append(f"      matched: {', '.join(r.matched_terms)}")
        if r.snippet:
            snip = r.snippet[:160]
            if len(r.snippet) > 160:
                snip += "..."
            lines.append(f"      {snip}")
        lines.append("")
    return "\n".join(lines)


def _format_json(results: list[hs.HybridResult], query: str, surface: str) -> str:
    out = {
        "query": query,
        "surface": surface,
        "semantic_active": hs.semantic_available(),
        "result_count": len(results),
        "results": [
            {
                "rank": i + 1,
                "path": r.path,
                "label": r.label,
                "final_score": round(r.final_score, 4),
                "lexical_score": round(r.lexical_score, 4),
                "semantic_score": round(r.semantic_score, 4),
                "recency_score": round(r.recency_score, 4),
                "matched_terms": r.matched_terms,
                "snippet": r.snippet[:300],
                "meta": r.meta,
            }
            for i, r in enumerate(results)
        ],
    }
    return json.dumps(out, indent=2, ensure_ascii=False)


def _parse_weights(s: str) -> tuple[float, float, float]:
    parts = s.split(",")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("weights must be three comma-separated floats (lex,sem,rec)")
    try:
        vals = tuple(float(p.strip()) for p in parts)
    except ValueError:
        raise argparse.ArgumentTypeError("weights must be numeric")
    total = sum(vals)
    if total <= 0:
        raise argparse.ArgumentTypeError("weights must sum to > 0")
    return (vals[0] / total, vals[1] / total, vals[2] / total)  # type: ignore[return-value]


def _validate_surface(value: str) -> str:
    if value not in SURFACES:
        allowed = ", ".join(sorted(SURFACES))
        raise argparse.ArgumentTypeError(f"invalid surface: {value}. allowed: {allowed}")
    return value


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Hybrid retrieval across non-canonical Grace-Mar surfaces.",
        epilog="Lexical + optional semantic + recency. Stdlib-only. See docs/hybrid-retrieval.md.",
    )
    ap.add_argument("--surface", required=True, type=_validate_surface,
                    help=f"Retrieval surface ({', '.join(sorted(SURFACES))})")
    ap.add_argument("--query", "-q", required=True, help="Search query (free text)")
    ap.add_argument("--top-k", type=int, default=5, dest="top_k", help="Number of results (default 5)")
    ap.add_argument("--use-semantic", choices=("auto", "on", "off"), default="auto", dest="use_semantic",
                    help="Semantic scoring: auto (use if available), on (require), off (disable)")
    ap.add_argument("--use-recency", choices=("auto", "on", "off"), default="auto", dest="use_recency",
                    help="Recency influence: auto/on (apply), off (disable)")
    ap.add_argument("--weights", type=_parse_weights, default=None,
                    help="Score weights as lex,sem,rec (e.g. '0.80,0.15,0.05'); auto-normalised")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--log-miss", action="store_true", dest="log_miss",
                    help="Log a retrieval miss if results are empty or fewer than --top-k")
    ap.add_argument("--user", default=DEFAULT_USER, help="User id for evidence lookup (default grace-mar)")
    return ap.parse_args()


def main() -> int:
    args = parse_args()

    global DEFAULT_USER
    DEFAULT_USER = args.user

    use_recency = args.use_recency != "off"
    weights = args.weights or hs.DEFAULT_WEIGHTS

    if args.use_semantic == "on" and not hs.semantic_available():
        print("error: semantic scoring requested but not available in v1", file=sys.stderr)
        return 2

    try:
        results = retrieve(
            args.surface,
            args.query,
            top_k=args.top_k,
            use_recency=use_recency,
            weights=weights,
        )
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.log_miss and len(results) < args.top_k:
        _log_miss(args.surface, args.query, args.top_k, len(results))

    if args.json:
        print(_format_json(results, args.query, args.surface))
    else:
        print(_format_text(results, args.query, args.surface))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
