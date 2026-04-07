#!/usr/bin/env python3
"""Semantic search over Evidence (self-archive.md) using TF-IDF + cosine similarity.

Stdlib-only — no external dependencies.  Parses self-archive.md into individual
entries (WRITE-*, READ-*, CREATE-*, ACT-*, MEDIA-*, etc.) and ranks them against
a free-text query.  Significantly better than grep for natural-language questions
about the Record.

Usage:
    python3 scripts/search_evidence.py -u grace-mar "swimming fear"
    python3 scripts/search_evidence.py -u grace-mar "Chinese story" --top 3
    python3 scripts/search_evidence.py -u grace-mar "bravery" --type ACT --json
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USERS_DIR = REPO_ROOT / "users"
DEFAULT_USER = os.getenv("GRACE_MAR_USER_ID", "grace-mar")

STOP_WORDS = frozenset(
    "a an the is are was were be been being have has had do does did will would "
    "shall should may might can could of in to for on with at by from as into "
    "through during before after above below between out off over under again "
    "further then once here there when where why how all each every both few "
    "more most other some such no nor not only own same so than too very and "
    "but or if while that this these those it its he she they them their his "
    "her my your we our what which who whom".split()
)


@dataclass
class EvidenceEntry:
    entry_id: str
    entry_type: str
    title: str
    date: str
    text: str
    line_start: int
    line_end: int
    section: str = ""


@dataclass
class SearchResult:
    entry: EvidenceEntry
    score: float
    matched_terms: list[str] = field(default_factory=list)


def _tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation, remove stop words."""
    tokens = re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


def _extract_yaml_entries(text: str, lines: list[str]) -> list[EvidenceEntry]:
    """Extract entries from YAML code blocks (WRITE-*, READ-*, CREATE-*, ACT-*, MEDIA-*)."""
    entries: list[EvidenceEntry] = []
    id_pattern = re.compile(r"^\s+-\s+id:\s+(([A-Z]+-)\d+)", re.MULTILINE)
    section_pattern = re.compile(r"^## ([IVX]+)\.\s+(.+)$", re.MULTILINE)

    sections: list[tuple[int, str]] = []
    for m in section_pattern.finditer(text):
        sections.append((m.start(), m.group(2).strip()))

    def _section_for_pos(pos: int) -> str:
        name = ""
        for start, sname in sections:
            if start <= pos:
                name = sname
        return name

    id_positions = list(id_pattern.finditer(text))
    for idx, m in enumerate(id_positions):
        entry_id = m.group(1)
        entry_type = m.group(2).rstrip("-")
        start_pos = m.start()
        end_pos = id_positions[idx + 1].start() if idx + 1 < len(id_positions) else len(text)

        chunk = text[start_pos:end_pos]
        line_start = text[:start_pos].count("\n") + 1
        line_end = text[:end_pos].count("\n") + 1

        title_match = re.search(r'title:\s*["\']?(.+?)["\']?\s*$', chunk, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else entry_id

        date_match = re.search(r"created_at:\s*(\S+)", chunk)
        if not date_match:
            date_match = re.search(r"date:\s*(\S+)", chunk)
        date = date_match.group(1) if date_match else ""

        entries.append(EvidenceEntry(
            entry_id=entry_id,
            entry_type=entry_type,
            title=title,
            date=date,
            text=chunk,
            line_start=line_start,
            line_end=line_end,
            section=_section_for_pos(start_pos),
        ))

    return entries


def _extract_gated_entries(text: str) -> list[EvidenceEntry]:
    """Extract entries from § VIII. GATED APPROVED LOG."""
    entries: list[EvidenceEntry] = []
    marker = "## VIII. GATED APPROVED LOG"
    start = text.find(marker)
    if start < 0:
        return entries

    section_text = text[start:]
    pattern = re.compile(
        r"\*\*\[([^\]]+)\]\*\*\s+`(\w+)`\s+\(([^)]+)\)\s*\n"
        r"((?:>.*\n?)+)",
        re.MULTILINE,
    )
    for m in pattern.finditer(section_text):
        date = m.group(1).strip()
        status = m.group(2)
        source = m.group(3)
        body_lines = m.group(4)
        body = re.sub(r"^>\s?", "", body_lines, flags=re.MULTILINE).strip()

        id_match = re.search(r"(CANDIDATE-\d+)\s*→\s*((?:ACT|READ|WRITE|CREATE|MEDIA|LEARN|CUR|PER)-\d+)", body)
        if id_match:
            entry_id = id_match.group(2)
            entry_type = entry_id.split("-")[0]
        else:
            cand_match = re.search(r"(CANDIDATE-\d+)", body)
            entry_id = cand_match.group(1) if cand_match else f"GATE-{date}"
            entry_type = "GATE"

        abs_pos = start + m.start()
        line_start = text[:abs_pos].count("\n") + 1
        line_end = text[:abs_pos + m.end()].count("\n") + 1

        entries.append(EvidenceEntry(
            entry_id=entry_id,
            entry_type=entry_type,
            title=body[:80].replace("\n", " "),
            date=date,
            text=f"[{status}] ({source}) {body}",
            line_start=line_start,
            line_end=line_end,
            section="GATED APPROVED LOG",
        ))

    return entries


def parse_evidence(archive_path: Path) -> list[EvidenceEntry]:
    text = archive_path.read_text(encoding="utf-8")
    entries = _extract_yaml_entries(text, text.splitlines())
    entries.extend(_extract_gated_entries(text))

    seen: set[str] = set()
    deduped: list[EvidenceEntry] = []
    for e in entries:
        key = f"{e.entry_id}:{e.line_start}"
        if key not in seen:
            seen.add(key)
            deduped.append(e)

    return deduped


def _build_tfidf(docs: list[list[str]]) -> tuple[list[dict[str, float]], dict[str, float]]:
    """Build TF-IDF vectors for a list of tokenized documents."""
    n = len(docs)
    if n == 0:
        return [], {}

    df: Counter[str] = Counter()
    for tokens in docs:
        df.update(set(tokens))

    idf: dict[str, float] = {}
    for term, count in df.items():
        idf[term] = math.log((n + 1) / (count + 1)) + 1.0

    vectors: list[dict[str, float]] = []
    for tokens in docs:
        tf = Counter(tokens)
        total = len(tokens) or 1
        vec: dict[str, float] = {}
        for term, count in tf.items():
            vec[term] = (count / total) * idf.get(term, 1.0)
        vectors.append(vec)

    return vectors, idf


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[k] * b[k] for k in common)
    mag_a = math.sqrt(sum(v * v for v in a.values()))
    mag_b = math.sqrt(sum(v * v for v in b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def search(
    query: str,
    entries: list[EvidenceEntry],
    *,
    top: int = 5,
    entry_type: str | None = None,
) -> list[SearchResult]:
    if entry_type:
        entries = [e for e in entries if e.entry_type.upper() == entry_type.upper()]

    if not entries:
        return []

    docs = [_tokenize(e.text) for e in entries]
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    all_docs = docs + [query_tokens]
    vectors, idf = _build_tfidf(all_docs)

    query_vec = vectors[-1]
    doc_vectors = vectors[:-1]

    results: list[SearchResult] = []
    query_terms_set = set(query_tokens)
    for i, (entry, dvec) in enumerate(zip(entries, doc_vectors)):
        score = _cosine(dvec, query_vec)
        if score > 0:
            matched = sorted(query_terms_set & set(docs[i]))
            results.append(SearchResult(entry=entry, score=score, matched_terms=matched))

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:top]


def _load_graph(users_dir: Path, user: str) -> dict | None:
    """Load evidence-graph.json if it exists."""
    graph_path = users_dir / user / "evidence-graph.json"
    if not graph_path.exists():
        return None
    try:
        return json.loads(graph_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def expand_results_with_graph(
    results: list[SearchResult],
    entries: list[EvidenceEntry],
    graph: dict | None,
    max_related: int = 3,
) -> list[EvidenceEntry]:
    """Return related entries via 1-hop graph expansion from search hits."""
    if not graph or not results:
        return []
    adj = graph.get("adjacency", {})
    hit_ids = {r.entry.entry_id for r in results}
    neighbor_ids: set[str] = set()
    for r in results:
        for neighbor in adj.get(r.entry.entry_id, []):
            if neighbor not in hit_ids:
                neighbor_ids.add(neighbor)
    entry_map = {e.entry_id: e for e in entries}
    related = [entry_map[nid] for nid in neighbor_ids if nid in entry_map]
    return related[:max_related]


def format_text(results: list[SearchResult], query: str, related: list[EvidenceEntry] | None = None) -> str:
    if not results:
        return f'No results for "{query}".'

    lines = [f'Evidence search: "{query}" — {len(results)} result(s)\n']
    for rank, r in enumerate(results, 1):
        e = r.entry
        lines.append(f"  [{rank}] {e.entry_id} — {e.title}")
        meta = []
        if e.date:
            meta.append(e.date)
        if e.section:
            meta.append(e.section)
        meta.append(f"lines {e.line_start}–{e.line_end}")
        lines.append(f"      {' | '.join(meta)}")
        lines.append(f"      Score: {r.score:.3f}  Matched: {', '.join(r.matched_terms)}")

        snippet = e.text[:200].replace("\n", " ").strip()
        if len(e.text) > 200:
            snippet += "…"
        lines.append(f"      {snippet}")
        lines.append("")

    if related:
        lines.append(f"  Related (via graph, 1-hop):")
        for e in related:
            lines.append(f"    ~ {e.entry_id} — {e.title}")
        lines.append("")

    return "\n".join(lines)


def format_json(results: list[SearchResult], query: str, related: list[EvidenceEntry] | None = None) -> str:
    out: dict = {
        "query": query,
        "result_count": len(results),
        "results": [
            {
                "rank": i + 1,
                "entry_id": r.entry.entry_id,
                "entry_type": r.entry.entry_type,
                "title": r.entry.title,
                "date": r.entry.date,
                "section": r.entry.section,
                "score": round(r.score, 4),
                "matched_terms": r.matched_terms,
                "lines": [r.entry.line_start, r.entry.line_end],
                "snippet": r.entry.text[:300],
            }
            for i, r in enumerate(results)
        ],
    }
    if related:
        out["related"] = [
            {"entry_id": e.entry_id, "type": e.entry_type, "title": e.title}
            for e in related
        ]
    return json.dumps(out, indent=2)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Search Evidence (self-archive.md) by semantic similarity.",
        epilog="Stdlib-only TF-IDF + cosine. No external dependencies.",
    )
    ap.add_argument("query", nargs="*", help="Search query (free text)")
    ap.add_argument("-u", "--user", default=DEFAULT_USER)
    ap.add_argument("--users-dir", type=Path, default=DEFAULT_USERS_DIR)
    ap.add_argument("--top", type=int, default=5, help="Number of results (default 5)")
    ap.add_argument("--type", dest="entry_type", default=None,
                    help="Filter by entry type (ACT, WRITE, CREATE, READ, MEDIA, GATE)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--graph", action="store_true",
                    help="Include related entries via 1-hop graph expansion (requires evidence-graph.json)")
    ap.add_argument("--stats", action="store_true", help="Show index stats and exit")
    args = ap.parse_args()

    archive_path = args.users_dir / args.user / "self-archive.md"
    if not archive_path.exists():
        print(f"Evidence file not found: {archive_path}", file=sys.stderr)
        return 1

    entries = parse_evidence(archive_path)

    if args.stats:
        type_counts: Counter[str] = Counter(e.entry_type for e in entries)
        print(f"Evidence index: {len(entries)} entries from {archive_path.name}")
        for etype, count in type_counts.most_common():
            print(f"  {etype}: {count}")
        return 0

    if not args.query:
        ap.error("query is required (unless --stats)")

    query = " ".join(args.query)
    results = search(query, entries, top=args.top, entry_type=args.entry_type)

    related = None
    if args.graph:
        graph = _load_graph(args.users_dir, args.user)
        related = expand_results_with_graph(results, entries, graph)

    if args.json:
        print(format_json(results, query, related=related))
    else:
        print(format_text(results, query, related=related))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
