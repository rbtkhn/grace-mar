# Strategy notebook — operator preferences

**Status:** ACTIVE  
**Set:** 2026-04 (from multiple-choice questionnaire)  
**Governed by:** [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) — this file **narrows** daily practice; it does not replace architecture for repo-wide defaults (e.g. architecture still describes a **~1000w** consolidated target where no override applies).  
**Skill contract:** Together with the architecture doc and [daily-strategy-inbox.md](daily-strategy-inbox.md), this file is **part of** [`skill-strategy`](../../../../.cursor/skills/skill-strategy/SKILL.md) — operator defaults the skill **must** apply on a **`strategy`** pass; not optional flavor beside the skill.

---

## Summary

| Area | Preference |
|------|------------|
| **Daily length** | **Variable by day** — no fixed default word budget. |
| **Minimum `days.md` sections** | **`### Signal` · `### Judgment` · `### Links`** only. |
| **Weave-time prose register** | **Popular-academic** by default — reader-facing **Signal / Judgment** in `days.md` after **weave**; avoid **internal repo nicknames**, **operator-only path tokens**, and **backend shorthand** in the **notebook spine** (spell out ideas or use public equivalents). Operator docs and inbox may keep technical labels. Aligns with [skill-strategy Session hygiene](../../../../.cursor/skills/skill-strategy/SKILL.md) § *Session hygiene*. |
| **Inbox vs notebook** | **Raw paste and URL dumps** → [daily-strategy-inbox.md](daily-strategy-inbox.md). **Notebook** = **synthesis + key links**, not mirrors of the inbox. |
| **Weave → page structure** | **Promotion choice** — what lands under **Signal** vs **Judgment** vs **Links** vs **Open** follows **what you choose to weave** and at **which** weave, not inbox length or equal padding per section. Intra-day weaves **iterate one** `## YYYY-MM-DD` block (merge, don’t duplicate). See [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Weave choice and section weighting*. |
| **Judgment priority** | **Structural first** — power, incentives, constraints; narrative second. |
| **Islamabad / US–Iran / pause** | When the day touches this thread, **always capture scope fights**: what is in/out of the **pause**, **Lebanon**, **Hormuz** definition. |
| **Leo XIV / Holy See / Rome (primary thread)** | **Voice** = papal / Holy See moral–diplomatic lines (**Leo XIV**, `@Pontifex`, audiences). **Hub** = [work-strategy-rome](../work-strategy-rome/README.md) + [ROME-PASS](../work-strategy-rome/ROME-PASS.md). When the day touches this thread, **keep planes separate** from Beltway mechanics: **IHL / legitimacy vocabulary** is not a forecast of **kinetic** facts; weave **Judgment** with **dated** vatican.va or press-office URLs when claiming official text (see ROME-PASS source order). If **Lebanon** (or other crises) appears in **both** expert-commentary and papal lines, prefer **two bullets** or **Thesis A / B** — do not merge registers without verify. |
| **JD Vance / VP channel (primary thread)** | **Voice** = **Vice President** public lines, travel, and **White House** readouts (not Senate archive unless window-relevant). **Hub** = [daily-brief-jd-vance-watch.md](../daily-brief-jd-vance-watch.md) (**§1e** in daily briefs — coffee **C** pass). When the day touches **U.S.–Iran**, **Islamabad**, **war powers**, or **coalition** framing, **tag whether Vance is acting as channel** (delegation lead, “final offer” voice, restraint narrative) vs **atmospheric** quote — separate **official** URL from **cable analysis**. If **Vance** and **Pentagon / State** lines **diverge** on scope (**Lebanon**, **Hormuz**, pause), **two bullets** or **Thesis A / B**; do not collapse into one “White House says.” |
| **Vladimir Putin / Kremlin (primary thread)** | **Voice** = **Russian President** public lines, **Kremlin** schedule (events, calls, transcripts). **Hub** = [daily-brief-putin-watch.md](../daily-brief-putin-watch.md) (**§1d** — coffee **C** pass, rolling **48h**). When the day touches **Ukraine**, **Iran** (Russia as actor), **NATO**, or **multilateral** ceasefire framing, separate **Kremlin-primary** quotes from **Western wire paraphrase**; add **Russian-language or Kremlin-primary** triangulation per [daily-brief-native-international-pass.md](../daily-brief-native-international-pass.md) when Russia is load-bearing. If **Putin** lines and **U.S. / allied** readouts **diverge** on **facts or scope**, **two bullets** or **Thesis A / B** — do not merge **personality** headlines with **operational** claims without URLs. |
| **PRC / Beijing (primary thread)** | **Voice** = **People’s Republic of China** **party–state** lines (**MFA**, **summits**, major **state** readouts). **Hub** = [daily-brief-prc-watch.md](../daily-brief-prc-watch.md) (**§1g** — coffee **C** pass, rolling **48h**). When the day touches **U.S.–China**, **cross-strait**, **Indo-Pacific**, **trade / sanctions**, or **PRC** as **named** party beside **Russia** / **Iran** / **U.S.** stories, separate **MFA / state-primary** wording from **Western** “China” **analysis**; add **Mandarin-primary** triangulation per [daily-brief-native-international-pass.md](../daily-brief-native-international-pass.md) when the PRC thread is load-bearing. If **Beijing** and **Washington** lines **diverge** on **terms or scope**, **two bullets** or **Thesis A / B**. |
| **Islamic Republic of Iran (primary thread)** | **Voice** = **Iranian state** lines (**MFA**, **presidency**, **IRNA** / major **state-adjacent** wires). **Hub** = [daily-brief-iran-watch.md](../daily-brief-iran-watch.md) (**§1h** — coffee **C** pass, rolling **48h**). **Not** a substitute for the **Islamabad** bargaining **framework** ([islamabad-operator-index.md](../islamabad-operator-index.md), gap matrices)—use **both**: framework for **trade space**, IRI watch for **what Tehran says** on **pause**, **Hormuz**, **Lebanon**, **nuclear** terms. Separate **Persian-primary** or **MFA** quotes from **Western** “Iran” **digest**; add **Persian** triangulation per [daily-brief-native-international-pass.md](../daily-brief-native-international-pass.md) when the Iran thread is load-bearing. If **Tehran** and **Washington** lines **diverge** on **facts or scope**, **two bullets** or **Thesis A / B**. |
| **Predictive History (work-jiang)** | **Episodic** — cite when you **actually** engaged lecture/corpus that day; no standing PH obligation in the notebook. |
| **Lenses (B / M / Merc)** | After **substantive** notebook-relevant work, assistant **offers three one-liners** — operator **picks or skips** (see [strategy-minds-granular.mdc](../../../../.cursor/rules/strategy-minds-granular.mdc)). |
| **Where lens depth lives** | **Daily brief mind shells** and **`minds/outputs/`** as needed; **strategy-notebook day block stays thin**. |
| **Inbox → `days.md`** | **Weave** at **`dream`** (day-end), on **`weave`** / **`fold`** (legacy) / **explicit** operator direction (intra-day), or equivalent — assistants do **not** append `days.md` on ingest alone (see [daily-strategy-inbox.md](daily-strategy-inbox.md)). |
| **Promotion to `STRATEGY.md`** | **Weekly** when the **week** had a **clear thesis** (not only rare milestones). |
| **STATUS.md** | **Minimal** — last entry / pointer; no rich dashboard unless asked. |
| **Uncertainty** | Emphasize **narrative and framing risk** over formal numeric confidence tags. |
| **Analogue-app patterns (Metaculus / Kialo / etc.)** | **Do not** add **numeric or ordinal confidence** tags, **forecast scoreboards**, or **argument-tree “impact” / branch-vote** metadata to default notebook or `skill-strategy` output — they **conflict** with the **Uncertainty** row unless this file is **revised** to allow them. Prefer **Thesis A / B** and falsifiers in `meta.md` / expert index. |
| **Conflicting experts** | **Two Judgment bullets** — **Thesis A** / **Thesis B** — preserve tension; no forced merge. |

---

## Short paste block (meta / handoff)

Operator notebook prefs: variable daily length; minimum Signal / Judgment / Links; weave-time prose popular-academic (no internal nicknames in spine). Inbox = raw; notebook = synthesis + key links. Weave choice weights sections (Signal/Judgment/Links/Open), not inbox order. Judgment leads structure. Islamabad / US–Iran: scope (pause, Lebanon, Hormuz). Leo XIV / Rome: moral–diplomatic plane vs mechanics; ROME-PASS source order. JD Vance: VP channel vs cable; §1e watch doc. Putin / Kremlin: §1d watch; Kremlin vs wire. PRC / Beijing: §1g watch; MFA vs Western analysis. IRI / Tehran: §1h watch; MFA/IRNA vs Western digest (framework = Islamabad index). PH when engaged that day. Offer B/M/M one-liners after substantive passes; lens depth in daily brief minds, notebook thin. Weave inbox at dream or explicit **weave** / **fold** (legacy); not on ingest alone. Promote to STRATEGY weekly on clear thesis. STATUS minimal. Framing risk over numeric confidence; analogue-app confidence scores / branch-vote metadata out of band until this file revises that. Split disagreements as Thesis A / Thesis B.

---

## Relation to assistants

- **Calibration / branch patterns from external analogue apps** (e.g. Metaculus-style scores, Kialo-style branch weights): gated by the **Analogue-app patterns** summary row — assistants **do not** introduce them into default captures or weaves until **Uncertainty** / that row is explicitly changed here.
- **Default on-disk capture** for strategy ingests remains **[daily-strategy-inbox.md](daily-strategy-inbox.md)** per [skill-strategy SKILL.md](../../../../.cursor/skills/skill-strategy/SKILL.md).
- **Rome / Leo XIV:** When the month’s **`meta.md`** includes **Leo XIV / Rome helix** or ingests touch the Holy See, follow [ROME-PASS](../work-strategy-rome/ROME-PASS.md) source order for **Judgment** claims; optional **`ROME` / `LeoXIV`** tags in inbox cold lines per [daily-strategy-inbox.md](daily-strategy-inbox.md).
- **JD Vance:** When **`meta.md`** includes **JD Vance thread** or the day covers **Islamabad / VP travel / war powers**, align notebook **Links** with [daily-brief-jd-vance-watch.md](../daily-brief-jd-vance-watch.md) guardrails (URLs, 48h window); optional **`JDVance` / `VANCE`** tags in inbox cold lines.
- **Putin / Kremlin:** When **`meta.md`** includes **Putin thread** or the day covers **Ukraine**, **Russia** as negotiation actor, or **NATO**–Russia framing, align **Links** with [daily-brief-putin-watch.md](../daily-brief-putin-watch.md) (Kremlin + wire + native triangulation); optional **`PUTIN` / `KREMLIN`** tags in inbox cold lines.
- **PRC / Beijing:** When **`meta.md`** includes **PRC thread** or the day covers **U.S.–China**, **cross-strait**, **Indo-Pacific**, or **PRC**–adjacent **trade** / **sanctions**, align **Links** with [daily-brief-prc-watch.md](../daily-brief-prc-watch.md) (MFA + wire + Mandarin triangulation); optional **`PRC` / `CN` / `CHINA`** tags in inbox cold lines.
- **IRI / Tehran:** When **`meta.md`** includes **IRI thread** or the day covers **Islamabad**, **pause / Hormuz / Lebanon**, **nuclear** talks, or **Iranian** **state** messaging, align **Links** with [daily-brief-iran-watch.md](../daily-brief-iran-watch.md) (MFA + IRNA + Persian triangulation) alongside **Islamabad** framework artifacts when relevant; optional **`IRAN` / `IRI` / `TEHRAN`** tags in inbox cold lines.
- **Do not** extend `chapters/YYYY-MM/days.md` unless **`dream`** weave, **`weave`** / **`fold`** (legacy) / **explicit** operator instruction, or equivalent — unchanged. Section weighting per weave: architecture § *Weave choice and section weighting*.

---

## Changelog

| Date | Change |
|------|--------|
| 2026-04-12 | Initial preferences from operator questionnaire (1D, 2A, 3A, 4A, 5A, 6D, 7C, 8C, 9A, 10B, 11A, 12C, 13C). |
| 2026-04-12 | **Leo XIV / Rome primary thread:** naming — **Leo XIV / Holy See** = voice; **ROME-PASS** / **work-strategy-rome** = hub. Implementation: architecture paragraph + `meta.md` helix + inbox grep tags + `skill-strategy` + [daily-brief-focus.md](../daily-brief-focus.md). |
| 2026-04-12 | **JD Vance primary thread:** **VP channel** = voice; [daily-brief-jd-vance-watch.md](../daily-brief-jd-vance-watch.md) = hub — mirrored in architecture, `meta.md`, inbox tags, `skill-strategy`, [daily-brief-focus.md](../daily-brief-focus.md). |
| 2026-04-12 | **Vladimir Putin / Kremlin primary thread:** [daily-brief-putin-watch.md](../daily-brief-putin-watch.md) = hub — same mirror pattern as JD Vance / Rome. |
| 2026-04-12 | **PRC / Beijing primary thread:** [daily-brief-prc-watch.md](../daily-brief-prc-watch.md) = hub (**§1g**); generator + `meta` + prefs + `skill-strategy`. |
| 2026-04-12 | **Islamic Republic of Iran primary thread:** [daily-brief-iran-watch.md](../daily-brief-iran-watch.md) = hub (**§1h**); complements Islamabad index; generator + `meta` + prefs + `skill-strategy`. |
| 2026-04-11 | **Weave → page structure:** [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Weave choice and section weighting*; inbox weave rhythm cross-link; prefs table + Relation to assistants + short paste block (explicit intra-day **weave**). |
| 2026-04-14 | **Operator command `weave`:** Canonical name for inbox → `days.md` merge; **`fold`** retained as legacy synonym ([STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Weave vs fold*; [skill-strategy SKILL.md](../../../../.cursor/skills/skill-strategy/SKILL.md) **Weave** mode). |
