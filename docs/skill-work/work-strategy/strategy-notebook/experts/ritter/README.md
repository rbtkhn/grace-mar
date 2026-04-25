# Expert `ritter` — thread layout (WORK)

- **[`thread.md`](thread.md)** — multi-month journal (`## 2026-02` onward and shared material); **coexists** with monthly `*-thread-YYYY-MM.md` files during a phased split. **`rebuild_threads`** (operator **`thread`**) does **not** update this file’s machine layer when any `ritter-thread-*.md` exists; machine extraction for the rolling bundle lives in the **per-month** files and **transcript** routing per [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Thread*.

- **[`ritter-thread-2026-01.md`](ritter-thread-2026-01.md)** — **January 2026** monthly chapter. Canonical journal + machine block for that month when both this file and `thread.md` hold `## 2026-01` (union discovery **dedupes** `strategy-page` by `id=`, **preferring** the monthly copy).

- **`ritter-thread-2026-04.md` (if present)** — may be **auto-created** by `rebuild_threads` when **`transcript.md`** has April date sections, before a human `## 2026-04` journal is moved here from `thread.md`. Safe to **delete** if you only want a machine stub after moving prose; or add a real journal block **above** the machine markers. Other months may appear the same way.

- **[`transcript.md`](transcript.md)** — 7-day rolling verbatim (inbox `thread:ritter` triage). · **[`profile.md`](profile.md)** — commentator card.

Run **`python3 scripts/strategy_thread.py`** (repo root) after inbox / ingest updates.
