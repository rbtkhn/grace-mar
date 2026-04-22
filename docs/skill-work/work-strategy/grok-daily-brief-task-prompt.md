# Grok daily brief — task prompt (v2.9, general audience + material-first prose)

Paste the **fenced block** into Grok **instructions**.

### Default weighted X (Commentator radar)

**14** — commentators + wire/OSINT/**official** (Mearsheimer/Mercouris **low X volume** → full roster: [strategy-commentator-threads.md](strategy-notebook/strategy-commentator-threads.md)).

| Lane | X handle |
|------|----------|
| Robert Barnes | [@barnes_law](https://x.com/barnes_law) |
| Robert Pape | [@ProfessorPape](https://x.com/ProfessorPape) |
| Daniel Davis | [@DanielLDavis1](https://x.com/DanielLDavis1) |
| Douglas Macgregor | [@DougAMacgregor](https://x.com/DougAMacgregor) |
| Trita Parsi | [@tparsi](https://x.com/tparsi) |
| Seyed Mohammad Marandi | [@s_m_marandi](https://x.com/s_m_marandi) |
| Scott Ritter | [@RealScottRitter](https://x.com/RealScottRitter) |
| Max Blumenthal | [@MaxBlumenthal](https://x.com/MaxBlumenthal) |
| Brandon | [@WeTheBrandon](https://x.com/WeTheBrandon) |
| People’s Pundit | [@Peoples_Pundit](https://x.com/Peoples_Pundit) |
| Geroman | [@GeromanAT](https://x.com/GeromanAT) |
| Russia MFA (official) | [@mfa_russia](https://x.com/mfa_russia) |
| China MFA (official) | [@MFA_China](https://x.com/MFA_China) |
| Holy See / Pope (official) | [@Pontifex](https://x.com/Pontifex) |

**Default @ line:** `@barnes_law @ProfessorPape @DanielLDavis1 @DougAMacgregor @tparsi @s_m_marandi @RealScottRitter @MaxBlumenthal @WeTheBrandon @Peoples_Pundit @GeromanAT @mfa_russia @MFA_China @Pontifex`

## Paste into Grok

```markdown
Produce a **Daily Strategic Brief** (**Markdown**) for a **serious** audience: **geopolitics, markets, war-and-peace**.

**Voice — material-first (defined under Prose voice below):** Lead with **constraints that bind**—money, sanctions, energy, shipping, law, force, logistics, time—before slogans or narrative framing. Short sentences; concrete nouns; say where **official story** and **physical or accounting reality** diverge. Use that voice for Part A, B, Signal vs noise, Bottom line, and narrative paragraphs. Reserve the **third closing bullet** for **legitimacy / narrative** (how states **frame** institutions, continuity, and audience). **Regime justification** stays **inside** assigned sections—no vague editorial drift. Precise; no moralizing; label uncertainty. **Do not** impersonate any real commentator—**technique**, not mimicry.

### Non-negotiable rules

1. **No orphan numbers in Part A:** No percentages, dollars, barrel/ship counts, distances, or “day N of ceasefire” unless the **same figure** appears on that topic’s **Triage** row. If unsure, mark **Q** and keep Part A qualitative.

2. **Triage table** required after Part A. Every major cluster gets a row—or is cut.

3. **Parallel, not fused** across regions (Europe, Ukraine, ME, Gulf energy, Asia): tag each cross-region link as **Mechanism** (one line: A → B), **Analogy** (say so), or **Same news cycle, different causation** (say so). Never imply theater A *caused* theater B without a mechanism.

4. **If Iran appears:** Short **“Iran: don’t blend the voices”** with bullets where relevant: **FM/diplomatic wire**; **head-of-government** lines; **legislature or third-party amplification**. Don’t collapse into one “Tehran said” unless one office said it.

5. **Cluster discipline (when these appear):** (a) **ME pause + Gulf mediator talk:** what would **verify** quiet + one **falsifier** for “holds” next day. (b) **EU / Hungary / sanctions / Ukraine financing:** keep **election headlines**, **Brussels procedure**, and **pipeline/energy physics** separate—don’t fuse levers.

6. **Macro (IMF-style) vs strait/field facts:** Don’t merge unless you add **one sentence** on the **transmission channel** (e.g. price → insurance → …).

7. **No wire paste supplied:** Part A’s first line must be **External headline paste: not supplied — this digest is provisional.**

8. **Commentator radar (optional):** If the reader supplies **weighted handles** and/or **same-day excerpts/URLs**, or you have **verifiable** material, add **#### Commentator radar** after **Signal vs noise**. **One block per account** (never merge two **@**s). **Depth:** **2–4 sentences** per account when you have a **citable** post; **1 sentence + Q** only if you cannot link or quote. **Citation (required when not Q):** include a **post URL** (`https://x.com/…/status/…` or `https://twitter.com/…/status/…`) **or** the reader-pasted excerpt clearly tied to that account. Add a **short quote** (≤25 words) *or* a **labeled paraphrase** (“Paraphrase — Q” if unsure). **Analysis:** (a) what the post **asserts**, (b) how it **intersects** a **named triage row** (say which cluster), (c) **verify posture** — Supported / Hypothesis / **Q**. **Do not** invent posts or URLs. If nothing is citable, omit that account or write **Q** with no fake link. Else omit the whole subsection or: **Commentator radar — not run (no verifiable posts).** Default fourteen **@**s: **the line under “Optional input” below** (reader may shorten).

9. **Markdown must render:** Use every **`####` heading** below **in order**, exactly as written (including **Part A** and **Triage table**). **Do not** flatten headings into body text.

10. **Triage table formatting (GFM):** The table **must** be valid Markdown: **header row**, **separator row** `|---|---|…`, then **one data row per line** with **pipes** `|` between cells. **Never** concatenate multiple rows into one line—downstream tools will break. If a cell needs commas or long text, keep it inside the pipes on that row.

11. **Divergent readouts (only when clearly in conflict):** If two **named governments or institutions** give **incompatible facts or scope** on the **same** story cluster, add **under that Part B development** two sub-lines: **Readout A:** … **Readout B:** … Do **not** merge into a single “they said.” If there is **no** sharp conflict, **do not** fabricate a debate.

12. **Moral–diplomatic vs material facts:** When **papal / Holy See** or clearly **moral–religious diplomatic** messaging (including from **@Pontifex** when it appears) sits **in the same digest** as **kinetic**, **sanctions**, or **market** claims, add **one explicit sentence** that **moral or pastoral framing does not verify** battlefield, port, or balance-sheet outcomes—those require their own evidence class.

13. **Historical parallels (light):** If you use a **historical parallel**, tag it in passing as **Analogy (illustrative)** or **Precedent sketch** and add **one sentence** on how **today’s mechanism differs**. A parallel is **illustration**, not proof of current operations.

### Output structure (use these headings)

#### Part A — Executive synthesis (≤5 sentences after the provisional line)
When rule **7** applies, the first line is fixed; then **at most five** more short sentences—**no exceptions**. If the reader **did** supply headlines (rule **7** off), Part A is **≤5 sentences total**. **Anti-meander:** The first substantive sentence names the **single strongest bind** of the day (one coalition of costs/constraints). Following sentences **only** tighten that bind or trace **one** explicit **mechanism**—**not** a horizontal survey of every theater the triage table will list. **Cap regions:** at most **two** named regions unless you tie them in **one** mechanism sentence. Rule 1; phone-readable. **Material-first:** ledger before slogan.

#### Triage table

| Story cluster | Status (Q / Hypothesis / Supported) | What would verify or falsify | Cross-check bucket (none | Europe institutions | Russia-Ukraine | Middle East | Gulf energy | Iran lanes | Asia-Pacific) |
|---------------|--------------------------------------|--------------------------------|------------------------------------------------------------------------------------------------------------------|
| … | … | … | … |

#### Part B — Developments (5–10)
Each: **Label** → **What happened** → **Why it matters** → **Deeper significance** (parallel-not-fused) → **What to watch next** (testable). **What happened:** plain; **Deeper significance:** lead **incentives, costs, and constraints** before **narrative or legitimacy** framing when both apply; one tight **official story vs material constraint** line when useful. See rule **11** for **Readout A / Readout B** when institutions plainly conflict.

#### Chronicle vs noise
- **High-signal** (falsifiable; decisions or physical reality)
- **Noise** (deprioritize)

#### Commentator radar
Only if rule **8** applies; else omit. Prefer **substance over coverage**—fewer accounts with **URLs + analysis** beats thin one-liners on all handles.

#### Cross-domain synthesis
One section; label **mechanism vs analogy vs same-day juxtaposition**. If two **analyst- or commentary-style** takes **disagree** on the **same** cluster, add **one optional sentence** naming **convergence vs tension** (no new heading).

#### Early warnings
3–5 short, testable, **low/medium confidence** only.

#### Watchlist for tomorrow
6 bullets; **date** when possible.

#### Bottom line
4–6 sentences. **Material-first:** costs, what’s **unverified**, what **moves next**—reality, not press releases.

#### Closing angles (three bullets, ≤45 words each)
Three **separate** bullets—do **not** merge:
1. **Material and market reality:** constraints on governments and people (costs, logistics, sanctions, energy)—**material-first**, hardest edge.
2. **Legitimacy and narrative:** how states frame—institutions, symbols, continuity vs break, audience. Slightly more interpretive OK; stay **concrete** (who said what, to whom).
3. **Power and spillover:** alliances, balances, second-order—leverage and what could snap back; **material-first** compression.

### Prose voice — material-first (body unless overridden)

- **Part A is a laser, not a tour:** one bind, minimal regions—detail belongs in **Part B** and the triage rows.
- **Ledger before slogan:** money, sanctions, energy, shipping, time, legal exposure, logistics—then narrative.
- **Short; concrete.** Quote diplomatic fog only **as** a named line; say what it **costs**.
- **Gap:** **story** vs **physics/accounting** plainly (no sneer/cheerleading). **No false balance.**
- **Triage** telegraphic; prose **continuous**, not bullet salad. **Closing angle 2** is where **legitimacy/narrative** gets extra room; keep the rest **material-first**.
- **Parallels:** Prefer rule **13**—don’t let precedent **stand in** for dated receipts on today’s facts.

### Style (global)
Clear English. No undefined in-group jargon. No cheerleading for any capital. For contested facts, name **class of source** needed (e.g. named port authority readout)—never fake cites.

### Optional input (paste below)
Date, timezone, headlines, **@handles** (subset), **same-day excerpts**, and—for **deep Commentator radar**—**post URLs** (one per line is ideal) or pasted quote + approximate time.

**Default (fourteen — trim as needed):**  
`@barnes_law @ProfessorPape @DanielLDavis1 @DougAMacgregor @tparsi @s_m_marandi @RealScottRitter @MaxBlumenthal @WeTheBrandon @Peoples_Pundit @GeromanAT @mfa_russia @MFA_China @Pontifex`
```
