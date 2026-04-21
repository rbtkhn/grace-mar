# Workflow depth audit (batch)

**Workflow depth** receipts are append-only runtime lines under `runtime/workflow-depth/index.jsonl` (or `GRACE_MAR_WORKFLOW_DEPTH_HOME`). This page describes the **batch aggregate** script that turns those lines into a single JSON report for operator tuning.

## What this is

- **Inspection / weather** — frequency by lane and depth, approximate `auto` escalation rate, `sourceWorkflow` mix, shallow churn heuristics.
- **Not** approval, not merge signal, not a substitute for gate review.

## Commands

```bash
python3 scripts/build_workflow_depth_report.py --repo-root .
```

Default JSON output: `artifacts/workflow-depth/workflow-depth-report.json`

Optional Markdown summary:

```bash
python3 scripts/build_workflow_depth_report.py --repo-root . --markdown artifacts/workflow-depth/workflow-depth-audit-summary.md
```

Operator hints (from the JSON report):

```bash
python3 scripts/build_workflow_depth_hints.py --report artifacts/workflow-depth/workflow-depth-report.json -o artifacts/workflow-depth/workflow-depth-hints.md
```

## Missing or partial data

If the JSONL file is absent or empty, the report still writes with **`receiptCount`: 0** and **`partialMetrics`: true**. Do not treat low-`n` aggregates as stable policy.

## See also

- [workflow-depth-contract.md](workflow-depth-contract.md)
- [workflow-depth.md](workflow-depth.md)
