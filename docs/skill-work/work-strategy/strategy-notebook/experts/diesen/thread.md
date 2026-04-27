# Expert thread — `diesen`
<!-- word_count: 4730 -->

WORK only; not Record.

**Source:** Distilled from [`strategy-expert-diesen-transcript.md`](strategy-expert-diesen-transcript.md) (what the expert said recently) and relevant pages (where that material was used in strategy work).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-diesen.md`](strategy-expert-diesen.md) (profile) and [`strategy-expert-diesen-transcript.md`](strategy-expert-diesen-transcript.md) (7-day verbatim).

---
## Journal layer — Narrative (operator)

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **pages**, convergence/tension with other **`thread:`** experts, and **Open** pins. The **journal layer** is **not** overwritten by the **`thread`** script._

**Layout:** Stay on **one** `strategy-expert-diesen-thread.md` file. Within the **journal layer**, each **`## YYYY-MM`** heading is a **month segment**. For **2026:** **Segment 1** = January (`## 2026-01`), **Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), **Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** (script-maintained) is **only** the fenced block between the **strategy-expert-thread** HTML start and end comments — do not call that "Segment 2" in the month sense.

_(No narrative distillation yet — add prose above the markers, not inside them.)_

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (quarter-scale or ongoing). **Default:** **at least ~500 words** of **prose** per month-segment (words on non-bullet substantive lines; see `validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the prose minimum and are **not** an equally canonical substitute for the prose-first journal unless the operator opts into ledger-only months (see HTML comment below). To scaffold prose to the minimum from roster metadata, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.

- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id diesen --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`diesen-<start>-to-<end>.md`) plus **per-month** files (`diesen/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.

- **`<!-- backfill:diesen:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.

- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.
## 2026-01

**Greater Eurasia** long-forms with **Marandi** anchor the month — **multipolar** / **non-Western** register on escalation, domestic unrest narrative, and **“limited strike”** assumptions; cross-host **Macgregor** on **rising war risk** keeps the **importer / distance** lane visible beside pure Tehran voice.


Verification stance for Glenn Diesen in 2026-01 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

The `diesen` lane’s role (Eurasia / multipolar discourse; non-Western institutional / rationality frames when distinct from Mearsheimer’s structural-realist register) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a page as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-01, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for pages, for open pins, or for the next verify pass.

Cross-lane convergence and tension are notebook-native concepts. For 2026-01, read × mearsheimer, × macgregor, × pape, × sachs as the default **short list** of other experts whose fingerprints commonly collide with `diesen` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

Finally, 2026-01 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Eurasia / multipolar discourse; non-Western institutional / rationality frames when distinct from Mearsheimer’s structural-realist register), **pairing map** (× mearsheimer, × macgregor, × pape, × sachs), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

Open pins belong in prose, not only as bullets. For this `diesen` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

When historical expert context artifacts exist for `diesen` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-01 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

- [strength: high] **Through-line:** **Marandi** on **overwhelming retaliation** to any U.S. strike — host **Diesen** — [YouTube I6XHVDtHRX4](https://www.youtube.com/watch?v=I6XHVDtHRX4) — indexes cite **~30 Jan 2026** — verify **title/date** in UI.
- [strength: medium] **Mechanism:** **Civil unrest** / **war preparation** thread — [Singju Post — Greater Eurasia + Marandi transcript](https://singjupost.com/greater-eurasia-podcast-w-seyed-m-marandi-on-irans-civil-unrest-transcript/) — **transcript-grade**; pair with **Mercouris** diplomatic tickers only via **batch-analysis** seam.
- [strength: medium] **Parallel lane:** **Macgregor** — **rising war risks** — [Singju Post transcript](https://singjupost.com/greater-eurasia-podcast-w-macgregor-on-rising-war-risks-transcript/) — third-country **distance** from U.S.–Israel frame — **do not** merge with **Marandi** lines without labels.
- [strength: low] **Lattice:** Upstream of **April** **PH vi-14** / Diesen×Sachs petrodollar vs Hormuz (page id `diesen-vi14-petrodollar-vs-sachs-hormuz`) abstract — Q1 is **voice + episode** discipline only.
## 2026-02

February weight shifts to **Ukraine** **information** / **Istanbul** theses at the **UN** and podcast — still **same** multipolar toolkit; **Iran** material continues on the feed (**Marandi** “war for survival”) for cross-week **batch-analysis** with January arc.


Cross-lane convergence and tension are notebook-native concepts. For 2026-02, read × mearsheimer, × macgregor, × pape, × sachs as the default **short list** of other experts whose fingerprints commonly collide with `diesen` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

Open pins belong in prose, not only as bullets. For this `diesen` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

If pages named this expert during 2026-02, the narrative should eventually say **which page** and **what job** the voice did (pressure, validate, narrate) in plain English. If legacy index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate page references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

The `diesen` lane’s role (Eurasia / multipolar discourse; non-Western institutional / rationality frames when distinct from Mearsheimer’s structural-realist register) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a page as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-02, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for pages, for open pins, or for the next verify pass.

When historical expert context artifacts exist for `diesen` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-02 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Verification stance for Glenn Diesen in 2026-02 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

- [strength: high] **Through-line:** **UN Security Council** — **media manipulation** in the **Ukraine** war — [Brave New Europe](https://braveneweurope.com/diesen-at-the-un-security-council-media-manipulation-in-the-ukraine-war) · [Podscan episode](https://www.podscan.fm/podcasts/diesen-greater-eurasia-podcast/episodes/media-manipulation-in-the-ukraine-war-diesen-at-the-un-security-council) — **~22 Feb 2026** class in third-party indexes.
- [strength: medium] **Mechanism:** **NATO’s war of choice** — **Istanbul** sabotage thesis — [Podscan](https://www.podscan.fm/podcasts/diesen-greater-eurasia-podcast/episodes/diesen-natos-war-of-choice-the-sabotage-of-the-istanbul-negotiations) — **~24 Feb 2026** — **hypothesis-grade** until primary **negotiation** docs pinned.
- [strength: high] **Signal (Iran):** **Marandi** — **“War for Survival”** — [Podscan](https://www.podscan.fm/podcasts/diesen-greater-eurasia-podcast/episodes/seyed-m-marandi-war-for-survival-irans-strategy-as-war-is-imminent) — **imminent-war** framing — **convergence** with **Mearsheimer** structural reads only with **dated** shared material.
## 2026-03

March stacks **Marandi** interviews (military strategy, ceasefire posture, **South Pars** / energy warfare), a **Mercouris** cross-episode on **Iran** ↔ **Ukraine**, and **Substack** synthesis on **U.S. dominance** — density supports **April** id compares without collapsing registers.


Cross-lane convergence and tension are notebook-native concepts. For 2026-03, read × mearsheimer, × macgregor, × pape, × sachs as the default **short list** of other experts whose fingerprints commonly collide with `diesen` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

If pages named this expert during 2026-03, the narrative should eventually say **which page** and **what job** the voice did (pressure, validate, narrate) in plain English. If legacy index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate page references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Typical pairings on file for `diesen` emphasize contrast surfaces: × mearsheimer, × macgregor, × pape, × sachs. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

When historical expert context artifacts exist for `diesen` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-03 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

The 2026-03 segment for the Glenn Diesen lane (`diesen`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Eurasia / multipolar discourse; non-Western institutional / rationality frames when distinct from Mearsheimer’s structural-realist register. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (page cites, transcript rows, or hub URLs) without pretending those pins are already closed.


Cross-lane convergence and tension are notebook-native concepts. For 2026-03, read × mearsheimer, × macgregor, × pape, × sachs as the default **short list** of other experts whose fingerprints commonly collide with `diesen` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

If pages named this expert during 2026-03, the narrative should eventually say **which page** and **what job** the voice did (pressure, validate, narrate) in plain English. If legacy index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate page references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

- [strength: high] **Through-line:** **Iran’s Military Strategy and U.S. Miscalculations** — [Brave New Europe](https://braveneweurope.com/seyed-m-marandi-diesen-irans-military-strategy-and-u-s-miscalculations) — companion to **YouTube** mirrors (re-verify **publish** date).
- [strength: high] **Mechanism:** **Iran Rejects Ceasefire — Demands New Status Quo** — [Brave New Europe](https://braveneweurope.com/seyed-m-marandi-diesen-iran-rejects-ceasefire-demands-new-status-quo) — **ceasefire** language vs **April** Lebanon / nuclear forks — **seam** not merge.
- [strength: medium] **Cross-thread:** **Mercouris** — **Iran war transforms Ukraine war** — [Podscan](https://www.podscan.fm/podcasts/diesen-greater-eurasia-podcast/episodes/mercouris-iran-war-transforms-ukraine-war) — **~21 Mar 2026** class — **orthogonal** to **tri-mind** passes unless operator opts in.
- [strength: medium] **Synthesis:** [Substack — Iran war accelerating end of U.S. dominance](https://glenndiesen.substack.com/p/iran-war-is-accelerating-the-end) — **operator-authored** — tier **B** for causal claims until **cited** primaries align.

Canonical page paths and raw ingest lines live in **Segment 2** below (regenerated each **`thread`** run).
<!-- backfill:diesen:start -->
## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `diesen` from **2026-01-01** through **2026-04-30** (partial April).
**Status:** Reconstructed summary from primary notebook artifacts and best-effort git history; not contemporaneous journal prose.
**Rules:** Dated bullets only; contradictions should be preserved in source materials rather than harmonized here.

### 2026-01

- **2026-01-30** (index) — Marandi on overwhelming retaliation — Greater Eurasia — YouTube.  
  _Source:_ web: `https://www.youtube.com/watch?v=I6XHVDtHRX4`

- **2026-01** — Greater Eurasia — Iran civil unrest — Singju transcript (Marandi).  
  _Source:_ web: `https://singjupost.com/greater-eurasia-podcast-w-seyed-m-marandi-on-irans-civil-unrest-transcript/`

- **2026-01-14** (index) — Macgregor — rising war risks — Singju transcript.  
  _Source:_ web: `https://singjupost.com/greater-eurasia-podcast-w-macgregor-on-rising-war-risks-transcript/`

### 2026-02

- **2026-02-22** (class) — UN Security Council — media manipulation Ukraine war — Brave New Europe / Podscan.  
  _Source:_ web: `https://braveneweurope.com/diesen-at-the-un-security-council-media-manipulation-in-the-ukraine-war`

- **2026-02-24** (class) — NATO’s war of choice / Istanbul sabotage — Podscan.  
  _Source:_ web: `https://www.podscan.fm/podcasts/diesen-greater-eurasia-podcast/episodes/diesen-natos-war-of-choice-the-sabotage-of-the-istanbul-negotiations`

- **2026-02** — Marandi — War for Survival — Podscan.  
  _Source:_ web: `https://www.podscan.fm/podcasts/diesen-greater-eurasia-podcast/episodes/seyed-m-marandi-war-for-survival-irans-strategy-as-war-is-imminent`

### 2026-03

- **2026-03** — Iran’s Military Strategy and U.S. Miscalculations — Brave New Europe.  
  _Source:_ web: `https://braveneweurope.com/seyed-m-marandi-diesen-irans-military-strategy-and-u-s-miscalculations`

- **2026-03** — Iran Rejects Ceasefire — Demands New Status Quo — Brave New Europe.  
  _Source:_ web: `https://braveneweurope.com/seyed-m-marandi-diesen-iran-rejects-ceasefire-demands-new-status-quo`

- **2026-03-21** (class) — Mercouris — Iran war transforms Ukraine war — Podscan.  
  _Source:_ web: `https://www.podscan.fm/podcasts/diesen-greater-eurasia-podcast/episodes/mercouris-iran-war-transforms-ukraine-war`

- **2026-03** — Substack — Iran war accelerating end of U.S. dominance.  
  _Source:_ web: `https://glenndiesen.substack.com/p/iran-war-is-accelerating-the-end`


### 2026-04

- **2026-04** — Ledger mirror 1 (partial month).  
  _Source:_ web: `https://www.youtube.com/watch?v=P_DHMUdOVdo`

<!-- backfill:diesen:end -->
## 2026-04

_Partial month — **2026-04-12** cold ingest (Jiang × Diesen) + **2026-04-14** knots; not a full April ledger._

April folds **petrodollar / Treasury / Hormuz–Malacca** framing beside Islamabad spine — **vi-14** work-jiang lecture verify path — and abstract compare vs Sachs in dedicated knot.


When historical expert context artifacts exist for `diesen` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-04 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

The 2026-04 segment for the Glenn Diesen lane (`diesen`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Eurasia / multipolar discourse; non-Western institutional / rationality frames when distinct from Mearsheimer’s structural-realist register. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (page cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Verification stance for Glenn Diesen in 2026-04 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

Finally, 2026-04 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Eurasia / multipolar discourse; non-Western institutional / rationality frames when distinct from Mearsheimer’s structural-realist register), **pairing map** (× mearsheimer, × macgregor, × pape, × sachs), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

The `diesen` lane’s role (Eurasia / multipolar discourse; non-Western institutional / rationality frames when distinct from Mearsheimer’s structural-realist register) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a page as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

If pages named this expert during 2026-04, the narrative should eventually say **which page** and **what job** the voice did (pressure, validate, narrate) in plain English. If legacy index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate page references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

- [strength: high] **Signal (cold):** Jiang × Glenn Diesen — Iran war as petrodollar / Treasury stress — [YouTube P_DHMUdOVdo](https://www.youtube.com/watch?v=P_DHMUdOVdo) — verify:work-jiang-vi-14 + lecture markdown per ingest line.
- [strength: medium] **Abstract fork:** `diesen-vi14-petrodollar-vs-sachs-hormuz` — Judgment-only; not merged voice with Ritter blockade mechanics.
- [strength: medium] **Lattice:** `ritter-blockade-hormuz-weave` — closure economics seam.

---
<!-- strategy-page:start id="diesen-vi14-petrodollar-vs-sachs-hormuz" date="2026-04-14" watch="hormuz" -->
### Page: diesen-vi14-petrodollar-vs-sachs-hormuz

**Date:** 2026-04-14
**Watch:** hormuz
**Source page:** `diesen-vi14-petrodollar-vs-sachs-hormuz`

# Knot — 2026-04-14 — PH vi-14 Diesen (petrodollar) vs Diesen × Sachs (Hormuz)

| Field | Value |
|--------|--------|
| **Date** | 2026-04-14 |
| **page_id** (machine slug) | `diesen-vi14-petrodollar-vs-sachs-hormuz` — matches basename and the legacy index file [`knot-index.yaml`](../../../knot-index.yaml) |
| **Day block** | [`days.md` § 2026-04-14](../days.md) |

### Page type (**pick per strategy-page** — mixed types allowed)

- [ ] **Thesis page**
- [ ] **Synthesis page**
- [x] **Case page**
- [ ] **Mechanism page**
- [ ] **Watch page**
- [ ] **Link hub**

### Lineage

- **Inbox:** [`daily-strategy-inbox.md`](../../../daily-strategy-inbox.md) — `batch-analysis | 2026-04-14 | Diesen × Sachs` (`crosses:diesen+sachs`); PH **vi-14** `YT | cold` (`thread:diesen`, `P_DHMUdOVdo`); **Diesen × Sachs** `YT | cold` (`thread:diesen` + `thread:sachs`, `S6mlCuvKKIQ`). **Expert threads:** `diesen`, `sachs`.
- **History resonance:** none this pass
- **Civilizational bridge:** none this pass
- **Expert threads:** `thread:diesen` appears **twice** same calendar day — different episodes; `thread:sachs` only on the blockade episode.

### Chronicle

See [`days.md` § Signal — `diesen` × `sachs`](../days.md) and **Weave** lead bullet for 2026-04-14.

### Reflection

**Abstract (this page):** **`diesen`** carries two **2026-04-14** expert threads — **work-jiang PH vi-14** (Jiang × Diesen lecture: petrodollar / chokepoint / Islamabad frame) and **Diesen × Sachs** (Hormuz blockade / DC institutional decay). Same **`expert_id`** on the **`thread:`** line does **not** make them the same **Judgment** object: **`crosses:diesen+sachs`** is **orthogonal** to **vi-14** petrodollar spine; do **not** fold Sachs hypotheses into PH overlay without **verify** tier. Full seam: [`days.md` § Judgment — *Diesen × Sachs vs PH vi-14*](../days.md).

### References

- **PH vi-14 (lecture):** [interviews-14-diesen-iran-war-petrodollar.md](../../../../../../../research/external/work-jiang/lectures/interviews-14-diesen-iran-war-petrodollar.md) · [YouTube](https://www.youtube.com/watch?v=P_DHMUdOVdo)
- **Diesen × Sachs (blockade episode):** [YouTube](https://www.youtube.com/watch?v=S6mlCuvKKIQ)

### Receipt

Pins keep **Glenn Diesen**’s **PH vi-14** lane and the **Glenn Diesen × Jeffrey Sachs** blockade episode tethered to distinct artifacts—**merge-by-mood** is out of scope.

| Pin | Target | URL |
|-----|--------|-----|
| **1** | PH vi-14 lecture (repo body + watch link) | [lecture `.md`](../../../../../../../research/external/work-jiang/lectures/interviews-14-diesen-iran-war-petrodollar.md) · [YouTube `P_DHMUdOVdo`](https://www.youtube.com/watch?v=P_DHMUdOVdo) |
| **2** | Diesen × Sachs episode (same-day **`thread:diesen` + `thread:sachs`**) | [YouTube `S6mlCuvKKIQ`](https://www.youtube.com/watch?v=S6mlCuvKKIQ) |
| **3** | Inbox **`batch-analysis`** spine (`crosses:diesen+sachs`) | [daily-strategy-inbox.md](../../../daily-strategy-inbox.md) — search `Diesen × Sachs` / `crosses:diesen+sachs` |

**Falsifier:** This page’s **orthogonal Judgment** fails if a single authoritative source treats **vi-14** petrodollar claims and **Sachs**-layer **NYT** / **DC-process** hypotheses as **one** merged **Glenn Diesen** verdict **without** separate episode grounding—i.e. **collapse-by-edit** replaces **`crosses:`** discipline.

### Foresight / verify

- **NYT** war-room / **Sachs** capacity claims: **journalistic / hypothesis** until on-record primary or wire tier.
- Re-run **`python3 scripts/strategy_thread.py`** if inbox **`thread:`** lines for these experts change.

---

### Optional legacy index row (copy-paste into [`knot-index.yaml`](../../../knot-index.yaml))

```yaml
  - page_id: `diesen-vi14-petrodollar-vs-sachs-hormuz` (legacy path removed)
    date: "2026-04-14"
    knot_label: diesen-vi14-petrodollar-vs-sachs-hormuz
```

Optional keys (omit if unused): `clusters` (list of strings), `patterns` (list of strings), `note` (string).
<!-- strategy-page:end -->
<!-- strategy-page:start id="ritter-blockade-hormuz-weave" date="2026-04-14" watch="" -->
### Page: ritter-blockade-hormuz-weave

**Date:** 2026-04-14
**Source page:** `scott-ritter-blockade-hormuz-weave`
**Also in:** barnes, davis, jermy, johnson, marandi, mearsheimer, mercouris, parsi, ritter, sachs

### Chronicle

**Davis × Jermy** Deep Dive ([YouTube `etxmqrdm3V0`](https://www.youtube.com/watch?v=etxmqrdm3V0)) — **`thread:davis`**, **`thread:jermy`** — same-episode **blockade** **brinkmanship** + **energy–GDP** cascade; stacks **Ritter** **porous** **blockade** thesis vs **slide-order** macro (**not** wire ORBAT).

### Reflection

**Weave (this page):** **`ritter`** carries **Hormuz** **sea-control** / **blockade** **mechanics** (semantics, hull burden, third-party **hull** behavior, **time** / **storage**). **Same topic**, **non-interchangeable** **expert** **objects:** **`davis`** + **`jermy`** = **executive** **clock** + **systemic** **energy** **lag**; **`diesen`** + **`sachs`** = **talks**/**institutions** **collapse** **frame** on **blockade** (**orthogonal** to **vi-14** per related weave); **`parsi`** + **`davis`** = **EU** **naming** vs **Congress** **lane**; **`barnes`** = **domestic** **TS** **liability** **pole** (inbox **Disclose**/**Truth Social** **chain**) — **not** **Navy** **facts**; **`johnson`** = **digest** **ORBAT** **Haiphong** **roundtable** path ([transcript digest](../../../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)); **`marandi`** / **`mercouris`** / **`mearsheimer`** = **continuity spine** **room** / **geometry** — **triangulate**, **do not** **collapse** into **one** **Ritter** **paragraph** without **labeled** **seams**.

### Foresight

- [Ritter blockade mechanics — verify checklist (2026-04-13)](../../../daily-strategy-inbox.md) (inbox **§ Ritter blockade mechanics**)
- Re-run **`python3 scripts/strategy_thread.py`** after inbox **`thread:`** updates.

---

### Appendix

# Knot — 2026-04-14 — Scott Ritter — Hormuz blockade weave (expert lattice)

| Field | Value |
|--------|--------|
| **Date** | 2026-04-14 |
| **page_id** (machine slug) | `ritter-blockade-hormuz-weave` — matches basename and the legacy index file [`knot-index.yaml`](../../../knot-index.yaml) |
| **Day block** | [`days.md` § 2026-04-14](../days.md) |

### Page type (**pick per strategy-page** — mixed types allowed)

- [ ] **Thesis page**
- [x] **Synthesis page**
- [ ] **Case page**
- [ ] **Mechanism page**
- [ ] **Watch page**
- [x] **Link hub**

### Lineage — **`thread:ritter`** (anchor)

- **Primary ingest:** [`daily-strategy-inbox.md`](../../../daily-strategy-inbox.md) — **`YT | cold: Scott Ritter — Ritter's Rant 085: The Blockade`** (`thread:ritter`) — **blockade** vs **quarantine**, hull count, **Kennedy** analogy, **China/Russia/India** exceptions thesis, porous / political blockade read — URL `TBD-canonical-085` until pinned; **verify** vs **AP/Reuters** hull + **MFA** lines per inbox tail.
- **Same-topic expert threads (indexed only — no new anchors):** pull **`davis`**, **`jermy`**, **`diesen`**, **`sachs`**, **`parsi`**, **`mearsheimer`**, **`mercouris`**, **`barnes`**, **`johnson`**, **`marandi`** only where **`daily-strategy-inbox.md`** / **`days.md`** already carries a **`thread:`** or **continuity-spine** line for **2026-04-12–14** **Hormuz** / **blockade** — this page **weaves**; it does **not** mint **new** **`expert_id`** rows.

### Prior days (same Hormuz arc — cross-links)

| Day | Knot | Notes |
|-----|------|--------|
| **2026-04-12** | `islamabad-hormuz-thesis-weave` | **Islamabad → Hormuz** **Thesis A/B** + **Pape/Parsi/Freeman** **fork** |
| **2026-04-13** | `marandi-ritter-mercouris-hormuz-scaffold` | **Marandi × Ritter × Mercouris** **scaffold** **before** **04-14** **`batch-analysis`** **density** |

### Related weaves (same calendar day — cross-links)

| Knot | `page_id` | Experts (from those files) | Relation to **Ritter** blockade |
|------|----------------|------------------------------|--------------------------------|
| `parsi-davis-war-powers` | `parsi-davis-war-powers` | **`parsi`**, **`davis`** | **Speech-act** / **war-powers** **accountability** vs **Ritter** **sea-control** mechanics — **orthogonal** planes; **Parsi × Davis** `batch-analysis` names **Mercouris**/**Barnes**/**Mearsheimer** as **layers**, not substitutes for **hull** facts. |
| `diesen-vi14-petrodollar-vs-sachs-hormuz` | `diesen-vi14-petrodollar-vs-sachs-hormuz` | **`diesen`**, **`sachs`** | **Diesen × Sachs** **Hormuz blockade** episode ([YouTube `S6mlCuvKKIQ`](https://www.youtube.com/watch?v=S6mlCuvKKIQ)) — **institutional** / **chaos** thesis; **do not** merge **PH vi-14** petrodollar lane with **Ritter** **ORBAT** without **seam**; **Ritter** = **operations** vocabulary, **Sachs** = **DC process** **hypothesis** tier. |
| `mercouris-mearsheimer-lebanon-split` | `mercouris-mearsheimer-lebanon-split` | **`mercouris`**, **`mearsheimer`** | **Lebanon**/**Washington** **fork** — **adjacent** **news week** to **Hormuz** **blockade**; use for **legitimacy vs structure** **language** only — **not** a substitute for **Ritter** **interdiction** **mechanics**. |
| `armstrong-cash-hormuz-digital-dollar-arc` | `armstrong-cash-hormuz-digital-dollar-arc` | **minds** + **Armstrong** X + **Fink**/**BlackRock** + **Congress.gov** | **Money-law / fertilizer-definition** plane — **orthogonal** to **`thread:`** **ORBAT**; **fertilizer** **mood** may **echo** **Jermy** cascade **without** **merging** **quantity** claims. |

### History resonance

none this pass

### Civilizational bridge

none this pass

### References

- **Ritter 085 (pin):** inbox line — `TBD-canonical-085` → replace when canonical **YouTube** ID is fixed.
- **Davis × Jermy (same day):** [YouTube `etxmqrdm3V0`](https://www.youtube.com/watch?v=etxmqrdm3V0) — **`thread:davis`**, **`thread:jermy`**
- **Diesen × Sachs blockade:** [YouTube `S6mlCuvKKIQ`](https://www.youtube.com/watch?v=S6mlCuvKKIQ) — **`thread:diesen`**, **`thread:sachs`**
- **Haiphong / Johnson / Ritter digest:** [transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md](../../../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) — **`thread:johnson`**, **`thread:ritter`** (digest rows)

### Receipt

Pins keep **`ritter`** **mechanics** **distinct** from **speech**/**institution**/**macro** **lanes** on the same **Hormuz** **headline**.

| Pin | Target | URL |
|-----|--------|-----|
| **1** | **Ritter** **Rant 085** (canonical episode) | `TBD` — [inbox `thread:ritter`](../../../daily-strategy-inbox.md) |
| **2** | **Davis × Jermy** Deep Dive (blockade **same week**) | [YouTube](https://www.youtube.com/watch?v=etxmqrdm3V0) |
| **3** | **Related weave** registry (this file’s **cross-links**) | [knot-index.yaml](../../../knot-index.yaml) — search `2026-04-14` |

**Falsifier:** This weave fails if **one** **merged** **Judgment** treats **Ritter** **hull**/**interdiction** **claims** as **fully** **confirmed** by **`parsi`** **EU** **wording**, **`sachs`** **NYT** **room** **hypotheses**, or **`jermy`** **GDP** **slides** **without** **tiered** **verify** — **expert** **lattice** **collapsed** into **mood**.
<!-- strategy-page:end -->
<!-- strategy-expert-thread:start -->
## Machine layer — Extraction (script-maintained)

_Auto-generated from `transcript.md` + **on-disk** and **inbox** `raw-input/` (de-duped union) + `strategy-page` blocks + optional legacy on-disk index rows. **Journal layer** (narrative) lives **above** the **strategy-expert-thread** start HTML comment. The machine-layer HTML block is replaced on each `thread` run._

### Recent transcript material

## 2026-04-26
- Inbox | cold: full text in [`transcript-diesen-escobar-connectivity-wars-multipolarity-2026-04-23.md`](raw-input/2026-04-23/transcript-diesen-escobar-connectivity-wars-multipolarity-2026-04-23.md) (pointer; SSOT raw-input) | thread:diesen
- Inbox | cold: full text in [`transcript-macgregor-diesen-total-war-iran-2026-04-21.md`](raw-input/2026-04-21/transcript-macgregor-diesen-total-war-iran-2026-04-21.md) (pointer; SSOT raw-input) | thread:diesen
- YT | cold: **Glenn Diesen** — **host** / interviewer; **same** **episode** **as** **verbatim** **above** (Baltic/Finland, Article 5, Trump, Iran↔Ukraine spillover) // hook: **paired** **`expert_id`** **per** **commentator-threads** **two-speaker** **rule** | https://www.youtube.com/watch?v=TBD-diesen-ritter-finland-baltic-2026-04 | verify:paired-host+pin-canonical-URL | thread:diesen | grep:Diesen+Greater-Eurasia+Ritter
## 2026-04-25
- YT | cold: **Glenn** **Diesen** **×** **Pepe** **Escobar** — *Connectivity Wars — The U.S. War on Multipolarity* — **aired** **2026-04-23** — **cleaned** **caption** **(inferred** **speakers):** **INSTC** **/ BRI** **/ corridor** **competition** **(IMEC** **dead,** **Qatar–Turkey** **pipe** **dreams),** **Hormuz** **/ Iran** **war** **×** **north–south** **connectivity,** **Chabahar** **/** **Gwadar** **/ India** **/** **China;** **Mackinder** **/ sea** **vs** **land** **frame** **(commentary)** // hook: **`thread:diesen`** **(Escobar** **=** **guest,** **no** **`expert_id`)** **×** **§1e** **/** **§1g** **Eurasia** **connectivity** **—** **full** [raw-input/2026-04-23/transcript-diesen-escobar-connectivity-wars-multipolarity-2026-04-23.md](raw-input/2026-04-23/transcript-diesen-escobar-connectivity-wars-multipolarity-2026-04-23.md) | TBD (pin `watch?v=`) | verify:operator-file+cleaned-caption+guest-not-in-roster+opinion-narrative-tier+not-Record | thread:diesen | EURASIA | IRAN | BRICS | grep:Diesen+Escobar+connectivity+multipolarity+2026-04-23
- YT | cold: **Glenn Diesen** (host — **same** **episode** **as** **Macgregor** **row** **above**) — **multipolar** **/** **“world** **order** **dismantled”** **/** **int’l** **law** **+** **global** **empathy** **for** **Iran;** **Asia** **economic** **shock;** **Europe** **×** **Russia** **/** **Ukraine** **/** **drone** **escalation** **questions;** **Trump** **“victory”** **/ school** **strike** **framing** **—** **not** **merge** **Macgregor** **ORBAT** **without** **seams** // hook: **`thread:diesen`** **Eurasia** **host** **lane** **×** **`thread:macgregor`** **—** **same** **raw** [raw-input/2026-04-21/transcript-macgregor-diesen-total-war-iran-2026-04-21.md](raw-input/2026-04-21/transcript-macgregor-diesen-total-war-iran-2026-04-21.md) | https://www.youtube.com/watch?v=1AZPNUaXJ-k | verify:same+raw+reingest-2026-04-25+host-not-guest+operator-transcript | thread:diesen | Eurasia | grep:Diesen+host+2026-04-21
- YT | cold: **Glenn Diesen** — **host** / interviewer; **same** **episode** **as** **verbatim** **above** (Baltic/Finland, Article 5, Trump, Iran↔Ukraine spillover) // hook: **paired** **`expert_id`** **per** **commentator-threads** **two-speaker** **rule** | https://www.youtube.com/watch?v=TBD-diesen-ritter-finland-baltic-2026-04 | verify:paired-host+pin-canonical-URL | thread:diesen | grep:Diesen+Greater-Eurasia+Ritter
## 2026-04-23
- Inbox | cold: full text in [`transcript-diesen-escobar-connectivity-wars-multipolarity-2026-04-23.md`](raw-input/2026-04-23/transcript-diesen-escobar-connectivity-wars-multipolarity-2026-04-23.md) (pointer; SSOT raw-input) | thread:diesen
## 2026-04-20
- YT | cold: **Glenn Diesen** — **host** / interviewer; **same** **episode** **as** **verbatim** **above** (Baltic/Finland, Article 5, Trump, Iran↔Ukraine spillover) // hook: **paired** **`expert_id`** **per** **commentator-threads** **two-speaker** **rule** | https://www.youtube.com/watch?v=TBD-diesen-ritter-finland-baltic-2026-04 | verify:paired-host+pin-canonical-URL | thread:diesen | grep:Diesen+Greater-Eurasia+Ritter

### Recent raw-input (lane)

_Union of **on-disk** `raw-input/…` files tagged with this expert’s `thread:` and **inbox** lines (same paths de-duped; disk line kept first)._

- [transcript-diesen-escobar-connectivity-wars-multipolarity-2026-04-23.md](raw-input/2026-04-23/transcript-diesen-escobar-connectivity-wars-multipolarity-2026-04-23.md) _on-disk_
- [transcript-macgregor-diesen-total-war-iran-2026-04-21.md](raw-input/2026-04-21/transcript-macgregor-diesen-total-war-iran-2026-04-21.md)

### Page references

- **diesen-vi14-petrodollar-vs-sachs-hormuz** — 2026-04-14 watch=`hormuz`
- **ritter-blockade-hormuz-weave** — 2026-04-14
<!-- strategy-expert-thread:end -->
