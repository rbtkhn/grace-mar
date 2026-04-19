# Expert thread — `mearsheimer`

WORK only; not Record.

**Source:** Human **narrative journal** (below) + [`strategy-expert-mearsheimer-transcript.md`](strategy-expert-mearsheimer-transcript.md) (verbatim ingests) + relevant **knot** files (where this expert’s material was used).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-mearsheimer.md`](strategy-expert-mearsheimer.md) (profile), [`strategy-expert-mearsheimer-transcript.md`](strategy-expert-mearsheimer-transcript.md) (7-day verbatim), [`strategy-expert-mearsheimer-mind.md`](strategy-expert-mearsheimer-mind.md) (long-form mind).

---
## Journal layer — Narrative (operator)

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **knots**, convergence/tension with other **`thread:`** experts, and **Open** pins. The **journal layer** is **not** overwritten by the **`thread`** script._

**Layout:** Stay on **one** `strategy-expert-mearsheimer-thread.md` file. Within the **journal layer**, each **`## YYYY-MM`** heading is a **month segment**. For **2026:** **Segment 1** = January (`## 2026-01`), **Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), **Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** (script-maintained) is **only** the fenced block between the **strategy-expert-thread** HTML start and end comments — do not call that "Segment 2" in the month sense.

_(No narrative distillation yet — add prose above the markers, not inside them.)_

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (quarter-scale or ongoing). **Default:** **at least ~500 words** of **prose** per month-segment (words on non-bullet substantive lines; see `validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the prose minimum and are **not** an equally canonical substitute for the prose-first journal unless the operator opts into ledger-only months (see HTML comment below). To scaffold prose to the minimum from roster metadata, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.

- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id mearsheimer --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`mearsheimer-<start>-to-<end>.md`) plus **per-month** files (`mearsheimer/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.

- **`<!-- backfill:mearsheimer:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.

- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.
## 2026-01


The 2026-01 segment for the John Mearsheimer lane (`mearsheimer`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Offensive realism: security dilemma, Israel structural, great-power geometry. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Typical pairings on file for `mearsheimer` emphasize contrast surfaces: × davis, × mercouris, × diesen, × sachs. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-01 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

Verification stance for John Mearsheimer in 2026-01 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

If knots named this expert during 2026-01, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

When historical expert context artifacts exist for `mearsheimer` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-01 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Cross-lane convergence and tension are notebook-native concepts. For 2026-01, read × davis, × mercouris, × diesen, × sachs as the default **short list** of other experts whose fingerprints commonly collide with `mearsheimer` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

Open pins belong in prose, not only as bullets. For this `mearsheimer` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

- [strength: medium] **Through-line:** Iran as **US–Israel playbook** (upend regime / wreck) and **Gulf** states increasingly treating the **US–Israel tag team** as the **stability threat** — own summary in [Antiwar reprint **2026-01-16**](https://www.antiwar.com/blog/2026/01/16/mearsheimer-on-the-iran-playbook/) of Substack “Iran Playbook”; **Judging Freedom** appearance **15 Jan** cited there.
- [strength: medium] **Mechanism:** **“Old-style imperialism”** vs great-power competition — **SCMP** “Open Questions” interview **19 Jan** — [Substack mirror + PDF](https://mearsheimer.substack.com/p/its-not-great-power-politics-its) (Iran ≠ Venezuela on regime-change difficulty, Greenland, Trump administration).
- [strength: low] **Ambiguity:** Full broadcast transcripts not in-repo — treat pull quotes as **verify-tier** until pinned.
- [strength: medium] **Tension / lattice:** Same Q1 window as **Davis × Mearsheimer** “classic regime change” long-form on [Daniel Davis Deep Dive **2026-01-14**](https://danieldavisdeepdive.substack.com/p/prof-mearsheimer-classic-us) — notebook cross; do not merge with **Mercouris** diplomatic-room reads without seam discipline.
## 2026-02


Finally, 2026-02 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Offensive realism: security dilemma, Israel structural, great-power geometry), **pairing map** (× davis, × mercouris, × diesen, × sachs), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

The 2026-02 segment for the John Mearsheimer lane (`mearsheimer`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Offensive realism: security dilemma, Israel structural, great-power geometry. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Cross-lane convergence and tension are notebook-native concepts. For 2026-02, read × davis, × mercouris, × diesen, × sachs as the default **short list** of other experts whose fingerprints commonly collide with `mearsheimer` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

When historical expert context artifacts exist for `mearsheimer` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-02 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

The `mearsheimer` lane’s role (Offensive realism: security dilemma, Israel structural, great-power geometry) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

Typical pairings on file for `mearsheimer` emphasize contrast surfaces: × davis, × mercouris, × diesen, × sachs. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-02 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

Open pins belong in prose, not only as bullets. For this `mearsheimer` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

- [strength: medium] **Through-line:** **Netanyahu–Trump** **11 Feb** meeting **poor from an Israeli perspective**; **no** apparent military strategy to **win** vs Iran — [A Deep Dive on Iran](https://mearsheimer.substack.com/p/a-deep-dive-on-iran) Substack **14 Feb** (Deep Dive w/ Danny Davis **12 Feb**).
- [strength: medium] **Mechanism:** Critique of **experts** claiming a **clean military fix** for Iran; parallel skepticism on **Ukraine** “upper hand” narrative in same conversation.
- [strength: low] **Ambiguity:** Video vs Substack emphasis — strength capped where only Substack body used here.
- [strength: medium] **Lattice:** Feeds **Mercouris × Mearsheimer** fork (incentives vs speech-acts) — see April [`mercouris-mearsheimer-lebanon-split`](strategy-notebook-knot-2026-04-14-mercouris-mearsheimer-lebanon-split.md); Q1 is **upstream** thesis only.
## 2026-03


Verification stance for John Mearsheimer in 2026-03 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

Typical pairings on file for `mearsheimer` emphasize contrast surfaces: × davis, × mercouris, × diesen, × sachs. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

Finally, 2026-03 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Offensive realism: security dilemma, Israel structural, great-power geometry), **pairing map** (× davis, × mercouris, × diesen, × sachs), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

Open pins belong in prose, not only as bullets. For this `mearsheimer` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

If knots named this expert during 2026-03, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

When historical expert context artifacts exist for `mearsheimer` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-03 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.


Verification stance for John Mearsheimer in 2026-03 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

Typical pairings on file for `mearsheimer` emphasize contrast surfaces: × davis, × mercouris, × diesen, × sachs. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

- [strength: medium] **Through-line:** Iran war **historical analogy** and “what went wrong” — **Chris Hedges Report** interview **11 Mar** — [The Unfolding Disaster in the Gulf](https://mearsheimer.substack.com/p/the-unfolding-disaster-in-the-gulf) Substack **13 Mar**.
- [strength: medium] **Mechanism:** **Piers Morgan Uncensored** **18 Mar** — rare alignment with Piers on trajectory vs **Conricus** optimistic line — [Agreeing with Piers on Iran](https://mearsheimer.substack.com/p/agreeing-with-piers-on-iran) Substack **22 Mar**.
- [strength: low] **Ambiguity:** Broadcast embeds not mirrored in-repo — pin canonical URLs for verify.
- [strength: medium] **Tension:** Structural **off-ramp / blunder** framing vs **`thread:mercouris`** March **surface** (Hormuz headlines, tanker narratives) — compare in **batch-analysis**, do not **voice-merge** in prose.

---

Canonical knot paths and raw ingest lines live in **Segment 2** below (regenerated each **`thread`** run).
<!-- backfill:mearsheimer:start -->
## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `mearsheimer` from **2026-01-01** through **2026-04-30** (partial April).
**Status:** Reconstructed summary from primary notebook artifacts and best-effort git history; not contemporaneous journal prose.
**Rules:** Dated bullets only; contradictions should be preserved in source materials rather than harmonized here.

### 2026-01

- **2026-01-15** — Judging Freedom / Iran playbook (Antiwar reprint cites appearance).  
  _Source:_ web: `https://www.antiwar.com/blog/2026/01/16/mearsheimer-on-the-iran-playbook/`

- **2026-01-19** — SCMP “Open Questions” / imperialism vs great-power politics — Substack.  
  _Source:_ web: `https://mearsheimer.substack.com/p/its-not-great-power-politics-its`

- **2026-01-14** — Daniel Davis Deep Dive — classic U.S. regime change in Iran (cross-appearance).  
  _Source:_ web: `https://danieldavisdeepdive.substack.com/p/prof-mearsheimer-classic-us`

### 2026-02

- **2026-02-12** — Deep Dive on Iran w/ Danny Davis (Substack **14 Feb**).  
  _Source:_ web: `https://mearsheimer.substack.com/p/a-deep-dive-on-iran`

### 2026-03

- **2026-03-11** — Chris Hedges Report lane — Unfolding Disaster in the Gulf — Substack **13 Mar**.  
  _Source:_ web: `https://mearsheimer.substack.com/p/the-unfolding-disaster-in-the-gulf`

- **2026-03-18** — Piers Morgan Uncensored — Agreeing with Piers on Iran — Substack **22 Mar**.  
  _Source:_ web: `https://mearsheimer.substack.com/p/agreeing-with-piers-on-iran`


### 2026-04

- **2026-04** — Notebook knot cross-ref (partial month).  
  _Source:_ notebook: `strategy-notebook-knot-2026-04-14-mercouris-mearsheimer-lebanon-split.md`

- **2026-04** — Notebook knot cross-ref (partial month).  
  _Source:_ notebook: `strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md`

- **2026-04** — Notebook knot cross-ref (partial month).  
  _Source:_ notebook: `strategy-notebook-knot-2026-04-14-ritter-blockade-hormuz-weave.md`

<!-- backfill:mearsheimer:end -->
## 2026-04

_Partial month — Segment 2 is **knot-index** only for April; no standalone Mearsheimer ingest line in machine block at authoring time._

April lattice is **Mercouris × Mearsheimer** (speech-act vs structural incentives) on Lebanon / Hormuz week — scaffold and blockade weaves carry the cross-expert seam; Pape Janssen block adds domestic escalation-trap vocabulary beside same cycle.


Finally, 2026-04 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Offensive realism: security dilemma, Israel structural, great-power geometry), **pairing map** (× davis, × mercouris, × diesen, × sachs), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

Cross-lane convergence and tension are notebook-native concepts. For 2026-04, read × davis, × mercouris, × diesen, × sachs as the default **short list** of other experts whose fingerprints commonly collide with `mearsheimer` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

Open pins belong in prose, not only as bullets. For this `mearsheimer` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

The 2026-04 segment for the John Mearsheimer lane (`mearsheimer`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Offensive realism: security dilemma, Israel structural, great-power geometry. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Typical pairings on file for `mearsheimer` emphasize contrast surfaces: × davis, × mercouris, × diesen, × sachs. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-04 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

Verification stance for John Mearsheimer in 2026-04 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

- [strength: medium] **Fork:** [mercouris-mearsheimer-lebanon-split](strategy-notebook-knot-2026-04-14-mercouris-mearsheimer-lebanon-split.md) — diplomatic surface vs incentive geometry — **do not** voice-merge.
- [strength: medium] **Scaffold:** [marandi-ritter-mercouris-hormuz-scaffold](strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md) — Davis×Freeman×Mearsheimer parallel plane named in knot header.
- [strength: medium] **Lattice:** [ritter-blockade-hormuz-weave](strategy-notebook-knot-2026-04-14-ritter-blockade-hormuz-weave.md) · [pape-janssen-escalation-blockade](strategy-notebook-knot-2026-04-16-pape-janssen-escalation-blockade.md) — blockade calendar vs structural off-ramp framing — tier discipline.

---
<!-- strategy-page:start id="mercouris-mearsheimer-lebanon-split" date="2026-04-14" watch="accountability-language" -->
### Page: mercouris-mearsheimer-lebanon-split

**Date:** 2026-04-14
**Watch:** accountability-language
**Source knot:** strategy-notebook-knot-2026-04-14-mercouris-mearsheimer-lebanon-split.md
**Also in:** mercouris, pape

# Knot — 2026-04-14 — Mercouris × Mearsheimer — Lebanon split (surface vs structure)

| Field | Value |
|--------|--------|
| **Date** | 2026-04-14 |
| **knot_label** (machine slug) | `mercouris-mearsheimer-lebanon-split` — matches basename and [`knot-index.yaml`](../../../knot-index.yaml) |
| **Day block** | [`days.md` § 2026-04-14](../days.md) |

### Page type (**pick per knot** — mixed types allowed)

- [x] **Thesis page**
- [ ] **Synthesis page**
- [ ] **Case page**
- [ ] **Mechanism page**
- [ ] **Watch page**
- [ ] **Link hub**

### Lineage

- **Inbox:** [`daily-strategy-inbox.md`](../../../daily-strategy-inbox.md) — when present, a **`batch-analysis | … | Mercouris × Mearsheimer`** or separate **`thread:mercouris`** / **`thread:mearsheimer`** lines on **Lebanon**/**Israel**/**Washington** **talks** (search `Lebanon`, `Mercouris`, `Mearsheimer`). **Typical pairing:** [strategy-commentator-threads.md](../../../strategy-commentator-threads.md) (`mercouris` × `mearsheimer`).
- **Expert threads:** `mercouris`, `mearsheimer` — **two** **Judgment** **planes**: **diplomatic** **legitimacy** / **room** **narrative** vs **offensive-realist** **incentives** / **alliance** **geometry**; **not** a merged **single** **expert** **object**.
- **History resonance:** none this pass
- **Civilizational bridge:** none this pass

### Signal

See [`days.md` § Signal / § Judgment](../days.md) when **Lebanon**/**Washington** **venue** lines appear beside **Hormuz**/**Iran** **cycle**; this knot **abstracts** **Mercouris**/**Mearsheimer** **fork** only.

### Judgment

**Abstract (this knot):** **Alexander Mercouris** tracks **who sounds credible** in **room** **diplomacy** (**Lebanon–Israel** **framing**, **U.S.** **messaging**, **legitimacy** **choreography**). **John Mearsheimer** tracks **what states can afford** and **how power** **distributes** **incentives** (**alliance** **strain**, **escalation** **geometry**) — **orthogonal** **default**: **speech-act** **success** ≠ **structural** **settlement** **without** **evidence** **coupling**. **Do not** **tri-mind**-merge into one **verdict** in **`days.md`** without **labeled** **Thesis A / B** or **`batch-analysis`** **`crosses:mercouris+mearsheimer`** when ingests exist.

### Links

- **Mind registers (in-voice discipline):** [CIV-MIND-MERCOURIS.md](../../../minds/CIV-MIND-MERCOURIS.md) · [CIV-MIND-MEARSHEIMER.md](../../../minds/CIV-MIND-MEARSHEIMER.md)
- **Tri-mind skill:** [`.cursor/skills/tri-mind/SKILL.md`](../../../../../../../.cursor/skills/tri-mind/SKILL.md) (**A** = Mercouris, **B** = Mearsheimer)
- **Primary / episode pins:** add **Duran** / **Mercouris** **YouTube** or **Mearsheimer** **appearance** URLs here when this knot is **tightened** to a **dated** **show** — **`TBD`** until operator pins.

### Receipt

Pins keep **Mercouris** **legitimacy** **layer** and **Mearsheimer** **structure** **layer** on **separate** **artifacts**—**synthesis** requires **evidence**, not **tone** **matching**.

| Pin | Target | URL |
|-----|--------|-----|
| **1** | Active month **`days.md`** **Judgment** / **Signal** (Lebanon-relevant lines) | [`days.md` § 2026-04-14](../days.md) |
| **2** | **`thread:mercouris`** / **`thread:mearsheimer`** grep surface | [daily-strategy-inbox.md](../../../daily-strategy-inbox.md) |
| **3** | **Mercouris** / **Mearsheimer** **episode** or **transcript** (when scoped to this knot) | `TBD` — pin **canonical** **watch** **URL** |

**Falsifier:** This knot fails if **Lebanon**/**Washington** **progress** is **asserted** from **Mercouris**-class **narrative** **alone** **without** **Mearsheimer**-class **incentive** **checks** (or **vice versa**: **structure** **only** **without** **on-record** **speech** **acts**) — **forced** **merge** **replaces** **Thesis A / B** **discipline**.

### Open / verify

- Add **`batch-analysis | YYYY-MM-DD | Mercouris × Mearsheimer`** to inbox when **both** **`thread:`** ingests land same day.
- **Wire** **Lebanon–Israel** **Washington** **talks** primaries vs **commentary** **only** — tier before **Links-grade** **Judgment**.

---

### Index row (YAML — paste into `knots:` in `knot-index.yaml`)

```yaml
  - path: docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04/knots/strategy-notebook-knot-2026-04-14-mercouris-mearsheimer-lebanon-split.md
    date: "2026-04-14"
    knot_label: mercouris-mearsheimer-lebanon-split
```

Optional keys (omit if unused): `clusters` (list of strings), `patterns` (list of strings), `note` (string).
<!-- strategy-page:end -->

<!-- strategy-expert-thread:start -->
## Machine layer — Extraction (script-maintained)

_Auto-generated from `-transcript.md` + knot index. **Journal layer** (narrative) lives **above** the **strategy-expert-thread** start HTML comment. The machine-layer HTML block is replaced on each `thread` run._

### Knot references

- [strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md](strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md) 2026-04-13 (marandi-ritter-mercouris-hormuz-scaffold) — Marandi×Ritter×Mercouris shared scaffold; Davis×Freeman×Mearsheimer parallel; cross-day to 04-12/04-14
- [strategy-notebook-knot-2026-04-14-mercouris-mearsheimer-lebanon-split.md](strategy-notebook-knot-2026-04-14-mercouris-mearsheimer-lebanon-split.md) 2026-04-14 (mercouris-mearsheimer-lebanon-split) — Abstract Mercouris diplomatic surface vs Mearsheimer incentives; Lebanon fork; Pape lane (escalation-trap / sectarian map) indexes here for expert-thread knot refs
- [strategy-notebook-knot-2026-04-14-armstrong-cash-hormuz-digital-dollar-arc.md](strategy-notebook-knot-2026-04-14-armstrong-cash-hormuz-digital-dollar-arc.md) 2026-04-14 (armstrong-cash-hormuz-digital-dollar-arc) — Synthesis: Barnes/Mercouris/Mearsheimer mind files + Armstrong X + Fink/BlackRock + Congress.gov + Statista/Signal Gulf fertilizer; orthogonal to thread: Hormuz lattice
- [strategy-notebook-knot-2026-04-16-pape-janssen-escalation-blockade.md](strategy-notebook-knot-2026-04-16-pape-janssen-escalation-blockade.md) 2026-04-16 (pape-janssen-escalation-blockade) — Weave D: Pape-primary Janssen trap + blockade calendar + spoiler; same-day Marandi+Blumenthal evidence streams → sister weave C; lattice vs Mearsheimer/Davis
<!-- strategy-expert-thread:end -->
