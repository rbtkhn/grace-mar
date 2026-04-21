# Workflow observability (v1)

**Workflow observability** is an **inspection layer** over receipts, runtime traces, prepared-context outputs, review artifacts, validators, and lane-specific observability JSON. It answers **workflow-shaped** questions—which flows are effective, expensive, stale, or high-friction—not only “what proposals exist.”

This document **extends** [observability.md](observability.md); it does not replace proposal-centric observability or the Change Proposal pipeline.

## Principles (governance-aligned)

| Rule | Meaning |
|------|---------|
| **Inspection, not approval** | Metrics and reports do not merge the Record or approve gate candidates. |
| **No silent mutation** | Batch scripts emit JSON/Markdown under `artifacts/` or gitignored `runtime/` paths only. |
| **Additive** | Existing observability scripts and schemas remain; workflow events **compose** on top. |
| **Honest uncertainty** | Partial or inferred metrics are labeled (`partialConfidence`, `partialMetrics` on reports). |

## What it measures

- **Workflows** (normalized **events**) with lane, phase, status, and optional cost/review fields.
- **Rollups** (aggregate **reports**) by `workflowType` and `lane`, plus friction and leverage hints.

## Doc hierarchy

1. [observability.md](observability.md) — umbrella: inspection vs Record, proposal queue contract.
2. **This page** — workflow-level events and batch reports.
3. [context-efficiency.md](context-efficiency.md) — token/compression/miss heuristics (drill-down).

## Artifacts (v1)

| Artifact | Role |
|----------|------|
| [`schema-registry/workflow-observability-event.v1.json`](../schema-registry/workflow-observability-event.v1.json) | Event JSON shape. |
| [`schema-registry/workflow-observability-report.v1.json`](../schema-registry/workflow-observability-report.v1.json) | Aggregate report shape. |
| `scripts/emit_workflow_event.py` | Batch: scan sources → normalized events (JSONL). |
| `scripts/build_workflow_observability.py` | Aggregate report from events. |
| `scripts/build_review_friction_report.py` | Friction-focused JSON/MD. |
| `scripts/build_context_efficiency_report.py` | Context-efficiency JSON/MD. |
| `scripts/build_workflow_observability_summary.py` | Operator-facing compact MD. |
| `artifacts/workflow-observability/` | Default committed-friendly report outputs (policy: regenerate via scripts). |
| `runtime/observability/workflow-events/` | Local normalized events (gitignored); includes `batchId` for idempotent batch runs. |

## Commands (typical)

```bash
python3 scripts/emit_workflow_event.py --repo-root .
python3 scripts/build_workflow_observability.py --repo-root .
python3 scripts/build_review_friction_report.py --repo-root .
python3 scripts/build_context_efficiency_report.py --repo-root .
python3 scripts/build_workflow_observability_summary.py --repo-root .
```

## See also

- [workflow-observability-thresholds.md](workflow-observability-thresholds.md) — human guidance thresholds (not automation).
- [runtime/context-budgeting.md](runtime/context-budgeting.md) — context policy context.
- [observability.md](observability.md) — proposal observability.

---

Companion-Self template · Workflow observability v1
