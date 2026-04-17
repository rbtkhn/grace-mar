# Expert thread — `scott-ritter`

WORK only; not Record.

**Source:** Human **narrative journal** (below) + [`strategy-expert-scott-ritter-transcript.md`](strategy-expert-scott-ritter-transcript.md) (verbatim ingests) + relevant **knot** files (where this expert’s material was used).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-scott-ritter.md`](strategy-expert-scott-ritter.md) (profile) and [`strategy-expert-scott-ritter-transcript.md`](strategy-expert-scott-ritter-transcript.md) (7-day verbatim).

---
## Journal layer — Narrative (operator)

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **knots**, convergence/tension with other **`thread:`** experts, and **Open** pins. The **journal layer** is **not** overwritten by the **`thread`** script._

**Layout:** Stay on **one** `strategy-expert-scott-ritter-thread.md` file. Within the **journal layer**, each **`## YYYY-MM`** heading is a **month segment**. For **2026:** **Segment 1** = January (`## 2026-01`), **Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), **Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** (script-maintained) is **only** the fenced block between the **strategy-expert-thread** HTML start and end comments — do not call that "Segment 2" in the month sense.

_(No narrative distillation yet — add prose above the markers, not inside them.)_

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (quarter-scale or ongoing). **Default:** **at least ~500 words** of **prose** per month-segment (words on non-bullet substantive lines; see `validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the prose minimum and are **not** an equally canonical substitute for the prose-first journal unless the operator opts into ledger-only months (see HTML comment below). To scaffold prose to the minimum from roster metadata, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.

- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id scott-ritter --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`scott-ritter-<start>-to-<end>.md`) plus **per-month** files (`scott-ritter/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.

- **`<!-- backfill:scott-ritter:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.

- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.
## 2026-01


Cross-lane convergence and tension are notebook-native concepts. For 2026-01, read × seyed-marandi, × robert-barnes, × rome-invective (split from ecumenical) as the default **short list** of other experts whose fingerprints commonly collide with `scott-ritter` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-01, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

Verification stance for Scott Ritter in 2026-01 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

The `scott-ritter` lane’s role (U.S. military dissent: Hormuz sea control, blockade ops, Vance frame; faith-politics register when Ritter is the speaking expert) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

The 2026-01 segment for the Scott Ritter lane (`scott-ritter`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on U.S. military dissent: Hormuz sea control, blockade ops, Vance frame; faith-politics register when Ritter is the speaking expert. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Typical pairings on file for `scott-ritter` emphasize contrast surfaces: × seyed-marandi, × robert-barnes, × rome-invective (split from ecumenical). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-01 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

When historical expert context artifacts exist for `scott-ritter` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-01 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

- [strength: low] **Signal:** Public lines in this window emphasize US–Iran military buildup and strike risk; Iran framed as able to disrupt regional energy and base posture if conflict widens (see reconstructed arc URLs — third-party transcripts, not in-repo verbatim).
- [strength: low] **Mechanism:** Stresses command continuity and pre-planned resilience vs a telegraphed strike — narrative “warning” tone on escalation path.
## 2026-02


The 2026-02 segment for the Scott Ritter lane (`scott-ritter`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on U.S. military dissent: Hormuz sea control, blockade ops, Vance frame; faith-politics register when Ritter is the speaking expert. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Open pins belong in prose, not only as bullets. For this `scott-ritter` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

The `scott-ritter` lane’s role (U.S. military dissent: Hormuz sea control, blockade ops, Vance frame; faith-politics register when Ritter is the speaking expert) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

Cross-lane convergence and tension are notebook-native concepts. For 2026-02, read × seyed-marandi, × robert-barnes, × rome-invective (split from ecumenical) as the default **short list** of other experts whose fingerprints commonly collide with `scott-ritter` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-02, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

Verification stance for Scott Ritter in 2026-02 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

Typical pairings on file for `scott-ritter` emphasize contrast surfaces: × seyed-marandi, × robert-barnes, × rome-invective (split from ecumenical). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-02 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

- [strength: low] **Signal:** Iran policy framed as a diplomatic corner: long-form commentary on negotiations vs coercion (paired sources in backfill block).
- [strength: medium] **Tension:** Potential **versus** other experts on whether a diplomatic off-ramp exists at all — use current batch-analysis pairs to test, not this stub alone.
## 2026-03


Verification stance for Scott Ritter in 2026-03 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

When historical expert context artifacts exist for `scott-ritter` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-03 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-03, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

Typical pairings on file for `scott-ritter` emphasize contrast surfaces: × seyed-marandi, × robert-barnes, × rome-invective (split from ecumenical). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

If knots named this expert during 2026-03, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

The `scott-ritter` lane’s role (U.S. military dissent: Hormuz sea control, blockade ops, Vance frame; faith-politics register when Ritter is the speaking expert) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.


Verification stance for Scott Ritter in 2026-03 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

When historical expert context artifacts exist for `scott-ritter` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-03 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

- [strength: low] **Signal:** US–Israel campaign against Iran described as underperforming strategically; missile-defense and dispersal themes recur in cited pieces.
- [strength: low] **Shift:** Emphasis moves from “buildup” framing (Jan) to “campaign trajectory / failure mode” framing (Mar) in the reconstructed arc — **drift** to be checked against April machine extraction.

---
<!-- backfill:scott-ritter:start -->
## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `scott-ritter` from **2026-01-01** through **2026-04-30** (partial April).
**Status:** Reconstructed summary from primary notebook artifacts and best-effort git history; not contemporaneous journal prose.
**Rules:** Dated bullets only; contradictions should be preserved in source materials rather than harmonized here.

### 2026-01

- **2026-01-27** — Transcript dated Jan 27–28, 2026: US–Iran military buildup, risks of strikes, Iran continuity and Hormuz / global energy exposure (third-party transcript page).  
  _Source:_ web: `https://singjupost.com/scott-ritter-us-iran-war-imminent-as-military-buildup-peaks-transcript/`

### 2026-02

- **2026-02-16** — YouTube published 2026-02-16: long-form interview on Iran policy and diplomacy (metadata and opening dated Feb 16, 2026 on episode).  
  _Source:_ web: `https://www.youtube.com/watch?v=jJWd9zYB0WY`

### 2026-03

- **2026-03-18** — Article dated March 18, 2026: Ritter quoted on US–Israel Iran campaign framed as failing militarily and strategically; missile defense and dispersal themes per piece.  
  _Source:_ web: `https://greatreporter.com/2026/03/18/were-losing-this-war-scott-ritter-says-u-s-israeli-assault-on-iran-is-failing-militarily-legally-and-strategically/`


### 2026-04

- **2026-04** — Notebook knot cross-ref (partial month).  
  _Source:_ notebook: `strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md`

- **2026-04** — Notebook knot cross-ref (partial month).  
  _Source:_ notebook: `strategy-notebook-knot-2026-04-14-scott-ritter-blockade-hormuz-weave.md`

- **2026-04** — Notebook knot cross-ref (partial month).  
  _Source:_ notebook: `strategy-notebook-knot-2026-04-14-armstrong-cash-hormuz-digital-dollar-arc.md`

<!-- backfill:scott-ritter:end -->
## 2026-04

_Partial month — coverage from indexed machine lines through **2026-04-15** knot refs; April not calendar-complete._

April centers **Hormuz / blockade** mechanics vs digest-scale ORBAT: Haiphong–Ritter–Johnson quantitative lane (2026-04-10), Ritter×Davis batch-analysis fold (2026-04-12 → days **2026-04-14**), and sister knots through uranium dual-register **2026-04-15**.


Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-04, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

If knots named this expert during 2026-04, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

When historical expert context artifacts exist for `scott-ritter` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-04 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

The `scott-ritter` lane’s role (U.S. military dissent: Hormuz sea control, blockade ops, Vance frame; faith-politics register when Ritter is the speaking expert) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

Finally, 2026-04 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: U.S. military dissent: Hormuz sea control, blockade ops, Vance frame; faith-politics register when Ritter is the speaking expert), **pairing map** (× seyed-marandi, × robert-barnes, × rome-invective (split from ecumenical)), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

The 2026-04 segment for the Scott Ritter lane (`scott-ritter`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on U.S. military dissent: Hormuz sea control, blockade ops, Vance frame; faith-politics register when Ritter is the speaking expert. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

- [strength: medium] **Mechanism:** Digest §B — hypothetical Hormuz **seizure** at scale framed **infeasible** (long LOC / echelon math) — [transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) — verify:operator-transcript-digest.
- [strength: medium] **Cross:** `batch-analysis` **Ritter × Davis** — OOB/closure skepticism vs ultimatum vs negotiation + resumption clock — [`chapters/2026-04/days.md`](chapters/2026-04/days.md) **2026-04-14** — `crosses:scott-ritter+daniel-davis`.
- [strength: medium] **Knot lattice:** [marandi-ritter-mercouris-hormuz-scaffold](strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md) · [scott-ritter-blockade-hormuz-weave](strategy-notebook-knot-2026-04-14-scott-ritter-blockade-hormuz-weave.md) · [armstrong-cash-hormuz-digital-dollar-arc](strategy-notebook-knot-2026-04-14-armstrong-cash-hormuz-digital-dollar-arc.md) · [kremlin-iri-uranium-dual-register](strategy-notebook-knot-2026-04-15-kremlin-iri-uranium-dual-register.md).
<!-- strategy-expert-thread:start -->
## Machine layer — Extraction (script-maintained)

_Auto-generated from `-transcript.md` + knot index. **Journal layer** (narrative) lives **above** the **strategy-expert-thread** start HTML comment. The machine-layer HTML block is replaced on each `thread` run._

### Recent transcript material

## 2026-04-12
- `batch-analysis | 2026-04-14 | Ritter × Davis | **Tension-first:** **Ritter** digest §B = **OOB / closure** skepticism on a Hollywood-grade Hormuz **seizure** at scale; **Davis** X = **ultimatum vs negotiation** + **resumption clock** + **U.S.-side macro** hurt if talks read as final offer—**convergence:** both undercut a clean **bomb → fold** story. **Do not** treat **digest quants** as **proof** of **Davis** claims or vice versa until **status URLs** + **wire** rows land. **`crosses:scott-ritter+daniel-davis`** — **membership:** **`thread:scott-ritter`** (brief-handoff bundle **2026-04-10**) + **`thread:daniel-davis`** (Prior scratch **2026-04-12** block); folded **[`## 2026-04-14`](chapters/2026-04/days.md)** **Signal**/**Judgment**/**Links**/**Open**.`
- `batch-analysis | 2026-04-14 | Ritter × Davis | **Tension-first:** **Ritter** digest §B = **OOB / closure** skepticism on a Hollywood-grade Hormuz **seizure** at scale; **Davis** X = **ultimatum vs negotiation** + **resumption clock** + **U.S.-side macro** hurt if talks read as final offer—**convergence:** both undercut a clean **bomb → fold** story. **Do not** treat **digest quants** as **proof** of **Davis** claims or vice versa until **status URLs** + **wire** rows land. **`crosses:scott-ritter+daniel-davis`** — **membership:** **`thread:scott-ritter`** (brief-handoff bundle **2026-04-10**) + **`thread:daniel-davis`** (Prior scratch **2026-04-12** block); folded **[`## 2026-04-14`](chapters/2026-04/days.md)** **Signal**/**Judgment**/**Links**/**Open**.`
    `batch-analysis | 2026-04-14 | Ritter × Davis | crosses:scott-ritter+daniel-davis`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | **Tension-first:** thread:alexander-mercouris **15 Apr 2026** **The Duran** strand (contested Hormuz narratives, Islamabad reads, Lavrov–Wang–Xi, Russian SC commentary, attrition frame) × tri-mind **B→A→C** + solo A; fact-check triage rows in days.md **## 2026-04-15** **Links**—do not merge second-hand ORBAT with tanker AIS facts without tier discipline. seam:mercouris-tri-frame — WORK only; not a crosses: two-expert row.`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | seam:mercouris-tri-frame`
    ### Expert ingest — 2026-04-16 (Robert Pape × Cyrus Janssen; operator transcript)
- `batch-analysis | 2026-04-14 | Ritter × Davis | **Tension-first:** **Ritter** digest §B = **OOB / closure** skepticism on a Hollywood-grade Hormuz **seizure** at scale; **Davis** X = **ultimatum vs negotiation** + **resumption clock** + **U.S.-side macro** hurt if talks read as final offer—**convergence:** both undercut a clean **bomb → fold** story. **Do not** treat **digest quants** as **proof** of **Davis** claims or vice versa until **status URLs** + **wire** rows land. **`crosses:scott-ritter+daniel-davis`** — **membership:** **`thread:scott-ritter`** (brief-handoff bundle **2026-04-10**) + **`thread:daniel-davis`** (Prior scratch **2026-04-12** block); folded **[`## 2026-04-14`](chapters/2026-04/days.md)** **Signal**/**Judgment**/**Links**/**Open**.`
    `batch-analysis | 2026-04-14 | Ritter × Davis | crosses:scott-ritter+daniel-davis`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | **Tension-first:** thread:alexander-mercouris **15 Apr 2026** **The Duran** strand (contested Hormuz narratives, Islamabad reads, Lavrov–Wang–Xi, Russian SC commentary, attrition frame) × tri-mind **B→A→C** + solo A; fact-check triage rows in days.md **## 2026-04-15** **Links**—do not merge second-hand ORBAT with tanker AIS facts without tier discipline. seam:mercouris-tri-frame — WORK only; not a crosses: two-expert row.`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | seam:mercouris-tri-frame`
    ### Expert ingest — 2026-04-16 (Robert Pape × Cyrus Janssen; operator transcript)
- `batch-analysis | 2026-04-14 | Ritter × Davis | **Tension-first:** **Ritter** digest §B = **OOB / closure** skepticism on a Hollywood-grade Hormuz **seizure** at scale; **Davis** X = **ultimatum vs negotiation** + **resumption clock** + **U.S.-side macro** hurt if talks read as final offer—**convergence:** both undercut a clean **bomb → fold** story. **Do not** treat **digest quants** as **proof** of **Davis** claims or vice versa until **status URLs** + **wire** rows land. **`crosses:scott-ritter+daniel-davis`** — **membership:** **`thread:scott-ritter`** (brief-handoff bundle **2026-04-10**) + **`thread:daniel-davis`** (Prior scratch **2026-04-12** block); folded **[`## 2026-04-14`](chapters/2026-04/days.md)** **Signal**/**Judgment**/**Links**/**Open**.`
    `batch-analysis | 2026-04-14 | Ritter × Davis | crosses:scott-ritter+daniel-davis`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | **Tension-first:** thread:alexander-mercouris **15 Apr 2026** **The Duran** strand (contested Hormuz narratives, Islamabad reads, Lavrov–Wang–Xi, Russian SC commentary, attrition frame) × tri-mind **B→A→C** + solo A; fact-check triage rows in days.md **## 2026-04-15** **Links**—do not merge second-hand ORBAT with tanker AIS facts without tier discipline. seam:mercouris-tri-frame — WORK only; not a crosses: two-expert row.`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | seam:mercouris-tri-frame`
    ### Expert ingest — 2026-04-16 (Robert Pape × Cyrus Janssen; operator transcript)
- `batch-analysis | 2026-04-14 | Ritter × Davis | **Tension-first:** **Ritter** digest §B = **OOB / closure** skepticism on a Hollywood-grade Hormuz **seizure** at scale; **Davis** X = **ultimatum vs negotiation** + **resumption clock** + **U.S.-side macro** hurt if talks read as final offer—**convergence:** both undercut a clean **bomb → fold** story. **Do not** treat **digest quants** as **proof** of **Davis** claims or vice versa until **status URLs** + **wire** rows land. **`crosses:scott-ritter+daniel-davis`** — **membership:** **`thread:scott-ritter`** (brief-handoff bundle **2026-04-10**) + **`thread:daniel-davis`** (Prior scratch **2026-04-12** block); folded **[`## 2026-04-14`](chapters/2026-04/days.md)** **Signal**/**Judgment**/**Links**/**Open**.`
    `batch-analysis | 2026-04-14 | Ritter × Davis | crosses:scott-ritter+daniel-davis`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | **Tension-first:** thread:alexander-mercouris **15 Apr 2026** **The Duran** strand (contested Hormuz narratives, Islamabad reads, Lavrov–Wang–Xi, Russian SC commentary, attrition frame) × tri-mind **B→A→C** + solo A; fact-check triage rows in days.md **## 2026-04-15** **Links**—do not merge second-hand ORBAT with tanker AIS facts without tier discipline. seam:mercouris-tri-frame — WORK only; not a crosses: two-expert row.`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | seam:mercouris-tri-frame`
    ### Expert ingest — 2026-04-16 (Robert Pape × Cyrus Janssen; operator transcript)
- `batch-analysis | 2026-04-14 | Ritter × Davis | **Tension-first:** **Ritter** digest §B = **OOB / closure** skepticism on a Hollywood-grade Hormuz **seizure** at scale; **Davis** X = **ultimatum vs negotiation** + **resumption clock** + **U.S.-side macro** hurt if talks read as final offer—**convergence:** both undercut a clean **bomb → fold** story. **Do not** treat **digest quants** as **proof** of **Davis** claims or vice versa until **status URLs** + **wire** rows land. **`crosses:scott-ritter+daniel-davis`** — **membership:** **`thread:scott-ritter`** (brief-handoff bundle **2026-04-10**) + **`thread:daniel-davis`** (Prior scratch **2026-04-12** block); folded **[`## 2026-04-14`](chapters/2026-04/days.md)** **Signal**/**Judgment**/**Links**/**Open**.`
    `batch-analysis | 2026-04-14 | Ritter × Davis | crosses:scott-ritter+daniel-davis`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | **Tension-first:** thread:alexander-mercouris **15 Apr 2026** **The Duran** strand (contested Hormuz narratives, Islamabad reads, Lavrov–Wang–Xi, Russian SC commentary, attrition frame) × tri-mind **B→A→C** + solo A; fact-check triage rows in days.md **## 2026-04-15** **Links**—do not merge second-hand ORBAT with tanker AIS facts without tier discipline. seam:mercouris-tri-frame — WORK only; not a crosses: two-expert row.`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | seam:mercouris-tri-frame`
    ### Expert ingest — 2026-04-16 (Robert Pape × Cyrus Janssen; operator transcript)
- `batch-analysis | 2026-04-14 | Ritter × Davis | **Tension-first:** **Ritter** digest §B = **OOB / closure** skepticism on a Hollywood-grade Hormuz **seizure** at scale; **Davis** X = **ultimatum vs negotiation** + **resumption clock** + **U.S.-side macro** hurt if talks read as final offer—**convergence:** both undercut a clean **bomb → fold** story. **Do not** treat **digest quants** as **proof** of **Davis** claims or vice versa until **status URLs** + **wire** rows land. **`crosses:scott-ritter+daniel-davis`** — **membership:** **`thread:scott-ritter`** (brief-handoff bundle **2026-04-10**) + **`thread:daniel-davis`** (Prior scratch **2026-04-12** block); folded **[`## 2026-04-14`](chapters/2026-04/days.md)** **Signal**/**Judgment**/**Links**/**Open**.`
    `batch-analysis | 2026-04-14 | Ritter × Davis | crosses:scott-ritter+daniel-davis`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | **Tension-first:** thread:alexander-mercouris **15 Apr 2026** **The Duran** strand (contested Hormuz narratives, Islamabad reads, Lavrov–Wang–Xi, Russian SC commentary, attrition frame) × tri-mind **B→A→C** + solo A; fact-check triage rows in days.md **## 2026-04-15** **Links**—do not merge second-hand ORBAT with tanker AIS facts without tier discipline. seam:mercouris-tri-frame — WORK only; not a crosses: two-expert row.`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | seam:mercouris-tri-frame`
    ### Expert ingest — 2026-04-16 (Robert Pape × Cyrus Janssen; operator transcript)
- `batch-analysis | 2026-04-14 | Ritter × Davis | **Tension-first:** **Ritter** digest §B = **OOB / closure** skepticism on a Hollywood-grade Hormuz **seizure** at scale; **Davis** X = **ultimatum vs negotiation** + **resumption clock** + **U.S.-side macro** hurt if talks read as final offer—**convergence:** both undercut a clean **bomb → fold** story. **Do not** treat **digest quants** as **proof** of **Davis** claims or vice versa until **status URLs** + **wire** rows land. **`crosses:scott-ritter+daniel-davis`** — **membership:** **`thread:scott-ritter`** (brief-handoff bundle **2026-04-10**) + **`thread:daniel-davis`** (Prior scratch **2026-04-12** block); folded **[`## 2026-04-14`](chapters/2026-04/days.md)** **Signal**/**Judgment**/**Links**/**Open**.`
    `batch-analysis | 2026-04-14 | Ritter × Davis | crosses:scott-ritter+daniel-davis`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | **Tension-first:** thread:alexander-mercouris **15 Apr 2026** **The Duran** strand (contested Hormuz narratives, Islamabad reads, Lavrov–Wang–Xi, Russian SC commentary, attrition frame) × tri-mind **B→A→C** + solo A; fact-check triage rows in days.md **## 2026-04-15** **Links**—do not merge second-hand ORBAT with tanker AIS facts without tier discipline. seam:mercouris-tri-frame — WORK only; not a crosses: two-expert row.`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | seam:mercouris-tri-frame`
    ### Expert ingest — 2026-04-16 (Robert Pape × Cyrus Janssen; operator transcript)
- `batch-analysis | 2026-04-14 | Ritter × Davis | **Tension-first:** **Ritter** digest §B = **OOB / closure** skepticism on a Hollywood-grade Hormuz **seizure** at scale; **Davis** X = **ultimatum vs negotiation** + **resumption clock** + **U.S.-side macro** hurt if talks read as final offer—**convergence:** both undercut a clean **bomb → fold** story. **Do not** treat **digest quants** as **proof** of **Davis** claims or vice versa until **status URLs** + **wire** rows land. **`crosses:scott-ritter+daniel-davis`** — **membership:** **`thread:scott-ritter`** (brief-handoff bundle **2026-04-10**) + **`thread:daniel-davis`** (Prior scratch **2026-04-12** block); folded **[`## 2026-04-14`](chapters/2026-04/days.md)** **Signal**/**Judgment**/**Links**/**Open**.`
    `batch-analysis | 2026-04-14 | Ritter × Davis | crosses:scott-ritter+daniel-davis`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | **Tension-first:** thread:alexander-mercouris **15 Apr 2026** **The Duran** strand (contested Hormuz narratives, Islamabad reads, Lavrov–Wang–Xi, Russian SC commentary, attrition frame) × tri-mind **B→A→C** + solo A; fact-check triage rows in days.md **## 2026-04-15** **Links**—do not merge second-hand ORBAT with tanker AIS facts without tier discipline. seam:mercouris-tri-frame — WORK only; not a crosses: two-expert row.`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | seam:mercouris-tri-frame`
    ### Expert ingest — 2026-04-16 (Robert Pape × Cyrus Janssen; operator transcript)
- `batch-analysis | 2026-04-14 | Ritter × Davis | **Tension-first:** **Ritter** digest §B = **OOB / closure** skepticism on a Hollywood-grade Hormuz **seizure** at scale; **Davis** X = **ultimatum vs negotiation** + **resumption clock** + **U.S.-side macro** hurt if talks read as final offer—**convergence:** both undercut a clean **bomb → fold** story. **Do not** treat **digest quants** as **proof** of **Davis** claims or vice versa until **status URLs** + **wire** rows land. **`crosses:scott-ritter+daniel-davis`** — **membership:** **`thread:scott-ritter`** (brief-handoff bundle **2026-04-10**) + **`thread:daniel-davis`** (Prior scratch **2026-04-12** block); folded **[`## 2026-04-14`](chapters/2026-04/days.md)** **Signal**/**Judgment**/**Links**/**Open**.`
    `batch-analysis | 2026-04-14 | Ritter × Davis | crosses:scott-ritter+daniel-davis`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | **Tension-first:** thread:alexander-mercouris **15 Apr 2026** **The Duran** strand (contested Hormuz narratives, Islamabad reads, Lavrov–Wang–Xi, Russian SC commentary, attrition frame) × tri-mind **B→A→C** + solo A; fact-check triage rows in days.md **## 2026-04-15** **Links**—do not merge second-hand ORBAT with tanker AIS facts without tier discipline. seam:mercouris-tri-frame — WORK only; not a crosses: two-expert row.`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | seam:mercouris-tri-frame`
    ### Expert ingest — 2026-04-16 (Robert Pape × Cyrus Janssen; operator transcript)
- `batch-analysis | 2026-04-14 | Ritter × Davis | **Tension-first:** **Ritter** digest §B = **OOB / closure** skepticism on a Hollywood-grade Hormuz **seizure** at scale; **Davis** X = **ultimatum vs negotiation** + **resumption clock** + **U.S.-side macro** hurt if talks read as final offer—**convergence:** both undercut a clean **bomb → fold** story. **Do not** treat **digest quants** as **proof** of **Davis** claims or vice versa until **status URLs** + **wire** rows land. **`crosses:scott-ritter+daniel-davis`** — **membership:** **`thread:scott-ritter`** (brief-handoff bundle **2026-04-10**) + **`thread:daniel-davis`** (Prior scratch **2026-04-12** block); folded **[`## 2026-04-14`](chapters/2026-04/days.md)** **Signal**/**Judgment**/**Links**/**Open**.`
    `batch-analysis | 2026-04-14 | Ritter × Davis | crosses:scott-ritter+daniel-davis`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | **Tension-first:** thread:alexander-mercouris **15 Apr 2026** **The Duran** strand (contested Hormuz narratives, Islamabad reads, Lavrov–Wang–Xi, Russian SC commentary, attrition frame) × tri-mind **B→A→C** + solo A; fact-check triage rows in days.md **## 2026-04-15** **Links**—do not merge second-hand ORBAT with tanker AIS facts without tier discipline. seam:mercouris-tri-frame — WORK only; not a crosses: two-expert row.`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | seam:mercouris-tri-frame`
    ### Expert ingest — 2026-04-16 (Robert Pape × Cyrus Janssen; operator transcript)
- `batch-analysis | 2026-04-14 | Ritter × Davis | **Tension-first:** **Ritter** digest §B = **OOB / closure** skepticism on a Hollywood-grade Hormuz **seizure** at scale; **Davis** X = **ultimatum vs negotiation** + **resumption clock** + **U.S.-side macro** hurt if talks read as final offer—**convergence:** both undercut a clean **bomb → fold** story. **Do not** treat **digest quants** as **proof** of **Davis** claims or vice versa until **status URLs** + **wire** rows land. **`crosses:scott-ritter+daniel-davis`** — **membership:** **`thread:scott-ritter`** (brief-handoff bundle **2026-04-10**) + **`thread:daniel-davis`** (Prior scratch **2026-04-12** block); folded **[`## 2026-04-14`](chapters/2026-04/days.md)** **Signal**/**Judgment**/**Links**/**Open**.`
    `batch-analysis | 2026-04-14 | Ritter × Davis | crosses:scott-ritter+daniel-davis`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | **Tension-first:** thread:alexander-mercouris **15 Apr 2026** **The Duran** strand (contested Hormuz narratives, Islamabad reads, Lavrov–Wang–Xi, Russian SC commentary, attrition frame) × tri-mind **B→A→C** + solo A; fact-check triage rows in days.md **## 2026-04-15** **Links**—do not merge second-hand ORBAT with tanker AIS facts without tier discipline. seam:mercouris-tri-frame — WORK only; not a crosses: two-expert row.`
    `batch-analysis | 2026-04-15 | Mercouris × tri-mind | seam:mercouris-tri-frame`
    ### Expert ingest — 2026-04-16 (Robert Pape × Cyrus Janssen; operator transcript)

### Knot references

- [strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md](strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md) 2026-04-13 (marandi-ritter-mercouris-hormuz-scaffold) — Marandi×Ritter×Mercouris shared scaffold; Davis×Freeman×Mearsheimer parallel; cross-day to 04-12/04-14
- [strategy-notebook-knot-2026-04-14-scott-ritter-blockade-hormuz-weave.md](strategy-notebook-knot-2026-04-14-scott-ritter-blockade-hormuz-weave.md) 2026-04-14 (scott-ritter-blockade-hormuz-weave) — Ritter blockade mechanics + sister knots + indexed threads same topic; weave_count from knot_seam_metrics.py (outgoing knot links)
- [strategy-notebook-knot-2026-04-14-armstrong-cash-hormuz-digital-dollar-arc.md](strategy-notebook-knot-2026-04-14-armstrong-cash-hormuz-digital-dollar-arc.md) 2026-04-14 (armstrong-cash-hormuz-digital-dollar-arc) — Synthesis: Barnes/Mercouris/Mearsheimer mind files + Armstrong X + Fink/BlackRock + Congress.gov + Statista/Signal Gulf fertilizer; orthogonal to thread: Hormuz lattice
- [strategy-notebook-knot-2026-04-15-kremlin-iri-uranium-dual-register.md](strategy-notebook-knot-2026-04-15-kremlin-iri-uranium-dual-register.md) 2026-04-15 (kremlin-iri-uranium-dual-register) — Synthesis+Thesis: Kremlin-IRI uranium convergence, MFA vs IRGC dual register, Leo-France-UK legitimacy stack
<!-- strategy-expert-thread:end -->
