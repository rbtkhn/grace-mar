# Expert thread — `blumenthal`

WORK only; not Record.

**Source:** Distilled from [`strategy-expert-blumenthal-transcript.md`](strategy-expert-blumenthal-transcript.md) (what the expert said recently) and relevant knots (where that material was used in strategy work).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-blumenthal.md`](strategy-expert-blumenthal.md) (profile) and [`strategy-expert-blumenthal-transcript.md`](strategy-expert-blumenthal-transcript.md) (7-day verbatim).

---
## Journal layer — Narrative (operator)

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **knots**, convergence/tension with other **`thread:`** experts, and **Open** pins. The **journal layer** is **not** overwritten by the **`thread`** script._

**Layout:** Stay on **one** `strategy-expert-blumenthal-thread.md` file. Within the **journal layer**, each **`## YYYY-MM`** heading is a **month segment**. For **2026:** **Segment 1** = January (`## 2026-01`), **Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), **Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** (script-maintained) is **only** the fenced block between the **strategy-expert-thread** HTML start and end comments — do not call that "Segment 2" in the month sense.

_(No narrative distillation yet — add prose above the markers, not inside them.)_

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (quarter-scale or ongoing). **Default:** **at least ~500 words** of **prose** per month-segment (words on non-bullet substantive lines; see `validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the prose minimum and are **not** an equally canonical substitute for the prose-first journal unless the operator opts into ledger-only months (see HTML comment below). To scaffold prose to the minimum from roster metadata, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.

- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id blumenthal --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`blumenthal-<start>-to-<end>.md`) plus **per-month** files (`blumenthal/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.

- **`<!-- backfill:blumenthal:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.

- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.
## 2026-01

January has **no dated** notebook ingest for Blumenthal in this Q1 snapshot; the lane is **Grayzone / elite-access / Middle East policy critique** — distinct from **`mate`** investigative ownership focus — per roster.


The `blumenthal` lane’s role (Grayzone / antiwar pole: U.S. Middle East policy and elite-access critique; Lebanon/Gulf narrative framing; media-layer “who engineered what” — access and backchannel claims stay hypothesis-grade until primary tape or on-record source) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

The 2026-01 segment for the Max Blumenthal (@MaxBlumenthal) lane (`blumenthal`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Grayzone / antiwar pole: U.S. Middle East policy and elite-access critique; Lebanon/Gulf narrative framing; media-layer “who engineered what” — access and backchannel claims stay hypothesis-grade until primary tape or on-record source. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Typical pairings on file for `blumenthal` emphasize contrast surfaces: × mate, × parsi, × mercouris, × marandi, × freeman. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-01 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

If knots named this expert during 2026-01, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Open pins belong in prose, not only as bullets. For this `blumenthal` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

Cross-lane convergence and tension are notebook-native concepts. For 2026-01, read × mate, × parsi, × mercouris, × marandi, × freeman as the default **short list** of other experts whose fingerprints commonly collide with `blumenthal` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

- [strength: low] **Identity anchor:** Grayzone author index + X + Patreon (Seed).  
  [thegrayzone.com — Max Blumenthal](https://thegrayzone.com/author/blumenthal/) · [X @MaxBlumenthal](https://x.com/MaxBlumenthal)
## 2026-02

February shows **no indexed Q1 primary** in-repo; Lebanon / Gulf access claims stay **hypothesis-grade** until primary tape — per profile discipline.


Verification stance for Max Blumenthal (@MaxBlumenthal) in 2026-02 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

Finally, 2026-02 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: Grayzone / antiwar pole: U.S. Middle East policy and elite-access critique; Lebanon/Gulf narrative framing; media-layer “who engineered what” — access and backchannel claims stay hypothesis-grade until primary tape or on-record source), **pairing map** (× mate, × parsi, × mercouris, × marandi, × freeman), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

Open pins belong in prose, not only as bullets. For this `blumenthal` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

Cross-lane convergence and tension are notebook-native concepts. For 2026-02, read × mate, × parsi, × mercouris, × marandi, × freeman as the default **short list** of other experts whose fingerprints commonly collide with `blumenthal` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

When historical expert context artifacts exist for `blumenthal` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-02 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-02, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

If knots named this expert during 2026-02, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

- [strength: low] **Support hub:** Patreon — not a dated February post list.  
  [patreon.com/grayzone](https://www.patreon.com/grayzone)
## 2026-03

March remains **thin** on calendar rows here; **`marandi`** / **`parsi`** seams need explicit labels when the same week is folded.


Cross-lane convergence and tension are notebook-native concepts. For 2026-03, read × mate, × parsi, × mercouris, × marandi, × freeman as the default **short list** of other experts whose fingerprints commonly collide with `blumenthal` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

Verification stance for Max Blumenthal (@MaxBlumenthal) in 2026-03 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

The 2026-03 segment for the Max Blumenthal (@MaxBlumenthal) lane (`blumenthal`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Grayzone / antiwar pole: U.S. Middle East policy and elite-access critique; Lebanon/Gulf narrative framing; media-layer “who engineered what” — access and backchannel claims stay hypothesis-grade until primary tape or on-record source. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

If knots named this expert during 2026-03, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Typical pairings on file for `blumenthal` emphasize contrast surfaces: × mate, × parsi, × mercouris, × marandi, × freeman. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

The `blumenthal` lane’s role (Grayzone / antiwar pole: U.S. Middle East policy and elite-access critique; Lebanon/Gulf narrative framing; media-layer “who engineered what” — access and backchannel claims stay hypothesis-grade until primary tape or on-record source) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a knot as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

- [strength: low] **Repeat anchor:** Grayzone author page — scope unchanged.

<!-- backfill:blumenthal:start -->
## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `blumenthal` from **2026-01-01** through **2026-04-30** (partial April).
**Status:** Reconstructed summary; no dated primary lines in the Q1 ledger at authoring time.
**Rules:** Hub anchors only where dated captures are missing.

### 2026-01

- **2026-01** — No dated notebook ingest — Grayzone author index.  
  _Source:_ web: `https://thegrayzone.com/author/blumenthal/`

### 2026-02

- **2026-02** — No dated notebook ingest — X profile pointer.  
  _Source:_ web: `https://x.com/MaxBlumenthal`

### 2026-03

- **2026-03** — No dated notebook ingest — Patreon hub.  
  _Source:_ web: `https://www.patreon.com/grayzone`


### 2026-04

- **2026-04** — Ledger mirror 1 (partial month).  
  _Source:_ web: `https://thegrayzone.com/author/blumenthal/`

- **2026-04** — Ledger mirror 2 (partial month).  
  _Source:_ web: `https://x.com/MaxBlumenthal`

<!-- backfill:blumenthal:end -->
## 2026-04

_Partial month — no April machine line for Blumenthal in-repo; **Grayzone / elite-access** lane — hub anchors only._


Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-04, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for knots, for open pins, or for the next verify pass.

The 2026-04 segment for the Max Blumenthal (@MaxBlumenthal) lane (`blumenthal`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on Grayzone / antiwar pole: U.S. Middle East policy and elite-access critique; Lebanon/Gulf narrative framing; media-layer “who engineered what” — access and backchannel claims stay hypothesis-grade until primary tape or on-record source. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (knot cites, transcript rows, or hub URLs) without pretending those pins are already closed.

When historical expert context artifacts exist for `blumenthal` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-04 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Verification stance for Max Blumenthal (@MaxBlumenthal) in 2026-04 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

If knots named this expert during 2026-04, the narrative should eventually say **which knot** and **what job** the voice did (pressure, validate, narrate) in plain English. If knot index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate knot references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Open pins belong in prose, not only as bullets. For this `blumenthal` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

- [strength: low] **Identity anchor:** [Grayzone — Blumenthal](https://thegrayzone.com/author/blumenthal/) · [X @MaxBlumenthal](https://x.com/MaxBlumenthal) — not a dated April appearance list.
- [strength: low] **Note:** Distinct from **mate** investigative ownership focus — roster seam.

Canonical knot paths and raw ingest lines live in **Segment 2** below (regenerated each **`thread`** run).

---
<!-- strategy-page:start id="marandi-blumenthal-jf-primary" date="2026-04-16" watch="" -->
### Page: marandi-blumenthal-jf-primary

**Date:** 2026-04-16
**Source knot:** strategy-notebook-knot-2026-04-16-marandi-blumenthal-jf-primary.md
**Also in:** marandi

# Knot — 2026-04-16 — Marandi-primary: Breaking Points × Blumenthal (Judging Freedom)

WORK only; not Record.

| Field | Value |
|--------|--------|
| **Date** | 2026-04-16 |
| **knot_label** (machine slug) | `marandi-blumenthal-jf-primary` — matches basename and [`knot-index.yaml`](../../../knot-index.yaml) |
| **Day block** | [`days.md` § 2026-04-16](../days.md#2026-04-16) |
| **Primary expert (`thread:`)** | `marandi` — **Signal / Judgment** follow **Iranian English process + red-line register** first. |

### Page type

- [x] **Synthesis page** — **Marandi** spine + **Blumenthal** as **US/UK amplifier**; **not** the Pape-primary trap page (see [weave D](strategy-notebook-knot-2026-04-16-pape-janssen-escalation-blockade.md)).

### Lineage

- **Weave option C** (strategy session): Marandi-primary; Blumenthal = domestic/media amplifier; **Pape** = **validate fork** only → pointer to **same-day** [Pape × Janssen knot](strategy-notebook-knot-2026-04-16-pape-janssen-escalation-blockade.md), **not** merged analysis here.
- **Inbox:** [`daily-strategy-inbox.md`](../../../daily-strategy-inbox.md) **`## 2026-04-16`** — **`- BP |`** Marandi row; **Judging Freedom — Max Blumenthal — 2026-04-16** (operator session; paste to inbox when ready).
- **Expert threads:** `thread:marandi` · `thread:blumenthal`
- **Sister:** [04-13 Marandi × Ritter × Mercouris scaffold](strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md)

---

### Signal

**`thread:marandi` — Breaking Points (2026-04-16):** Tehran-remote **process** read — **full delegation authority** vs **US executive** channel **tethered** to **Netanyahu** / late pivots; **Hormuz** / **blockade** as **leverage on Trump’s economy**; **next war** restart **“quite soon”** — **Iranian elite speech**; **verify** clips and readouts before ORBAT merge.

**`thread:blumenthal` — Judging Freedom (2026-04-16):** **Amplifier stream** — **US-facing** narrative on **10-day** Lebanon **pause** and **Islamabad** round-two **optics**; **Aoun/Salam** vs **Hezbollah** **monopoly on violence**; **Iran** **counter-leverage** after **Black Wednesday**; **Islamabad** as **failed process** — **Vance** / **Rubio** / **Thiessen** (delegation includes **Marandi** — named); **UK** **Palestine Action** / **gag** / **jury** as **parallel** **speech-state** story. **Does not** replace **Marandi** **process** facts or **wire** **Lebanon** **terms**.

**Validate fork (`thread:pape`):** For **escalation-trap** / **commodity-calendar** / **spoiler** **stress-test** vocabulary on the **same calendar day**, use **[weave D — Pape Janssen](strategy-notebook-knot-2026-04-16-pape-janssen-escalation-blockade.md)** — **do not** duplicate that mechanism page here.

---

### Judgment

**Primary spine:** **Tehran register** leads — **what the Iranian side was optimizing for** in **public diplomacy** (non-rejectionist **presentation**, **authority** to negotiate, **Hormuz** **leverage**) versus **military** and **blockade** **clock**. **Blumenthal** **colors** **why** **Washington** **cannot** **hold** a **stable negotiation story** (**humiliation**, **faction**, **media** **calls** **targeting** **diplomats**) **without** becoming the **same** claim as **Marandi’s** **in-room** **authority** **read**.

**Pape (fork):** **Ratchet / checkpoints / third-player spoiler** **validate** whether **short pauses** **re-price** **next escalation** — see **D** knot; **C** **does not** **answer** **“exitless ratchet?”** **as** **primary** **thesis**.

**Lattice:** **Ritter** / **Davis** **ORBAT**, **Mercouris** **institutional** — [04-13](strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md) / [04-14 Ritter](strategy-notebook-knot-2026-04-14-ritter-blockade-hormuz-weave.md); **do not** **merge** **registers**.

**Falsifier:** If **primaries** show **sustained** **US** **flexibility** **at** **Islamabad** **and** **documented** **closure** **path**, **re-weight** **Marandi** **“not serious”** **frame** — **Blumenthal** **amplifier** **may** **still** **track** **domestic** **politics** **separately**.

---

### Links

- **Weave D (same day, separate knot):** [strategy-notebook-knot-2026-04-16-pape-janssen-escalation-blockade.md](strategy-notebook-knot-2026-04-16-pape-janssen-escalation-blockade.md)
- **Scaffold:** [strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md](strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md)
- **Threads:** [`strategy-expert-marandi-thread.md`](../../../strategy-expert-marandi-thread.md) · [`strategy-expert-blumenthal-thread.md`](../../../strategy-expert-blumenthal-thread.md)
- **Inbox:** [`daily-strategy-inbox.md`](../../../daily-strategy-inbox.md) **`## 2026-04-16`**

---

### Open / verify

- Pin **canonical** **Breaking Points** / **Judging Freedom** **`watch?v=`** URLs in inbox.
- **Thiessen** / **delegation** / **Marandi**: **tier** before **Links-grade** merge.
- **Lebanon 10-day:** **wire** vs **commentary** — **separate** **pins**.

---

### Index row (YAML — `knot-index.yaml`)

```yaml
  - path: docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04/knots/strategy-notebook-knot-2026-04-16-marandi-blumenthal-jf-primary.md
    date: "2026-04-16"
    knot_label: marandi-blumenthal-jf-primary
    clusters: [marandi, blumenthal, islamabad, hormuz]
    patterns: [weave-c, marandi-primary, blumenthal-amplifier]
    note: "Weave C: Marandi BP primary + Blumenthal JF amplifier; Pape validate fork → sister pape-janssen knot (weave D)"
```
<!-- strategy-page:end -->

<!-- strategy-expert-thread:start -->
## Machine layer — Extraction (script-maintained)

_Auto-generated from `-transcript.md` + knot index. **Journal layer** (narrative) lives **above** the **strategy-expert-thread** start HTML comment. The machine-layer HTML block is replaced on each `thread` run._

### Knot references

- [strategy-notebook-knot-2026-04-16-pape-janssen-escalation-blockade.md](strategy-notebook-knot-2026-04-16-pape-janssen-escalation-blockade.md) 2026-04-16 (pape-janssen-escalation-blockade) — Weave D: Pape-primary Janssen trap + blockade calendar + spoiler; same-day Marandi+Blumenthal evidence streams → sister weave C; lattice vs Mearsheimer/Davis
- [strategy-notebook-knot-2026-04-16-marandi-blumenthal-jf-primary.md](strategy-notebook-knot-2026-04-16-marandi-blumenthal-jf-primary.md) 2026-04-16 (marandi-blumenthal-jf-primary) — Weave C: Marandi BP primary + Blumenthal JF amplifier; Pape validate fork → sister pape-janssen (weave D)
<!-- strategy-expert-thread:end -->
