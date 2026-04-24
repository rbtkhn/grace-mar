# Workbench — Strategy notebook visualizer (pilot)

**Status:** **Workbench pilot artifact** (WORK / demo). **Not** the Record, **not** EVIDENCE, **not** a merge path, **not** a gate effect.

**Purpose:** A **static, dependency-free** map of how major strategy-notebook surfaces relate (experts, minds, knots / graph, state threads, watches, compiled views, demo runs, inbox, and key contracts). The browser loads a **pre-built JSON fixture**; it does not walk the tree at runtime. The fixture is **generated** from the live notebook tree (see [GENERATED-FIXTURE.md](GENERATED-FIXTURE.md)). Use it to **see structure** and to practice the Workbench loop: generate → run → inspect → revise → [workbench receipt](../../../../work-dev/workbench/WORKBENCH-RECEIPT-SPEC.md) → operator review.

- **`recordAuthority`:** `none` — the HTML does not assert SELF, EVIDENCE, or external truth.
- **`gateEffect`:** `none` — nothing here stages candidates or merges to the Record.
- **Truth scope:** **Notebook structure and paths only** (plus labels from the fixture). It does not validate strategic claims, wires, or production readiness. Before using this as an **operator demo**, run the [Workbench preflight](../../../../work-dev/workbench/PREFLIGHT.md) (`python3 scripts/work_dev/preflight_workbench.py` from repo root).

**Inspection:** Use [VISUAL-INSPECTION-PROTOCOL.md](../../../../work-dev/workbench/VISUAL-INSPECTION-PROTOCOL.md) in spirit (browser, screenshots optional). For machine validation of receipt JSON, use `scripts/work_dev/validate_workbench_receipt.py`. To author a new receipt: [SCRIPT-USAGE.md](../../../../work-dev/workbench/SCRIPT-USAGE.md) and `new_workbench_receipt.py`.

## Files

| File | Role |
|------|--------|
| [strategy-notebook-visualizer.html](strategy-notebook-visualizer.html) | Single-page UI (fetches the fixture; **requires HTTP** for `fetch`). |
| [strategy-notebook-visualizer.fixture.json](strategy-notebook-visualizer.fixture.json) | Nodes, edges, paths (repo-root-relative), `authority: "work-only"`. Regenerate with the script below. |

## UI affordances

The single-page visualizer (after loading a fixture) includes: **search** (nodes and the edge list); **kind** and **relation** filter chips; a **selected-node** **detail** panel and **copy path**; an **edge** table (source, relation, target) with **unresolved** endpoint highlighting; a compact **adjacency** (hub) view for the selection; a **summary** of counts by kind and relation; **inspection** warnings; and a **Workbench boundary** panel. Use **reset** to clear filters and selection.

## Regenerating the fixture

```bash
python3 scripts/work_strategy/generate_strategy_notebook_visualizer_fixture.py
python3 scripts/work_strategy/generate_strategy_notebook_visualizer_fixture.py --check
```

Details: [GENERATED-FIXTURE.md](GENERATED-FIXTURE.md).

## Launch (from repository root)

Browsers may block `fetch()` when the page is opened as `file://`. Serve this directory, then open the HTML over HTTP:

```bash
python3 -m http.server 8765 --directory docs/skill-work/work-strategy/strategy-notebook/demo-runs/workbench-visualizer
```

Open:

- [http://localhost:8765/strategy-notebook-visualizer.html](http://localhost:8765/strategy-notebook-visualizer.html)

## Suggested Workbench follow-up (operator)

1. Screenshot (optional) under `artifacts/work-dev/workbench-screenshots/` (see that folder’s README).
2. Write a workbench receipt under `artifacts/work-dev/workbench-receipts/` (see [examples](../../../../work-dev/workbench/examples/strategy-notebook-visualizer-workbench-receipt.example.json)) or generate one with the CLI.

---

*Pilot only — derived structure map; not canonical doctrine.*
