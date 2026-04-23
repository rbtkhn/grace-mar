# Strategy notebook — page update operations contract

WORK only; not Record. **Source of truth** is still Markdown (`strategy-page` fences, `days.md`, etc.). This document names **governed operation labels** for scripted or proposed changes so evolution is testable and inspectable — not a license for silent bulk rewrites.

## PageOperation enum (v1)

| Value | Meaning (normative) |
|-------|---------------------|
| `NOOP` | No `strategy-page` or notebook file mutation; read-only or reporting only. |
| `APPEND` | Add new content (e.g. new `strategy-page` scaffold) without removing existing page bodies. |
| `REFINE` | In-place edit of an existing page while preserving `id=` and general thesis lane (operator-governed). |
| `SPLIT` | One logical page becomes two or more distinct `id=` blocks (provenance in receipt `details`). |
| `MERGE` | Two or more pages or blocks combined into one with explicit supersedes list in `details`. |
| `CONTRADICT` | Explicit recording of tension; may add a new page or section that *contradicts* another without deleting it. |
| `DEPRECATE` | Mark a page or block superseded; replacement references in `details`. |

**v1 enforcement:** Script entrypoints that **mutate** pages should declare the operation; human-only edits require **no** receipt (see [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](STRATEGY-NOTEBOOK-TRACE-CONTRACT.md)). Stricter CI checks are optional follow-ups.

## Default for `strategy_page.py`

- Default **`APPEND`**: inserts a new `strategy-page` block (scaffold) per expert thread.

## Proposals (future MCP / agents)

`propose_page_update`-style tools must emit **proposals** (WORK staging, copy-paste, or explicit apply by operator) — not silent writes to `thread.md`. Aligned with [AGENTS.md](../../../../AGENTS.md) (no ungated identity merges).

## Links

- [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](STRATEGY-NOTEBOOK-TRACE-CONTRACT.md) — receipt JSONL fields
- [PAGE-CONTRACT.md](PAGE-CONTRACT.md) — page vs thread
- [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) — EOD session and `thread` command
