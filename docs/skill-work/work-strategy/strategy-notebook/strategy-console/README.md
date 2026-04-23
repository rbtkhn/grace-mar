# Strategy Console

**WORK only;** not **Record**. **Derived, refresh-only, non-canonical.**

## 1. What it is

The **Strategy Console** is a **derived orientation surface** for the [strategy notebook](../README.md). One command (`scripts/strategy_console.py`) rewrites `console-view.md` with a **structural** snapshot: what files moved, which expert lanes have a recent mtime signal, which watches / state folders are present, where escalation markers appear, and a **conservative** suggested route toward the EOD **MCQ** (not a substitute for the evidence pile or MCQ choices).

## 2. Why it exists

The notebook already holds **experts** (who), **watches** (what), **days** (when), **minds** (lens), and **pages** (primary unit). Material is **scattered** across inbox, `raw-input/`, threads, `chapters/`, and state lanes. The console is the **unhobbling layer for orientation** in the sense of **unblocking the operator’s next move**: it turns scattered **read surfaces** into a single **command view** of *what to open next*—without **automating judgment** or **claiming** to be the archive of truth.

## 3. What it reads (read-only)

Documented in [STRATEGY-CONSOLE-CONTRACT.md](STRATEGY-CONSOLE-CONTRACT.md). In practice: `STATUS.md`, `daily-strategy-inbox.md`, `forecast-watch-log.md`, `strategy-commentator-threads.md`, `chapters/YYYY-MM/days.md`, `experts/<id>/thread.md` and `transcript.md`, `watches/`, `strategy-state-iran/`, `US-IRAN-KINETIC-TRACKER.md` when present, `raw-input/YYYY-MM-DD/`, and `compiled-views/` (metadata). **No** network access.

## 4. What it writes

- **`console-view.md`** in this directory (full replace each run).
- **Optional:** one JSONL **receipt** line per [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](../STRATEGY-NOTEBOOK-TRACE-CONTRACT.md) (same pattern as `compile_strategy_view.py`); use `--no-receipt` to skip.

## 5. What it must never do

- Edit **expert** `thread.md` or **`strategy-page`** blocks.
- Edit **`chapters/YYYY-MM/days.md`**.
- Edit **`raw-input/`** or prune sources.
- **Promote** WORK into **Record** or merge through the gate.
- Replace **EOD-MCQ** or the **evidence pile**; **no automatic MCQ answers**.

See [STRATEGY-CONSOLE-CONTRACT.md](STRATEGY-CONSOLE-CONTRACT.md) for the full list.

## 6. How it relates to EOD-MCQ

[EOD-MCQ-PROTOCOL.md](../EOD-MCQ-PROTOCOL.md) is the **authorized decision procedure** (session type → lanes → promotion threshold → page shape → page action → `days.md` continuity). The console may run **before** Stage 0 as **orientation**; the assistant still **builds the evidence pile** and drives MCQs. The console’s **Recommended EOD route** is a **heuristic nudge**—verify against today’s material.

## 7. How it relates to compiled views

[compiled-views/](../compiled-views/README.md) and `compile_strategy_view.py` produce a **source bundle** for **polyphony / recipe** work (e.g. five-conductors). The **console** is a **different** derived artifact: **front-door** situational awareness, not recipe execution. You may use **both** in one day (console first, bundle when composing a long synthesis).

## 8. Example commands

```bash
python3 scripts/strategy_console.py --help
python3 scripts/strategy_console.py
python3 scripts/strategy_console.py --mode eod
python3 scripts/strategy_console.py --mode morning
python3 scripts/strategy_console.py --mode crisis --watch iran
python3 scripts/strategy_console.py --notebook-dir docs/skill-work/work-strategy/strategy-notebook
python3 scripts/strategy_console.py --no-receipt
```

**Heuristics:** recent file mtimes, date strings, simple counts for `strategy-page` markers and escalation tokens (`[watch]`, `[decision]`, `[promote]`), `batch-analysis`, and roster-derived expert lanes. **Not** an LLM; **not** semantic analysis.

**Examples:** [examples/](examples/) — static illustrations only.

**Schema (documentation):** [console-schema.yaml](console-schema.yaml)
