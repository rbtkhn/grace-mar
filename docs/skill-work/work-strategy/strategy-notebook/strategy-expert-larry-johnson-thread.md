# Expert thread — `larry-johnson`

WORK only; not Record.

**Source:** Distilled from [`strategy-expert-larry-johnson-transcript.md`](strategy-expert-larry-johnson-transcript.md) (what the expert said recently) and relevant knots (where that material was used in strategy work).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-larry-johnson.md`](strategy-expert-larry-johnson.md) (profile) and [`strategy-expert-larry-johnson-transcript.md`](strategy-expert-larry-johnson-transcript.md) (7-day verbatim).

---
## Journal layer — Narrative (operator)

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **knots**, convergence/tension with other **`thread:`** experts, and **Open** pins. The **journal layer** is **not** overwritten by the **`thread`** script._

**Layout:** Stay on **one** `strategy-expert-larry-johnson-thread.md` file. Within the **journal layer**, each **`## YYYY-MM`** heading is a **month segment**. For **2026:** **Segment 1** = January (`## 2026-01`), **Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), **Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** (script-maintained) is **only** the fenced block between the **strategy-expert-thread** HTML start and end comments — do not call that "Segment 2" in the month sense.

_(No narrative distillation yet — add prose above the markers, not inside them.)_

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (quarter-scale or ongoing). **Default:** **at least ~500 words** of **prose** per month-segment (words on non-bullet substantive lines; see `validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the prose minimum and are **not** an equally canonical substitute for the prose-first journal unless the operator opts into ledger-only months (see HTML comment below). To scaffold prose to the minimum from roster metadata, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.

- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id larry-johnson --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`larry-johnson-<start>-to-<end>.md`) plus **per-month** files (`larry-johnson/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.

- **`<!-- backfill:larry-johnson:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.

- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.
## 2026-01

January has **no dated** notebook `thread:` row for Johnson in this Q1 snapshot; the lane is **ex-CIA material / ORBAT / Hormuz geometry** beside Haiphong–Ritter roundtables — per roster. Hubs are anchors only.


Verification stance for Larry Johnson in 2026-01 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

Typical pairings on file for `larry-johnson` emphasize contrast surfaces: × scott-ritter, × daniel-davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-01 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

If knots named this expert during 2026-01, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Cross-lane convergence and tension are notebook-native concepts. For 2026-01, read × scott-ritter, × daniel-davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) as the default **short list** of other experts whose fingerprints commonly collide with `larry-johnson` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

The `larry-johnson` lane’s role (Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

When historical expert context artifacts exist for `larry-johnson` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-01 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Finally, 2026-01 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)), **pairing map** (× scott-ritter, × daniel-davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

- [strength: low] **Identity anchor:** Sonar21 + Substack + X (Seed).  
  [sonar21.com](https://sonar21.com/) · [larrycjohnson.substack.com](https://larrycjohnson.substack.com/) · [X @LarrySonar21](https://x.com/LarrySonar21)
## 2026-02

February shows **no indexed Q1 primary** in-repo; **`scott-ritter`** / **`daniel-davis`** crosses stay **seam-labeled** when the same week needs material detail.


Cross-lane convergence and tension are notebook-native concepts. For 2026-02, read × scott-ritter, × daniel-davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) as the default **short list** of other experts whose fingerprints commonly collide with `larry-johnson` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

The `larry-johnson` lane’s role (Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

Finally, 2026-02 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)), **pairing map** (× scott-ritter, × daniel-davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

The 2026-02 segment for the Larry Johnson lane (`larry-johnson`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables). That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

When historical expert context artifacts exist for `larry-johnson` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-02 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-02, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

- [strength: low] **Digest pointer (April-heavy):** Haiphong / Ritter / Johnson digest is **not** a February dated line — future operator cross-link only.  
  [transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)
## 2026-03

March remains **thin** here; **April** machine extraction references **F-15 / Isfahan** narrative math — Q1 is **identity + routing** only.


Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-03, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

The 2026-03 segment for the Larry Johnson lane (`larry-johnson`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables). That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Finally, 2026-03 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)), **pairing map** (× scott-ritter, × daniel-davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

Typical pairings on file for `larry-johnson` emphasize contrast surfaces: × scott-ritter, × daniel-davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

The `larry-johnson` lane’s role (Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.


Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-03, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

The 2026-03 segment for the Larry Johnson lane (`larry-johnson`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables). That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

- [strength: low] **Repeat anchor:** Substack hub — no implied posting calendar.
<!-- backfill:larry-johnson:start -->
## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `larry-johnson` from **2026-01-01** through **2026-04-30** (partial April).
**Status:** Reconstructed summary; no dated primary lines in the Q1 ledger at authoring time.
**Rules:** Hub anchors only where dated captures are missing.

### 2026-01

- **2026-01** — No dated notebook ingest — Sonar21 hub.  
  _Source:_ web: `https://sonar21.com/`

### 2026-02

- **2026-02** — No dated notebook ingest — Substack hub.  
  _Source:_ web: `https://larrycjohnson.substack.com/`

### 2026-03

- **2026-03** — No dated notebook ingest — X profile pointer.  
  _Source:_ web: `https://x.com/LarrySonar21`


### 2026-04

- **2026-04** — Notebook knot cross-ref (partial month).  
  _Source:_ notebook: `strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md`

- **2026-04** — Notebook knot cross-ref (partial month).  
  _Source:_ notebook: `strategy-notebook-knot-2026-04-14-scott-ritter-blockade-hormuz-weave.md`

<!-- backfill:larry-johnson:end -->
## 2026-04

_Partial month — **2026-04-10** digest §B line + Hormuz scaffold / blockade knots; not calendar-complete._

April centers **F-15 / Isfahan “rescue”** deployment narrative and C-130 / Little Bird load math from Haiphong–Ritter–Johnson digest — **same digest §B** as Ritter ORBAT skepticism lane.


Verification stance for Larry Johnson in 2026-04 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

If knots named this expert during 2026-04, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Typical pairings on file for `larry-johnson` emphasize contrast surfaces: × scott-ritter, × daniel-davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-04 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

The 2026-04 segment for the Larry Johnson lane (`larry-johnson`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables). That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Cross-lane convergence and tension are notebook-native concepts. For 2026-04, read × scott-ritter, × daniel-davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) as the default **short list** of other experts whose fingerprints commonly collide with `larry-johnson` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

Finally, 2026-04 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)), **pairing map** (× scott-ritter, × daniel-davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

- [strength: medium] **Mechanism:** YT cold **2026-04-10** — F-15/Isfahan rescue narrative; deployment ~Mar 10–11; load-math scenarios — path: [transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) — verify:operator-transcript-digest.
- [strength: medium] **Knot lattice:** [marandi-ritter-mercouris-hormuz-scaffold](strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md) · [scott-ritter-blockade-hormuz-weave](strategy-notebook-knot-2026-04-14-scott-ritter-blockade-hormuz-weave.md).

Canonical knot paths and raw ingest lines live in **Segment 2** below (regenerated each **`thread`** run).

---
<!-- strategy-expert-thread:start -->
## Machine layer — Extraction (script-maintained)

_Auto-generated from `-transcript.md` + knot index. **Journal layer** (narrative) lives **above** the `<!-- strategy-expert-thread:start -->` marker._

### Knot references

- [strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md](strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md) 2026-04-13 (marandi-ritter-mercouris-hormuz-scaffold) — Marandi×Ritter×Mercouris shared scaffold; Davis×Freeman×Mearsheimer parallel; cross-day to 04-12/04-14
- [strategy-notebook-knot-2026-04-14-scott-ritter-blockade-hormuz-weave.md](strategy-notebook-knot-2026-04-14-scott-ritter-blockade-hormuz-weave.md) 2026-04-14 (scott-ritter-blockade-hormuz-weave) — Ritter blockade mechanics + sister knots + indexed threads same topic; weave_count from knot_seam_metrics.py (outgoing knot links)
<!-- strategy-expert-thread:end -->
