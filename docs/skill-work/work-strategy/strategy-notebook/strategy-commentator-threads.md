# Strategy commentator threads (index)

**Purpose:** Stable **thread ids** for recurring **analyst / commentator** ingests so `batch-analysis` lines can name **divergence and correlation** without re-deriving the roster each session. **WORK only** — not Record.

**Topic threads vs analyst threads (mental model):** It helps to separate two layers — they are not mutually exclusive.

- **Topic threads** — *what* the ingest is about: recurring **substantive** lanes (e.g. **Islamabad** negotiation arc, **Hormuz** / blockade / sea control, **Lebanon vs nuclear** scope, **U.S. domestic** liability on executive war policy, **escalation / game-theory** commitment, **third-country** / importer distance from the kinetic frame, **Rome** / legitimacy when the Holy See or faith-politics is the axis). These often show up as **grep tags** (`IRAN`, `JDVance`, `ROME`, `narrative-escalation`, …) or as **Related voices** / linked docs ([rome-persia-legitimacy-signal-check.md](rome-persia-legitimacy-signal-check.md), [trump-religion-papacy-arc.md](trump-religion-papacy-arc.md)).
- **Analyst threads** — *who* is speaking: a stable **voice** or **show** anchor (the **Anchor** column below). The table is **analyst-first** so pairings stay grep-friendly.

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
