# Strategy Console Contract

**Status:** Derived / refresh-only / non-canonical.

## Purpose

Prepare operator orientation before EOD, morning review, or crisis review. The console **structures** what to look at; it does **not** author judgment, `strategy-page` prose, or `days.md` blocks.

## Allowed reads

- `STATUS.md` (notebook root)
- `daily-strategy-inbox.md`
- `forecast-watch-log.md`
- `strategy-commentator-threads.md` (expert roster / lane SSOT)
- `chapters/YYYY-MM/days.md` (read-only; tail or light scan for markers and dates)
- `experts/<expert_id>/thread.md` and `transcript.md` (read-only)
- `watches/` and `watches/README.md` when present
- `strategy-state-iran/` (institutional / state lane; read-only)
- `US-IRAN-KINETIC-TRACKER.md` (when present; crisis / Iran focus)
- `raw-input/YYYY-MM-DD/` (list / metadata only)
- `compiled-views/` (file list / mtimes; not authoritative content)
- Any other path the implementation documents in [README.md](README.md) as a **read** surface for the same orientation goal.

## Allowed writes

- **`strategy-console/console-view.md` only** (regenerated in full each run).
- **Optional:** append one line to the strategy-notebook v1 JSONL receipt log per [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](../STRATEGY-NOTEBOOK-TRACE-CONTRACT.md) (`append_receipt` / `artifacts/work-strategy/strategy-notebook/receipts/strategy-notebook-receipts.jsonl`).

## Prohibited actions

- No expert `thread.md` edits.
- No `chapters/YYYY-MM/days.md` edits.
- No `strategy-page` creation or revision.
- No promotion into **Record** (SELF / EVIDENCE / gate merge).
- No `raw-input/` pruning, moves, or deletion.
- No deletion of source material.
- No automatic EOD **MCQ** answers; the console may **recommend** a route, not select menus.
- No claim that the console is canonical truth; operator evidence pile and EOD process remain primary.

## Boundary rule

The console may recommend a path into [EOD-MCQ-PROTOCOL.md](../EOD-MCQ-PROTOCOL.md) (session type, lanes, threshold, page shape, continuity). **EOD-MCQ** remains the **authorized decision procedure** for structured EOD sessions. **Compiled views** ([compiled-views/README.md](../compiled-views/README.md)) remain a separate derived bundle path (`compile_strategy_view.py`); the console is **front-door orientation**, not a replacement for those recipes.

**WORK** only; not Record.
