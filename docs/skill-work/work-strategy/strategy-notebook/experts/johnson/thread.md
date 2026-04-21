# Expert thread — `johnson`

WORK only; not Record.

**Source:** Distilled from [`strategy-expert-johnson-transcript.md`](strategy-expert-johnson-transcript.md) (what the expert said recently) and relevant knots (where that material was used in strategy work).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-johnson.md`](strategy-expert-johnson.md) (profile) and [`strategy-expert-johnson-transcript.md`](strategy-expert-johnson-transcript.md) (7-day verbatim).

---
## Journal layer — Narrative (operator)

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **knots**, convergence/tension with other **`thread:`** experts, and **Open** pins. The **journal layer** is **not** overwritten by the **`thread`** script._

**Layout:** Stay on **one** `strategy-expert-johnson-thread.md` file. Within the **journal layer**, each **`## YYYY-MM`** heading is a **month segment**. For **2026:** **Segment 1** = January (`## 2026-01`), **Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), **Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** (script-maintained) is **only** the fenced block between the **strategy-expert-thread** HTML start and end comments — do not call that "Segment 2" in the month sense.

_(No narrative distillation yet — add prose above the markers, not inside them.)_

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (quarter-scale or ongoing). **Default:** **at least ~500 words** of **prose** per month-segment (words on non-bullet substantive lines; see `validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the prose minimum and are **not** an equally canonical substitute for the prose-first journal unless the operator opts into ledger-only months (see HTML comment below). To scaffold prose to the minimum from roster metadata, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.

- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id johnson --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`johnson-<start>-to-<end>.md`) plus **per-month** files (`johnson/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.

- **`<!-- backfill:johnson:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.

- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.
## 2026-01

January has **no dated** notebook `thread:` row for Johnson in this Q1 snapshot; the lane is **ex-CIA material / ORBAT / Hormuz geometry** beside Haiphong–Ritter roundtables — per roster. Hubs are anchors only.


Verification stance for Larry Johnson in 2026-01 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

Typical pairings on file for `johnson` emphasize contrast surfaces: × ritter, × davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-01 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

If knots named this expert during 2026-01, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Cross-lane convergence and tension are notebook-native concepts. For 2026-01, read × ritter, × davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) as the default **short list** of other experts whose fingerprints commonly collide with `johnson` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

The `johnson` lane’s role (Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

When historical expert context artifacts exist for `johnson` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-01 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Finally, 2026-01 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)), **pairing map** (× ritter, × davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

- [strength: low] **Identity anchor:** Sonar21 + Substack + X (Seed).  
  [sonar21.com](https://sonar21.com/) · [larrycjohnson.substack.com](https://larrycjohnson.substack.com/) · [X @LarrySonar21](https://x.com/LarrySonar21)
## 2026-02

February shows **no indexed Q1 primary** in-repo; **`ritter`** / **`davis`** crosses stay **seam-labeled** when the same week needs material detail.


Cross-lane convergence and tension are notebook-native concepts. For 2026-02, read × ritter, × davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) as the default **short list** of other experts whose fingerprints commonly collide with `johnson` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

The `johnson` lane’s role (Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

Finally, 2026-02 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)), **pairing map** (× ritter, × davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

The 2026-02 segment for the Larry Johnson lane (`johnson`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables). That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

When historical expert context artifacts exist for `johnson` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-02 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-02, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

- [strength: low] **Digest pointer (April-heavy):** Haiphong / Ritter / Johnson digest is **not** a February dated line — future operator cross-link only.  
  [transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)
## 2026-03

March remains **thin** here; **April** machine extraction references **F-15 / Isfahan** narrative math — Q1 is **identity + routing** only.


Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-03, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

The 2026-03 segment for the Larry Johnson lane (`johnson`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables). That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Finally, 2026-03 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)), **pairing map** (× ritter, × davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

Typical pairings on file for `johnson` emphasize contrast surfaces: × ritter, × davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

The `johnson` lane’s role (Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.


Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-03, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

The 2026-03 segment for the Larry Johnson lane (`johnson`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables). That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

- [strength: low] **Repeat anchor:** Substack hub — no implied posting calendar.
<!-- backfill:johnson:start -->
## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `johnson` from **2026-01-01** through **2026-04-30** (partial April).
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
  _Source:_ notebook: `marandi-ritter-mercouris-hormuz-scaffold``

- **2026-04** — Notebook knot cross-ref (partial month).  
  _Source:_ notebook: `ritter-blockade-hormuz-weave``

<!-- backfill:johnson:end -->
## 2026-04

_Partial month — **2026-04-10** digest §B line + **2026-04-17** Davis×Johnson YT (Hormuz / blockade dual-register) + **2026-04-20** Judging Freedom overlap row + Hormuz scaffold / blockade knots; not calendar-complete._

April centers **F-15 / Isfahan “rescue”** deployment narrative and C-130 / Little Bird load math from Haiphong–Ritter–Johnson digest — **same digest §B** as Ritter ORBAT skepticism lane. **2026-04-20** **Judging Freedom** names **Larry Johnson** as reporter (**two sources**) on **CJCS Caine** / **nuclear** **codes** (**hypothesis** **tier**) — **distinct** **from** digest **§B** **Johnson** **F-15/Isfahan** **ORBAT** **lane** (**same** **name**, **different** **speech** **act**); seam in [`days.md` § 2026-04-20](../../chapters/2026-04/days.md#2026-04-20).


Verification stance for Larry Johnson in 2026-04 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

If knots named this expert during 2026-04, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Typical pairings on file for `johnson` emphasize contrast surfaces: × ritter, × davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-04 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

The 2026-04 segment for the Larry Johnson lane (`johnson`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables). That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Cross-lane convergence and tension are notebook-native concepts. For 2026-04, read × ritter, × davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) as the default **short list** of other experts whose fingerprints commonly collide with `johnson` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

Finally, 2026-04 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Ex-CIA / material and ORBAT emphasis: force structure, Hormuz geometry, F-15/Isfahan raid narrative reconstructions (Haiphong–Ritter roundtables)), **pairing map** (× ritter, × davis; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

- [strength: medium] **Overlap (2026-04-20 — not digest §B):** **Judging Freedom** — **[YouTube `geWpX8w7BNU`](https://www.youtube.com/watch?v=geWpX8w7BNU)** (*Who Controls Hormuz?*, **2026-04-20**) **Johnson** **on-mic:** **Saturday** **White** **House** **meeting**, **Trump** **nuclear** **codes**, **Gen.** **Caine** **refusal** **/** **“head** **down”** **—** **orthogonal** **to** **[digest §B](../../../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)** **F-15/Isfahan** **ORBAT** **math**; **NYT** **(4/7)** **via** **[Substack 4/9](https://larrycjohnson.substack.com/p/trump-got-played-by-israel-and-the)** **for** **Caine-in-room** **read** **—** **see** **[`days.md` § 2026-04-20](../../chapters/2026-04/days.md#2026-04-20)** **Receipts** **table**.
- [strength: medium] **Mechanism:** YT cold **2026-04-10** — F-15/Isfahan rescue narrative; deployment ~Mar 10–11; load-math scenarios — path: [transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md](../../../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) — verify:operator-transcript-digest.
- [strength: medium] **2026-04-17 — Countercurrent × Robert Barnes** (*What the HELL is going on in the White House?*): Johnson **hosts** Barnes on **US politics** / **White House** **process** (executive cognition **frame**, **Vance**/**ceasefire**/**Witkoff–Kushner**, **Navy** Hormuz **“mall cop”**, **electoral** brake) — **`thread:barnes`** **primary** **analytic** **voice**; Johnson = **interviewer**. Verbatim excerpt: [barnes-countercurrent-2026-04-17-verbatim.md](barnes-countercurrent-2026-04-17-verbatim.md); **`crosses:barnes+johnson`**.
- [strength: medium] **2026-04-17 — Daniel Davis × Larry Johnson** (*HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages*): Johnson stresses **dual messaging** — Trump “Strait open” alongside **blockade** on **Iran**; **IFM / spokesman** lines on **Lebanon** contingency and **three passage conditions** (commercial-only, Iran-designated routes, coordination); **military** contact “WTF” lane; **Bessent** re-sanctions same day as ceasefire; **Islamabad** mediated by **Pakistan** with **China** in the story; Davis’s **three-option** endgame (10-point diplomacy vs **Keane**-style escalation vs sanctions long game) with Johnson predicting **escalation** and **Gulf** pressure as a possible de-escalation lever. **C-plane:** Johnson uses **maximal clinical language** on Trump (**detached**, **delusional**, removal call) — **analyst rhetoric**, not §1h; keep **separate** from **`@araghchi` / `@s_m_marandi`** primaries and from **Ritter** 04-17 **ego/theater** Iran segment until explicit **seam** in Judgment. Verbatim: [strategy-expert-johnson-transcript.md](strategy-expert-johnson-transcript.md) **2026-04-17**; inbox: [daily-strategy-inbox.md](daily-strategy-inbox.md) (same-day scratch). **Cross:** `thread:davis` same episode; **`ritter`** **2026-04-17** Diesen (Iran block).
- [strength: medium] **Knot lattice:** `marandi-ritter-mercouris-hormuz-scaffold` · `ritter-blockade-hormuz-weave`.

Canonical knot paths and raw ingest lines live in **Segment 2** below (regenerated each **`thread`** run).

---
<!-- strategy-page:start id="marandi-ritter-mercouris-hormuz-scaffold" date="2026-04-13" watch="hormuz" -->
### Page: marandi-ritter-mercouris-hormuz-scaffold

**Date:** 2026-04-13
**Watch:** hormuz
**Source page:** `marandi-ritter-mercouris-hormuz-scaffold`
**Also in:** davis, freeman, marandi, mearsheimer, mercouris, parsi, ritter

### Judgment

**Weave:** **Mercouris** = **institutional / analyst-constellation / zugzwang** language; **Marandi** = **Iranian red lines** + **wire-verify** roster (**Ghalibaf** head; **Larijani** = transcript **misname**); **Ritter** = **USN mechanics** + **faith invective** lane. **Davis × Freeman × Mearsheimer** = **systemic / bargaining / alliance-cost** folds — **parallel** **Ritter ego-reduction** **lane** until primaries show sequence ([`days.md`](../days.md#2026-04-13)). **Do not** collapse **leadership-psychology** into **Links** without **`narrative-escalation`** + primaries. **Rome–faith registers** (Marandi ecumenical vs Ritter invective vs **SkyVirginSon** vs **Milad**) — **parallel legitimacy combat** — **not** Hormuz **material** **row** without **seam**.

### Open

- Pin **canonical** episode URLs for **Breaking Points**, **The Duran**, **Judging Freedom**, **Daniel Davis Deep Dive** (Freeman, Mearsheimer), **Napolitano × Johnson** per [`days.md` Open](../days.md#2026-04-13).

---

### Technical appendix

# Knot — 2026-04-13 — Marandi × Ritter × Mercouris — Hormuz scaffold (expert lattice)

| Field | Value |
|--------|--------|
| **Date** | 2026-04-13 |
| **knot_label** (machine slug) | `marandi-ritter-mercouris-hormuz-scaffold` — matches basename and [`knot-index.yaml`](../../../knot-index.yaml) |
| **Day block** | [`days.md` § 2026-04-13](../days.md#2026-04-13) |

### Page type (**pick per knot** — mixed types allowed)

- [ ] **Thesis page**
- [x] **Synthesis page**
- [ ] **Case page**
- [ ] **Mechanism page**
- [ ] **Watch page**
- [x] **Link hub**

### Lineage — **triple anchor** (same Judgment sentence)

- **`thread:marandi`** — *Why the Iran Talks Failed* — channel-authority, structural deadlocks (stock / program / Hormuz governance), **Lebanon–Hormuz** linkage, **Easter ecumenical** register vs wire lane — episode URL **operator to pin** per [`days.md`](../days.md#2026-04-13).
- **`thread:ritter`** — **Judging Freedom** (*Who Controls Hormuz?*) — **porous blockade**, picket vs boarding, third-country hulls, **Trump–Pope** narrative-escalation segment — **lane-split** from Marandi — URL **operator to pin**.
- **`thread:mercouris`** — **The Duran** 2026-04-13 monologue — Islamabad recap, blockade/Keane lineage, **zugzwang**, multilateral tickers — **verify each chain** before one arc — URL **operator to pin**.

**Same showrunner, structural lanes (not interchangeable):** **`davis`** Deep Dive × **`freeman`** (process failure, ROE, Bessent vs recession — URL TBD); × **`mearsheimer`** (15 vs 10 point frames, bargaining asymmetry, allies clips — URL TBD). **`thread:parsi`** — Breaking Points / Quincy — Ravid red-lines leak tier — **not** WH primary.

**Process overlap:** **`thread:johnson`** × Mercouris (Napolitano / Johnson digest vs Duran monologue) — **strip to process + price** for parity; **park** Bab el-Mandeb / pipeline under verify ([`days.md` Judgment](../days.md#2026-04-13)).

### History resonance

none this pass

### Civilizational bridge

none this pass

### Cross-day links

| Direction | Target | Relation |
|-----------|--------|----------|
| **Prior day** | `islamabad-hormuz-thesis-weave` | **Thesis A/B** + **Pape/Parsi/Freeman** **fork** **before** this **scaffold** **densifies**. |
| **Next day** | `ritter-blockade-hormuz-weave` | **Ritter**-centered **04-14** lattice + **Parsi×Davis** / **Diesen×Sachs** / **Mercouris×Mearsheimer** **knot** files. |
| **Day prose** | [`days.md` § 2026-04-14](../days.md#2026-04-14) | **Continuity spine** **explicitly** **stacks** **04-12–04-14** **`thread:`** **carries**. |

### Links

- [daily-strategy-inbox.md](../../../daily-strategy-inbox.md) — **Primary pulls (2026-04-13)** · **Ritter blockade checklist** (paste-grade)
- [Al Jazeera — Islamabad talks unfolded](https://www.aljazeera.com/news/2026/4/13/how-the-us-iran-talks-in-islamabad-unfolded)
- [Vatican News — Grand Mosque Algiers (2026-04-13)](https://www.vaticannews.va/en/pope/news/2026-04/pope-leo-apostolic-journey-algeria-grand-mosque-algiers-dialogue.html) — tier-A; **Trump–Leo** fold **tier split** per day **Judgment**
- [rome-persia-legitimacy-signal-check.md](../../../rome-persia-legitimacy-signal-check.md)
- **Episodes (pin):** Breaking Points (Parsi), The Duran (Mercouris), Judging Freedom (Ritter), Davis Deep Dive (Freeman, Mearsheimer), Johnson stack — **`operator to pin`** strings in [`days.md` Links / Open](../days.md#2026-04-13)

### Receipt

| Pin | Target | URL / pointer |
|-----|--------|----------------|
| **1** | **Wire** — Islamabad timeline | [Al Jazeera](https://www.aljazeera.com/news/2026/4/13/how-the-us-iran-talks-in-islamabad-unfolded) |
| **2** | **Tier-A** Holy See — **Grand Mosque** | [Vatican News](https://www.vaticannews.va/en/pope/news/2026-04/pope-leo-apostolic-journey-algeria-grand-mosque-algiers-dialogue.html) |
| **3** | **Inbox** checklist + **episode** queue | [daily-strategy-inbox.md](../../../daily-strategy-inbox.md) — Ritter mechanics / Mercouris verify hooks |

**Falsifier:** One **merged** arc treats **Mercouris** **multilateral** **tickers** + **Johnson** **OOB** **skepticism** + **Marandi** **ecumenical** **register** + **Ritter** **hull** **claims** as **one** **voice** **without** **seams** — **lattice** **collapsed**.
<!-- strategy-page:end -->

<!-- strategy-page:start id="ritter-blockade-hormuz-weave" date="2026-04-14" watch="" -->
### Page: ritter-blockade-hormuz-weave

**Date:** 2026-04-14
**Source page:** `scott-ritter-blockade-hormuz-weave`
**Also in:** barnes, davis, diesen, jermy, marandi, mearsheimer, mercouris, parsi, ritter, sachs

### Signal

**Davis × Jermy** Deep Dive ([YouTube `etxmqrdm3V0`](https://www.youtube.com/watch?v=etxmqrdm3V0)) — **`thread:davis`**, **`thread:jermy`** — same-episode **blockade** **brinkmanship** + **energy–GDP** cascade; stacks **Ritter** **porous** **blockade** thesis vs **slide-order** macro (**not** wire ORBAT).

### Judgment

**Weave (this knot):** **`ritter`** carries **Hormuz** **sea-control** / **blockade** **mechanics** (semantics, hull burden, third-party **hull** behavior, **time** / **storage**). **Same topic**, **non-interchangeable** **expert** **objects:** **`davis`** + **`jermy`** = **executive** **clock** + **systemic** **energy** **lag**; **`diesen`** + **`sachs`** = **talks**/**institutions** **collapse** **frame** on **blockade** (**orthogonal** to **vi-14** per sister knot); **`parsi`** + **`davis`** = **EU** **naming** vs **Congress** **lane**; **`barnes`** = **domestic** **TS** **liability** **pole** (inbox **Disclose**/**Truth Social** **chain**) — **not** **Navy** **facts**; **`johnson`** = **digest** **ORBAT** **Haiphong** **roundtable** path ([transcript digest](../../../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)); **`marandi`** / **`mercouris`** / **`mearsheimer`** = **continuity spine** **room** / **geometry** — **triangulate**, **do not** **collapse** into **one** **Ritter** **paragraph** without **labeled** **seams**.

### Open

- [Ritter blockade mechanics — verify checklist (2026-04-13)](../../../daily-strategy-inbox.md) (inbox **§ Ritter blockade mechanics**)
- Re-run **`python3 scripts/strategy_thread.py`** after inbox **`thread:`** updates.

---

### Technical appendix

# Knot — 2026-04-14 — Scott Ritter — Hormuz blockade weave (expert lattice)

| Field | Value |
|--------|--------|
| **Date** | 2026-04-14 |
| **knot_label** (machine slug) | `ritter-blockade-hormuz-weave` — matches basename and [`knot-index.yaml`](../../../knot-index.yaml) |
| **Day block** | [`days.md` § 2026-04-14](../days.md) |

### Page type (**pick per knot** — mixed types allowed)

- [ ] **Thesis page**
- [x] **Synthesis page**
- [ ] **Case page**
- [ ] **Mechanism page**
- [ ] **Watch page**
- [x] **Link hub**

### Lineage — **`thread:ritter`** (anchor)

- **Primary ingest:** [`daily-strategy-inbox.md`](../../../daily-strategy-inbox.md) — **`YT | cold: Scott Ritter — Ritter's Rant 085: The Blockade`** (`thread:ritter`) — **blockade** vs **quarantine**, hull count, **Kennedy** analogy, **China/Russia/India** exceptions thesis, porous / political blockade read — URL `TBD-canonical-085` until pinned; **verify** vs **AP/Reuters** hull + **MFA** lines per inbox tail.
- **Same-topic expert threads (indexed only — no new anchors):** pull **`davis`**, **`jermy`**, **`diesen`**, **`sachs`**, **`parsi`**, **`mearsheimer`**, **`mercouris`**, **`barnes`**, **`johnson`**, **`marandi`** only where **`daily-strategy-inbox.md`** / **`days.md`** already carries a **`thread:`** or **continuity-spine** line for **2026-04-12–14** **Hormuz** / **blockade** — this knot **weaves**; it does **not** mint **new** **`expert_id`** rows.

### Prior days (same Hormuz arc — cross-links)

| Day | Knot | Notes |
|-----|------|--------|
| **2026-04-12** | `islamabad-hormuz-thesis-weave` | **Islamabad → Hormuz** **Thesis A/B** + **Pape/Parsi/Freeman** **fork** |
| **2026-04-13** | `marandi-ritter-mercouris-hormuz-scaffold` | **Marandi × Ritter × Mercouris** **scaffold** **before** **04-14** **`batch-analysis`** **density** |

### Sister knots (same calendar day — cross-links)

| Knot | `knot_label` | Experts (from those files) | Relation to **Ritter** blockade |
|------|----------------|------------------------------|--------------------------------|
| `parsi-davis-war-powers` | `parsi-davis-war-powers` | **`parsi`**, **`davis`** | **Speech-act** / **war-powers** **accountability** vs **Ritter** **sea-control** mechanics — **orthogonal** planes; **Parsi × Davis** `batch-analysis` names **Mercouris**/**Barnes**/**Mearsheimer** as **layers**, not substitutes for **hull** facts. |
| `diesen-vi14-petrodollar-vs-sachs-hormuz` | `diesen-vi14-petrodollar-vs-sachs-hormuz` | **`diesen`**, **`sachs`** | **Diesen × Sachs** **Hormuz blockade** episode ([YouTube `S6mlCuvKKIQ`](https://www.youtube.com/watch?v=S6mlCuvKKIQ)) — **institutional** / **chaos** thesis; **do not** merge **PH vi-14** petrodollar lane with **Ritter** **ORBAT** without **seam**; **Ritter** = **operations** vocabulary, **Sachs** = **DC process** **hypothesis** tier. |
| `mercouris-mearsheimer-lebanon-split` | `mercouris-mearsheimer-lebanon-split` | **`mercouris`**, **`mearsheimer`** | **Lebanon**/**Washington** **fork** — **adjacent** **news week** to **Hormuz** **blockade**; use for **legitimacy vs structure** **language** only — **not** a substitute for **Ritter** **interdiction** **mechanics**. |
| `armstrong-cash-hormuz-digital-dollar-arc` | `armstrong-cash-hormuz-digital-dollar-arc` | **minds** + **Armstrong** X + **Fink**/**BlackRock** + **Congress.gov** | **Money-law / fertilizer-definition** plane — **orthogonal** to **`thread:`** **ORBAT**; **fertilizer** **mood** may **echo** **Jermy** cascade **without** **merging** **quantity** claims. |

### History resonance

none this pass

### Civilizational bridge

none this pass

### Links

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
| **3** | **Sister knot** registry (this file’s **cross-links**) | [knot-index.yaml](../../../knot-index.yaml) — search `2026-04-14` |

**Falsifier:** This weave fails if **one** **merged** **Judgment** treats **Ritter** **hull**/**interdiction** **claims** as **fully** **confirmed** by **`parsi`** **EU** **wording**, **`sachs`** **NYT** **room** **hypotheses**, or **`jermy`** **GDP** **slides** **without** **tiered** **verify** — **expert** **lattice** **collapsed** into **mood**.
<!-- strategy-page:end -->
<!-- strategy-expert-thread:start -->
## Machine layer — Extraction (script-maintained)

_Auto-generated from `-transcript.md` + `strategy-page` blocks in this thread + optional knot-index rows (legacy). **Journal layer** (narrative) lives **above** the **strategy-expert-thread** start HTML comment. The machine-layer HTML block is replaced on each `thread` run._

### Recent transcript material

## 2026-04-18
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- batch-analysis | 2026-04-17 | **Barnes × Johnson (YT) — US politics room × Iran week** | **Tension-first:** **`thread:barnes`** **long-form** **domestic-liability** **+** **White** **House** **process** **(C-plane** **hypothesis)** **—** **not** **§1e** **text** **and** **not** **Pentagon** **primary.** **Same** **calendar** **day** **as** **Hormuz** **/** **Islamabad** **expert** **stack** **—** **cross** **`thread:davis`**, **`thread:johnson`** **(Davis** **×** **Johnson** **earlier** **YT),** **`thread:ritter`** **with** **explicit** **plane** **tags** **(room** **vs** **ORBAT** **vs** **FM).** **Falsifiers:** **named** **official** **statements,** **vote** **counts,** **Navy** **press,** **TS** **screenshots.** | crosses:barnes+johnson
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
    Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
    Guests: Lt. Col. Daniel Davis & Larry Johnson
    Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
    The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
    Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
    Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
    What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
    Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
    You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
    Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
    “The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
    Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
    And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
    He also laid out three conditions:
    Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
    Ships must pass through routes designated by Iran (meaning Iran retains control).
    Ship passage must be coordinated with Iranian forces responsible for it.
    So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
    What does that mean going forward?
    Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
    I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
    Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
    Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
    On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
    Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
    Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
    This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
    Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
    Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
    The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
    This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
    Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
    Daniel Davis: As I see it, there are three main options for how this war could end.
    Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
    This would be the best outcome for the world and actually has a chance of working. What do you think?
    Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
    Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
    Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
    Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
    Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
    Daniel Davis: The wild card in all of this is Israel. What role will they play?
    Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
    The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
    Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
    Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
    Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
    Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
    Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
    Larry Johnson: All right, my brother. We’ll see you later
## 2026-04-17
- YT | cold: **Daniel Davis** × **Larry Johnson** — *HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages* — dual-register Trump TS vs IRI Lebanon/Hormuz conditions; Bessent sanctions; military “WTF”; three-option endgame; Johnson strong C-plane on Trump // hook: stack 04-17 §1h + Ritter Diesen Iran segment — seams not one Judgment | https://www.youtube.com/watch?v=TBD-davis-johnson-hormuz-2026-04-17 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17+Truth-Social-primary | thread:johnson | grep:Hormuz+Johnson+Davis+blockade+Bessent
Title: HORMUZ OPENING, CEASEFIRE ENDING: Conflicting Messages
Guests: Lt. Col. Daniel Davis & Larry Johnson
Daniel Davis: President Trump has announced that the Strait of Hormuz is open. That's great news. Hopefully this means the war is coming to an end — hopefully by next Wednesday when the current ceasefire period ends.
The Iranian Foreign Minister, Abbas Araghchi, also said yes, the Strait is open, but it is contingent upon the ceasefire in Lebanon. So we're good to go.
Now there are real problems with that, because what does it actually mean for the Strait to be open? What does the Iranian side say it means versus what President Trump says it means? And even before the ink dries on these social media posts, we’ve already got contradictions.
Larry, let me properly introduce you: Larry Johnson, former CIA analyst, runs Son of the New American Revolution, and a great friend of the show.
What was the first thing you thought when you heard that both President Trump and the Iranian side announced — within minutes of each other — that the Strait of Hormuz was open?
Larry Johnson: They’re not paying attention to what the U.S. government is actually saying. I’ve been talking to folks in the military and they’re going, “WTF, what is going on?”
You say the Strait of Hormuz is open, right? But then Trump says the naval blockade is still in full effect. So if the blockade is still in effect, then the Strait is not really open.
Daniel Davis: Let me show you what President Trump posted this morning at 9:27:
“The Strait of Hormuz is completely open and ready for business and full passage. But the naval blockade — the American naval blockade — will remain in full force and effect as it pertains only to Iran.”
Then the Iranian Foreign Ministry spokesman posted something similar to what Araghchi said: this is contingent upon the implementation of certain terms and conditions for the ceasefire in Lebanon.
And here’s the rub: if the naval blockade continues, it will be considered a violation of the ceasefire and passage through the Strait of Hormuz will be closed again.
He also laid out three conditions:
Ships must be commercial — passage of military ships is prohibited, and ships/cargo cannot be linked to belligerent states.
Ships must pass through routes designated by Iran (meaning Iran retains control).
Ship passage must be coordinated with Iranian forces responsible for it.
So Trump says the Strait is fully open — except it’s only open for what we want to come out, while Iran stays blocked. Iran is saying it’s either all open or none of it is open.
What does that mean going forward?
Larry Johnson: Iran is the only one in a position to keep it closed. The United States can’t open it. I was watching Gordon Chang and that other guy, Quinn, drawing parallels to the Malacca Strait. That’s nonsense. Iran has shore-based cruise missiles, ballistic missiles, underwater drones, surface drones, and aerial drones. They can close the Strait whenever they want without even putting ships out there. You don’t have that capability in the Malacca Strait.
I thought we might actually be on the verge of an exit ramp after the Hezbollah-Israel ceasefire. Then I saw what Scott Bessent (Treasury Secretary) did yesterday — they reimposed sanctions on Iran the very same day they announced a ceasefire.
Four weeks ago they lifted sanctions on Iranian oil and on Russia to restore market stability. Now they double down on sanctions. One of Iran’s 10-point demands is that all sanctions must be lifted — and it’s not negotiable.
Is there nobody in the Trump administration who understands how contradictory these messages are? Iran is not going to surrender on that point.
On top of that, the talks in Islamabad happened largely because of Chinese influence with Pakistan — and Bessent threatens China. The Chinese are pissed off. I think they’ve reached their limit. There’s not going to be a meeting between Xi Jinping and Donald Trump.
Daniel Davis: Trump also posted: “Iran has agreed to never close the Strait of Hormuz again. It will no longer be used as a weapon against the world.” Then he thanked Pakistan, said the deal is not tied to Lebanon, claimed Iran with the help of the USA is removing all sea mines (there’s no evidence of that), and said NATO offered help but he told them to stay away because they’re a paper tiger.
Another post said the USA will get all the “nuclear dust” created by our B2 bombers, and no money will exchange hands in any way.
This morning there were reports of a possible deal to unfreeze $20 billion of Iranian assets in exchange for this “nuclear dust.” What do you make of all this? How is any of this supposed to work? Is there any truth to it?
Larry Johnson: Donald Trump is detached from reality. He is living in a fantasy world and none of the people around him are willing to tell him the truth.
Just because he writes something on Truth Social doesn’t make it true. He is delusional. If your mother or elderly parent was acting like this, you wouldn’t let them drive. This guy is capable of starting a nuclear war.
The Strait of Hormuz is not “wide open.” It is under Iranian control. We have no control over it. Our blockade is miles offshore. You’ve seen the photos of Marines on the ships — they’re not even getting full rations. When 20–23-year-old Marines aren’t being fed properly, you’ve got serious problems.
This is a total failure of leadership. Officers are supposed to eat last. Instead, it looks like the officers eat first. That’s not how you treat troops you expect to put their lives on the line.
Trump has zero empathy. He’s divorced from reality. The American people need to stand up. He must be removed from office as soon as possible. This is dangerous.
Daniel Davis: As I see it, there are three main options for how this war could end.
Option 1: Trump agrees to base a diplomatic agreement on Iran’s 10-point plan. At minimum that would mean lifting sanctions, providing security guarantees, some form of reparations, and limited uranium enrichment/reprocessing (Iran sees even limited enrichment as an act of sovereignty).
This would be the best outcome for the world and actually has a chance of working. What do you think?
Larry Johnson: That would be the ideal outcome, but based on what we’ve seen in the last 24 hours — doubling down on sanctions and maintaining the blockade while claiming the Strait is open — that option is now off the table.
Daniel Davis: Option 2: Trump doubles down. He listens to people like Jack Keane who say “give nothing, take everything.” He launches a massive air campaign to try to crush Iran once and for all — obliterating energy infrastructure, bridges, and the economy — hoping to force total submission.
Larry Johnson: Unfortunately, I think that’s where this is headed. Within Trump’s delusional mindset, he believes the U.S. is winning militarily and just needs to finish the job. But the United States cannot actually destroy Iran. We have deluded ourselves about our military potency. We don’t have that capability anymore.
Daniel Davis: Option 3: Trump recognizes the limits of power and plays the long game — ramping up sanctions (“Operation Economic Fury”) and trying to outlast Iran economically, betting the U.S. can suffer longer than Iran can.
Larry Johnson: That’s pure magical thinking. Look at the case studies: Cuba (66 years of sanctions — didn’t work), North Korea, Russia — none of them surrendered. Iran has options: access to the Caspian Sea and Russia to the north, Turkmenistan, Pakistan, etc. We’re not sealing them off. This ignores reality.
Daniel Davis: The wild card in all of this is Israel. What role will they play?
Larry Johnson: Israel will try to destroy any prospect of an agreement if they can. Their words don’t match their capabilities. They’ve destroyed buildings in Gaza but after nearly three years still haven’t defeated Hamas. They’re bogged down in southern Lebanon fighting over towns like Bint Jbeil and taking significant casualties from Hezbollah.
The ceasefire in Lebanon was largely a cynical move to use the Lebanese army against Hezbollah. Israel will never accept Hezbollah as anything other than a terrorist group. They’re trying to build on a cracked foundation.
Daniel Davis: Iran has made its position very clear. This isn’t a real-estate negotiation where you can haggle. They want sanctions lifted, U.S. military out of the Gulf, reparations, and an end to attacks on Hezbollah and Lebanon. It’s black or white.
Larry Johnson: Exactly. Iran is the Islamic Republic of Iran. They have deep religious faith and a history of enduring pain. They will not surrender. They have alternative routes for oil and trade. They’ve also shown the world they can disrupt the Strait of Hormuz, making themselves a player that must be taken seriously. Countries like Italy and Spain are already distancing themselves from U.S. and Israeli policy.
Daniel Davis: What about our allies in the Gulf States? They’re losing massive amounts of money every day this stays closed. At what point do they pressure Trump to go back to Option 1 and get the Strait fully open?
Larry Johnson: I think that pressure is coming. Russia and China are actively courting the Gulf states, telling them they have alternatives and don’t have to keep taking the abuse. The Gulf Arabs are like an abused spouse being offered counseling. The UAE may be too far gone, but the Saudis are starting to reconsider. That may be one of the few things that could move the needle away from escalation.
Daniel Davis: We’ll find out soon enough. Larry, really appreciate you making time on such a busy day. Thanks for coming on.
Larry Johnson: All right, my brother. We’ll see you later
- batch-analysis | 2026-04-17 | **Barnes × Johnson (YT) — US politics room × Iran week** | **Tension-first:** **`thread:barnes`** **long-form** **domestic-liability** **+** **White** **House** **process** **(C-plane** **hypothesis)** **—** **not** **§1e** **text** **and** **not** **Pentagon** **primary.** **Same** **calendar** **day** **as** **Hormuz** **/** **Islamabad** **expert** **stack** **—** **cross** **`thread:davis`**, **`thread:johnson`** **(Davis** **×** **Johnson** **earlier** **YT),** **`thread:ritter`** **with** **explicit** **plane** **tags** **(room** **vs** **ORBAT** **vs** **FM).** **Falsifiers:** **named** **official** **statements,** **vote** **counts,** **Navy** **press,** **TS** **screenshots.** | crosses:barnes+johnson

### Page references

- **marandi-ritter-mercouris-hormuz-scaffold** — 2026-04-13 watch=`hormuz`
- **ritter-blockade-hormuz-weave** — 2026-04-14
<!-- strategy-expert-thread:end -->
