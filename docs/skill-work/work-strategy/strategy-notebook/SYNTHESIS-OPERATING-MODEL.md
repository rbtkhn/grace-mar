# Strategy notebook — synthesis operating model

**Purpose:** A **single ergonomic entry point** for turning inputs into strategy-notebook **`strategy-page`** blocks and `days.md` continuity. Deep algorithms (condense tiers, summarize-and-condense steps, word targets) stay in [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md); **minds recipes** stay in [MINDS-SKILL-STRATEGY-PATTERNS.md](../minds/MINDS-SKILL-STRATEGY-PATTERNS.md). This file answers: *what do I run, in what order, and where does each kind of content go?*

**Territory:** WORK / operator strategy — not Record unless promoted through the gate.

---

## 1. Synthesis stack (five levels)

Think top-down; **stop** when the day’s job is done — do not fill every optional layer.

| Level | Name | What it is | Required? |
|-------|------|--------------|-----------|
| **L0** | **Intent** | One line: *what decision or warrant this page must support* (draft Islamabad graf, rank a spoiler risk, close an Open, etc.) | Implicit; state in **`### Judgment`** if unclear |
| **L1** | **Inputs** | Briefs, transcript digests, sessions, wires, framework files — **sources**, not the notebook | Never paste full sources in-page |
| **L2** | **Spine** | **`### Signal`** (what crossed the threshold) + **`### Judgment`** (cross-cutting inference) + **`### Links`** (paths out) + **`### Open`** | **Yes** for a substantive day; Signal may be “nothing crossed threshold” |
| **L3** | **Overlays** | Optional: **`### Jiang resonance`**, **`### History resonance`**, **`### Analogy / tension`**, **`### Web verification`**, minds (in-page or Links-only), **`### Bets / watches`** | **Opt-in** per day |
| **L4** | **Promotion** | [STRATEGY.md](../STRATEGY.md) watches / §IV — **only** when the operator asks | Not daily |

**Rule:** L2 is the **product**; L3 **sharpens or tensions** without becoming a second full narrative.

---

## 2. Ergonomic session types (pick one)

| Type | When | Sequence | Condense path |
|------|------|----------|----------------|
| **A — Minimum** | Quiet day, tight time | L2 only: Signal → Judgment → Links → Open. Optional one-line Jiang/History **none** or **deferred**. | **Fast** (tiers A→D) if over budget |
| **B — Standard** | Normal news / strategy day | L2 + route long material to Links; add **Analogy / tension** only if a parallel is load-bearing; **one** optional overlay (Jiang *or* History *or* single-lens mind line via Links). | **Fast** default |
| **C — Heavy** | DEMO, multi-transcript, lens walls, web tables in draft | Run **[Full]** summarize-and-condense (architecture § Summarize-and-condense) **before** tiers A→D; outboard ARTIFACT bodies first. | **Full** then **Fast** |
| **D — Verify-forward** | Numbers, law, or claims that may ship publicly | L2 + **`### Web verification`** (claim → URL → correction) + hot numbers dated or omitted | **Fast** after verify block is lean |

**Default:** **B**. Escalate to **C** only when the draft is visibly mixed notebook + bulk.

---

## 3. Section router (where content goes)

| Kind of material | Primary home | Never |
|------------------|--------------|--------|
| Raw quotes, long transcript lines | **Outboard** + one **Links** line | In Signal/Judgment as walls |
| Same fact from three wires | **Signal** (one bullet) or merge per tier B | Three bullets repeating one fact |
| Your operative thesis | **Judgment** | Split across Signal and Judgment as duplicate K |
| File paths, digests, frameworks | **`### Links`** | Orphan URLs in Judgment |
| PH lecture fit | **`### Jiang resonance`** | Implied PH alignment without a link |
| HN mechanism / chapter id | **`### History resonance`** | Full chapter text |
| Legitimacy vs structure tension | **`### Analogy / tension`** or **meta** polyphony | Merged voice in one sentence |
| Falsifiable bets | **`### Bets / watches`** or **meta** | Vague mood |

---

## 4. Minds — ergonomic defaults

Aligned with [.cursor/rules/strategy-minds-granular.mdc](../../../../.cursor/rules/strategy-minds-granular.mdc): **no default tri-frame.**

**Ensemble shorthand** (same habit as [architecture § Ensemble metaphor](STRATEGY-NOTEBOOK-ARCHITECTURE.md#ensemble-metaphor-chamber-group-gloss)):

| Situation | Minds | Metaphor |
|-----------|--------|----------|
| **Default** | **0** — plain Judgment | **Tacet** — ensemble rests; Judgment only |
| **One dominant uncertainty** | **1** — single-lens; one paragraph or Links-only + stub link | **Solo** — one part carries the line |
| **Contradiction you want visible** | **2** — tension pass (often Mercouris vs Mearsheimer); put tension in **Analogy / tension** or polyphony | **Duet** — counterpoint; convergence vs tension explicit |
| **Operator says tri-frame / LEARN MODE** | **3** — full lens pass per [LEARN_MODE_RULES.md](../LEARN_MODE_RULES.md) / operator | **Tutti** — all parts explicit in one scored pass |

**Ergonomic rule:** If adding minds would push past **~1200 words**, use **Links-only lensing** (one line + mind file link) or move month-scale voice to **`meta.md` § Polyphony**.

---

## 5. Pre-flight checklist (≤30 seconds)

- [ ] **Session type A/B/C/D** chosen (above).
- [ ] **L0** clear enough to know what Judgment must deliver.
- [ ] Long bodies **already** under stable paths or flagged ARTIFACT for routing.

---

## 6. Post-flight checklist

Use the **Condense checklist** in [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Condense checklist](STRATEGY-NOTEBOOK-ARCHITECTURE.md#condense-checklist-operator--agent) plus word-count on **today’s block only**.

---

## 7. Polyphony synthesis rules

**Metaphor:** **Polyphony** — multiple independent melodic lines at once — not **homophony** (one dominant melody with accompaniment). In the strategy-notebook, expert threads and civilizational registers are **parts**; together they form the operator’s **Symphony of Civilization** image.

**Core philosophy:**

- Multiple expert and civilizational voices must **sound together** without **collapsing into one melody**.
- Each expert thread supplies its own **part** on the score.
- **Batch-analysis** names **convergences** (alignments) vs **tensions** (dissonances).
- The **operator** (not the experts or the AI) sets **balance, tempo, and emphasis** through EOD sessions, thesis A/B testing, and verification discipline.
- Dissonance is often intentional and valuable — it is **preserved** unless deliberately resolved and promoted.

This counters the failure mode of **wiki-style synthesis** that smooths contradictions and hides raw provenance (see **Wiki drift** below).

### Rules (operational)

1. **Preserve distinct voices (no flattening)**  
   Each expert keeps a cognitive fingerprint (e.g. legitimacy/narrative vs power/incentives). In the **Journal layer** of `thread.md`: light gloss, source pins, pointers to verbatim `transcript.md` — not heavy paraphrase that rewrites the expert. Attribution stays explicit (“X frames…”, “Y counters…”). Do not merge planes/registers without tagging.

2. **Separate layers strictly (Journal vs Machine)**  
   **Journal** (above `<!-- strategy-expert-thread:start -->`): operator narrative, tension notes, `strategy-page` blocks — **never overwritten** by scripts. **Machine** (between the fences): script-maintained extraction — refreshed on `thread` runs. Interpretive synthesis belongs in EOD / compiled-view **recipes**, not in overwriting the Journal.

3. **Convergences and tensions explicitly**  
   Name genuine cross-expert alignments when warranted. Surface contradictions; use **Analogy / tension** or a **tension line** in monthly `meta.md`. Format for synthesis artifacts can be: **Issue / Voice A / Voice B / Implication** — leave unresolved unless promoted.

4. **Operator as conductor (human-in-the-loop)**  
   Primary conducting moment: **EOD strategy session** (“strategy page”, “notebook compose”, “close the strategy day”). `strategy-page` blocks use **Signal / Judgment / Open** with substantive prose. Judgment is cross-cutting inference — not a second recap of briefs. Promotion is gated (`[promote]`, recursion-gate).

5. **Verification and traceability**  
   Proper nouns, dates, stats, disputed claims get `verify:` and **Web verification** / **Links** as appropriate. Dual-track seams (web facts vs CIV-MEM patterns) stay visible.

6. **Scale and cadence**  
   Monthly `chapters/YYYY-MM/` and rolling transcripts keep scope bounded. **Polyphony / lens tension** in `meta.md` updates when the month’s arc shifts — not necessarily daily. Promotion is rare; daily volatility stays in the notebook “rehearsal” space.

### Compiled views tie-in

[Compiled views](../compiled-views/README.md) apply these rules in a **derived** layer: pull Journal + Machine across experts; preserve voices; surface convergences and tensions; ground **Emerging Operator Judgment** only in existing `strategy-page` prose; mark outputs **refresh-only** and link back to sources.

### Why polyphony (vs wiki drift)

Layered wikis and undifferentiated “consensus” synthesis tend to **flatten contradictions** and **obscure provenance** — the reader sees a smooth article, not which voices disagreed or what was primary. Grace-Mar polyphony **keeps instrument lines distinct**, **surfaces tensions**, and routes promotion through the **operator**. Derived snapshots (compiled views) are **explicitly regeneratable** so errors are not baked in — fix sources, regenerate. *(Principle-level contrast; add a `raw-input` link here if you ingest a specific source transcript later.)*

---

## 8. Operator as conductor

**Definition:** The operator is the **human-in-the-loop apex**: not merely a reviewer — the active **conductor** of the Symphony of Civilization. Expert voices and civilizational registers are **independent lines**; the operator sets **balance, tempo, emphasis**, when to resolve dissonance, and **when to promote** stabilized arcs (`STRATEGY.md`, recursion-gate, personal Record). This role is **not** automated. It is the layer that prevents the notebook from becoming only a raw dump **or** an AI-smoothed consensus artifact.

**You are the conductor, not one of the instruments.** Experts and scripts play the parts; you shape the performance.

**Polyphony is the goal, not forced consensus.** Dissonance may remain audible until you deliberately resolve and promote.

### Where this shows up in your workflow

**Polyphony** (you hear distinct parts, not one smoothed melody):

- **Per-expert threads** — `experts/<expert_id>/thread.md` (and `voices/…` where used): each lane is a different **instrument line**; the **Journal** above the machine fence is where your reading meets their material without collapsing voices.
- **`strategy-page` blocks** — same calendar day can carry **multiple pages** and the same logical `id=` **across experts** with **different Judgment by voice** — polyphony on disk.
- **`chapters/YYYY-MM/days.md`** — **Thesis A / B**, parallel bullets, **Open** carrying unresolved tension — dissonance preserved in the chronology layer.
- **`meta.md` § Polyphony / lens tension** — month-scale **tension line** (e.g. readings that disagree **by design**).
- **Batch-analysis / cross-expert work** — naming **convergence vs tension** across indexed threads — reading the **score** as many parts.
- **Optional:** after `compile_strategy_view.py`, the **bundle** puts slices side by side; the narrative pass must still **attribute** and **not flatten** (see [compiled views README](../compiled-views/README.md)).

**Conductor** (you set balance, tempo, promotion — not another part):

- **End-of-day strategy session** — the real podium: `skill-strategy` / notebook compose, **page-shape menu**, then edits to **`days.md`** and **`strategy-page`** blocks.
- **Journal layer only** — substantive **Signal / Judgment / Links / Open** (and overlays) **above** `<!-- strategy-expert-thread:start -->`. You do **not** conduct by hand-editing the **Machine** fence.
- **Markers** — `[watch]`, `[decision]`, `[promote]` and your **promotion** choices (`STRATEGY.md`, gate) — rehearsal vs performance.
- **Meta “baton”** — `NOTEBOOK-PREFERENCES.md`, `meta.md`, this architecture/synthesis doc set — cadence and emphasis across the month.
- **Compiled views** — you decide whether to **generate**, **fill**, or **discard** a snapshot; scripts **bundle**; they do **not** replace your judgment in the threads.

### Daily / tactical responsibilities

During or after an EOD session:

- Review the **score** (Machine extractions + transcripts as needed).
- Compose or revise **`strategy-page`** blocks in the **Journal layer** — **Signal / Judgment / Open**; substantive prose; verbatim-forward scaffolds where appropriate.
- Set **emphasis**: which threads weigh more this month; which tensions get a **tension line** in `meta.md`; which convergences are strong enough to name.
- Use markers: `[watch]`, `[decision]`, `[promote]` per your governance.
- Run **verification** when claims bite; keep **dual-track** seams visible.

All of the above sits **above** the Machine fence — you do not hand-edit the Machine layer.

### Strategic / long-term responsibilities

- Shape **month-scale arcs**; decide what stabilizes vs stays deliberately open.
- **Promotion timing** — notebook rehearsal vs higher surfaces; recursion-gate discipline.
- **Tempo** — chapter boundaries, rolling windows, batch-analysis cadence.
- Maintain **meta documents**: `NOTEBOOK-PREFERENCES.md`, monthly `meta.md`, `STRATEGY-NOTEBOOK-ARCHITECTURE.md` as the baton’s home.

### Hybrid memory model (Karpathy / OpenBrain)

| Strength | Role of the conductor |
|----------|----------------------|
| **Raw preservation (OpenBrain)** | Never corrupt raw inputs or Machine extraction; provenance stays pristine. |
| **Evolving synthesis (Karpathy)** | Interpretive weaving lives in the **Journal layer** and optional **compiled views**. |
| **Anti-drift** | Compiled views are **derived** and **regeneratable**; SSOT remains `thread.md` + pages. You remain final authority on whether a snapshot is good enough. |

### Sacred boundaries

- Do not update core **SELF**, **EVIDENCE**, **SKILLS**, or personal **Record** from this lane without the normal gate.
- Do not let scripts overwrite the **Journal layer**.
- Do not collapse polyphony into a single “correct” narrative in prose meant to be authoritative.
- **Promotion is gated** — explicit `[promote]` / operator decision before leaving rehearsal space.

### Real orchestra vs Grace-Mar conductor

| Aspect | Orchestral conducting | Operator as conductor (strategy-notebook) |
|--------|----------------------|-------------------------------------------|
| **Role** | Interpreter / unifier of many voices into one performance | Interpreter / unifier of expert & civilizational voices into **polyphonic** judgment |
| **Not playing instruments** | Does not play; shapes overall sound | Does not author raw expert threads; shapes **Journal** judgment |
| **Listening** | Balance, intonation, timing | Reading across threads — convergences, tensions, resonances |
| **Polyphony** | Multiple melodic lines at once | Distinct expert voices without premature consensus |
| **Tempo & balance** | Pace, dynamics, sections | Which threads/tensions matter; EOD cadence; monthly arcs |
| **Dissonance** | Controlled tension; resolved when required | Strategic tensions preserved unless you promote resolution |
| **Rehearsal vs performance** | Rehearsal refines; concert delivers | EOD = **rehearsal**; stabilized arcs → `STRATEGY.md` / Record = **performance** |
| **Non-authoritative production** | Relies on musicians’ skill | Relies on scripts + experts; operator does not “own” their facts |

| Aspect | Traditional orchestra | Grace-Mar |
|--------|----------------------|-----------|
| **Score** | Fixed composer score | Operator is **composer-and-conductor in part**: transcripts/Machine supply parts; **Journal** authors stabilization choices |
| **Material** | Fixed repertoire | Dynamic inputs — briefs, transcripts, CIV-MEM |
| **Automation** | Minimal | Scripts run Machine extraction; conductor focuses on **high-judgment** synthesis |
| **Promotion** | Concert is the goal | Strict ladder — notebook until `[promote]` + gate |
| **Drift / error** | Limited fixes in concert | Derived views **regenerate**; threads stay authoritative |
| **Audience** | External listeners | Operator’s durable judgment — not primarily a public performance |
| **Maestro myth** | Omniscient-leader trope | **Anti-maestro:** operator is **not** the source of expert voices; tools are **not** maestro either |

**Why the metaphor fits:** Polyphony over homophony; HITL apex; rehearsal discipline; long-term arc across “movements.” Practical conductor **modes** (precision, expression, economy) live under **Techniques inspired by the masters** below.

### Techniques inspired by the masters

Transferable shorthand — pedagogical only; fingerprint rules in architecture remain authoritative.

| Figure | Grace-Mar anchor |
|--------|------------------|
| **Toscanini** | **Precision** — boundaries, verbatim-forward, validation, unambiguous convergences; see **extended map** below. |
| **Bernstein** | **Journal / EOD** — embodied operator voice in Signal/Judgment/Open; heat without losing the threads-as-score. |
| **Karajan** | **Long arc** — economical edits, `meta.md` themes, blended balance; avoid over-writing. |
| **Kleiber** | **Selectivity** — deep prep before promote; minimal high-impact interventions; sparse `[promote]`. |
| **Furtwängler / “grammar of conducting”** | **Flow vs ictus** — intuition and connection across threads; clarity of intent without mechanical bullet-stacking. |

**Cross-cutting:** Most work in **rehearsal** (EOD); **clarity of intent** beats flamboyance; **less is more** once the ensemble knows the interpretation; **score mastery** then freedom; sections retain **character** under your balance.

**Transferable lessons:** Precision → clean Machine/Journal seams and verify discipline. Expression → authentic Judgment. Economy → selective promotion and light touch on derived snapshots. Listening → preserve polyphony and name tensions. Rehearsal vs performance → EOD vs promotion. Compiled views → safe, regeneratable performance **snapshots**, not SSOT.

#### Toscanini — extended rehearsal map

Historical accounts emphasize **rigor**, **clarity**, and **concert-level seriousness** — alongside a perfectionism that could show as harsh temper. In Grace-Mar we take the **disciplines** without glorifying abusive rehearsal culture: use **structured governance** (pause, gate, regenerate) instead of “volume” as a management tool.

| # | Toscanini move | Grace-Mar application |
|---|----------------|------------------------|
| 1 | **From-memory / concert-serious rehearsal** | Pre-EOD **internalization**; optional **memory run** (7–30d convergences/tensions without files); session focuses on **judgment**, not re-reading raw walls. |
| 2 | **Clear beat — “feel what I want”** | **Economical, unambiguous** Signal/Judgment/Open; convergence/tension labels a reader can grasp immediately; expressive flourishes **sparingly**. |
| 3 | **Relentless precision** | Verify claims, visible seams, prose standards; if synthesis feels wrong, **direct frustration inward** first; **Toscanini pause** (stop, break, return) — no forced smoothing of contradictions. |
| 4 | **Obsessive prep + Cantare** | Re-study even familiar voices; **read aloud** or mentally “sing” the rhythm of tensions before composing. |
| 5 | **Economy of motion** | After solid rehearsal, **light interpretive overlay** on compiled views — interpretation should already live in the Journal. |

**Takeaway:** Adopt **preparation, clarity, polyphony-preserving precision**; **soften** perfectionism’s costs via WORK rules and regeneratable derived artifacts.

---

## 9. See also

| Topic | Path |
|-------|------|
| Daily template headings | [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Daily entry template](STRATEGY-NOTEBOOK-ARCHITECTURE.md#daily-entry-template) |
| Tiers A→D, Full vs Fast | [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Condense-to-target](STRATEGY-NOTEBOOK-ARCHITECTURE.md#condense-to-target-mechanism-fit-1000-words) |
| Daily synthesis division of labor | [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Daily synthesis](STRATEGY-NOTEBOOK-ARCHITECTURE.md#daily-synthesis-briefs-transcripts-other-work-strategy) |
| Ensemble metaphor (score / parts / conductor) | [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Ensemble metaphor](STRATEGY-NOTEBOOK-ARCHITECTURE.md#ensemble-metaphor-chamber-group-gloss) |
| **Polyphony + compiled views** | [compiled-views/README.md](compiled-views/README.md) · [expert-polyphony recipe](compiled-views/recipes/expert-polyphony-synthesis.md) |
| Minds recipes | [MINDS-SKILL-STRATEGY-PATTERNS.md](../minds/MINDS-SKILL-STRATEGY-PATTERNS.md) |
| Skill behavior | [.cursor/skills/skill-strategy/SKILL.md](../../../../.cursor/skills/skill-strategy/SKILL.md) |

### Adjacent lane (Xavier journal)

**Multi-source day digest** for OB1 / companion handoff (inbox, transcript, strategy-notebook block, artifacts) is a **different write surface** with overlapping *synthesis* vocabulary — see [xavier-journal/SYNTHESIS-SOURCES.md](../../work-xavier/xavier-journal/SYNTHESIS-SOURCES.md). Use that path when the deliverable is a **journal page**, not the strategy-notebook `days.md` block alone.
