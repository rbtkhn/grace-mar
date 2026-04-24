#!/usr/bin/env python3
"""Generate the strategy-notebook workbench visualizer fixture from the live tree.

Writes JSON consumed by
docs/skill-work/work-strategy/strategy-notebook/demo-runs/workbench-visualizer/
strategy-notebook-visualizer.html (nodes + edges only; extra top-level keys are ignored by the UI).

WORK only. Does not touch Record, gate, or users/ paths.

Usage (repo root):
  python3 scripts/work_strategy/generate_strategy_notebook_visualizer_fixture.py
  python3 scripts/work_strategy/generate_strategy_notebook_visualizer_fixture.py --check
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

DEFAULT_NOTEBOOK = "docs/skill-work/work-strategy/strategy-notebook"
DEFAULT_OUT = (
    "docs/skill-work/work-strategy/strategy-notebook/demo-runs/"
    "workbench-visualizer/strategy-notebook-visualizer.fixture.json"
)

SCHEMA_VERSION = "strategy-notebook-visualizer-fixture/v1"


def _to_repo_rel(p: Path, *, repo_root: Path) -> str:
    return p.resolve().relative_to(repo_root).as_posix()


def _slugify_for_id(raw: str) -> str:
    s = raw.lower().replace("\\", "/")
    s = re.sub(r"[^a-z0-9/_.-]+", "-", s)
    s = s.replace("/", "-").replace(".md", "")
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "x"


def knot_id_from_path(repo_rel_path: str) -> str:
    return f"knot-{_slugify_for_id(repo_rel_path)}"


def _try_yaml_load(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.is_file():
        return None, f"missing file: {path}"
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError as e:
        return None, f"PyYAML not available: {e}"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return None, f"parse error: {e}"
    if not isinstance(data, dict):
        return None, "root is not a mapping"
    return data, None


def _build_fixture(*, repo_root: Path, notebook_rel: str) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    nb = (repo_root / notebook_rel).resolve()
    if not nb.is_dir():
        raise SystemExit(f"error: not a directory: {nb}")

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []

    def add_node(
        node_id: str,
        label: str,
        kind: str,
        relpath: str,
        description: str,
    ) -> None:
        nodes.append(
            {
                "id": node_id,
                "label": label,
                "kind": kind,
                "path": relpath,
                "description": description,
                "authority": "work-only",
            }
        )

    def add_edge(source: str, target: str, relation: str) -> None:
        edges.append({"source": source, "target": target, "relation": relation})

    # --- Baseline (required) nodes ---
    base: list[tuple[str, str, str, str, str]] = [
        (
            "strategy-notebook",
            "Strategy Notebook",
            "hub",
            f"{notebook_rel}/README.md",
            "Root of the work-strategy strategy-notebook tree.",
        ),
        (
            "experts",
            "Experts",
            "area",
            f"{notebook_rel}/experts/",
            "Per-expert threads, profiles, and strategy-page units.",
        ),
        (
            "minds",
            "Minds",
            "area",
            f"{notebook_rel}/minds/",
            "Lens files for tri-frame / voice work.",
        ),
        (
            "watches",
            "Watches",
            "area",
            f"{notebook_rel}/watches/",
            "Evolving situation hooks and watch surfaces.",
        ),
        (
            "compiled-views",
            "Compiled views",
            "area",
            f"{notebook_rel}/compiled-views/",
            "Polyphony and compiled orientation outputs.",
        ),
        (
            "demo-runs",
            "Demo runs",
            "area",
            f"{notebook_rel}/demo-runs/",
            "Exercises, rubrics, and the workbench visualizer folder.",
        ),
        (
            "daily-strategy-inbox",
            "Daily strategy inbox",
            "inbox",
            f"{notebook_rel}/daily-strategy-inbox.md",
            "Accumulator for ingest cadence and weave lines.",
        ),
        (
            "knot-index",
            "knot-index.yaml",
            "data",
            f"{notebook_rel}/knot-index.yaml",
            "Machine-readable knot inventory (legacy; may be empty).",
        ),
        (
            "knot-connections",
            "knot-connections.yaml",
            "data",
            f"{notebook_rel}/knot-connections.yaml",
            "Governed edge layer between knot paths (may be empty).",
        ),
        (
            "graph-schema",
            "GRAPH-SCHEMA",
            "contract",
            f"{notebook_rel}/GRAPH-SCHEMA.md",
            "Graph and knot vocabulary.",
        ),
        (
            "page-contract",
            "PAGE-CONTRACT",
            "contract",
            f"{notebook_rel}/PAGE-CONTRACT.md",
            "Page-in-thread link contract.",
        ),
        (
            "trace-contract",
            "STRATEGY-NOTEBOOK-TRACE-CONTRACT",
            "contract",
            f"{notebook_rel}/STRATEGY-NOTEBOOK-TRACE-CONTRACT.md",
            "Trace / JSONL contract for tools.",
        ),
        (
            "synthesis-operating-model",
            "SYNTHESIS-OPERATING-MODEL",
            "protocol",
            f"{notebook_rel}/SYNTHESIS-OPERATING-MODEL.md",
            "L0–L4 stack and session types.",
        ),
        (
            "eod-mcq-protocol",
            "EOD-MCQ-PROTOCOL",
            "protocol",
            f"{notebook_rel}/EOD-MCQ-PROTOCOL.md",
            "Optional decision-first EOD menu.",
        ),
        (
            "strategy-state-iran",
            "State thread — Iran",
            "state-thread",
            f"{notebook_rel}/strategy-state-iran/README.md",
            "Institution-centric parallel lane (channels, weave, clusters).",
        ),
    ]
    for row in base:
        add_node(*row)

    # --- Baseline edges (required) ---
    for child in (
        "experts",
        "minds",
        "watches",
        "compiled-views",
        "demo-runs",
        "daily-strategy-inbox",
        "knot-index",
        "knot-connections",
        "graph-schema",
        "page-contract",
        "trace-contract",
        "synthesis-operating-model",
        "eod-mcq-protocol",
        "strategy-state-iran",
    ):
        add_edge("strategy-notebook", child, "contains")
    add_edge("knot-index", "knot-connections", "serializes_to")
    add_edge("graph-schema", "knot-connections", "informs")
    add_edge("page-contract", "compiled-views", "constrains_inputs_to")
    add_edge("trace-contract", "compiled-views", "constrains_outputs_from")
    add_edge("eod-mcq-protocol", "synthesis-operating-model", "optional_preface_to")

    # --- experts/ ---
    experts_dir = nb / "experts"
    if experts_dir.is_dir():
        for child in sorted(experts_dir.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            eid = f"expert-{_slugify_for_id(child.name)}"
            rp = _to_repo_rel(child, repo_root=repo_root)
            add_node(
                eid,
                child.name,
                "expert",
                rp if rp.endswith("/") else rp + "/",
                f"Expert lane ({child.name}).",
            )
            add_edge("experts", eid, "contains")
    else:
        warnings.append("experts/ missing; skipped")

    # --- minds/ (top-level .md and subdirs) ---
    minds_dir = nb / "minds"
    if minds_dir.is_dir():
        for child in sorted(minds_dir.iterdir()):
            if child.name.startswith("."):
                continue
            if child.is_file() and child.suffix.lower() == ".md":
                mid = f"mind-{_slugify_for_id(child.stem)}"
                rp = _to_repo_rel(child, repo_root=repo_root)
                add_node(mid, child.stem, "mind", rp, "Mind / lens file.")
                add_edge("minds", mid, "contains")
            elif child.is_dir():
                mid = f"mind-{_slugify_for_id(child.name)}"
                rp = _to_repo_rel(child, repo_root=repo_root)
                add_node(
                    mid, child.name, "mind", rp + "/", "Mind / lens subtree."
                )
                add_edge("minds", mid, "contains")
    else:
        warnings.append("minds/ missing; skipped")

    # --- watches/ ---
    wdir = nb / "watches"
    if wdir.is_dir():
        for child in sorted(wdir.iterdir()):
            if child.name.startswith("."):
                continue
            if child.is_file() and child.suffix.lower() == ".md":
                wid = f"watch-{_slugify_for_id(child.stem)}"
                rp = _to_repo_rel(child, repo_root=repo_root)
                add_node(wid, child.stem, "watch", rp, "Watch file.")
                add_edge("watches", wid, "contains")
            elif child.is_dir():
                wid = f"watch-{_slugify_for_id(child.name)}"
                rp = _to_repo_rel(child, repo_root=repo_root)
                add_node(
                    wid, child.name, "watch", rp + "/", "Watch subtree."
                )
                add_edge("watches", wid, "contains")
    else:
        warnings.append("watches/ missing; skipped")

    # --- strategy-state-iran/ children (voices, chapters, iri-institutional, daily) ---
    ssi = nb / "strategy-state-iran"
    if ssi.is_dir():
        for name, rel_suffix, desc in (
            ("voices", "voices/", "Institutional / expert voices under Iran lane."),
            ("chapters", "chapters/", "Month chapters and days."),
        ):
            p = ssi / name
            if p.is_dir():
                cid = f"strategy-state-iran-{name}"
                rp = _to_repo_rel(p, repo_root=repo_root)
                add_node(
                    cid, name, "state-thread", rp + "/", desc
                )
                add_edge("strategy-state-iran", cid, "contains")
        iri = ssi / "voices" / "iri-institutional"
        if iri.exists():
            cid = "strategy-state-iran-iri-institutional"
            rp = _to_repo_rel(iri, repo_root=repo_root)
            if iri.is_dir() and not rp.endswith("/"):
                rp = rp + "/"
            add_node(
                cid,
                "iri-institutional",
                "state-thread",
                rp,
                "IRI institutional voice (under voices).",
            )
            add_edge("strategy-state-iran", cid, "contains")
        # nested daily: first .../daily directory found
        for daily in sorted(ssi.glob("chapters/**/daily")):
            if daily.is_dir():
                cid = "strategy-state-iran-daily"
                rp = _to_repo_rel(daily, repo_root=repo_root)
                add_node(
                    cid,
                    "daily (chapters/…/daily)",
                    "state-thread",
                    rp + "/",
                    "Day-scale files under a chapter month.",
                )
                add_edge("strategy-state-iran", cid, "contains")
                break
    else:
        warnings.append("strategy-state-iran/ missing; skipped")

    # --- knot-index.yaml ---
    knot_path_to_id: dict[str, str] = {}
    kidx = nb / "knot-index.yaml"
    kdata, kerr = _try_yaml_load(kidx)
    if kerr:
        warnings.append(f"knot-index: {kerr}")
    elif kdata is not None:
        rows = kdata.get("knots")
        if not isinstance(rows, list):
            warnings.append("knot-index: knots is not a list; skipped")
        else:
            for i, row in enumerate(rows):
                if not isinstance(row, dict) or "path" not in row:
                    continue
                rp = str(row["path"]).replace("\\", "/")
                kid = knot_id_from_path(rp)
                if kid in (n["id"] for n in nodes):
                    kid = f"{kid}-{i}"
                parts: list[str] = []
                if "date" in row:
                    parts.append(f"date: {row['date']}")
                for key in ("clusters", "patterns"):
                    v = row.get(key)
                    if v:
                        parts.append(f"{key}: {v}")
                if "note" in row and row["note"]:
                    parts.append(f"note: {row['note']}")
                label = str(row.get("knot_label") or Path(rp).name)
                add_node(
                    kid,
                    label,
                    "knot",
                    rp,
                    "; ".join(parts) if parts else f"Knot file ({rp}).",
                )
                add_edge("knot-index", kid, "indexes")
                knot_path_to_id[rp] = kid

    # --- knot-connections.yaml ---
    kc_path = nb / "knot-connections.yaml"
    kc_data, kcerr = _try_yaml_load(kc_path)
    connections_unparsed = False
    if kcerr:
        warnings.append(f"knot-connections: {kcerr}")
        connections_unparsed = True
    elif kc_data is not None:
        conns = kc_data.get("connections")
        if conns is None:
            connections_unparsed = True
        elif not isinstance(conns, list):
            connections_unparsed = True
        else:
            for row in conns:
                if not isinstance(row, dict):
                    continue
                fr = row.get("from")
                to = row.get("to")
                rel = row.get("relation", "relates")
                if not fr or not to:
                    warnings.append("knot-connections: row missing from/to; skipped")
                    continue
                f = str(fr).replace("\\", "/")
                t = str(to).replace("\\", "/")
                sid = knot_path_to_id.get(f) or knot_id_from_path(f)
                tid = knot_path_to_id.get(t) or knot_id_from_path(t)
                # ensure nodes exist for orphan paths
                for pid, iid, label in (
                    (f, sid, f),
                    (t, tid, t),
                ):
                    if not any(n["id"] == iid for n in nodes):
                        add_node(
                            iid,
                            Path(label).name,
                            "knot",
                            pid,
                            "Referenced by knot-connections; not in knot-index.",
                        )
                add_edge(sid, tid, str(rel))
    if connections_unparsed:
        add_node(
            "knot-connections-unparsed",
            "knot-connections (unparsed)",
            "parser-warning",
            f"{notebook_rel}/knot-connections.yaml",
            "knot-connections.yaml present but shape was not parsed (PyYAML or schema).",
        )
        add_edge("knot-connections", "knot-connections-unparsed", "warns")

    nodes.sort(key=lambda x: x["id"])
    edges.sort(key=lambda x: (x["source"], x["target"], x["relation"]))

    doc: dict[str, Any] = {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "sourceRoot": notebook_rel,
        "recordAuthority": "none",
        "gateEffect": "none",
        "truthScope": "derived structure visualization only",
        "nodes": nodes,
        "edges": edges,
    }
    return doc, warnings


def _normalize_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _write_json(
    data: Any, path: Path, *, pretty: bool
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if pretty:
        text = json.dumps(
            data, ensure_ascii=False, indent=2, sort_keys=True
        ) + "\n"
    else:
        text = json.dumps(
            data, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ) + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--notebook-root",
        default=DEFAULT_NOTEBOOK,
        help="Path relative to repository root (default: %(default)s)",
    )
    p.add_argument(
        "--output",
        "-o",
        default=DEFAULT_OUT,
        help="Output JSON path relative to repository root (default: %(default)s)",
    )
    p.add_argument(
        "--no-pretty",
        action="store_true",
        help="Write compact one-line JSON (default is pretty-printed).",
    )
    p.add_argument(
        "--check",
        action="store_true",
        help="Do not write; exit 0 if file matches generated output, else 1.",
    )
    args = p.parse_args()

    nb_rel = str(Path(args.notebook_root).as_posix()).strip().strip("/")
    out = Path(args.output)
    if not out.is_absolute():
        out = REPO_ROOT / out

    doc, warnings = _build_fixture(repo_root=REPO_ROOT, notebook_rel=nb_rel)
    n_nodes, n_edges = len(doc["nodes"]), len(doc["edges"])

    if args.check:
        if not out.is_file():
            print(f"check: output missing: {out}", file=sys.stderr)
            print(
                f"would generate: nodes={n_nodes} edges={n_edges}",
                file=sys.stderr,
            )
            for w in warnings:
                print(f"warning: {w}", file=sys.stderr)
            return 1
        existing = json.loads(out.read_text(encoding="utf-8"))
        # Time-only drift: align generatedAt to on-disk so --check is stable
        # across runs; structure/node changes still fail the compare.
        comp_doc = copy.deepcopy(doc)
        if (
            isinstance(existing, dict)
            and isinstance(comp_doc, dict)
            and "generatedAt" in existing
        ):
            comp_doc["generatedAt"] = existing["generatedAt"]
        a = _normalize_json(comp_doc)
        b = _normalize_json(existing)
        if a == b:
            print(
                f"ok: fixture up to date ({n_nodes} nodes, {n_edges} edges, "
                f"{len(warnings)} warnings)"
            )
            for w in warnings:
                print(f"warning: {w}")
            return 0
        print("check: fixture would change", file=sys.stderr)
        old_ids = {n["id"] for n in existing.get("nodes", []) if isinstance(n, dict)}
        new_ids = {n["id"] for n in doc["nodes"] if isinstance(n, dict)}
        print(
            f"  nodes: was {len(old_ids)} now {len(new_ids)}; "
            f"+{len(new_ids - old_ids)} -{len(old_ids - new_ids)}",
            file=sys.stderr,
        )
        if new_ids - old_ids:
            print(
                f"  new ids: {sorted(new_ids - old_ids)[:30]!r}…",
                file=sys.stderr,
            )
        if old_ids - new_ids:
            print(
                f"  removed: {sorted(old_ids - new_ids)[:30]!r}…",
                file=sys.stderr,
            )
        for w in warnings:
            print(f"warning: {w}", file=sys.stderr)
        return 1

    _write_json(doc, out, pretty=not args.no_pretty)
    print(
        f"Wrote fixture: {out} (nodes: {n_nodes}, edges: {n_edges}, "
        f"warnings: {len(warnings)})"
    )
    for w in warnings:
        print(f"warning: {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
