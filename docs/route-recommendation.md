# Route Recommendation Receipt

A **small advisory helper**: given a plain-language task description, emit a compact **markdown receipt** with a heuristic task shape (coding, synthesis, recurring workflow, harness/gate-ish work, unclear) and pointers into existing Grace-Mar lanes—not a runner, not orchestration.

## What it is

- **Script:** [`scripts/recommend_route.py`](../scripts/recommend_route.py)
- **Config:** [`config/route_recommendation.json`](../config/route_recommendation.json) — human-editable keywords and path blurbs only
- **Outputs:** Derived files under [`artifacts/route-recommendations/`](../artifacts/route-recommendations/README.md) (default; git ignores per-receipt blobs like other advisory buckets)

## What it is not

- Not a worker architecture, MCP router, or replacement for [`scripts/runtime/worker_router.py`](runtime-worker.md).
- Not a governance authority: it does **not** stage `CANDIDATE-*`, merge into [SELF](../AGENTS.md), or bypass companion review.
- Not the same taxonomy as [**work-strategy task-shape classification**](skill-work/work-strategy/task-shape-routing.md) (`notebook_synthesis`, `watch_update`, …). That lane uses [`scripts/work_strategy/classify_task_shape.py`](../scripts/work_strategy/classify_task_shape.py) + [`config/work_strategy_task_shapes.yaml`](../config/work_strategy_task_shapes.yaml) for **strategy carry harness** JSON. Use whichever tool matches your question (“which strategy job kind?” vs “which coarse repo lane / governance posture?”).

## When to use

- Cold-thread triage inside Cursor before choosing operator lane prefixes ([`docs/operator-agent-lanes.md`](operator-agent-lanes.md)).
- Quick “does this imply gate work?” sniff test when wording is muddy (receipt echoes [`AGENTS.md`](../AGENTS.md) norms; **you** still judge).

## How to run

```bash
python3 scripts/recommend_route.py \
  -t "Read sources and draft memo for inbox" \
  [--lane-hint work-strategy] \
  [--stdout] [--no-write]
```

Writes `artifacts/route-recommendations/YYYY-MM-DD/<HHMMSS>-<slug>.md` unless `--no-write`; print only with `--stdout` (combine with `--no-write` to avoid cluttering disk).

## Governance & Record boundary

- Receipts sit in **artifacts** ([`docs/runtime-vs-record.md`](runtime-vs-record.md)); they are advisory and disposable.
- `requires_gate_review: true` in the YAML means “this task shape usually touches governed surfaces — confirm”; it is **not** automatic approval.
- Forbidden output paths reuse the same **`users/`** prohibition as harness scripts (see [`scripts/work_strategy/packet_common.py`](../scripts/work_strategy/packet_common.py)).

---

## Implementation report (2026)

### What was added

- `scripts/recommend_route.py` — keyword scoring, optional lane-hint bonus, markdown receipt render, CLI.
- `config/route_recommendation.json` — six coarse shapes + suggested next steps.
- `artifacts/route-recommendations/` — README + `.gitkeep`; `.gitignore` ignores generated `*.md` receipts.
- `tests/test_recommend_route.py` — classification, unclear fallback, render, forbidden path, lane bonus.
- `docs/route-recommendation.md` (this page) plus `artifacts/README.md` row and registry pointer.

### Why it is not redundant

- Differs from **strategy task-shape routing** (`classify_task_shape`) in goal and taxonomy: **cross-repo lane compass** vs **strategy harness job classifier**.
- Differs from **worker router** runtime: no queues, traces, or execution hooks—only on-demand markdown receipts.

### Deliberately left out

- No LLM/embeddings scoring, regen harness hook in `regenerate_all_derived.py`, or integration into MCP manifests.
- No JSON schema/registry entry requirement beyond normal docs upkeep.

### Fit with Grace-Mar patterns

- **Derived artifact** discipline ([`artifacts/README.md`](../artifacts/README.md)).
- **Operator lane prefixes** documented separately; receipts **recommend**, never EXECUTE automatically.
- **Gate semantics** delegated to canonical [`users/<id>/recursion-gate.md`](../users/grace-mar/recursion-gate.md) flows.
