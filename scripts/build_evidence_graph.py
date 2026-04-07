#!/usr/bin/env python3
"""Build a derived relationship graph over Evidence (self-archive.md) entries.

Generates an adjacency list (JSON) with two edge types:
  - explicit: cross-references found in YAML fields (contributes_to, source,
    artifact_id, knowledge_entry, CANDIDATE → ACT, etc.)
  - implicit: thematic similarity via TF-IDF cosine (above a configurable
    threshold)

The graph is a derived index — not authoritative, rotatable, regenerated on
demand.  Same governance class as PRP and search_evidence.py.

Usage:
    python3 scripts/build_evidence_graph.py -u grace-mar
    python3 scripts/build_evidence_graph.py -u grace-mar --threshold 0.20 --json
    python3 scripts/build_evidence_graph.py -u grace-mar --stats
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USERS_DIR = REPO_ROOT / "users"
DEFAULT_USER = os.getenv("GRACE_MAR_USER_ID", "grace-mar")

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from search_evidence import (
    EvidenceEntry,
    parse_evidence,
    _tokenize,
    _build_tfidf,
    _cosine,
)


@dataclass
class GraphEdge:
    source: str
    target: str
    edge_type: str
    score: float
    detail: str


ID_PATTERN = re.compile(r"\b((?:ACT|WRITE|CREATE|READ|MEDIA|LEARN|CUR|PER|CANDIDATE)-\d+)\b")
CONTRIBUTES_PATTERN = re.compile(r"contributes_to|artifact_id|source.*?:|knowledge_entr|curiosity_entr|personality_entr", re.IGNORECASE)
CANDIDATE_ARROW = re.compile(r"(CANDIDATE-\d+)\s*(?:→|->|—>)+\s*((?:ACT|WRITE|CREATE|READ|MEDIA|LEARN|CUR|PER)-\d+)")


def _extract_explicit_edges(entries: list[EvidenceEntry]) -> list[GraphEdge]:
    """Find explicit cross-references between entries."""
    entry_ids = {e.entry_id for e in entries}
    edges: list[GraphEdge] = []
    seen: set[tuple[str, str, str]] = set()

    for entry in entries:
        mentioned_ids = set(ID_PATTERN.findall(entry.text))
        mentioned_ids.discard(entry.entry_id)

        for mid in mentioned_ids:
            if mid not in entry_ids:
                continue
            key = (entry.entry_id, mid, "explicit")
            rev_key = (mid, entry.entry_id, "explicit")
            if key in seen or rev_key in seen:
                continue
            seen.add(key)

            detail = "cross-reference"
            if CANDIDATE_ARROW.search(entry.text):
                detail = "pipeline"
            elif CONTRIBUTES_PATTERN.search(entry.text):
                detail = "contributes_to"

            edges.append(GraphEdge(
                source=entry.entry_id,
                target=mid,
                edge_type="explicit",
                score=1.0,
                detail=detail,
            ))

    return edges


def _extract_implicit_edges(
    entries: list[EvidenceEntry],
    threshold: float = 0.12,
    max_edges_per_node: int = 5,
) -> list[GraphEdge]:
    """Compute TF-IDF cosine similarity between all pairs; keep edges above threshold."""
    docs = [_tokenize(e.text) for e in entries]
    if len(docs) < 2:
        return []

    vectors, _idf = _build_tfidf(docs)
    edges: list[GraphEdge] = []
    per_node: dict[str, int] = defaultdict(int)

    scored_pairs: list[tuple[float, int, int]] = []
    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            score = _cosine(vectors[i], vectors[j])
            if score >= threshold:
                scored_pairs.append((score, i, j))

    scored_pairs.sort(key=lambda x: x[0], reverse=True)

    for score, i, j in scored_pairs:
        src_id = entries[i].entry_id
        tgt_id = entries[j].entry_id
        if per_node[src_id] >= max_edges_per_node and per_node[tgt_id] >= max_edges_per_node:
            continue

        tokens_i = set(_tokenize(entries[i].text))
        tokens_j = set(_tokenize(entries[j].text))
        shared = sorted(tokens_i & tokens_j)[:8]

        edges.append(GraphEdge(
            source=src_id,
            target=tgt_id,
            edge_type="thematic",
            score=round(score, 4),
            detail=", ".join(shared) if shared else "cosine",
        ))
        per_node[src_id] += 1
        per_node[tgt_id] += 1

    return edges


def build_graph(
    archive_path: Path,
    *,
    threshold: float = 0.12,
    max_edges_per_node: int = 5,
) -> dict:
    """Build the full evidence graph."""
    entries = parse_evidence(archive_path)
    explicit = _extract_explicit_edges(entries)
    implicit = _extract_implicit_edges(entries, threshold=threshold, max_edges_per_node=max_edges_per_node)

    nodes = [
        {
            "id": e.entry_id,
            "type": e.entry_type,
            "title": e.title[:80],
            "date": e.date,
            "section": e.section,
        }
        for e in entries
    ]

    all_edges = explicit + implicit
    edges_json = [
        {
            "source": e.source,
            "target": e.target,
            "type": e.edge_type,
            "score": e.score,
            "detail": e.detail,
        }
        for e in all_edges
    ]

    adjacency: dict[str, list[str]] = defaultdict(list)
    for e in all_edges:
        adjacency[e.source].append(e.target)
        adjacency[e.target].append(e.source)

    return {
        "node_count": len(nodes),
        "edge_count": len(edges_json),
        "explicit_edges": len(explicit),
        "implicit_edges": len(implicit),
        "nodes": nodes,
        "edges": edges_json,
        "adjacency": dict(adjacency),
    }


def expand_one_hop(graph: dict, entry_ids: list[str]) -> list[str]:
    """Return entry ids reachable in 1 hop from the given set (excluding input ids)."""
    adj = graph.get("adjacency", {})
    seed = set(entry_ids)
    neighbors: set[str] = set()
    for eid in seed:
        for neighbor in adj.get(eid, []):
            if neighbor not in seed:
                neighbors.add(neighbor)
    return sorted(neighbors)


def format_stats(graph: dict) -> str:
    """Human-readable stats summary."""
    lines = [
        f"Evidence graph: {graph['node_count']} nodes, {graph['edge_count']} edges",
        f"  Explicit edges: {graph['explicit_edges']}",
        f"  Implicit (thematic) edges: {graph['implicit_edges']}",
    ]
    adj = graph.get("adjacency", {})
    if adj:
        degrees = [len(v) for v in adj.values()]
        lines.append(f"  Connected nodes: {len(adj)}/{graph['node_count']}")
        lines.append(f"  Degree: min={min(degrees)}, max={max(degrees)}, avg={sum(degrees)/len(degrees):.1f}")

    type_counts: dict[str, int] = defaultdict(int)
    for n in graph["nodes"]:
        type_counts[n["type"]] += 1
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"  {t}: {c} nodes")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build derived Evidence relationship graph.",
        epilog="Derived index — not authoritative. Regenerated from self-archive.md on demand.",
    )
    ap.add_argument("-u", "--user", default=DEFAULT_USER)
    ap.add_argument("--users-dir", type=Path, default=DEFAULT_USERS_DIR)
    ap.add_argument("--threshold", type=float, default=0.12,
                    help="Cosine threshold for implicit edges (default 0.12)")
    ap.add_argument("--max-edges", type=int, default=5,
                    help="Max implicit edges per node (default 5)")
    ap.add_argument("--json", action="store_true", help="Print full graph JSON to stdout")
    ap.add_argument("--stats", action="store_true", help="Print stats only")
    ap.add_argument("-o", "--output", type=Path, default=None,
                    help="Write graph JSON to file (default: users/<id>/evidence-graph.json)")
    args = ap.parse_args()

    archive_path = args.users_dir / args.user / "self-archive.md"
    if not archive_path.exists():
        print(f"Evidence file not found: {archive_path}", file=sys.stderr)
        return 1

    graph = build_graph(
        archive_path,
        threshold=args.threshold,
        max_edges_per_node=args.max_edges,
    )

    if args.stats:
        print(format_stats(graph))
        return 0

    out_path = args.output or (args.users_dir / args.user / "evidence-graph.json")
    if not args.json:
        out_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {out_path} ({graph['node_count']} nodes, {graph['edge_count']} edges)")
    else:
        print(json.dumps(graph, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
