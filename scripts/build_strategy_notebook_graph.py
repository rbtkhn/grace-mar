#!/usr/bin/env python3
"""Build a derived JSON graph of strategy pages, experts, and watches (WORK only).

Reads Markdown only. Writes artifacts/work-strategy/strategy-notebook/graph.json
and views under .../views/. See docs/.../GRAPH-SCHEMA.md
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_NOTEBOOK = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
)
DEFAULT_GRAPH = (
    REPO_ROOT
    / "artifacts"
    / "work-strategy"
    / "strategy-notebook"
    / "graph.json"
)
DEFAULT_VIEWS = (
    REPO_ROOT
    / "artifacts"
    / "work-strategy"
    / "strategy-notebook"
    / "views"
)


def _build_graph_data(notebook_dir: Path) -> dict:
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from strategy_page_reader import discover_all_pages

    by_expert = discover_all_pages(notebook_dir)
    nodes: list[dict] = []
    edges: list[dict] = []
    seen_node: set[str] = set()

    def add_node(n: dict) -> None:
        nid = n["id"]
        if nid in seen_node:
            return
        seen_node.add(nid)
        nodes.append(n)

    experts = set()
    watches: set[str] = set()
    for expert_id, pages in by_expert.items():
        experts.add(expert_id)
        for p in pages:
            if p.watch:
                watches.add(p.watch)
            page_nid = f"{expert_id}::{p.id}"
            add_node(
                {
                    "type": "page",
                    "id": page_nid,
                    "page_id": p.id,
                    "expert_id": expert_id,
                    "date": p.date,
                    "watch": p.watch,
                }
            )
            eid = f"expert:{expert_id}"
            add_node({"type": "expert", "id": eid})
            edges.append(
                {
                    "from": page_nid,
                    "to": eid,
                    "type": "belongs_to_expert",
                }
            )
            if p.watch:
                wid = f"watch:{p.watch}"
                add_node({"type": "watch", "id": wid})
                edges.append(
                    {
                        "from": page_nid,
                        "to": wid,
                        "type": "belongs_to_watch",
                    }
                )

    watch_clusters: dict[str, list[str]] = {}
    for expert_id, pages in by_expert.items():
        for p in pages:
            if not p.watch:
                continue
            w = p.watch
            if w not in watch_clusters:
                watch_clusters[w] = []
            if p.id not in watch_clusters[w]:
                watch_clusters[w].append(p.id)
    for w in watch_clusters:
        watch_clusters[w] = sorted(watch_clusters[w])

    page_experts: dict[str, set[str]] = defaultdict(set)
    for expert_id, pages in by_expert.items():
        for p in pages:
            page_experts[p.id].add(expert_id)
    convergence = {
        pid: sorted(eids)
        for pid, eids in page_experts.items()
        if len(eids) > 1
    }

    try:
        nb_dir_display = notebook_dir.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        # Notebook outside repo (e.g. tests) — store absolute path for traceability.
        nb_dir_display = notebook_dir.resolve().as_posix()

    return {
        "schema_version": "1.0.0-strategy-notebook-graph",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "notebook_dir": nb_dir_display,
        "nodes": nodes,
        "edges": edges,
        "_views": {
            "watch_clusters": watch_clusters,
            "expert_convergence": convergence,
        },
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--notebook-dir", type=Path, default=DEFAULT_NOTEBOOK)
    p.add_argument("--out", type=Path, default=DEFAULT_GRAPH, help="graph.json path")
    p.add_argument(
        "--views-dir",
        type=Path,
        default=DEFAULT_VIEWS,
        help="Directory for watch-clusters.json and expert-convergence.json",
    )
    args = p.parse_args()
    nb = args.notebook_dir.resolve()
    if not nb.is_dir():
        print(f"error: notebook-dir not found: {nb}", flush=True)
        return 1

    data = _build_graph_data(nb)
    views = data.pop("_views")
    out = args.out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    vdir = args.views_dir.resolve()
    vdir.mkdir(parents=True, exist_ok=True)
    (vdir / "watch-clusters.json").write_text(
        json.dumps(views["watch_clusters"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (vdir / "expert-convergence.json").write_text(
        json.dumps(views["expert_convergence"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    def _print_rel(path: Path) -> None:
        try:
            print(str(path.relative_to(REPO_ROOT)))
        except ValueError:
            print(str(path))

    _print_rel(out)
    _print_rel(vdir / "watch-clusters.json")
    _print_rel(vdir / "expert-convergence.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
