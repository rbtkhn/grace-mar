#!/usr/bin/env python3
"""Workbench preflight: read-only checks for the Workbench + visualizer pilot chain.

Validates doc paths, visualizer files, committed fixture shape, example workbench
receipts (delegates to validate_workbench_receipt rules), and optionally
``generate_strategy_notebook_visualizer_fixture.py --check``.

Does not read or write users/, recursion-gate, or Record. Does not stage or merge.
Standard library only.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

DOCS_REQUIRED: list[str] = [
    "docs/skill-work/work-dev/workbench/README.md",
    "docs/skill-work/work-dev/workbench/WORKBENCH-RECEIPT-SPEC.md",
    "docs/skill-work/work-dev/workbench/VISUAL-INSPECTION-PROTOCOL.md",
    "docs/skill-work/work-dev/workbench/CANDIDATE-COMPARISON-PROTOCOL.md",
]

VISUALIZER_REQUIRED: list[str] = [
    "docs/skill-work/work-strategy/strategy-notebook/demo-runs/workbench-visualizer/README.md",
    "docs/skill-work/work-strategy/strategy-notebook/demo-runs/workbench-visualizer/GENERATED-FIXTURE.md",
    "docs/skill-work/work-strategy/strategy-notebook/demo-runs/workbench-visualizer/strategy-notebook-visualizer.html",
    "docs/skill-work/work-strategy/strategy-notebook/demo-runs/workbench-visualizer/strategy-notebook-visualizer.fixture.json",
]

EXAMPLES_GLOB = "docs/skill-work/work-dev/workbench/examples"
FIXTURE_REL = (
    "docs/skill-work/work-strategy/strategy-notebook/demo-runs/"
    "workbench-visualizer/strategy-notebook-visualizer.fixture.json"
)
GENERATOR_SCRIPT = "scripts/work_strategy/generate_strategy_notebook_visualizer_fixture.py"


def _load_validate_receipt():
    vpath = REPO_ROOT / "scripts" / "work_dev" / "validate_workbench_receipt.py"
    spec = importlib.util.spec_from_file_location("validate_workbench_receipt", vpath)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {vpath}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.validate_receipt


def check_docs() -> tuple[str, list[str]]:
    """Return (pass|fail, missing paths)."""
    missing: list[str] = []
    for rel in DOCS_REQUIRED:
        p = REPO_ROOT / rel
        if not p.is_file():
            missing.append(rel)
    if missing:
        return "fail", missing
    return "pass", []


def check_visualizer_files() -> tuple[str, list[str]]:
    missing: list[str] = []
    for rel in VISUALIZER_REQUIRED:
        p = REPO_ROOT / rel
        if not p.is_file():
            missing.append(rel)
    if missing:
        return "fail", missing
    return "pass", []


def check_fixture_schema(data: Any) -> tuple[str, list[str]]:
    """Top-level + nodes/edges presence and authority boundaries."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return "fail", ["fixture root is not a JSON object"]
    for k in (
        "schemaVersion",
        "generatedAt",
        "sourceRoot",
        "recordAuthority",
        "gateEffect",
        "truthScope",
        "nodes",
        "edges",
    ):
        if k not in data:
            errors.append(f"fixture missing key: {k!r}")
    if errors:
        return "fail", errors
    if data.get("recordAuthority") != "none":
        errors.append(
            f"recordAuthority must be 'none', got {data.get('recordAuthority')!r}"
        )
    if data.get("gateEffect") != "none":
        errors.append(
            f"gateEffect must be 'none', got {data.get('gateEffect')!r}"
        )
    ts = data.get("truthScope")
    if not isinstance(ts, str) or not str(ts).strip():
        errors.append("truthScope must be a non-empty string")
    nodes = data.get("nodes")
    edges = data.get("edges")
    if not isinstance(nodes, list):
        errors.append("nodes must be a list")
    if not isinstance(edges, list):
        errors.append("edges must be a list")
    if errors:
        return "fail", errors
    return "pass", []


def check_fixture_nodes(data: Any) -> tuple[str, list[str]]:
    """Every node: id, label, kind, path, description, authority work-only."""
    errors: list[str] = []
    nodes = data.get("nodes")
    if not isinstance(nodes, list):
        return "fail", ["nodes is not a list"]
    for i, n in enumerate(nodes):
        if not isinstance(n, dict):
            errors.append(f"node[{i}] is not an object")
            continue
        for k in ("id", "label", "kind", "path", "description", "authority"):
            if k not in n:
                errors.append(f"node[{i}] missing key {k!r} (id={n.get('id')!r})")
        if n.get("authority") != "work-only":
            errors.append(
                f"node[{i}] authority must be 'work-only', got {n.get('authority')!r}"
            )
    if errors:
        return "fail", errors
    return "pass", []


def check_fixture_edges(data: Any) -> tuple[str, list[str], list[str]]:
    """Returns (status pass|warn, edge_errors, edge_warnings for missing id refs)."""
    errors: list[str] = []
    warnings: list[str] = []
    nodes = data.get("nodes")
    edges = data.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        return "pass", ["edges/nodes not validated"], []
    id_set: set[str] = set()
    for n in nodes:
        if isinstance(n, dict) and "id" in n and isinstance(n["id"], str):
            id_set.add(n["id"])
    for i, e in enumerate(edges):
        if not isinstance(e, dict):
            errors.append(f"edge[{i}] is not an object")
            continue
        for k in ("source", "target", "relation"):
            if k not in e:
                errors.append(f"edge[{i}] missing key {k!r}")
        s, t = e.get("source"), e.get("target")
        if isinstance(s, str) and s not in id_set:
            warnings.append(
                f"edge[{i}] source {s!r} is not a known node id"
            )
        if isinstance(t, str) and t not in id_set:
            warnings.append(
                f"edge[{i}] target {t!r} is not a known node id"
            )
    if errors:
        return "fail", errors, []
    if warnings:
        return "warn", [], warnings
    return "pass", [], []


def check_example_receipts(validate_receipt) -> tuple[str, list[str]]:
    """Load docs/.../workbench/examples/*.json; validate workbench receipts."""
    exdir = REPO_ROOT / EXAMPLES_GLOB
    if not exdir.is_dir():
        return "fail", [f"examples directory missing: {EXAMPLES_GLOB}"]
    errors: list[str] = []
    for path in sorted(exdir.glob("*.json")):
        try:
            raw = path.read_text(encoding="utf-8")
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            errors.append(f"{path.relative_to(REPO_ROOT)}: invalid JSON: {e}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{path.relative_to(REPO_ROOT)}: root must be object")
            continue
        if data.get("receiptKind") != "workbench":
            continue
        err = validate_receipt(data)
        for line in err:
            errors.append(f"{path.relative_to(REPO_ROOT)}: {line}")
    if errors:
        return "fail", errors
    return "pass", []


def check_freshness(*, skip: bool) -> tuple[str, int | None, str]:
    """Return (status pass|skip|fail, exit code or None, stderr/stdout tail)."""
    if skip:
        return "skip", None, ""
    gen = REPO_ROOT / GENERATOR_SCRIPT
    if not gen.is_file():
        return "fail", None, f"missing: {GENERATOR_SCRIPT}"
    proc = subprocess.run(
        [sys.executable, str(gen), "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    tail = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        return "pass", 0, tail.strip()[:2000]
    return "fail", proc.returncode, tail.strip()[:4000]


def run_preflight(
    *, strict: bool, skip_freshness: bool, as_json: bool
) -> int:
    validate_receipt = _load_validate_receipt()

    results: dict[str, Any] = {
        "ok": True,
        "docs": "unknown",
        "visualizer_files": "unknown",
        "fixture_schema": "unknown",
        "fixture_graph": "unknown",
        "example_receipts": "unknown",
        "freshness": "unknown",
    }
    all_warnings: list[str] = []
    has_fail = False
    has_warn = False

    dstatus, dmiss = check_docs()
    results["docs"] = dstatus
    results["docs_missing"] = dmiss
    if dstatus == "fail":
        has_fail = True

    vstatus, vmiss = check_visualizer_files()
    results["visualizer_files"] = vstatus
    results["visualizer_missing"] = vmiss
    if vstatus == "fail":
        has_fail = True

    fpath = REPO_ROOT / FIXTURE_REL

    if not fpath.is_file():
        results["fixture_schema"] = "fail"
        results["fixture_error"] = f"missing: {FIXTURE_REL}"
        results["fixture_nodes"] = "fail"
        results["fixture_graph"] = "fail"
        has_fail = True
    else:
        try:
            fdata = json.loads(fpath.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            results["fixture_schema"] = "fail"
            results["fixture_error"] = str(e)
            has_fail = True
        else:
            s1, e1 = check_fixture_schema(fdata)
            results["fixture_schema"] = s1
            if s1 == "fail":
                results["fixture_schema_errors"] = e1
                has_fail = True
            s2, e2 = check_fixture_nodes(fdata)
            results["fixture_nodes"] = s2
            if s2 == "fail":
                results["fixture_node_errors"] = e2
                has_fail = True
            s3, ee, ew = check_fixture_edges(fdata)
            results["fixture_graph"] = s3
            fedge_errs, fedge_warns = ee, ew
            if ee:
                results["fixture_edge_errors"] = ee
                has_fail = True
            if ew:
                results["fixture_edge_warnings"] = ew
                all_warnings.extend(ew)
                has_warn = True
            if s3 == "warn":
                has_warn = True
                if not ee:
                    results["fixture_graph"] = "warn"

    estatus, eerrs = check_example_receipts(validate_receipt)
    results["example_receipts"] = estatus
    if eerrs:
        results["example_receipt_errors"] = eerrs
    if estatus == "fail":
        has_fail = True

    fstat, fcode, ftail = check_freshness(skip=skip_freshness)
    results["freshness"] = fstat
    if fcode is not None:
        results["freshness_exit_code"] = fcode
    if ftail:
        results["freshness_output_tail"] = ftail
    if fstat == "fail":
        has_fail = True

    if strict and has_warn:
        has_fail = True

    results["ok"] = not has_fail
    results["strict"] = strict
    results["warnings"] = all_warnings

    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        def line(label: str, st: str) -> None:
            print(f"  {label:30} {st}")

        print("Workbench preflight")
        print("  " + ("STRICT (warnings fail)" if strict else "normal (warnings do not fail)"))
        line("docs", "PASS" if results["docs"] == "pass" else "FAIL")
        line("visualizer files", "PASS" if results["visualizer_files"] == "pass" else "FAIL")
        fs = results.get("fixture_schema")
        line("fixture schema", "PASS" if fs == "pass" else ("FAIL" if fs == "fail" else "—"))
        fn = results.get("fixture_nodes", "—")
        line("fixture nodes (authority)", "PASS" if fn == "pass" else ("FAIL" if fn == "fail" else "—"))
        fg = results.get("fixture_graph", "—")
        if fg == "warn":
            line("fixture graph (edge → id)", "WARN" if not strict else "FAIL (strict)")
        else:
            line("fixture graph (edge → id)", "PASS" if fg == "pass" else "FAIL")
        line(
            "example receipts",
            "PASS" if results["example_receipts"] == "pass" else "FAIL",
        )
        fr = results["freshness"]
        if fr == "skip":
            line("generated fixture --check", "SKIPPED")
        else:
            line("generated fixture --check", "PASS" if fr == "pass" else "FAIL")
        if all_warnings and not as_json:
            print("  Warnings (edge id refs):")
            for w in all_warnings[:20]:
                print(f"    - {w}")
            if len(all_warnings) > 20:
                print(f"    ... and {len(all_warnings) - 20} more")
        if fstat == "fail" and ftail and not as_json:
            print("  Freshness stderr/stdout (tail):")
            for ln in ftail.splitlines()[:15]:
                print(f"    {ln}")
        if has_fail:
            print("\nRESULT: FAIL")
        else:
            print("\nRESULT: OK")

    return 0 if not has_fail else 1


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--strict",
        action="store_true",
        help="Treat fixture edge id warnings as failures",
    )
    p.add_argument(
        "--skip-freshness",
        action="store_true",
        help="Do not run generate_strategy_notebook_visualizer_fixture.py --check",
    )
    p.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Print machine-readable JSON summary",
    )
    args = p.parse_args()
    return run_preflight(
        strict=args.strict,
        skip_freshness=args.skip_freshness,
        as_json=args.as_json,
    )


if __name__ == "__main__":
    raise SystemExit(main())
