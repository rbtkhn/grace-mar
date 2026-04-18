# Expert thread — `freeman`

WORK only; not Record.

**Source:** Distilled from [`strategy-expert-freeman-transcript.md`](strategy-expert-freeman-transcript.md) (what the expert said recently) and relevant knots (where that material was used in strategy work).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-freeman.md`](strategy-expert-freeman.md) (profile) and [`strategy-expert-freeman-transcript.md`](strategy-expert-freeman-transcript.md) (7-day verbatim).

---
## Journal layer — Narrative (operator)

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **knots**, convergence/tension with other **`thread:`** experts, and **Open** pins. The **journal layer** is **not** overwritten by the **`thread`** script._

**Layout:** Stay on **one** `strategy-expert-freeman-thread.md` file. Within the **journal layer**, each **`## YYYY-MM`** heading is a **month segment**. For **2026:** **Segment 1** = January (`## 2026-01`), **Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), **Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** (script-maintained) is **only** the fenced block between the **strategy-expert-thread** HTML start and end comments — do not call that "Segment 2" in the month sense.

_(No narrative distillation yet — add prose above the markers, not inside them.)_

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (quarter-scale or ongoing). **Default:** **at least ~500 words** of **prose** per month-segment (words on non-bullet substantive lines; see `validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the prose minimum and are **not** an equally canonical substitute for the prose-first journal unless the operator opts into ledger-only months (see HTML comment below). To scaffold prose to the minimum from roster metadata, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.

- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id freeman --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`freeman-<start>-to-<end>.md`) plus **per-month** files (`freeman/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.

- **`<!-- backfill:freeman:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.

- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.
## 2026-01

January carries **no dated** `thread:` line for Freeman in this notebook snapshot; the lane is **career-diplomat material / alliance framing** separate from papal moral registers — per roster. Hubs are routing anchors only.


When historical expert context artifacts exist for `freeman` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-01 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Cross-lane convergence and tension are notebook-native concepts. For 2026-01, read × parsi, × mercouris, × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (seam, not merge) as the default **short list** of other experts whose fingerprints commonly collide with `freeman` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

Typical pairings on file for `freeman` emphasize contrast surfaces: × parsi, × mercouris, × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (seam, not merge). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-01 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

Verification stance for Charles (“Chas”) Freeman in 2026-01 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

Finally, 2026-01 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Retired career diplomat: inconclusive talks, alliance and material framing (Islamabad as diplomacy-while-war); separate plane from papal moral register), **pairing map** (× parsi, × mercouris, × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (seam, not merge)), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

The 2026-01 segment for the Charles (“Chas”) Freeman lane (`freeman`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Retired career diplomat: inconclusive talks, alliance and material framing (Islamabad as diplomacy-while-war); separate plane from papal moral register. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

- [strength: low] **Identity anchor:** Chas Freeman site + Watson visiting profile (Seed).  
  [chasfreeman.net](https://chasfreeman.net/) · [Watson Institute](https://home.watson.brown.edu/people/faculty/visiting-fellows/chas-freeman)
## 2026-02

February shows **no indexed Q1 primary** in-repo; pair with **`parsi`** / **`mercouris`** only via **labeled** **`batch-analysis`** when diplomacy weeks overlap.


Open pins belong in prose, not only as bullets. For this `freeman` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

Verification stance for Charles (“Chas”) Freeman in 2026-02 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

If knots named this expert during 2026-02, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Typical pairings on file for `freeman` emphasize contrast surfaces: × parsi, × mercouris, × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (seam, not merge). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-02 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

Cross-lane convergence and tension are notebook-native concepts. For 2026-02, read × parsi, × mercouris, × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (seam, not merge) as the default **short list** of other experts whose fingerprints commonly collide with `freeman` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

The `freeman` lane’s role (Retired career diplomat: inconclusive talks, alliance and material framing (Islamabad as diplomacy-while-war); separate plane from papal moral register) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-02, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

- [strength: low] **Long-form pointer:** Example interview URL in profile — verify currency before cite (profile flags this).  
  [YouTube o7RQ_ue6iY0](https://www.youtube.com/watch?v=o7RQ_ue6iY0)
## 2026-03

March remains **scope-only** until transcript rows land; **April** Islamabad–Hormuz weave knots may reference Freeman beside Davis/Mearsheimer scaffolds.


Cross-lane convergence and tension are notebook-native concepts. For 2026-03, read × parsi, × mercouris, × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (seam, not merge) as the default **short list** of other experts whose fingerprints commonly collide with `freeman` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

The `freeman` lane’s role (Retired career diplomat: inconclusive talks, alliance and material framing (Islamabad as diplomacy-while-war); separate plane from papal moral register) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

Open pins belong in prose, not only as bullets. For this `freeman` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-03, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

Finally, 2026-03 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Retired career diplomat: inconclusive talks, alliance and material framing (Islamabad as diplomacy-while-war); separate plane from papal moral register), **pairing map** (× parsi, × mercouris, × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (seam, not merge)), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

Typical pairings on file for `freeman` emphasize contrast surfaces: × parsi, × mercouris, × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (seam, not merge). In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.


Cross-lane convergence and tension are notebook-native concepts. For 2026-03, read × parsi, × mercouris, × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (seam, not merge) as the default **short list** of other experts whose fingerprints commonly collide with `freeman` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

The `freeman` lane’s role (Retired career diplomat: inconclusive talks, alliance and material framing (Islamabad as diplomacy-while-war); separate plane from papal moral register) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

- [strength: low] **Repeat anchor:** chasfreeman.net — not a dated March appearance claim.
<!-- backfill:freeman:start -->
## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `freeman` from **2026-01-01** through **2026-04-30** (partial April).
**Status:** Reconstructed summary; no dated primary lines in the Q1 ledger at authoring time.
**Rules:** Hub anchors only where dated captures are missing.

### 2026-01

- **2026-01** — No dated notebook ingest — personal site hub.  
  _Source:_ web: `https://chasfreeman.net/`

### 2026-02

- **2026-02** — No dated notebook ingest — Watson visiting fellow page.  
  _Source:_ web: `https://home.watson.brown.edu/people/faculty/visiting-fellows/chas-freeman`

### 2026-03

- **2026-03** — No dated notebook ingest — example long-form (verify before cite).  
  _Source:_ web: `https://www.youtube.com/watch?v=o7RQ_ue6iY0`


### 2026-04

- **2026-04** — Notebook knot cross-ref (partial month).  
  _Source:_ notebook: `strategy-notebook-knot-2026-04-12-islamabad-hormuz-thesis-weave.md`

- **2026-04** — Notebook knot cross-ref (partial month).  
  _Source:_ notebook: `strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md`

- **2026-04-17** — Grayzone / Nima — Freeman monologue (Israel strategy, phony ceasefire, Hormuz, GCC hedge, US decay).  
  _Source:_ operator transcript + [strategy-expert-freeman-thread.md](strategy-expert-freeman-thread.md) § Grayzone / Nima — 2026-04-17

<!-- backfill:freeman:end -->
## 2026-04

_Partial month — April **Segment 2** lists **knot refs**; **2026-04-17** adds **Grayzone / Nima** operator transcript + **tri-mind** resolution (see below)._

April uses Freeman as **career-diplomat / alliance-material** plane beside Marandi legitimacy and Ritter mechanics — **inconclusive talks** discipline per knot cross-refs.

### Grayzone / Nima — 2026-04-17 (operator transcript)

**Session title (host copy):** *Amb. Charles Freeman: Israel’s Strategy Just COLLAPSED – Trump Steps In* (intro: **Friday, April 17, 2026**).

**Five theses (distilled for notebook):** (1) **Performative termination** — “ceasefire” / mediation can be **announcement** without **meeting of minds**; **electoral** and **market** **signaling** in an **unverifiable** information space. (2) **Israel strategic bind** — **no** stated **US/Israel** **objectives** **achieved** in Freeman’s read; **Netanyahu** **continuation** incentive; **Lebanon** **occupation / wasteland / annexation** appetite vs **Trump** **ceasefire** **story**; **Washington** talks as **fantasy** **foreign policy** **exercise**. (3) **Hormuz / blockade** — **perception** vs **export** **reality** (e.g. **tanker** **arithmetic** vs **Navy** **redirect** **story**); strait as **Iranian** **permissioning** (“door” metaphor); long-term posited fix: **rules-based** **Iranian–Omani** **management** (**Montreux**-style analogy). (4) **GCC hedge** / **dual containment** legacy / **multi-nodal** drift (**Saudi–Iran** **FM** channel, **UAE**, **Oman**, **Spain** **exemplar**). (5) **US institutional decay** + **Iran** **attrition** / **deterrence** — **Rubio** as **non-coordinating** figure; **Islamabad**-style round as **performance**; **morale** / **retention** claims; **NPT** / **enrichment** / **Hormuz** **rules** as **open** **structural** **issues**.

**Epistemic:** **Commentator monologue** — **quant** claims (**logistic** **flights**, **barrels**, **reserve** **rates**, **interdictions**) are **verify-first** before **Judgment** or **Links-grade** merge.

### Tri-mind resolution (`ab+c`, 2026-04-17)

WORK **operating rules** after **Mercouris / Mearsheimer / Barnes (litigator-close)** on this appearance:

1. **Three tiers, not one voice:** **Legitimacy / staging** (Mercouris) — parallel **performances** **not** **synchronizing**; **incentives / spoiler / exit** (Mearsheimer) — **alliance** **time** **horizons** **split**; **enforceability** (Barnes) — **terms** **unpinned** → **no** **single** **contract** **for** **insurers**, **allies**, or **Congress** until **primaries** **land**.
2. **“Phony ceasefire”** holds as **hypothesis** at **speech** tier; **structural** **read** (**pause** as **instrumental**) **orthogonal** — weave with **explicit** **seam**, not **merged** **verdict**.
3. **Hormuz** — **permissioning** / **“door”** language maps **Barnes** **lane** (published **rules** vs **coercion**); **cross-check** **export** and **interdiction** **metrics** **against** **independent** **series** before **Signal** **lead**.
4. **Netanyahu** **jail** **if** **peace** / **US** **buildup** **numbers** / **Europe** **capabilities** — **tier** as **analyst** **claims** until **wire** or **primary** **receipts**.

Open pins belong in prose, not only as bullets. For this `freeman` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

Cross-lane convergence and tension are notebook-native concepts. For 2026-04, read × parsi, × mercouris, × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (seam, not merge) as the default **short list** of other experts whose fingerprints commonly collide with `freeman` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

If knots named this expert during 2026-04, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

When historical expert context artifacts exist for `freeman` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-04 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-04, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

Finally, 2026-04 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Retired career diplomat: inconclusive talks, alliance and material framing (Islamabad as diplomacy-while-war); separate plane from papal moral register), **pairing map** (× parsi, × mercouris, × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (seam, not merge)), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

Verification stance for Charles (“Chas”) Freeman in 2026-04 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

- [strength: medium] **Thesis weave:** [islamabad-hormuz-thesis-weave](strategy-notebook-knot-2026-04-12-islamabad-hormuz-thesis-weave.md) — Islamabad collapse + Thesis A/B + indexed threads.
- [strength: medium] **Scaffold:** [marandi-ritter-mercouris-hormuz-scaffold](strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md) — Davis×Freeman×Mearsheimer parallel — **seam** vs papal moral register.
- [strength: medium] **2026-04-17 Grayzone / Nima** — operator transcript (session title on file); **tri-mind** **`ab+c`** **resolve** in § **Tri-mind resolution** above — pin canonical **YouTube** when stable.

Canonical knot paths and raw ingest lines live in **Segment 2** below (regenerated each **`thread`** run).

---
<!-- strategy-expert-thread:start -->
## Machine layer — Extraction (script-maintained)

_Auto-generated from `-transcript.md` + knot index. **Journal layer** (narrative) lives **above** the **strategy-expert-thread** start HTML comment. The machine-layer HTML block is replaced on each `thread` run._

### Recent transcript material

## 2026-04-17
- YT | cold: **Amb. Charles Freeman** (Grayzone / Nima, **2026-04-17** — *Israel’s Strategy Just COLLAPSED – Trump Steps In*) — **Phony ceasefire** / **Trump** **rhetoric** vs **reality**; **Israel** **aims unmet** + **Netanyahu** **bind**; **Hormuz** **perception** vs **export** **story** + **GCC hedge**; **US** **decay** / **Rubio**; **Iran** **attrition** // hook: **five theses** + **tri-mind** **`ab+c`** **resolve** — [strategy-expert-freeman-thread.md](strategy-expert-freeman-thread.md) § **Grayzone / Nima** + **Tri-mind resolution**; crosses **Davis×Freeman×Mearsheimer** [scaffold](strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md) | https://www.youtube.com/watch?v=TBD-grayzone-freeman-2026-04-17 | verify:operator-transcript+pin-canonical-URL | thread:freeman | grep:Freeman+Grayzone+2026-04-17

### Knot references

- [strategy-notebook-knot-2026-04-12-islamabad-hormuz-thesis-weave.md](strategy-notebook-knot-2026-04-12-islamabad-hormuz-thesis-weave.md) 2026-04-12 (islamabad-hormuz-thesis-weave) — Islamabad collapse + Thesis A/B + indexed threads; cross-links to 04-13 scaffold + 04-14 Ritter weave
- [strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md](strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md) 2026-04-13 (marandi-ritter-mercouris-hormuz-scaffold) — Marandi×Ritter×Mercouris shared scaffold; Davis×Freeman×Mearsheimer parallel; cross-day to 04-12/04-14
<!-- strategy-expert-thread:end -->
