# Context Failure Diagnostics Clinic

The Context Failure Diagnostics Clinic is a local diagnostic tool for identifying context, retrieval, routing, compression, and grounding failures in Grace-Mar workflows.

It does not call an LLM. It does not mutate Record surfaces. It does not approve or merge candidates.

## Purpose

Grace-Mar has many context-bearing surfaces:

- canonical Record surfaces;
- runtime memory;
- prepared context;
- work lanes;
- strategy notebooks;
- expert threads;
- evidence logs;
- dashboards;
- derived artifacts;
- review queues.

As the system grows, failures are often not reasoning failures. They are context failures:

```text
wrong source → wrong route → wrong authority → wrong synthesis
```

This clinic helps identify those failures before they become durable state.

## Diagnostic categories

| Category | Meaning |
|----------|---------|
| `surface_confusion` | Runtime/work/derived material is treated as canonical. |
| `stale_context` | Old context is used without freshness warning. |
| `missing_evidence` | Claims lack source, receipt, input path, or warrant. |
| `compression_loss` | Summary or compressed context drops required anchors. |
| `lane_misrouting` | Work is routed to the wrong lane or notebook. |
| `authority_drift` | Output claims approval, merge, or canonical authority it does not have. |
| `synthesis_overreach` | Ambiguous evidence is collapsed into a stronger conclusion than warranted. |

## When to use

Use this clinic after:

- a retrieval failure;
- a bad answer caused by stale context;
- a prepared-context compression mistake;
- an expert-thread update that missed raw input;
- a dashboard/report that seems too confident;
- a candidate that may have crossed from advisory work into canonical-state claims.

## Basic command

From the repository root:

```bash
python3 scripts/runtime/context_failure_clinic.py \
  --input artifacts/example-context-output.md \
  --out artifacts/context-failure-reports/example-context-failure.json \
  --markdown artifacts/context-failure-reports/example-context-failure.md
```

JSON output conforms to [`schemas/context-failure-report.v1.schema.json`](../../schemas/context-failure-report.v1.schema.json).

## Governance rule

All reports are **derived artifacts**. A diagnostic report may recommend review, rerouting, or restaging, but it may not directly alter canonical state.

## See also

- [`scripts/runtime/context_failure_clinic.py`](../../scripts/runtime/context_failure_clinic.py)
