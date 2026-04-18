# Expert thread — `barnes`

WORK only; not Record.

**Source:** Distilled from [`strategy-expert-barnes-transcript.md`](strategy-expert-barnes-transcript.md) (what the expert said recently) and relevant knots (where that material was used in strategy work).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-barnes.md`](strategy-expert-barnes.md) (profile), [`strategy-expert-barnes-transcript.md`](strategy-expert-barnes-transcript.md) (7-day verbatim), [`strategy-expert-barnes-mind.md`](strategy-expert-barnes-mind.md) (long-form mind).

---
## Journal layer — Narrative (operator)

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **knots**, convergence/tension with other **`thread:`** experts, and **Open** pins. The **journal layer** is **not** overwritten by the **`thread`** script._

**Layout:** Stay on **one** `strategy-expert-barnes-thread.md` file. Within the **journal layer**, each **`## YYYY-MM`** heading is a **month segment**. For **2026:** **Segment 1** = January (`## 2026-01`), **Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), **Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** (script-maintained) is **only** the fenced block between the **strategy-expert-thread** HTML start and end comments — do not call that "Segment 2" in the month sense.

_(No narrative distillation yet — add prose above the markers, not inside them.)_

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (quarter-scale or ongoing). **Default:** **at least ~500 words** of **prose** per month-segment (words on non-bullet substantive lines; see `validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the prose minimum and are **not** an equally canonical substitute for the prose-first journal unless the operator opts into ledger-only months (see HTML comment below). To scaffold prose to the minimum from roster metadata, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.

- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id barnes --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`barnes-<start>-to-<end>.md`) plus **per-month** files (`barnes/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.

- **`<!-- backfill:barnes:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.

- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.
## 2026-01

January has **no dated** notebook ingest for Barnes in this Q1 snapshot; the lane is **domestic liability / executive chain / TS framing** — not **`pape`** polling — per roster. Law-firm hubs are anchors only.


Verification stance for Robert Barnes in 2026-01 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-01, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

Open pins belong in prose, not only as bullets. For this `barnes` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

Finally, 2026-01 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Constitutional, civil rights, and criminal tax trial lawyer (Barnes Law LLP); political–legal commentator; co-host *Viva & Barnes: Law for the People* (with Viva Frei).), **pairing map** (× pape; × davis (institutional skepticism seam); topic forks (JTN-style “card” vs satirical spiral) in batch-analysis without a second expert), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

If knots named this expert during 2026-01, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Cross-lane convergence and tension are notebook-native concepts. For 2026-01, read × pape; × davis (institutional skepticism seam); topic forks (JTN-style “card” vs satirical spiral) in batch-analysis without a second expert as the default **short list** of other experts whose fingerprints commonly collide with `barnes` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

- [strength: low] **Identity anchor:** Barnes Law LLP + X (Seed).  
  [barneslawllp.com](https://www.barneslawllp.com/) · [X @barnes_law](https://x.com/barnes_law)
## 2026-02

February shows **no indexed Q1 primary** in-repo; **`baud`** / NATO mandate crosses require explicit seams — do not collapse registers.


When historical expert context artifacts exist for `barnes` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-02 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

If knots named this expert during 2026-02, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

The `barnes` lane’s role (Constitutional, civil rights, and criminal tax trial lawyer (Barnes Law LLP); political–legal commentator; co-host *Viva & Barnes: Law for the People* (with Viva Frei).) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

Typical pairings on file for `barnes` emphasize contrast surfaces: × pape; × davis (institutional skepticism seam); topic forks (JTN-style “card” vs satirical spiral) in batch-analysis without a second expert. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-02 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

Finally, 2026-02 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Constitutional, civil rights, and criminal tax trial lawyer (Barnes Law LLP); political–legal commentator; co-host *Viva & Barnes: Law for the People* (with Viva Frei).), **pairing map** (× pape; × davis (institutional skepticism seam); topic forks (JTN-style “card” vs satirical spiral) in batch-analysis without a second expert), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

The 2026-02 segment for the Robert Barnes lane (`barnes`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Constitutional, civil rights, and criminal tax trial lawyer (Barnes Law LLP); political–legal commentator; co-host *Viva & Barnes: Law for the People* (with Viva Frei).. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

- [strength: low] **Long-form example:** Podbean interview (profile — verify URL before cite).  
  [Podbean — Robert Barnes interview](https://unstructured.podbean.com/e/barnes-is-a-high-profile-constitutional-lawyer-and-political-gambler-defending-amy-cooper/)
## 2026-03

March remains **scope-only**; **April** machine lines capture Hormuz / Truth Social executive framing — Q1 is **identity + routing** only.


Typical pairings on file for `barnes` emphasize contrast surfaces: × pape; × davis (institutional skepticism seam); topic forks (JTN-style “card” vs satirical spiral) in batch-analysis without a second expert. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

The 2026-03 segment for the Robert Barnes lane (`barnes`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Constitutional, civil rights, and criminal tax trial lawyer (Barnes Law LLP); political–legal commentator; co-host *Viva & Barnes: Law for the People* (with Viva Frei).. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Verification stance for Robert Barnes in 2026-03 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

When historical expert context artifacts exist for `barnes` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-03 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Open pins belong in prose, not only as bullets. For this `barnes` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

If knots named this expert during 2026-03, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.


Typical pairings on file for `barnes` emphasize contrast surfaces: × pape; × davis (institutional skepticism seam); topic forks (JTN-style “card” vs satirical spiral) in batch-analysis without a second expert. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

- [strength: low] **Repeat anchor:** About page — not a March appearance claim.
<!-- backfill:barnes:start -->
## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `barnes` from **2026-01-01** through **2026-04-30** (partial April).
**Status:** Reconstructed summary; no dated primary lines in the Q1 ledger at authoring time.
**Rules:** Hub anchors only where dated captures are missing.

### 2026-01

- **2026-01** — No dated notebook ingest — firm site hub.  
  _Source:_ web: `https://www.barneslawllp.com/`

### 2026-02

- **2026-02** — No dated notebook ingest — X profile pointer.  
  _Source:_ web: `https://x.com/barnes_law`

### 2026-03

- **2026-03** — No dated notebook ingest — About page.  
  _Source:_ web: `https://www.barneslawllp.com/about`


### 2026-04

- **2026-04** — Ledger mirror 1 (partial month).  
  _Source:_ web: `https://x.com/barnes_law`

<!-- backfill:barnes:end -->
## 2026-04

_Partial month — **2026-04-12** X ingest on executive / TS / Hormuz domestic fork; **2026-04-17** Larry Johnson **Countercurrent** YT (Barnes — White House / Vance / Iran overlap); blockade weave knot **2026-04-14**._

April tracks **domestic liability** pole — Truth Social / executive chain framing on Hormuz blockade rhetoric — beside Islamabad thesis weave; **not** merged with Pape escalation-trap vocabulary without labeled seam. **04-17** adds long-form **U.S. politics** **room** narrative (cognition / staff–executive / **Congress**–money brake) with **Iran** blockade / **Islamabad** **lanes** as **second** **object** in same audio — **seam** from **§1h**.

**Excerpt audit:** [barnes-countercurrent-2026-04-17-verbatim.md](barnes-countercurrent-2026-04-17-verbatim.md) **collapses** long runtime spans in **`[...]`**; **themes** **named** **only** **inside** **collapsed** **bridges** **or** **post-**`[...]` **summary** **lines** **are** **not** **excerpt-audited** **here** — **restore** **unabridged** **transcript** **or** **independent** **wires** **before** **treating** **those** **claims** **as** **Judgment-grade**.

Finally, 2026-04 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Constitutional, civil rights, and criminal tax trial lawyer (Barnes Law LLP); political–legal commentator; co-host *Viva & Barnes: Law for the People* (with Viva Frei).), **pairing map** (× pape; × davis (institutional skepticism seam); topic forks (JTN-style “card” vs satirical spiral) in batch-analysis without a second expert), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-04, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

Typical pairings on file for `barnes` emphasize contrast surfaces: × pape; × davis (institutional skepticism seam); topic forks (JTN-style “card” vs satirical spiral) in batch-analysis without a second expert. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-04 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

When historical expert context artifacts exist for `barnes` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-04 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

If knots named this expert during 2026-04, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

The `barnes` lane’s role (Constitutional, civil rights, and criminal tax trial lawyer (Barnes Law LLP); political–legal commentator; co-host *Viva & Barnes: Law for the People* (with Viva Frei).) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

- [strength: medium] **Signal (cold):** @barnes_law — “Trump doubles down on dumb”; QT Disclose.tv re TS post (Hormuz blockade, toll, mines) — [X @barnes_law](https://x.com/barnes_law) — verify:pin-exact-status-URL+archive-Truth-Social-primary.
- [strength: medium] **2026-04-17 — Larry Johnson × Robert Barnes (YT, *Countercurrent*):** Barnes **C-plane** on **executive** **state** + **staff** **dynamics** (**Susie Wiles** negative-info reversal, **NYT** leak path); **Vance** **ceasefire** / **10 points** / **Witkoff–Kushner** vs **Driscoll** **State**/**Defense** lane; **Iran** **side** **shock** at **VP** **authority** limits; **Navy** **“mall cop”** **Hormuz** + **incentives** to **feed** **success** **to** **avoid** **escalation**; **electoral** **tsunami** / **House** **money** **brake**; **Hegseth**/**Bessent**/**Rubio** **survival** **reads**; **farmer** **supply** **shock**. **Cross:** **`thread:johnson`** **host**; **`thread:davis`** **/** **`thread:ritter`** **Iran** **week** **—** **explicit** **seams**. **Tier:** **analyst** **/** **room** **hypothesis**, **not** **Pentagon** **primary**. Verbatim (excerpted): [barnes-countercurrent-2026-04-17-verbatim.md](barnes-countercurrent-2026-04-17-verbatim.md); [strategy-expert-barnes-transcript.md](strategy-expert-barnes-transcript.md) **2026-04-17**.
- [strength: medium] **Knot lattice:** [islamabad-hormuz-thesis-weave](knots/strategy-notebook-knot-2026-04-12-islamabad-hormuz-thesis-weave.md) · [ritter-blockade-hormuz-weave](knots/strategy-notebook-knot-2026-04-14-ritter-blockade-hormuz-weave.md).

Canonical knot paths and raw ingest lines live in **Segment 2** below (regenerated each **`thread`** run).

---
<!-- strategy-expert-thread:start -->
## Machine layer — Extraction (script-maintained)

_Auto-generated from `-transcript.md` + knot index. **Journal layer** (narrative) lives **above** the **strategy-expert-thread** start HTML comment. The machine-layer HTML block is replaced on each `thread` run._

### Recent transcript material

## 2026-04-17
- YT | cold: **Larry Johnson** (*Countercurrent*) × **Robert Barnes** — *What the HELL is going on in the White House?* — US politics: executive cognition / room dynamics; **Vance** vs **Trump** on ceasefire **10 points**; **Witkoff**/**Kushner** vs **Driscoll** lane; **Iran** “VP no authority”; **Navy** “mall cop” blockade + **false** success feed; **polling**/**Congress** brake; **Hegseth**/**Bessent**; farmer supply shock; **work-politics** domestic fork // hook: **§1e** adjacent; stack **04-17** Iran **threads** with **labeled** **seam** — not §1h | https://www.youtube.com/watch?v=TBD-johnson-barnes-white-house-2026-04 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17 | thread:barnes | grep:Barnes+White+House+Vance+Iran+blockade+25th
**Full transcript (excerpted; operator may replace with unabridged):** [barnes-countercurrent-2026-04-17-verbatim.md](barnes-countercurrent-2026-04-17-verbatim.md)
Title: Robert Barnes | What the HELL is going on in the White House? — YouTube (Countercurrent / Larry Johnson)
- YT | cold: **Larry Johnson** (*Countercurrent*) × **Robert Barnes** — *What the HELL is going on in the White House?* — **US politics** **focus:** executive **cognition** / **staff** **dynamics** (**Wiles**, **NYT** leak path); **Vance** **ceasefire** **/** **10** **points** **vs** **Trump** **rug** **pull**; **Witkoff–Kushner** **vs** **Driscoll** **lane**; **Iran** **“VP** **no** **authority”**; **Navy** **Hormuz** **“mall** **cop”** + **incentive** to **feed** **success**; **electoral** **tsunami** **/** **House** **funding** **brake**; **Hegseth**/**Bessent**; **farmer** **supply** **shock** // hook: **work-politics** **domestic** **fork** **+** **Iran** **week** **overlap** — **seam** **§1e** **/** **§1h**; verbatim **excerpt** **[barnes-countercurrent-2026-04-17-verbatim.md](barnes-countercurrent-2026-04-17-verbatim.md)** | https://www.youtube.com/watch?v=TBD-johnson-barnes-white-house-2026-04 | verify:operator-transcript+pin-canonical-URL+aired:2026-04-17 | thread:barnes | grep:Barnes+White+House+Vance+Iran+blockade
- batch-analysis | 2026-04-17 | **Barnes × Johnson (YT) — US politics room × Iran week** | **Tension-first:** **`thread:barnes`** **long-form** **domestic-liability** **+** **White** **House** **process** **(C-plane** **hypothesis)** **—** **not** **§1e** **text** **and** **not** **Pentagon** **primary.** **Same** **calendar** **day** **as** **Hormuz** **/** **Islamabad** **expert** **stack** **—** **cross** **`thread:davis`**, **`thread:johnson`** **(Davis** **×** **Johnson** **earlier** **YT),** **`thread:ritter`** **with** **explicit** **plane** **tags** **(room** **vs** **ORBAT** **vs** **FM).** **Falsifiers:** **named** **official** **statements,** **vote** **counts,** **Navy** **press,** **TS** **screenshots.** | crosses:barnes+johnson
## 2026-04-12
- `X | cold: @barnes_law — “Trump doubles down on dumb”; QT Disclose.tv summarizing executive TS post (Hormuz blockade in/out, toll interdiction in international waters, mine clearing, escalation rhetoric) // hook: third **domestic** pole on Hormuz lever vs Solomon “card” / Martenson spiral; aligns §1e + notebook domestic-fork Judgment | https://x.com/barnes_law | verify:pin-exact-status-URL+archive-Truth-Social-primary | thread:barnes`

### Knot references

- [strategy-notebook-knot-2026-04-12-islamabad-hormuz-thesis-weave.md](strategy-notebook-knot-2026-04-12-islamabad-hormuz-thesis-weave.md) 2026-04-12 (islamabad-hormuz-thesis-weave) — Islamabad collapse + Thesis A/B + indexed threads; cross-links to 04-13 scaffold + 04-14 Ritter weave
- [strategy-notebook-knot-2026-04-14-ritter-blockade-hormuz-weave.md](strategy-notebook-knot-2026-04-14-ritter-blockade-hormuz-weave.md) 2026-04-14 (ritter-blockade-hormuz-weave) — Ritter blockade mechanics + sister knots + indexed threads same topic; weave_count from knot_seam_metrics.py (outgoing knot links)
<!-- strategy-expert-thread:end -->
