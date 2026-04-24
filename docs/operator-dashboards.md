# Operator dashboards (derived Markdown)

Grace-Mar can emit **compact, regeneratable Markdown “dashboards”** for operator navigation. They borrow the *visibility* idea from Dataview-style vault tools without making the repo an Obsidian-style truth system.

Dashboards are a **stable scripted subclass** of the [Interface Artifact Protocol](skill-work/work-dev/interface-artifacts/README.md): generated operator-facing views that remain **derived** and **non-canonical** even when they become reliable enough to script and regenerate routinely.

## What these are

- **Derived artifacts** under [`artifacts/`](../artifacts/README.md), produced by scripts:
  - `python3 scripts/build_library_index.py` → [`artifacts/library-index.md`](../artifacts/library-index.md)
  - `python3 scripts/build_lane_dashboards.py` → [`artifacts/lane-dashboards/README.md`](../artifacts/lane-dashboards/README.md) (optionally after `python3 scripts/build_work_lanes_dashboard.py` for JSON inputs)
  - `python3 scripts/build_review_dashboard.py` → [`artifacts/review-dashboard.md`](../artifacts/review-dashboard.md)
  - `python3 scripts/build_gate_board.py` → [`artifacts/gate-board.md`](../artifacts/gate-board.md) (Kanban-style; see [gate-board.md](gate-board.md))

## What they are not

- **Not** canonical Record surfaces (not SELF, SELF-LIBRARY, SKILLS, or EVIDENCE).
- **Not** a replacement for [`users/grace-mar/recursion-gate.md`](../users/grace-mar/recursion-gate.md) or structured review-queue JSON — they **summarize** and **link**, they do not hold merge authority.
- **Not** runtime truth — [`runtime/observations/`](../runtime/observations/README.md) remains non-canonical; dashboards may quote it as **hints** only.

## How to regenerate

From repo root (typical order):

```bash
python3 scripts/build_work_lanes_dashboard.py   # optional JSON feed for lane dashboard
python3 scripts/build_library_index.py
python3 scripts/build_lane_dashboards.py
python3 scripts/build_review_dashboard.py
python3 scripts/build_gate_board.py
```

Use `-u grace-mar` where scripts support it (default user is usually `grace-mar`).

**CI:** On push and pull requests to `main`, [`.github/workflows/library-index.yml`](../.github/workflows/library-index.yml) runs `build_library_index.py` and fails if `artifacts/library-index.md` is out of date — regenerate locally and commit with `self-library.md` changes.

## Design notes

- **Library index** parses the `entries:` YAML block in `users/<id>/self-library.md` (first `## Entries` fence); emitted Markdown is **dashboard-ordered** (summary → Start here → recent → compact lanes → appendix full inventory).
- **Review dashboard** uses [`scripts/gate_block_parser.py`](../scripts/gate_block_parser.py) for fenced `### CANDIDATE-*` blocks; pending rows are any block with `status: pending` (even if misplaced relative to `## Processed` — fix the gate file when possible).
- **Lane dashboards** aggregate `runtime/observations/index.jsonl` (when present) and embed or reference `artifacts/work-lanes-dashboard.json`.

See also: [runtime vs Record](runtime-vs-record.md), [claude-surface-contract.md](claude-surface-contract.md) (invocation / mutation language).
