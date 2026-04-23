# Run contract (shared operational grammar, v1)

**Scope:** A minimal vocabulary for **operational runs** in Grace-Mar: sessions that are **derived**, **inspectable**, and **governed** — not replacements for canonical Markdown or Record. This document is **generic**; the first implementation is the **work-strategy** strategy run (`lane = work-strategy`). Other lanes may adopt the same terms later.

**Doctrine (non-negotiable):**

- **Runs are derived.** Run state, receipts, and proposal sidecars are **operational metadata**. They are **rebuildable** or **deletable** without losing the lane’s **canonical** truth in Git.
- **Runs do not replace** expert threads, `days.md`, inbox, or other notebook source files.
- **Runs do not authorize mutation** of canonical surfaces on their own. Promotion into **Record** (SELF, EVIDENCE, `bot/prompt.py`) uses the **companion-gated** pipeline in [AGENTS.md](../AGENTS.md). Applying a proposed `days.md` or `strategy-page` change remains **human- or tool-explicit** (e.g. operator edit, or an approved script the operator invokes).

See [runtime-vs-record.md](runtime-vs-record.md) for the runtime vs. Record split.

## Core fields

| Field | Meaning |
|--------|---------|
| `run_id` | Stable identifier for one operational session (e.g. `stratrun-20260416-abc12def`). |
| `lane` | WORK lane (e.g. `work-strategy`). |
| `intent` | Short operator label for why the run exists (e.g. `eod`, `intake`, `synthesis`). |
| `session_type` | Finer kind of session (e.g. `eod_strategy`); may mirror skill-router language. |
| `inputs` | Resolved paths and flags for what this run *read* or *depends on* (not necessarily full file content). |
| `proposed_outputs` | Pointers to **sidecar** JSON (or null) for proposed day or page work — *proposals*, not applied edits. |
| `status` | Where the run is in its lifecycle (see below). |
| `approval_state` | Whether something in this run awaits human or companion decision (`none`, `pending`, `approved`, `rejected` for v1). |
| `receipts` | In practice, **receipt references**: repo-relative paths to `run-receipt` JSON files appended during the run. |
| `warnings` | Non-fatal issues (missing optional files, path quirks). |

## Suggested `status` values (v1)

| Status | Meaning |
|--------|---------|
| `started` | Run id allocated; minimal state written. |
| `inputs_resolved` | Key input paths (e.g. inbox, month `days.md`) are recorded. |
| `thesis_selected` | Operator (or future step) locked a thesis for the day. |
| `days_only` | Intent is to touch **continuity in `days.md`** only, not a full page. |
| `page_proposed` | A **page** proposal sidecar exists (not yet applied in threads). |
| `blocked_for_review` | Waiting on human/companion before continuing. |
| `completed` | Run closed successfully (no implication that Markdown was written). |
| `noop` | Intentional no-op (e.g. nothing to do). |
| `failed` | Unrecoverable error; completion should be refused unless forced. |

These are **guidance** for tools and UIs. Unknown future strings may exist; **schemas** in `schema-registry/` may enumerate a **stable subset** for validation.

## Related artifacts (avoid mixing)

| Artifact | Role |
|----------|------|
| **Strategy run state** (`artifacts/strategy-runs/…/state.json`) | One **session envelope**: resumable run, `proposed_outputs` pointers, lifecycle `status`. |
| **Run receipt** (`schema-registry/run-receipt.v1.json`) | One **event** (e.g. `start`, `complete`): files read/touched, `result_status`, `run_id`. |
| **Execution receipt** ([`execution-receipt.v1.json`](../schema-registry/execution-receipt.v1.json)) | **Runtime worker / task** domain — different shape; do not merge schemas blindly. |
| **Notebook script JSONL** ([STRATEGY-NOTEBOOK-TRACE-CONTRACT](skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-TRACE-CONTRACT.md)) | **Per-entrypoint** line audit (`strategy_page`, `compile_strategy_view`, …) — *which files a script read or wrote*. Complements session-scoped run state. |

## Links

- [STRATEGY-RUN-ARCHITECTURE.md](skill-work/work-strategy/STRATEGY-RUN-ARCHITECTURE.md) — doctrine in the strategy lane
- [STRATEGY-RUN-OPERATOR.md](skill-work/work-strategy/STRATEGY-RUN-OPERATOR.md) — how to use `strategy_run.py`
- [AGENTS.md](../AGENTS.md) — gate and Record boundary
