# Workflow depth receipts (Grace-Mar)

**Non-canonical.** Append-only lines in `index.jsonl` record halt/continue decisions for [`build_budgeted_context.py`](../../scripts/prepared_context/build_budgeted_context.py) when `--workflow-depth` is used.

| Path | Role |
|------|------|
| `index.jsonl` | One JSON object per run (gitignored) |

**Override home:** `GRACE_MAR_WORKFLOW_DEPTH_HOME` (default: `runtime/workflow-depth/` under repo root).

**Schema:** [`schema-registry/workflow-depth-receipt.v1.json`](../../schema-registry/workflow-depth-receipt.v1.json)

**Doctrine:** [docs/runtime/context-budgeting.md](../../docs/runtime/context-budgeting.md)

## Implementation audit (v1)

- **Implemented:** Adaptive `--workflow-depth` on `build_budgeted_context.py`; task anchor in markdown + receipt; fixed modes (`shallow`–`exhaustive`) and `auto` with explicit halt reasons; JSONL under this directory.
- **Deferred:** Diminishing-returns guard beyond simple auto heuristics; hybrid_retrieve fusion; routed “specialist” workers.
- **Pipeline:** Prepared-context budget builder only.
- **Governance:** No canonical writes; receipts are not Record; gate discipline unchanged.
