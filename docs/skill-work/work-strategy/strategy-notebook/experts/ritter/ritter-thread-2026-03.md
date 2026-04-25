# Expert thread — `ritter`

WORK only; not Record.

**Source:** Human **narrative journal** (below) + [`strategy-expert-ritter-transcript.md`](strategy-expert-ritter-transcript.md) (verbatim ingests) + relevant **`strategy-page`** work (where this expert’s material was used).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-ritter.md`](strategy-expert-ritter.md) (profile) and [`strategy-expert-ritter-transcript.md`](strategy-expert-ritter-transcript.md) (7-day verbatim).

---
## Journal layer — Narrative (operator)

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **pages**, convergence/tension with other **`thread:`** experts, and **Open** pins. The **journal layer** is **not** overwritten by the **`thread`** script._

**Layout (partial monthly split):** **January 2026** is **canonical** in [`ritter-thread-2026-01.md`](ritter-thread-2026-01.md) (this file may still hold a **duplicate** `## 2026-01` until the split is complete). In this file, each **`## YYYY-MM`** from **2026-02** onward is a **month segment**. For **2026** in this legacy file: **Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), **Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** below is **not** updated by **`thread`** when monthly `ritter-thread-*.md` files exist; see monthly files + [`README.md`](README.md). Do not call the machine block "Segment 2" in the month sense.

_(No narrative distillation yet — add prose above the markers, not inside them.)_

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (quarter-scale or ongoing). **Default:** **at least ~500 words** of **prose** per month-segment (words on non-bullet substantive lines; see `validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the prose minimum and are **not** an equally canonical substitute for the prose-first journal unless the operator opts into ledger-only months (see HTML comment below). To scaffold prose to the minimum from roster metadata, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.

- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id ritter --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`ritter-<start>-to-<end>.md`) plus **per-month** files (`ritter/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.

- **`<!-- backfill:ritter:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.

- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.

## 2026-03



Verification stance for Scott Ritter in 2026-03 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

When historical expert context artifacts exist for `ritter` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-03 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-03, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for pages, for open pins, or for the next verify pass.

Typical pairings on file for `ritter` emphasize contrast surfaces: × marandi, × barnes, × rome-invective (split from ecumenical). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

If pages named this expert during 2026-03, the narrative should eventually say **which page** and **what job** the voice did (pressure, validate, narrate) in plain English. If legacy index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate page references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

The `ritter` lane’s role (U.S. military dissent: Hormuz sea control, blockade ops, Vance frame; faith-politics register when Ritter is the speaking expert) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a page as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.


Verification stance for Scott Ritter in 2026-03 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

When historical expert context artifacts exist for `ritter` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-03 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

- [strength: low] **Signal:** US–Israel campaign against Iran described as underperforming strategically; missile-defense and dispersal themes recur in cited pieces.
- [strength: low] **Shift:** Emphasis moves from “buildup” framing (Jan) to “campaign trajectory / failure mode” framing (Mar) in the reconstructed arc — **drift** to be checked against April machine extraction.

---
<!-- strategy-expert-thread:start -->
## Machine layer — Extraction (script-maintained)

_Auto-generated from `-transcript.md` + `strategy-page` blocks in this thread + optional empty legacy on-disk index rows. **Journal layer** (narrative) lives **above** the **strategy-expert-thread** start HTML comment. The machine-layer HTML block is replaced on each `thread` run._

_(No transcript or page material for extraction.)_
<!-- strategy-expert-thread:end -->
