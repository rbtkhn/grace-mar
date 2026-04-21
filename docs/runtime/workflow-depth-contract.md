# Workflow depth routing contract

This document defines the **shared runtime contract** for **workflow depth** in Grace-Mar: a small routing membrane that maps operator intent to **budget class** and **bounded retrieval** behavior before packing prepared context or related runtime follow-ons.

It extends the narrative in [workflow-depth.md](workflow-depth.md) and the budget doctrine in [context-budgeting.md](context-budgeting.md). It does **not** replace them.

## What this is

- A **runtime efficiency and repeatability** tool: same knobs produce comparable packs and receipts across scripts.
- **Additive** to existing CLIs; legacy flags keep working.

## What this is not

- **Not** a second governance layer. Depth does not approve, merge, or rank gate truth.
- **Not** a determination of factual truth — it only shapes **how much** context is assembled under a budget.
- **Does not** bypass [abstention policy](../abstention-policy.md), retrieval doctrine, or companion gate review.
- **Not** Record truth — receipts under `runtime/workflow-depth/` are **runtime weather** (inspection and tuning), not SELF or EVIDENCE.

## Canonical depth values

| Depth | Maps to budget class | Notes |
|-------|------------------------|--------|
| `shallow` | `compact` | Cheapest pass; default max observation candidates unless overridden. |
| `normal` | `medium` | Standard operator path. |
| `deep` | `deep` | Broader excerpts. |
| `exhaustive` | `deep` | Same class as deep with a **higher** observation candidate cap (bounded). |
| `auto` | resolved `compact` / `medium` / `deep` | Compact dry-pack, metrics, optional escalation; halt/continue heuristics. |

## Shared inputs (conceptual)

- **lane** — work lane string (exact match against budget tables).
- **task anchor** — operator problem statement (required whenever depth is set for prepared context and aligned scripts).
- **constraint** — optional scope/abstention line.
- **operator override** — when true, depth was explicitly chosen over a default (receipt field; scripts set when applicable).

## Shared outputs (conceptual)

- **initial depth** — what was requested (`shallow` … `auto`).
- **final depth** — resolved label: for fixed presets, same as initial; for `auto`, the effective pack depth (`compact` / `medium` / `deep`).
- **budget class** — `compact` | `medium` | `deep` used for character budget and formatting.
- **escalation** — whether `auto` (or similar) increased depth vs a compact-only stop.
- **rationale / halt reason** — human-legible stop or veto strings (heuristic; not approval).

Machine-readable shape: [workflow-depth-decision.v1.json](../../schema-registry/workflow-depth-decision.v1.json).

## Implementations

- Library: [`src/grace_mar/runtime/workflow_depth.py`](../../src/grace_mar/runtime/workflow_depth.py)
- Prepared context: [`scripts/prepared_context/build_budgeted_context.py`](../../scripts/prepared_context/build_budgeted_context.py)
- Memory brief (optional follow-on): [`scripts/runtime/memory_brief.py`](../../scripts/runtime/memory_brief.py)
- Review orchestrator (suggested commands only): [`scripts/runtime/review_orchestrator.py`](../../scripts/runtime/review_orchestrator.py)

## Receipts and reports

Append-only JSONL: `runtime/workflow-depth/index.jsonl` (or `GRACE_MAR_WORKFLOW_DEPTH_HOME`). Inspection only — see [workflow-depth.md](workflow-depth.md) and [workflow-depth-audit.md](workflow-depth-audit.md).

## See also

- [workflow-depth-implementation-note.md](workflow-depth-implementation-note.md) — what shipped, paths, narrow scope
- [worker-candidates.md](worker-candidates.md) — future routed workers (documentation only; no router in-repo)
