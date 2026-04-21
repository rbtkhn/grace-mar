# Context efficiency (workflow observability)

This document complements [workflow-observability.md](workflow-observability.md) and [runtime/context-budgeting.md](runtime/context-budgeting.md).

## Role

- Describes **how to interpret** token and retrieval-miss metrics emitted by batch scripts.
- **Does not** set policy or override context budgets in `config/context_budgets/`.

## Honest labeling

Many metrics are **inferred** or **partial**:

- `contextTokensLoaded` appears on workflow events only when upstream tools record it.
- **Compression rate** and **prepared-context reuse** require instrumentation not always present in v1—reports may show `null`.

When `partialMetrics` or `inferredPartial` is true, treat numbers as **directional**, not accounting-grade.

## Commands

```bash
python3 scripts/build_context_efficiency_report.py --repo-root .
```

Output: `artifacts/workflow-observability/context-efficiency-report.json` (+ `.md`).

## Governance

Inspection only; no Record writes; no merge authority.
