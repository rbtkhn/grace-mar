# Strategy commentator threads (index)

**Purpose:** Stable **thread ids** for recurring **analyst / commentator** ingests so `batch-analysis` lines can name **divergence and correlation** without re-deriving the roster each session. The same **`thread:<id>`** on **different dates** is the **join key** for **accuracy** checks and **opinion drift** (see **Analyst threads: predictive accuracy and opinion drift**). **WORK only** — not Record.

**Topic threads vs analyst threads (mental model):** It helps to separate two layers — they are not mutually exclusive.

- **Topic threads** — *what* the ingest is about: recurring **substantive** lanes (e.g. **Islamabad** negotiation arc, **Hormuz** / blockade / sea control, **Lebanon vs nuclear** scope, **U.S. domestic** liability on executive war policy, **escalation / game-theory** commitment, **third-country** / importer distance from the kinetic frame, **Rome** / legitimacy when the Holy See or faith-politics is the axis). These often show up as **grep tags** (`IRAN`, `JDVance`, `ROME`, `narrative-escalation`, …) or as **Related voices** / linked docs ([rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md), [trump-religion-papacy-arc.md](trump-religion-papacy-arc.md)).
- **Analyst threads** — *who* is speaking: a stable **voice** or **show** anchor (the **Anchor** column below). The table is **analyst-first** so pairings stay grep-friendly. Reusing **`thread:<id>`** across weeks lets you **diff** the same voice over time (drift / pivot), not only compare analysts in one session.

Many **`thread_id`** rows are **hybrid**: the id is tied to a **named analyst** but the **Role** line is really a **topic signature** (e.g. `islamabad-process`, `lebanon-scope`, `hormuz-domestic`). **`batch-analysis`** is where **topic** tension (same crisis, different mechanisms) meets **analyst** tension (same week, different predictions or moral registers).

**How to use:** When appending a paste-ready line in [daily-strategy-inbox.md](daily-strategy-inbox.md), add **`thread:<id>`** to the **`verify:`** tail or prefix the cold clause with the **grep tag** below. Pair ingests in **`batch-analysis | YYYY-MM-DD | …`** using **Typical pairings**.

**Maintenance:** Add rows when a new anchor appears **repeatedly** in `days.md` or inbox; **deprecate** with a line in **Notes** — do not delete history without operator say-so.

---

| thread_id | Anchor | Role (one line) | Default grep tag | Typical `batch-analysis` pairings |
|-----------|--------|-----------------|------------------|-----------------------------------|
| `islamabad-process` | Seyed Mohammad Marandi | Iranian English long-form: negotiation **process**, red lines, legitimacy register | `IRAN`, `TEHRAN`, or `Marandi` in cold | × `washington-channel` (Ritter), × `lebanon-scope` (Parsi), × `rome-ecumenical` (Pontifex / Marandi Easter) |
| `washington-channel` | Scott Ritter; Andrew Napolitano (host) | U.S. **military dissent**: Hormuz **sea control**, blockade ops, Vance frame; separate **faith-politics** register | `JDVance`, `IRAN`, or `Ritter` | × `islamabad-process`, × `hormuz-domestic` (Barnes), × `rome-invective` (split from ecumenical) |
| `lebanon-scope` | Trita Parsi (`@tparsi`) | Beltway-facing **Lebanon vs nuclear** scope; “mask” thesis | `IRAN` + Parsi in cold | × `holy-see-moral` (Pontifex Lebanon), × `islamabad-process`, × `third-party-system` |
| `hormuz-domestic` | Robert Barnes (`@barnes_law`) | **Domestic liability** pole on Hormuz / executive TS chain | `JDVance` or `barnes` in cold | × `hormuz-story-fork` (Solomon/Martenson), × `game-theory-escalation` (Pape) |
| `hormuz-story-fork` | John Solomon (`@jsolomonReports`); Chris Martenson (`@chrismartenson`) | **Two U.S. narratives**: blockade as asset vs **spiral / satire** | tag both handles in cold | × `hormuz-domestic` (Barnes third pole); **three-way** domestic fork |
| `third-party-system` | Douglas Macgregor (`@DougAMacgregor`) | Importers / **Asia–Europe** distance from U.S.–Israel kinetic frame | `IRAN` or Macgregor in cold | × `game-theory-escalation` (Pape), × `structural-pause` (Mearsheimer), × `lebanon-scope` |
| `game-theory-escalation` | Robert Pape (`@ProfessorPape`) | **Escalation Trap** / commitment ratchet on demands | `ProfessorPape` or Pape in cold | × `extension-game` (Davis), × `hormuz-domestic`, × `structural-pause` |
| `extension-game` | Daniel Davis (Lt Col; `@DanielLDavis1`) | Ceasefire as **extension game**; ultimatum vs negotiation; macro pain to U.S. | `IRAN`, `JDVance`, or Davis in cold | × `structural-pause` (Mearsheimer), × `game-theory-escalation`, × `islamabad-process` |
| `structural-pause` | John Mearsheimer; Glenn Diesen (session pair) | **Offensive realism**: security dilemma, Israel structural, great-power geometry | `MEARSHEIMER` or session cite in cold | × `extension-game` (Davis material vs structure), × `diplomatic-institutional` (Mercouris), × `glenn-diesen` (solo Diesen ingests) |
| `diplomatic-institutional` | Alexander Mercouris | **Institutional / narrative** diplomatic read (Hormuz, Lebanon, Islamabad) | `Mercouris` or mind cite in cold | × `structural-pause`, × `islamabad-process`, × Tri-Frame [minds/](../minds/README.md) |
| `larry-johnson` | Larry Johnson | Ex-CIA / **material** and **ORBAT** emphasis: force structure, **Hormuz** geometry, **F-15/Isfahan** raid narrative reconstructions (Haiphong–Ritter roundtables) | `Johnson` or `LarryJohnson` in cold | × `washington-channel` (Ritter), × `extension-game` (Davis); see [transcript digest](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) |
| `charles-freeman` | Charles (“Chas”) Freeman | Retired **career diplomat**: **inconclusive** talks, **alliance** and **material** framing (Islamabad as diplomacy-while-war); **separate plane** from papal **moral** register | `Freeman` or `ChasFreeman` in cold | × `lebanon-scope` (Parsi), × `diplomatic-institutional` (Mercouris), × [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md) (**seam**, not merge) |
| `alastair-crooke` | Alastair Crooke | Former diplomat / **Levant–Islamabad** “room” and **spoiler** reads; often beside **Davis** in digests | `Crooke` in cold | × `extension-game`, × `islamabad-process`, × `lebanon-scope` |
| `glenn-diesen` | Glenn Diesen | **Eurasia / multipolar** discourse as **standalone** ingest (when not folded only into `structural-pause` session label) | `Diesen` in cold | × `structural-pause`, × `third-party-system`, × `game-theory-escalation` |

---

## Analyst threads: predictive accuracy and opinion drift

**Intent:** **Analyst** `thread_id`s are the right **bucket** for (1) **checkable** calls vs outcomes and (2) **same voice, different week** — how emphasis, mechanism, or verdict **moves** as facts and audiences shift. **Topic** threads organize *substance*; **analyst** threads keep **who** stable so you can grep **time series** without mixing voices.

**What to log (minimum viable):** Only claims that are **checkable** against **primaries or wires** (not vibes). For each candidate “prediction” or conditional forecast:

1. **Quote or tight paraphrase** + **source URL** (transcript timestamp, post, article).
2. **Date** the analyst said it (ingest date or stated event horizon).
3. **`thread:<id>`** matching the **Anchor** row (or closest hybrid row).
4. **Falsify** — one sentence on what would make the call **wrong** (or what outcome resolves a conditional).
5. Later: **`resolved:`** + cite (wire / official readout) or **`deferred:`** + reason (still ambiguous, horizon not reached).

**Where to put it:** Same session as the ingest — optional **`batch-analysis`** line comparing two analysts’ **testable** forks; or a bullet under **`### Open`** on the dated block in [`chapters/YYYY-MM/days.md`](chapters/2026-04/days.md) (replace month); or a running list in a scratch doc the operator names (no default new file). **Optional resolution pass:** [.cursor/skills/fact-check/SKILL.md](../../../../.cursor/skills/fact-check/SKILL.md) for tiered verdicts when wires exist.

**Guardrails:** **WORK only** — not Record, not **Voice** truth. Do **not** turn into **accuracy theater**: unfalsifiable rhetoric (“they are serious”) is **not** a prediction; **base rate** and **topic difficulty** matter; **conditional** forecasts (“if X then Y”) need **both** legs scored. Prefer **sparse** high-quality rows over scorecards full of mush.

### Changing opinions over time (drift / pivot detection)

**Why:** The same **`thread:<id>`** on ingests **weeks apart** is the **join key** for “has this analyst’s **story** changed?” — not only whether a single forecast hit.

**Minimum contrast (when you notice a shift):**

1. **Earlier** — date + source + one-line **thesis** (quote or tight paraphrase).
2. **Later** — date + source + one-line **thesis**.
3. **`thread:<id>`** (same anchor).
4. **Delta** — label the move: **update** (new information integrated), **scope shift** (topic or audience changed), **emphasis** (same mechanism, different stress), **tension** (two claims need reconciliation — do not assume **contradiction** until you have both texts).

**Where to log:** A single **`batch-analysis | YYYY-MM-DD | …`** line can carry **A vs B** for the same voice; or **`### Open`** on the **later** date (“follow-up: compare to 2026-04-01 ingest”); **git log** / **grep** on `thread:<id>` across [`daily-strategy-inbox.md`](daily-strategy-inbox.md) and [`days.md`](chapters/2026-04/days.md) history is the cheap detector.

**Guardrails:** **New facts** often justify revised judgment — distinguish **flip** from **Bayesian update**. Do **not** use drift tracking as **gotcha** copy unless the operator wants outreach; default is **notebook calibration**, not dunking.

---

## Crossing filters (what may cross the membrane)

Threads are **semi-permeable** by design; “optimization” here means **explicit rules** for what may **mix** so traceability stays high. This is **WORK** hygiene — not the **RECURSION-GATE** / Record membrane.

**Default allow (fast lane — crossing is permitted):**

1. **`batch-analysis | …`** lines that **name** the relationship (convergence / divergence / weak bridge) and implicitly or explicitly reference **which** `thread_id`s are in play — ideally aligned with the **Typical pairings** column.
2. **Two (or more) separate** paste-ready ingests, **each** with its own **`thread:<id>`**, followed by **one** `batch-analysis` — membership is unambiguous.
3. **`days.md` `### Judgment`** bullets that **label** both lanes when comparing (e.g. **Marandi × Ritter**) — prose bridge, not a merged ingest.
4. **Hybrid** table rows and **Related voices** — **documented** pores (you already know the seam).

**Slow lane or block (do not merge without a seam):**

- **One** ingest line that **smuggles** two named analysts’ claims **without** two cold attributions.
- **Cross-thread synthesis** promoted to **strong** public copy when **`verify:`** is still **OSINT / analyst-only** — raise tier or narrow the claim.
- **Legitimacy plane** vs **hard security** plane — keep the **seam** from [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md); do not “solve” in one breath without naming both registers.

**Filter knobs (operator-tunable, no code required):**

| Knob | Effect |
|------|--------|
| **Index pairings** | Pre-approved **analyst × analyst** crosses for `batch-analysis` — start here before inventing new pairings. |
| **`verify:` tier** | **`tier-A`** / **`operator-transcript`** / etc. — controls how far a cross-thread line may travel outside the notebook. |
| **One primary `thread:` per ingest** | Keeps **drift** and **accuracy** joins clean; secondary voice = **second line** or **batch-analysis**. |

**Optional `verify:` tail tokens** (all **optional** — use when you want grep + intent explicit):

- **`membrane:single`** — this line is **not** inviting pairing; `batch-analysis` should **not** fold it into a multi-thread claim without operator intent.
- **`membrane:pair`** — **invites** a following `batch-analysis` (same day) that names partners (e.g. after two ingests are captured).
- **`crosses:<id>+<id>`** — rare; **explicit** authorization when one line **synthesizes** two threads (prefer two ingests + `batch-analysis` instead).

**Future automation (optional):** a small **validator script** could flag “`batch-analysis` mentions thread B but no ingest on this day has `thread:B`” — not required for the filter to work; **pairing discipline** + **git grep** already implement most of the membrane.

### Same transcript, show, or panel (multiple analysts, one URL)

You do **not** get a special “joint thread.” You **populate** each analyst’s lane with **separate paste-ready lines** — [daily-strategy-inbox.md](daily-strategy-inbox.md) **Multi-item ingest** rule: **one canonical line per excerpt / per voice**, **same episode URL repeated** on each line is normal.

1. **Line A** — **cold** names **Speaker A** + claim; **`thread:<id_A>`** (their row in the table); **`verify:`** includes the shared URL (and timestamp/chapter if it helps grep).
2. **Line B** — **cold** names **Speaker B** + claim; **`thread:<id_B>`**; **same URL**.
3. **`batch-analysis | YYYY-MM-DD | …`** — **immediately after** the **last** ingest in the set (membership anchor). Name **tension** or **convergence** between the two **threads**; optional **`membrane:pair`** on the first line only if you want grep to show “invites synthesis.”

**Default workflow (operator canon): assistant draft + explicit approval before append** — Upload the transcript in-session; have the assistant **draft** the full bundle (**one line per named analyst** + shared URL + **`thread:<id>`**s + **`batch-analysis`**) **in chat** (or a scratch file). Treat the draft as **provisional** until you **approve**. **Append** to [daily-strategy-inbox.md](daily-strategy-inbox.md) **only after** approval, or say **`EXECUTE`** / **explicit append** so the edit is deliberate. The assistant must **not** merge unreviewed bundles into the inbox by default.

**Host-only** segments (no separate analyst row) — tag **`thread:`** by **substance** (closest **hybrid** row, e.g. `islamabad-process` for process commentary) or **omit** `thread:` and keep **`verify:operator-transcript`** until a named analyst speaks.

**Rare shortcut:** One line **cannot** carry two primary `thread:` ids cleanly — if the clip is **inseparably joint**, use **one** line with **`thread:`** = **primary** voice for **drift** tracking, **cold** names both, and optional **`crosses:<id>+<id>`** — or still prefer **two lines** + **`batch-analysis`**.

---

## Deprecated thread ids (operator removal)

Removed from the table **2026-04-13** — **git history** still has prior rows; do **not** reuse these ids for new anchors without clearing the deprecation note: `danny-haiphong`, `intervention-media-hawk`, `skyvirginson-lay-catholic`, `kelly-senate-catholic`, `narrative-faith-meme`, `delegation-babysitter`. **Coverage:** **Haiphong**-hosted digests stay linked from **`larry-johnson`** / digest file; **Keane**-class TV, **Kushner**/**Witkoff** narrators, **SkyVirginSon** / **Kelly** / **Milad** lanes → pair under existing rows (**`extension-game`**, **`washington-channel`**, **`islamabad-process`**, **`ROME`** / [trump-religion-papacy-arc.md](trump-religion-papacy-arc.md), **`narrative-escalation`** grep) instead of dedicated ids.

---

## Related voices (not separate rows)

- **`@Pontifex` / Holy See** — Institutional **Rome** line: use **`ROME`**, [ROME-PASS.md](../work-strategy-rome/ROME-PASS.md), [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md); not a freelance **analyst** row.
- **Joe Kent** — Resignation-letter **war rationale**; pair with **`extension-game`** / **`washington-channel`** when citing, not a duplicate of IAEA/DNI.
- **Milad33B** — **Meme** / **faith-escalation** lane: use **`narrative-escalation`** + `Milad` in cold and [trump-religion-papacy-arc.md](trump-religion-papacy-arc.md); policy Hormuz threads stay separate.

---

## File links

- Inbox format: [daily-strategy-inbox.md](daily-strategy-inbox.md)  
- Rome–Persia legitimacy: [rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md)  
- Tri-Frame minds: [minds/README.md](../minds/README.md)  
- Haiphong / Ritter / Johnson digest: [transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md](../transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md)  
- Fact-check skill (resolution / tiered verdicts): [.cursor/skills/fact-check/SKILL.md](../../../../.cursor/skills/fact-check/SKILL.md)
