# Expert `ritter` — thread layout (WORK)
<!-- word_count: 207 -->

**Reading order (2026, chronological):** [`ritter-thread-2026-01.md`](ritter-thread-2026-01.md) → [`ritter-thread-2026-02.md`](ritter-thread-2026-02.md) → [`ritter-thread-2026-03.md`](ritter-thread-2026-03.md) → [`ritter-thread-2026-04.md`](ritter-thread-2026-04.md). Then [`thread.md`](thread.md) for **ongoing 2026-04** journal (if not yet fully moved to the April monthly), **backfill**, and the legacy machine block (when still present there).

- **[`thread.md`](thread.md)** — Ongoing month segments (e.g. `## 2026-04`), backfill, and coexisting content during a phased split. **`rebuild_threads`** (operator **`thread`**) does **not** update this file’s machine layer when any `ritter-thread-*.md` exists; machine extraction for the monthly bundle lives in the **per-month** files and **transcript** routing per [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Thread*.

- **Monthlies** — **[`ritter-thread-2026-01.md`](ritter-thread-2026-01.md)** (January) through **03**; **[`ritter-thread-2026-04.md`](ritter-thread-2026-04.md)** (April). When both a monthly and `thread.md` held the same `## YYYY-MM`, union discovery **dedupes** `strategy-page` by `id=`, **preferring** the monthly file.

- **Gap scaffold** — If journal months exist in `thread.md` but a `ritter-thread-YYYY-MM.md` file is missing (partial split), run `python3 scripts/scaffold_missing_monthly_thread_files.py --expert ritter --apply`, then `python3 scripts/strategy_thread.py`.

- **[`transcript.md`](transcript.md)** — 7-day rolling verbatim (inbox `thread:ritter` triage). · **[`profile.md`](profile.md)** — commentator card.

- **Cross-expert membrane (optional):** After **`thread`**, check terminal **page candidate** lines (same `strategy-page` `id` spanning multiple experts). Same-page **`id` / `date` / `watch`** across experts; **Reflection** stays voice-specific. Day-level seams live in `chapters/YYYY-MM/days.md` **Links**.

Run **`python3 scripts/strategy_thread.py`** (repo root) after inbox / ingest updates.
