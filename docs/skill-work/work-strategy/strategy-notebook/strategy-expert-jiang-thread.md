# Expert thread — `jiang`

WORK only; not Record.

**Source:** Distilled from [`strategy-expert-jiang-transcript.md`](strategy-expert-jiang-transcript.md) (what the expert said recently) and relevant knots (where that material was used in strategy work).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-jiang.md`](strategy-expert-jiang.md) (profile) and [`strategy-expert-jiang-transcript.md`](strategy-expert-jiang-transcript.md) (7-day verbatim).

---
## Journal layer — Narrative (operator)

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **knots**, convergence/tension with other **`thread:`** experts, and **Open** pins. The **journal layer** is **not** overwritten by the **`thread`** script._

**Layout:** Stay on **one** `strategy-expert-jiang-thread.md` file. Within the **journal layer**, each **`## YYYY-MM`** heading is a **month segment**. For **2026:** **Segment 1** = January (`## 2026-01`), **Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), **Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** (script-maintained) is **only** the fenced block between the **strategy-expert-thread** HTML start and end comments — do not call that "Segment 2" in the month sense.

**Expert note (PH / work-jiang):** **Predictive History** notebook-facing ingest routes here only — see [strategy-commentator-threads](strategy-commentator-threads.md) special routing rule; corpus lives under `research/external/work-jiang/` (operator scope).

_(No narrative distillation yet — add prose above the markers, not inside them.)_

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (quarter-scale or ongoing). **Default:** **at least ~500 words** of **prose** per month-segment (words on non-bullet substantive lines; see `validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the prose minimum and are **not** an equally canonical substitute for the prose-first journal unless the operator opts into ledger-only months (see HTML comment below). To scaffold prose to the minimum from roster metadata, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.

- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id jiang --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`jiang-<start>-to-<end>.md`) plus **per-month** files (`jiang/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.

- **`<!-- backfill:jiang:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.

- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.
## 2026-01

January has **no calendar-indexed PH lecture row** in this strategy-notebook Q1 ledger; Q1 months may stay **episodic** or empty of public URLs — tooling still gets three **##** segments for continuity.


Finally, 2026-01 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Long-horizon civilizational / game-theory lectures; PH is the sole upstream for notebook-facing Jiang ingest), **pairing map** (x mearsheimer, x diesen, x sachs), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

The 2026-01 segment for the Jiang Xueqin (Predictive History) lane (`jiang`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Long-horizon civilizational / game-theory lectures; PH is the sole upstream for notebook-facing Jiang ingest. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Open pins belong in prose, not only as bullets. For this `jiang` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-01, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

If knots named this expert during 2026-01, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Verification stance for Jiang Xueqin (Predictive History) in 2026-01 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

- [strength: low] **Upstream anchor:** Predictive History YouTube (sole profile Seed).  
  [YouTube @PredictiveHistory](https://www.youtube.com/@PredictiveHistory)
## 2026-02

February likewise shows **no dated notebook-facing ingest** for Jiang in-repo; long-horizon **game-theory / civilizational** material remains in the **work-jiang** archive — not collapsed into other expert lanes.


Open pins belong in prose, not only as bullets. For this `jiang` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

The 2026-02 segment for the Jiang Xueqin (Predictive History) lane (`jiang`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Long-horizon civilizational / game-theory lectures; PH is the sole upstream for notebook-facing Jiang ingest. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

The `jiang` lane’s role (Long-horizon civilizational / game-theory lectures; PH is the sole upstream for notebook-facing Jiang ingest) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

Finally, 2026-02 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Long-horizon civilizational / game-theory lectures; PH is the sole upstream for notebook-facing Jiang ingest), **pairing map** (x mearsheimer, x diesen, x sachs), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

If knots named this expert during 2026-02, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-02, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

- [strength: low] **Corpus pointer (WORK):** Operator-scoped lecture tree — not a dated Feb appearance claim.  
  `../../../../research/external/work-jiang/` (repo-relative)
## 2026-03

March remains **scope-note** territory until the operator pins indexed transcripts; **April** machine lines may reference **vi-15** etc. — Q1 is **honest sparsity**.


Cross-lane convergence and tension are notebook-native concepts. For 2026-03, read x mearsheimer, x diesen, x sachs as the default **short list** of other experts whose fingerprints commonly collide with `jiang` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

Finally, 2026-03 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Long-horizon civilizational / game-theory lectures; PH is the sole upstream for notebook-facing Jiang ingest), **pairing map** (x mearsheimer, x diesen, x sachs), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

When historical expert context artifacts exist for `jiang` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-03 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Typical pairings on file for `jiang` emphasize contrast surfaces: x mearsheimer, x diesen, x sachs. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

The 2026-03 segment for the Jiang Xueqin (Predictive History) lane (`jiang`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Long-horizon civilizational / game-theory lectures; PH is the sole upstream for notebook-facing Jiang ingest. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

The `jiang` lane’s role (Long-horizon civilizational / game-theory lectures; PH is the sole upstream for notebook-facing Jiang ingest) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

- [strength: low] **Repeat:** PH channel hub — verify any calendar claim against lecture index before Links merge.

<!-- backfill:jiang:start -->
## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `jiang` from **2026-01-01** through **2026-04-30** (partial April).
**Status:** Reconstructed summary; **no** dated notebook-facing PH rows in Q1 at authoring time.
**Rules:** PH upstream only; hub / path anchors — not Record.

### 2026-01

- **2026-01** — No dated notebook ingest — Predictive History channel.  
  _Source:_ web: `https://www.youtube.com/@PredictiveHistory`

### 2026-02

- **2026-02** — No dated notebook ingest — repeat PH channel anchor (corpus: `research/external/work-jiang/`, WORK scope).  
  _Source:_ web: `https://www.youtube.com/@PredictiveHistory`

### 2026-03

- **2026-03** — No dated notebook ingest — repeat channel anchor.  
  _Source:_ web: `https://www.youtube.com/@PredictiveHistory`


### 2026-04

- **2026-04** — Ledger mirror 1 (partial month).  
  _Source:_ web: `https://www.youtube.com/watch?v=n44OF1Y7zgo`

<!-- backfill:jiang:end -->
## 2026-04

_Partial month — **2026-04-12** cold ingest only in Segment 2; PH / work-jiang routing unchanged._

April indexes **vi-15** tri-voice overlay (Jiang × Sneako × Dugin) — eschatology / multipolarity / narrative-escalation hook — cite lecture file, not headlines.


Finally, 2026-04 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Long-horizon civilizational / game-theory lectures; PH is the sole upstream for notebook-facing Jiang ingest), **pairing map** (x mearsheimer, x diesen, x sachs), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

The 2026-04 segment for the Jiang Xueqin (Predictive History) lane (`jiang`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Long-horizon civilizational / game-theory lectures; PH is the sole upstream for notebook-facing Jiang ingest. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-04, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

Typical pairings on file for `jiang` emphasize contrast surfaces: x mearsheimer, x diesen, x sachs. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-04 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

The `jiang` lane’s role (Long-horizon civilizational / game-theory lectures; PH is the sole upstream for notebook-facing Jiang ingest) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

Open pins belong in prose, not only as bullets. For this `jiang` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

- [strength: high] **Signal (cold):** Jiang × Sneako × Dugin — [YouTube n44OF1Y7zgo](https://www.youtube.com/watch?v=n44OF1Y7zgo) — verify:work-jiang-vi-15 + `research/external/work-jiang/lectures/interviews-15-sneako-jiang-dugin-eschatology.md`.

Canonical knot paths and raw ingest lines live in **Segment 2** below (regenerated each **`thread`** run).

---
<!-- strategy-expert-thread:start -->
## Machine layer — Extraction (script-maintained)

_Auto-generated from `-transcript.md` + knot index. **Journal layer** (narrative) lives **above** the **strategy-expert-thread** start HTML comment. The machine-layer HTML block is replaced on each `thread` run._

### Recent transcript material

## 2026-04-12
- `YT | cold: Jiang × Sneako × Dugin — eschatology stack (Scofield / Calvinism / Orthodox + traditionalist); Eurasian multipolarity vs US debt; Chabad as **convergence** not sole driver; katechon / antichrist closing // hook: **vi-15** tri-voice overlay; `narrative-escalation` | https://www.youtube.com/watch?v=n44OF1Y7zgo | verify:work-jiang-vi-15+thread:jiang+../../../../research/external/work-jiang/lectures/interviews-15-sneako-jiang-dugin-eschatology.md`
<!-- strategy-expert-thread:end -->
