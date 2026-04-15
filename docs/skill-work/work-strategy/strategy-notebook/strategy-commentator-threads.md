# Strategy commentator threads (index)

**Purpose:** Stable **expert lanes** for recurring **expert / commentator** ingests so `batch-analysis` lines can name **divergence and correlation** without re-deriving the roster each session. The same **`thread:<expert_id>`** on **different dates** is the **join key** for **accuracy** checks and **opinion drift** (see **Expert threads: predictive accuracy and opinion drift**). **WORK only** — not Record.

**Choreography (vs tri-mind):** Threads track **each commentator over time** (accuracy, narrative, compare–contrast). **Tri-mind** is a separate **analysis** pattern — usually **outboard** from `days.md`; see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § **Expert choreography**.

**Terminology — `expert_id`:** The **first column** in the table below — **one canonical slug per named expert** (e.g. `seyed-marandi`, `scott-ritter`). **Inbox `verify:`** tails use **`thread:<expert_id>`** — the token after **`thread:`** is the **`expert_id`**. **Legacy synonym:** **`thread_id`** (same column / value). **Legacy prose:** Older notes may say “analyst_id” / “analyst threads” — same field and lanes as **`expert_id`** / **expert threads**.

**Lane discipline (no hybrid slugs):** Each **`expert_id`** identifies **exactly one** **Anchor** (person). **Topic** framing (Islamabad process, Hormuz domestic politics, escalation trap, etc.) lives in the **Role** column, **cold** text, and **grep tags** — **not** in the slug. **Verbatim quotes** and **attributed analysis** belong on a line whose **`thread:`** matches **that speaker’s** row; putting another expert’s words under the wrong **`thread:`** is a **routing error**. **`batch-analysis`** is where **topic** tension (same crisis, different mechanisms) meets **expert** tension (same week, different predictions or registers).

**Metaphor — Symphony of Civilization:** Indexed commentators are **parts** in a **polyphonic** score; each daily **`## YYYY-MM-DD`** block in the active month’s `chapters/YYYY-MM/days.md` is a **movement**; **`batch-analysis`** states **harmony vs tension** between parts. Full gloss: [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § **Symphony of Civilization**.

**Topic tags vs expert threads (mental model):** Two layers — not mutually exclusive.

- **Topic tags** — *what* the material is about: recurring **substantive** lanes (Islamabad arc, Hormuz, Lebanon vs nuclear, U.S. domestic liability, Rome / legitimacy, …). These show up as **grep tags** (`IRAN`, `JDVance`, `ROME`, `narrative-escalation`, …) or linked docs ([rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md), [trump-religion-papacy-arc.md](trump-religion-papacy-arc.md)).
- **Expert threads** — *who* is speaking: one **`thread:<expert_id>`** per **named** indexed voice. Reusing the same **`expert_id`** across weeks **diffs** that **person** over time (drift / pivot).

**How to use:** When appending a paste-ready line in [daily-strategy-inbox.md](daily-strategy-inbox.md), add **`thread:<expert_id>`** to the **`verify:`** tail **only** when the **cold** line attributes speech or analysis to that **Anchor**. Pair ingests in **`batch-analysis | YYYY-MM-DD | …`** using **Typical pairings**.

**Expert ingest corpus (rolling 7 days):** Each indexed expert has a companion file **`strategy-expert-<expert_id>.md`** in this directory (same level as this index) — verbatim inbox lines (with **`thread:`**) grouped by date inside a script-delimited block; the **Seed** section above that block is operator-editable and preserved on rebuild. Run operator **`thread`**: **`python3 scripts/strategy_thread.py`** (delegates to `strategy_expert_corpus.py`; older daily sections inside the block fall off automatically). **Not Record**; only the marked rolling section is script-owned. Legacy path [`expert-ingest-corpus/README.md`](expert-ingest-corpus/README.md) redirects here. *Notebook contract (inbox → weave → `days.md`):* [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md#expert-choreography) § **Expert choreography**. Operator **`thread`** vs **`weave`:** [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Thread (terminology)*.

**Published outlets (starter list):** Each **`strategy-expert-<expert_id>.md`** **Seed** includes **`### Published sources (operator web index)`** — at least three **content** URLs (X / Substack / outlet / institutional host; **no Wikipedia**); re-verify handles and media URLs before cite-grade use.

**Wires and outlets (no expert `thread:`):** A **wire**, **pool paragraph**, or **outlet summary** is **not** an indexed expert unless the cold line names **that person** as the speaker or author. Use **`verify:wire-RSS`** (and topic grep tags) **without** **`thread:<expert_id>`**; optional **`membrane:single`** when the line must **not** imply **`batch-analysis`** membership for expert threads.

**Ephemeral / one-shot ingests (no persistent expert thread):** Not every line needs a **`thread:<expert_id>`**. The index exists so the **same** voice can be **joined across dates** (drift, accuracy). If the capture is **tactical** — one article, a stray clip, a **verify** pass, or material you **do not** want to treat as a standing **expert** lane — **omit** **`thread:`**. Use **cold** + **URL** + **`verify:`** and **topic** grep tags (`IRAN`, `ROME`, …) as usual. Optional **`verify:… | membrane:single`** signals that this line is **not** inviting a same-day **`batch-analysis`** membership claim for indexed threads (see **Crossing filters**). You are **not** required to mint a table row for every name that appears once.

**Maintenance:** Add rows when a new anchor appears **repeatedly** in `days.md` or inbox; **deprecate** with a line in **Notes** — do not delete history without operator say-so.

**Month arc pointer (chapter meta):** Cross-day **movement** and weave boundaries for the active month (example **2026-04-08–15**: Hormuz week, expert density, **04-15** Grok-vs-brief overlay) live in [chapters/2026-04/meta.md](chapters/2026-04/meta.md#april-arc-one-screen) (**April arc — one screen**). Use that block for **grep / calendar** orientation; it **does not** mint **`expert_id`** rows—this file remains the roster SSOT.

**Mearsheimer vs Diesen (individual anchors):** **`john-mearsheimer`** = **John Mearsheimer** only; **`glenn-diesen`** = **Glenn Diesen** only — **no** shared **`expert_id`** for a “session pair.” Same episode with **both** speakers → **two** paste-ready lines (each **`thread:<expert_id>`**) + optional **`batch-analysis`**.

---

| expert_id | Anchor | Role (one line) | Default grep tag | Typical `batch-analysis` pairings |
|-----------|--------|-----------------|------------------|-----------------------------------|
| `seyed-marandi` | Seyed Mohammad Marandi | Iranian English long-form: negotiation **process**, red lines, legitimacy register | `IRAN`, `TEHRAN`, or `Marandi` in cold | × `scott-ritter`, × `trita-parsi`, × `rome-ecumenical` (Pontifex / Marandi Easter) |
| `scott-ritter` | Scott Ritter | U.S. **military dissent**: Hormuz **sea control**, blockade ops, Vance frame; **faith-politics** register when **Ritter** is the speaking expert | `JDVance`, `IRAN`, or `Ritter` | × `seyed-marandi`, × `robert-barnes`, × `rome-invective` (split from ecumenical) |
| `trita-parsi` | Trita Parsi (`@tparsi`) | Beltway-facing **Lebanon vs nuclear** scope; “mask” thesis | `IRAN` + Parsi in cold | × `holy-see-moral` (Pontifex Lebanon), × `seyed-marandi`, × `douglas-macgregor` |
| `robert-barnes` | Robert Barnes (`@barnes_law`) | **Domestic liability** pole on Hormuz / executive TS chain | `JDVance` or `barnes` in cold | × `robert-pape`; **topic** forks (JTN-style “card” vs satirical spiral) in **`batch-analysis`** without a second expert |
| `douglas-macgregor` | Douglas Macgregor (`@DougAMacgregor`) | Importers / **Asia–Europe** distance from U.S.–Israel kinetic frame | `IRAN` or Macgregor in cold | × `robert-pape`, × `john-mearsheimer`, × `trita-parsi` |
| `robert-pape` | Robert Pape (`@ProfessorPape`) | **Escalation Trap** / commitment ratchet on demands | `ProfessorPape` or Pape in cold | × `daniel-davis`, × `robert-barnes`, × `john-mearsheimer` |
| `daniel-davis` | Daniel Davis (Lt Col; `@DanielLDavis1`) | Ceasefire as **extension game**; ultimatum vs negotiation; macro pain to U.S. | `IRAN`, `JDVance`, or Davis in cold | × `john-mearsheimer`, × `robert-pape`, × `seyed-marandi`, × `steve-jermy` |
| `steve-jermy` | Steve Jermy (Commodore, RN ret.) | **Energy–GDP / maritime system**: Hormuz closure **recovery lags** (Ever Given–style **knock-on**), **diesel** → supply chain / semis / fertilizer; **rough-order** macro slides vs **currency-first** economics; **close vs distant** blockade **risk geometry** | `Jermy`, `IRAN`, or `Hormuz` in cold | × `daniel-davis`, × `scott-ritter`, × `john-mearsheimer` (in-show cite) |
| `john-mearsheimer` | John Mearsheimer | **Offensive realism**: security dilemma, Israel structural, great-power geometry | `MEARSHEIMER` or `Mearsheimer` in cold | × `daniel-davis`, × `alexander-mercouris`, × `glenn-diesen`, × `jeffrey-sachs` |
| `alexander-mercouris` | Alexander Mercouris | **Institutional / narrative** diplomatic read (Hormuz, Lebanon, Islamabad) | `Mercouris` or mind cite in cold | × `john-mearsheimer`, × `glenn-diesen`, × `jeffrey-sachs`, × `seyed-marandi`, × Tri-Frame [minds/](../minds/README.md) |
| `max-blumenthal` | Max Blumenthal (`@MaxBlumenthal`) | **Grayzone** / **antiwar** pole: **U.S. Middle East** policy and **elite-access** critique; **Lebanon**/**Gulf** narrative framing; **media-layer** “who engineered what” — **access** and **backchannel** claims stay **hypothesis-grade** until **primary tape** or **on-record** source | `Blumenthal`, `Grayzone`, or `Lebanon` in cold | × `aaron-mate`, × `trita-parsi`, × `alexander-mercouris`, × `seyed-marandi`, × `charles-freeman` |
| `aaron-mate` | Aaron Maté (`@aaronjmate`) | **Grayzone** / **investigative** lane: **media ownership**, **corporate skin**, and **propaganda** framing; **Israel/Palestine** vocabulary (**colonization** thesis); **CBS** / **billionaire** / outlet **lineage** claims — **tier verify** (filings, corporate docs) before **Links-grade** | `Mate`, `Maté`, `Grayzone`, or `aaronjmate` in cold | × `max-blumenthal`, × `trita-parsi`, × `alexander-mercouris`, × `seyed-marandi` |
| `larry-johnson` | Larry Johnson | Ex-CIA / **material** and **ORBAT** emphasis: force structure, **Hormuz** geometry, **F-15/Isfahan** raid narrative reconstructions (Haiphong–Ritter roundtables) | `Johnson` or `LarryJohnson` in cold | × `scott-ritter`, × `daniel-davis`; see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) |
| `charles-freeman` | Charles (“Chas”) Freeman | Retired **career diplomat**: **inconclusive** talks, **alliance** and **material** framing (Islamabad as diplomacy-while-war); **separate plane** from papal **moral** register | `Freeman` or `ChasFreeman` in cold | × `trita-parsi`, × `alexander-mercouris`, × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (**seam**, not merge) |
| `alastair-crooke` | Alastair Crooke | Former diplomat / **Levant–Islamabad** “room” and **spoiler** reads; often beside **Davis** in digests | `Crooke` in cold | × `daniel-davis`, × `seyed-marandi`, × `trita-parsi` |
| `glenn-diesen` | Glenn Diesen | **Eurasia / multipolar** discourse; **non-Western** institutional / rationality frames when distinct from **Mearsheimer**’s structural-realist register | `Diesen` in cold | × `john-mearsheimer`, × `douglas-macgregor`, × `robert-pape`, × `jeffrey-sachs` |
| `jeffrey-sachs` | Jeffrey Sachs | **UN / development–macro + DC institutions** pole: **deinstitutionalization** thesis (group process vs personalized executive); **relative decline** and **multipolar** misrecognition; **Congress** war-and-peace **vacuum**; cites **NYT** “room” narratives — **hypothesis-grade** capacity/health claims stay **tier-C** unless clinical primary | `Sachs`, `IRAN`, or `Hormuz` in cold | × `glenn-diesen`, × `john-mearsheimer`, × `alexander-mercouris` |
| `jiang-xueqin` | Jiang Xueqin (Predictive History) | **Long-horizon civilizational / game-theory** lectures; PH is the sole upstream for notebook-facing Jiang ingest | `Jiang`, `PH`, or `predictive-history` in cold | × `john-mearsheimer`, × `glenn-diesen`, × `jeffrey-sachs` |
| `martin-armstrong` | Martin A. Armstrong (`@ArmstrongEcon`) | **Cycle / timing** models (Socrates-style), **sovereign debt** stress, **energy–food system** shocks (diesel, fertilizer) framed with **geopolitical war**; critiques **“perpetual wealth” vs “dollar crash”** as headline distractions | `Armstrong`, `debt`, `IRAN`, or `Hormuz` in cold | × `steve-jermy`, × `glenn-diesen`, × `jeffrey-sachs`, × `robert-pape` |

**Special routing rule — Predictive History:** PH-derived notebook-facing ingest must use `thread:jiang-xueqin`. Do not route PH directly into other expert lanes or directly into knots. See [strategy-notebook/README.md](README.md) § **Predictive History routing rule**.

### Distinctive lane shorthands (recommended sentences)

- **`robert-pape`:** This lane **names escalation as a trap** — a **commitment ratchet** on **demands** plus **staged** branches (e.g. **nuclear-stockpile** logic → **ground-force** scenarios, **Stage** framing, packaged graphics) — **not** a substitute for **`scott-ritter`** **Hormuz** **mechanics**, **`alexander-mercouris`** **room** **reads**, or **`john-mearsheimer`** **alliance** **geometry** alone; use **Typical pairings** and, when folded, **`### Judgment`** bullets such as **Thesis A — Pape / “escalation trap”** in the active month’s [`chapters/YYYY-MM/days.md`](chapters/2026-04/days.md) (replace **YYYY-MM**).

- **Domestic plane (do not collapse):** **`robert-barnes`** tracks **liability**, **coalition sell**, and the **executive / TS** **chain**. **Pape** may add **U.S. audience** **or** **polling** **theses** (e.g. political support **hardening** under casualties) — keep those **hypothesis-grade** until **ingested** with **`verify:`** (dated poll, screenshot, or primary); **do not** **merge** with Barnes **without** a **labeled seam**.

- **`martin-armstrong`:** **Cycle / timing** and **debt–war–commodity** convergence theses — **not** a substitute for **`steve-jermy`** **diesel / fertilizer / logistics** mechanics or **`jeffrey-sachs`** **institutional** reads without **tiered** verify; treat **“computer was right on timing”** claims as **hypothesis-grade** until **disclosed methodology** or **out-of-sample** documentation exists.

### Quantitative thread metrics (illustrative — civ-mem–style calibration)

**Purpose:** Optional **0–1** scores to classify threads using habits parallel to civ-mem: **relevance-spine stability** (does the voice stay on its lane?), **STATE-style closure** (resolved/deferred vs open claims), and **lattice edge weight** (hub role in `batch-analysis`). **Numbers below are placeholders** — replace with measured rates from inbox / `days.md` / resolution logs when you operationalize.

| Abbrev | Name | Idea |
|--------|------|------|
| **SCI** | Surface coherence index | Share of ingests where the dominant **plane** matches the row’s **Role**; penalize register smearing without a seam. |
| **AD** | Adjudication depth | \((\texttt{resolved} + \texttt{deferred})\) **÷** falsifiable claims logged (trailing window). |
| **CTC** | Cross-thread coupling | Distinct **other** `expert_id`s in **`batch-analysis`** with this anchor, normalized by activity (bridge centrality). |

| expert_id | SCI | AD | CTC | Plain-language note (Predictive History reader) |
|-----------|-----|----|-----|--------------------------------------------------|
| `seyed-marandi` | 0.78 | 0.42 | 0.71 | He usually sounds like one kind of speaker: negotiation, red lines, and how the Islamic Republic wants to be heard. Many of his strongest claims only settle when the diplomatic music stops, so “who was right?” often stays open. In the notebook he keeps showing up next to other Iran-facing voices, which is why the “bridge” score runs high. |
| `scott-ritter` | 0.82 | 0.48 | 0.74 | His lane is recognizable—sea control, blockade mechanics, the military story under the headlines—so he does not drift into generic punditry as often. Operational claims need time and evidence to judge, so verdicts arrive slowly. He is often placed beside diplomats or lawyers of war in the same week’s analysis, which raises the “compares with others” score. |
| `trita-parsi` | 0.74 | 0.45 | 0.69 | Washington’s story can pull him between Lebanon, nuclear scope, and what “the process” means, so the thread can feel like it crosses slightly different questions in one breath. What closes in the Beltway and what closes on the ground do not always move together. He still pairs often with other named voices, but he is not the hub everyone orbits. |
| `robert-barnes` | 0.88 | 0.36 | 0.52 | He stays on home law and politics—who is exposed, what the chain of command implies—which keeps his voice distinct from foreign-policy generalists. Poll-driven or coalition claims often stay “maybe” until hard numbers land, so clear yes/no resolution is rarer. He is essential when the story is liability; he is less often the center of multi-country roundtables. |
| `douglas-macgregor` | 0.76 | 0.40 | 0.68 | Third-country distance from the U.S.–Israel frame is a steady theme, easy to recognize week to week. Event-linked scorekeeping is uneven because his value is often framing, not a dated bet. He still shows up in side-by-side comparisons with other realists. |
| `robert-pape` | 0.81 | 0.55 | 0.77 | Escalation-as-trap is a named mechanism—demands, ratchets, staged branches—so the reader can see what would count as a test. When those pieces are written down clearly, time can actually grade the claim. That same clarity makes him a natural partner in “fork A vs fork B” discussions. |
| `daniel-davis` | 0.79 | 0.50 | 0.72 | Ceasefire as extension game, ultimatums, who hurts first—the architecture is easy to follow. Some forecasts need the calendar to catch up before you know. He is regularly read against other named analysts in the same crisis week. |
| `steve-jermy` | 0.74 | 0.44 | 0.58 | Energy–logistics modeling is a recognizable lane—diesel, closure recovery, systemic second-order effects. Macro numbers stay **rough-order** until primaries pin. Often paired on **Deep Dive** with Davis rather than as the widest crossover hub. |
| `john-mearsheimer` | 0.85 | 0.58 | 0.84 | Great-power geometry is his home turf; the listener rarely wonders which discipline they are in. If-then structure helps the record show what would falsify a line of argument. In comparative work he is the voice others are measured against, so he sits at the center of many paired readings. |
| `alexander-mercouris` | 0.72 | 0.44 | 0.88 | The diplomatic “room” story can shade into narrative that is harder to pin to a single falsifying fact, so discipline scores a little lower. The payoff is synthesis: he is the commentator most often placed beside others to hear harmony or dissonance, which drives the bridge score to the top. |
| `max-blumenthal` | 0.74 | 0.33 | 0.62 | Elite-network and media-critique framing is recognizable week to week; closure on “who whispered to whom” claims often waits on tape or official denial. Pairs well with Beltway-facing or diplomatic lanes when the notebook wants an alt-media tension. |
| `aaron-mate` | 0.75 | 0.34 | 0.64 | Media-structure and ownership critiques are a steady lane—outlet naming and corporate parentage need primary documents to close. Often read beside the same Grayzone-adjacent week as Blumenthal but keeps a distinct thread id for routing. |
| `larry-johnson` | 0.80 | 0.46 | 0.63 | Order-of-battle and material detail keep him in a narrow lane—useful when the question is what forces could actually do. Raid and battle narratives take time and sources to check. He shines on panels and roundtables more than as the universal hub for every thread. |
| `charles-freeman` | 0.83 | 0.41 | 0.66 | Veteran diplomat’s habit—“talks are inconclusive by nature”—matches a careful separation between moral language and hard security, which keeps the voice steady. Diplomatic time horizons mean many calls stay unresolved for a long while. Pairings happen, but he is not the busiest crossover node. |
| `alastair-crooke` | 0.75 | 0.39 | 0.70 | Levant room and spoiler logic hang together as a worldview. Spoiler readings often stay open until events force a fork. He appears often enough next to other specialists that the bridge score stays solid. |
| `glenn-diesen` | 0.77 | 0.43 | 0.79 | Multipolar language is clearly his own—not a copy of standard U.S. structural realism—so you can tell when Diesen is speaking. Closure looks like his peer group: partly about time and evidence. He is frequently read alongside other realist anchors when the week demands comparison. |
| `jeffrey-sachs` | 0.73 | 0.38 | 0.71 | Institutional-decay and macro-development framing is recognizable—UN/DC process contrasted to personalized executive behavior. Many strongest claims (war-room origin stories, capacity) need primaries before they close. Often paired with **Diesen** on multipolar episodes rather than as the widest mechanics hub. |
| `jiang-xueqin` | 0.70 | 0.35 | 0.65 | Long-horizon PH / game-theory material is coherent inside its archive; calendar-facing checks are slow. Notebook use stays bounded by the PH routing rule; pairs with realist and multipolar lanes when the operator explicitly bridges. |
| `martin-armstrong` | 0.68 | 0.32 | 0.55 | Cycle-timing and macro-war convergence claims are a recognizable brand; falsifiable windows need dated model outputs or method disclosure, not vibes. Useful beside energy-logistics or sovereign-debt weeks when Hormuz or fiscal stress is the question. |

---

## Expert threads: predictive accuracy and opinion drift

**Intent:** **`expert_id` rows** are the right **bucket** for (1) **checkable** calls vs outcomes and (2) **same voice, different week** — how emphasis, mechanism, or verdict **moves** as facts and audiences shift. **Topic** tags organize *substance*; **expert** threads keep **who** stable so you can grep **time series** without mixing voices.

**What to log (minimum viable):** Only claims that are **checkable** against **primaries or wires** (not vibes). For each candidate “prediction” or conditional forecast:

1. **Quote or tight paraphrase** + **source URL** (transcript timestamp, post, article).
2. **Date** the expert said it (ingest date or stated event horizon).
3. **`thread:<expert_id>`** matching the **Anchor** row for **that** speaker.
4. **Falsify** — one sentence on what would make the call **wrong** (or what outcome resolves a conditional).
5. Later: **`resolved:`** + cite (wire / official readout) or **`deferred:`** + reason (still ambiguous, horizon not reached).

**Where to put it:** Same session as the ingest — optional **`batch-analysis`** line comparing two experts’ **testable** forks; or a bullet under **`### Open`** on the dated block in [`chapters/YYYY-MM/days.md`](chapters/2026-04/days.md) (replace month); or a running list in a scratch doc the operator names (no default new file). **Optional resolution pass:** [.cursor/skills/fact-check/SKILL.md](../../../../.cursor/skills/fact-check/SKILL.md) for tiered verdicts when wires exist.

**Guardrails:** **WORK only** — not Record, not **Voice** truth. Do **not** turn into **accuracy theater**: unfalsifiable rhetoric (“they are serious”) is **not** a prediction; **base rate** and **topic difficulty** matter; **conditional** forecasts (“if X then Y”) need **both** legs scored. Prefer **sparse** high-quality rows over scorecards full of mush.

### Changing opinions over time (drift / pivot detection)

**Why:** The same **`thread:<expert_id>`** on ingests **weeks apart** is the **join key** for “has this expert’s **story** changed?” — not only whether a single forecast hit.

**Minimum contrast (when you notice a shift):**

1. **Earlier** — date + source + one-line **thesis** (quote or tight paraphrase).
2. **Later** — date + source + one-line **thesis**.
3. **`thread:<expert_id>`** (same anchor).
4. **Delta** — label the move: **update** (new information integrated), **scope shift** (topic or audience changed), **emphasis** (same mechanism, different stress), **tension** (two claims need reconciliation — do not assume **contradiction** until you have both texts).

**Where to log:** A single **`batch-analysis | YYYY-MM-DD | …`** line can carry **A vs B** for the same voice; or **`### Open`** on the **later** date (“follow-up: compare to 2026-04-01 ingest”); **git log** / **grep** on `thread:<expert_id>` across [`daily-strategy-inbox.md`](daily-strategy-inbox.md) and [`days.md`](chapters/2026-04/days.md) history is the cheap detector.

**Guardrails:** **New facts** often justify revised judgment — distinguish **flip** from **Bayesian update**. Do **not** use drift tracking as **gotcha** copy unless the operator wants outreach; default is **notebook calibration**, not dunking.

---

## Crossing filters (what may cross the membrane)

Threads are **semi-permeable** by design; “optimization” here means **explicit rules** for what may **mix** so traceability stays high. This is **WORK** hygiene — not the **RECURSION-GATE** / Record membrane.

**Default allow (fast lane — crossing is permitted):**

1. **`batch-analysis | …`** lines that **name** the relationship (convergence / divergence / weak bridge) and implicitly or explicitly reference **which** `expert_id`s are in play — ideally aligned with the **Typical pairings** column.
2. **Two (or more) separate** paste-ready ingests, **each** with its own **`thread:<expert_id>`**, followed by **one** `batch-analysis` — membership is unambiguous.
3. **`days.md` `### Judgment`** bullets that **label** both experts when comparing (e.g. **Marandi × Ritter**) — prose bridge, not a merged ingest.
4. **Related voices** (below) and linked docs — **documented** seams (you already know the pore).

**Slow lane or block (do not merge without a seam):**

- **One** ingest line that **smuggles** two named experts’ claims **without** two cold attributions.
- **Cross-thread synthesis** promoted to **strong** public copy when **`verify:`** is still **OSINT / expert-commentary-only** — raise tier or narrow the claim.
- **Legitimacy plane** vs **hard security** plane — keep the **seam** from [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md); do not “solve” in one breath without naming both registers.

**Filter knobs (operator-tunable, no code required):**

| Knob | Effect |
|------|--------|
| **Index pairings** | Pre-approved **expert × expert** crosses for `batch-analysis` — start here before inventing new pairings. |
| **`verify:` tier** | **`tier-A`** / **`operator-transcript`** / etc. — controls how far a cross-thread line may travel outside the notebook. |
| **One primary `thread:` per ingest** | Keeps **drift** and **accuracy** joins clean; secondary voice = **second line** or **batch-analysis**. |
| **`crosses:` vs `seam:`** | **`crosses:<expert_id>+<expert_id>`** — use on **`batch-analysis`** when **two indexed ingests** each carry **`thread:`** for those slugs. **`seam:<slug>+<slug>`** — use when the batch compares **thematic planes** (government **X**, wire bundle, **ROME**, same-week topic fork) and **`crosses:`** would wrongly imply **two table Anchors**; example: **Spain × China** in [daily-strategy-inbox.md](daily-strategy-inbox.md) (`seam:sanchez-xi-summit+hormuz-brief-same-week`). |

**Optional `verify:` tail tokens** (all **optional** — use when you want grep + intent explicit):

- **`membrane:single`** — this line is **not** inviting pairing; `batch-analysis` should **not** fold it into a multi-thread claim without operator intent.
- **`membrane:pair`** — **invites** a following `batch-analysis` (same day) that names partners (e.g. after two ingests are captured).
- **`crosses:<id>+<id>`** — rare; **explicit** authorization when one line **synthesizes** two **`expert_id`** threads (prefer two ingests + `batch-analysis` instead).
- **`seam:<slug>+<slug>`** — optional, usually on a **`batch-analysis`** line: names **which two thematic planes** are held side-by-side when **`crosses:`** is wrong (e.g. **no** **`thread:`** on one side — government **X**, **wire** bundle, **ROME** seam). Short kebab slugs; **`+`** joins them. **Distinct from `membrane:`:** **`membrane:`** = pairing **intent** on **ingests**; **`seam:`** = machine-grep **label** for **what** the batch compares.

**Future automation (optional):** a small **validator script** could flag “`batch-analysis` mentions thread B but no ingest on this day has `thread:B`” — not required for the filter to work; **pairing discipline** + **git grep** already implement most of the membrane.

### Same transcript, show, or panel (multiple experts, one URL)

You do **not** get a special “joint thread.” You **populate** each expert’s lane with **separate paste-ready lines** — [daily-strategy-inbox.md](daily-strategy-inbox.md) **Multi-item ingest** rule: **one canonical line per excerpt / per voice**, **same episode URL repeated** on each line is normal.

1. **Line A** — **cold** names **Speaker A** + claim; **`thread:<expert_id_A>`** (their row in the table); **`verify:`** includes the shared URL (and timestamp/chapter if it helps grep).
2. **Line B** — **cold** names **Speaker B** + claim; **`thread:<expert_id_B>`**; **same URL**.
3. **`batch-analysis | YYYY-MM-DD | …`** — **immediately after** the **last** ingest in the set (membership anchor). Name **tension** or **convergence** between the two **threads**; optional **`membrane:pair`** on the first line only if you want grep to show “invites synthesis.”

**Default workflow (operator canon): assistant draft + explicit approval before append** — Upload the transcript in-session; have the assistant **draft** the full bundle (**one line per named expert** + shared URL + **`thread:<expert_id>`**s + **`batch-analysis`**) **in chat** (or a scratch file). Treat the draft as **provisional** until you **approve**. **Append** to [daily-strategy-inbox.md](daily-strategy-inbox.md) **only after** approval, or say **`EXECUTE`** / **explicit append** so the edit is deliberate. The assistant must **not** merge unreviewed bundles into the inbox by default.

**Host-only** segments (no separate expert row) — **omit** **`thread:`** until a **named indexed expert** speaks; or tag **`thread:`** only when the **cold** attributes quoted/analysis material to that **Anchor**. Keep **`verify:operator-transcript`** when the clip is still provisional.

**Rare shortcut:** One line **cannot** carry two primary `thread:` ids cleanly — if the clip is **inseparably joint**, use **one** line with **`thread:`** = **primary** voice for **drift** tracking, **cold** names both, and optional **`crosses:<id>+<id>`** — or still prefer **two lines** + **`batch-analysis`**.

---

## Deprecated `expert_id` values (operator removal)

**Topic-slug ids (deprecated 2026-04-14)** — Replaced by **person slugs** (one expert per lane). Git history / old inbox lines may still use these; **do not** use on new ingests.

| Deprecated | Use instead |
|------------|-------------|
| `islamabad-process` | `seyed-marandi` |
| `washington-channel` | `scott-ritter` |
| `lebanon-scope` | `trita-parsi` |
| `hormuz-domestic` | `robert-barnes` |
| `third-party-system` | `douglas-macgregor` |
| `game-theory-escalation` | `robert-pape` |
| `extension-game` | `daniel-davis` |
| `structural-pause` | `john-mearsheimer` |
| `diplomatic-institutional` | `alexander-mercouris` |

Removed from the table **2026-04-13** — **git history** still has prior rows; do **not** reuse these **`expert_id`s** for new anchors without clearing the deprecation note: `danny-haiphong`, `intervention-media-hawk`, `skyvirginson-lay-catholic`, `kelly-senate-catholic`, `narrative-faith-meme`, `delegation-babysitter`. **Coverage:** **Haiphong**-hosted digests stay linked from **`larry-johnson`** / digest file; **Keane**-class TV, **Kushner**/**Witkoff** narrators, **SkyVirginSon** / **Kelly** / **Milad** lanes → pair under existing rows (**`daniel-davis`**, **`scott-ritter`**, **`seyed-marandi`**, **`ROME`** / [trump-religion-papacy-arc.md](trump-religion-papacy-arc.md), **`narrative-escalation`** grep) instead of dedicated ids.

Removed from the table **2026-04-14** — **`hormuz-story-fork`** (anchors John Solomon / Chris Martenson). **Coverage:** U.S. domestic Hormuz story split (e.g. JTN “strategic asset” vs satirical spiral) → `batch-analysis` + topic tags only; pair with **`robert-barnes`** when a third pole matters. Git history / 2026-04-12 inbox lines may still name Solomon or Martenson; do **not** use `thread:hormuz-story-fork` on new ingests.

---

## Related voices (not separate rows)

- **Andrew Napolitano** — **Judging Freedom** **host**; **not** **`scott-ritter`**. **`scott-ritter`** = **Scott Ritter** ingests only. **Host-only** segments → [daily-strategy-inbox.md](daily-strategy-inbox.md) **Host-only** rule: **`thread:`** only when a **named** indexed expert speaks, else **omit**.
- **`@Pontifex` / Holy See** — Institutional **Rome** line: use **`ROME`**, [ROME-PASS.md](../work-strategy-rome/ROME-PASS.md), [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md); not a freelance **expert** row.
- **Joe Kent** — Resignation-letter **war rationale**; pair with **`daniel-davis`** / **`scott-ritter`** when citing, not a duplicate of IAEA/DNI.
- **Milad33B** — **Meme** / **faith-escalation** lane: use **`narrative-escalation`** + `Milad` in cold and [trump-religion-papacy-arc.md](trump-religion-papacy-arc.md); policy Hormuz threads stay separate.

---

## File links

- Inbox format: [daily-strategy-inbox.md](daily-strategy-inbox.md)  
- Rome–Persia legitimacy: [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md)  
- Tri-Frame minds: [minds/README.md](../minds/README.md)  
- Haiphong / Ritter / Johnson digest: [transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)  
- Fact-check skill (resolution / tiered verdicts): [.cursor/skills/fact-check/SKILL.md](../../../../.cursor/skills/fact-check/SKILL.md)
