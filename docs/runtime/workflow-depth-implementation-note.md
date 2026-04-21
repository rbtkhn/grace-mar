# Workflow depth routing contract — implementation note

## What was added

- **Doctrine:** [workflow-depth-contract.md](workflow-depth-contract.md) — shared inputs/outputs, governance boundaries.
- **Library:** [`src/grace_mar/runtime/workflow_depth.py`](../../src/grace_mar/runtime/workflow_depth.py) — depth→budget mapping, decision helpers, append-only receipt builder.
- **Schema:** [`schema-registry/workflow-depth-decision.v1.json`](../../schema-registry/workflow-depth-decision.v1.json); enriched [`schema-registry/workflow-depth-receipt.v1.json`](../../schema-registry/workflow-depth-receipt.v1.json).
- **Scripts:** [`scripts/build_workflow_depth_report.py`](../../scripts/build_workflow_depth_report.py), [`scripts/build_workflow_depth_hints.py`](../../scripts/build_workflow_depth_hints.py).
- **Docs:** [workflow-depth-audit.md](workflow-depth-audit.md), [worker-candidates.md](worker-candidates.md).

## What was preserved

- [`scripts/prepared_context/build_budgeted_context.py`](../../scripts/prepared_context/build_budgeted_context.py) CLI: `--workflow-depth` / `--depth`, `--task-anchor` required with depth, `--mode` ignored when depth is set, append-only JSONL receipts.
- [`scripts/prepared_context/workflow_depth_control.py`](../../scripts/prepared_context/workflow_depth_control.py) **auto** heuristics unchanged in behavior; fixed depth mapping now delegates to `grace_mar.runtime.workflow_depth.fixed_depth_to_budget_and_max_obs`.
- Review orchestrator remains read-only; **`--context-mode`** suggestions unchanged when **`--workflow-depth`** is not used.

## Paths

| Artifact | Location |
|----------|----------|
| Workflow depth receipts | `runtime/workflow-depth/index.jsonl` or `GRACE_MAR_WORKFLOW_DEPTH_HOME` |
| Budget build sidecar | `prepared-context/last-budget-builds.json` |
| Audit JSON / hints | `artifacts/workflow-depth/` (default for report script) |

## Intentionally narrow

- No daemon, no DB, no worker router.
- `sourceWorkflow` tagging via optional `--source-workflow` on prepared context (e.g. `memory_brief`).
- Audit metrics are **batch** and **heuristic**; low-`n` sections flagged as partial.

## Suggested commit grouping (8)

1. `docs(schema): workflow-depth contract + decision schema`
2. `feat(runtime): grace_mar.runtime.workflow_depth + build_budgeted_context refactor`
3. `feat(runtime): memory_brief workflow-depth passthrough`
4. `feat(runtime): review_orchestrator workflow-depth suggestions`
5. `feat(schema): workflow-depth receipt enrichment`
6. `feat(runtime): workflow depth audit report + doc`
7. `feat(runtime): workflow depth hints script`
8. `docs(runtime): worker candidates + implementation note`
