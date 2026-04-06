# Lecture forward chain — Volume IV (Game Theory)

**Operator lane — not Record.** Blind backtest: predict **gt-(k+1)** from **gt-01 … gt-k** only (`lectures/game-theory-NN-*.md`), then score after opening the next file.

**Log started:** 2026-04-07  
**Mode:** `lectures-only`  
**Read depth note:** Rounds use full curated lecture files per [skill-jiang](../../../../.cursor/skills/skill-jiang/SKILL.md) (four levels up to repo root); this log was authored in one implementation pass with strict per-round prefix simulation.

## Scoring rubric (inline)

| Label | Meaning |
|-------|---------|
| **hit** | Top hypothesis matches dominant topic + mechanism. |
| **partial** | Right arc, wrong case/emphasis; or #2 was closer. |
| **miss** | Wrong frame or unpredicted pivot. |

---

## Round 1 → predict gt-02

**Prefix:** gt-01 only | **read_depth:** full (curated lecture)

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **School / education institutions** as next “life example” | Lecture #1 ends survey of drivers of behavior; #2 opening in transcript pattern (not read) implied “examples from your life”—school is the obvious parallel to dating for high-school audience | med | Next episode is workplace, family economics, or stays on gender/marriage only |
| H2 | **Family / household resource game** | Dating + fertility + superstructure naturally extends to intra-household allocation | low | No: pivots to abstract macro first |
| H3 | **Media / attention economy** | Liberalism + incentive stories could extend to screens and cognition | low | No: stays institutional |

### Resolution (gt-02 opened)

- **Actual:** **Why Schools Suck** — stakeholder analysis of schools; literacy vs incentives; superstructure link.
- **Scores:** H1 **hit**; H2 miss; H3 miss.
- **miss_taxonomy:** —
- **Adjustment:** Track explicit **pedagogical promise** (“first few classes = life examples”); overweight that cue vs abstract macro jumps until the series breaks the pattern.

---

## Round 2 → predict gt-03

**Prefix:** gt-01 … gt-02

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **University / admissions tournament** | Still “life you know”; natural sequel to high school | med | Episode jumps to national politics |
| H2 | **Success, class, parenting (“who wins life”)** | Schools lecture already names literacy + lifelong learning; next step may be **outcomes** and **mobility** games | med | Episode is immigration or macro-only |
| H3 | **Peer culture / social media game** | Attention + status adjacent to school failure mode | low | No social layer |

### Resolution (gt-03 opened)

- **Actual:** **Rich Dad, Poor Dad** — success theories vs structural constraints; parenting; elite overproduction.
- **Scores:** H1 miss; H2 **hit**; H3 miss.
- **Adjustment:** After **institution** lecture, Jiang often moves to **individual success/mobility** frame before scaling to society-wide conflict.

---

## Round 3 → predict gt-04

**Prefix:** gt-01 … gt-03

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Labor market / gig economy / workplace** | Life-course arc: dating → school → success → **work** | med | Skips to geopolitics |
| H2 | **Immigration or migration game** | Success + class + mobility + demographic undertones in #1–#3 set up **who crosses borders and why** | med | Stays US domestic abstraction only |
| H3 | **Housing / urbanization trap** | Elite overproduction + mobility → cities and rent | low | No built environment |

### Resolution (gt-04 opened)

- **Actual:** **The Immigration Trap** — group outcomes, status vs test scores, long-cycle demographic game.
- **Scores:** H1 miss; H2 **hit**; H3 miss.
- **miss_taxonomy:** arc_correct_case_wrong (workplace was plausible but migration won).

### skill_merge_id: **M3**

- Promote: **Life-example triad** then **boundary / group competition** (school → success → cross-border/status).

---

## Round 4 → predict gt-05

**Prefix:** gt-01 … gt-04

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Race / identity politics as explicit game** | Immigration lecture centers group competition; may zoom to **domestic** coalition games | med | Avoids identity frame |
| H2 | **Civilizational / “who replaces whom” cycle** | Immigration + elite/mobility themes invite **historical cycle** narrative | med | Single-country case study only |
| H3 | **Welfare state / citizenship rules** | Legal/status layer adjacent to immigration | low | No institutions focus |

### Resolution (gt-05 opened)

- **Actual:** **The World Game** — civilizational cycle; marginal cohesive groups vs wealthy cores; historical cases.
- **Scores:** H1 miss; H2 **hit**; H3 miss.

---

## Round 5 → predict gt-06

**Prefix:** gt-01 … gt-05

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Colonialism / empire case study** | World game → concrete **imperial** mechanics | med | Jumps to modern finance without empire label |
| H2 | **Trade war / sanctions game** | Cycles + cores/peripheries → **economic weapons** | low | No contemporary trade |
| H3 | **Money, dollar, Bretton Woods** | Scaling from civilizational winners to **currency rules** | med | Stays pre-modern only |

### Resolution (gt-06 opened)

- **Actual:** **The World’s Bank** — financial/legal institutions post-empire; offshore, schooling, capital protection.
- **Scores:** H1 partial; H2 miss; H3 **hit**.

---

## Round 6 → predict gt-07

**Prefix:** gt-01 … gt-06

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **China as challenger game** | Finance + institutions + civilizational cycle → **peer competitor** | med | Focus remains Anglosphere only |
| H2 | **America as hegemonic player** | Institutions lecture often pivots to **who runs the table** (U.S. constitutional/dollar story) | med | Episode is EU or UN-only |
| H3 | **Tech platforms as new banks** | “Inherited rules” could modernize to platforms | low | Traditional IR only |

### Resolution (gt-07 opened)

- **Actual:** **America’s Game** — British roots, U.S. scaling, constitution, Bretton Woods / dollar.
- **Scores:** H1 miss; H2 **hit**; H3 miss.

### skill_merge_id: **M6**

- Promote: After **institutional finance**, expect **hegemon-specific** “who designed the rules” episode (U.S. chapter).

---

## Round 7 → predict gt-08

**Prefix:** gt-01 … gt-07

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Soviet collapse / Russia game** | America’s game → **ideological rival** as mirror | med | Skips ideology |
| H2 | **Communism / left tradition as strategic system** | Dollar order vs alternative **coalition** grammar | med | Cold War as hot war only |
| H3 | **Middle East oil game** | Hegemony + finance → **Gulf** | low | Not region yet |

### Resolution (gt-08 opened)

- **Actual:** **Communist Specter** — capitalism/communism as interacting systems; Europe/Russia/China.
- **Scores:** H1 partial; H2 **hit**; H3 miss.

---

## Round 8 → predict gt-09

**Prefix:** gt-01 … gt-08

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **China–Taiwan or South China Sea** | Ideology + hegemony → **Indo-Pacific** flashpoint | med | Other region |
| H2 | **Ukraine / NATO–Russia** | Communist specter + Europe path | med | Different theater |
| H3 | **US–Iran / Gulf escalation** | Energy + empire + ideology can converge on **Gulf** | med | No Mideast |

### Resolution (gt-09 opened)

- **Actual:** **The US–Iran War** — live conflict framing; Hormuz; asymmetric escalation.
- **Scores:** H1 miss; H2 miss; H3 **hit**.

---

## Round 9 → predict gt-10

**Prefix:** gt-01 … gt-09

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **“Law of …” formalization** (first named law) | Hot war lecture sets up **pattern extraction** | med | Stays episodic news |
| H2 | **Israel / Palestine game** | Gulf + religious undertones elsewhere in series | low | Deferred |
| H3 | **Sanctions and resilience game** | Economic war follow-through | med | Pure military only |

### Resolution (gt-10 opened)

- **Actual:** **The Law of Asymmetry** — strengths invert to weaknesses; US vs Iran payoffs; consciousness framing.
- **Scores:** H1 **hit**; H2 miss; H3 partial.

### skill_merge_id: **M9**

- Promote: After **first dedicated hot-war** episode, expect **named “Law of …”** abstraction next.

---

## Round 10 → predict gt-11

**Prefix:** gt-01 … gt-10

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Law of escalation / ladder** | Asymmetry → **dynamic** escalation path | med | New unrelated law |
| H2 | **Law of deception / signaling** | Asymmetric info natural next | low | Not information theory |
| H3 | **Domestic US cleavage game** | War stress → **home front** | med | Stays foreign only |

### Resolution (gt-11 opened)

- **Actual:** **The Law of Escalation** — invasion, nuclear, Al-Aqsa pathway; calibration of escalation.
- **Scores:** H1 **hit**; H2 miss; H3 miss.

---

## Round 11 → predict gt-12

**Prefix:** gt-01 … gt-11

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Religious / eschatological convergence** | Escalation lecture + Al-Aqsa cue → **theology as strategy** | med | Secular IR only |
| H2 | **Law of alliance / bandwagoning** | Coalition game | low | No alliances frame |
| H3 | **Cyber / space escalation** | Tech asymmetry extension | low | Not tech |

### Resolution (gt-12 opened)

- **Actual:** **The Law of Eschatological Convergence** — three predictions arc; traditions map to geopolitics.
- **Scores:** H1 **hit**; H2 miss; H3 miss.

---

## Round 12 → predict gt-13

**Prefix:** gt-01 … gt-12

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Deep state / intelligence game** | Eschatology + empire → **maintenance of order** networks | med | Stays doctrinal only |
| H2 | **Elite corruption / Epstein-class scandal as case** | Narrative control lecture could **name** a glue event | low | Stays abstract |
| H3 | **Law of proximity (domestic)** | Pivot from cosmic to **nearest-player** drivers | med | Another global law |

### Resolution (gt-13 opened)

- **Actual:** **Epstein’s World** — narrative, dollar hierarchy, transnational elite maintenance.
- **Scores:** H1 partial; H2 **hit**; H3 miss.

### skill_merge_id: **M12**

- Promote: After **eschatological convergence**, expect **“who narrates reality” / deep-network** episode.

---

## Round 13 → predict gt-14

**Prefix:** gt-01 … gt-13

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Law of proximity** (domestic/near game) | Epistemic layer → **who actually decides when bombs fall** | med | Stays transnational only |
| H2 | **Media platform censorship game** | Narrative control → **distribution** | low | Not platforms |
| H3 | **Energy markets under war stress** | Iran arc continuation | med | Non-energy |

### Resolution (gt-14 opened)

- **Actual:** **The Law of Proximity** — overnight escalation news; domestic vs Tel Aviv vs Tehran internal games.
- **Scores:** H1 **hit**; H2 miss; H3 partial.

---

## Round 14 → predict gt-15

**Prefix:** gt-01 … gt-14

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Order vs multipolarity / “post-American”** | Proximity + war → **systemic transition** thesis | med | Single-battle focus |
| H2 | **China’s position in the war** | Asian energy exposure | low | Not China-centric |
| H3 | **Humanitarian / law-of-war frame** | Civilian costs emphasis | low | Not IHL lecture |

### Resolution (gt-15 opened)

- **Actual:** **The Return of History** — unipolar exhaustion; resilience; scenarios for decades.
- **Scores:** H1 **hit**; H2 miss; H3 miss.

---

## Round 15 → predict gt-16

**Prefix:** gt-01 … gt-15

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Israeli grand strategy / regional primacy** | Return of history + war arc → **who benefits structurally** | med | US-only closure |
| H2 | **Gulf monarchies game** | Energy + proximity | low | Not GCC |
| H3 | **Nuclear breakout game** | Escalation arc payoff | low | Deferred again |

### Resolution (gt-16 opened)

- **Actual:** **Pax Judaica Rising** — imperial replacement, US constraints, Israeli opening.
- **Scores:** H1 **hit**; H2 miss; H3 miss.

### skill_merge_id: **M15**

- Promote: After **macro transition** lecture, expect **regional hegemon thesis** tied to active war.

---

## Round 16 → predict gt-17

**Prefix:** gt-01 … gt-16

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Trump / US election–war nexus** | Pax + US constraints → **leadership-specific** world order | med | Stays institutional anonymous |
| H2 | **Great-power negotiation game** | Ceasefire / diplomacy | med | No leaders |
| H3 | **Economic reset / Bretton Woods II** | Structural money chapter | low | Not macro money |

### Resolution (gt-17 opened)

- **Actual:** **The Great Reset** — curated file lists **TBD after listen** in At a glance; title suggests reset/global order frame.
- **Scores:** H1 partial; H2 miss; H3 partial (title ambiguous vs hypothesis).
- **Adjustment:** When **At a glance** is TBD, down-rank confidence; use **title + series position** only.

---

## Round 17 → predict gt-18

**Prefix:** gt-01 … gt-17

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Trump doctrine / US world order** | Great Reset + Pax + active war → **named US leadership frame** | med | Returns to abstract law |
| H2 | **Energy / commodity realignment** | War + reset → **markets** | med | Pure politics |
| H3 | **Q&A synthesis / student questions** | End-of-unit recap | low | Full new thesis |

### Resolution (gt-18 opened)

- **Actual:** **Trump World Order** — war framing, Hormuz, resource realignment, Bush 1991 contrast.
- **Scores:** H1 **hit**; H2 **hit**; H3 miss.

### skill_merge_id: **M18** (final backtest merge)

- Promote: **Late-series** compresses **leadership + commodity + order** into one capstone after **reset**-language title.

---

## Live — predict gt-19 (prefix gt-01 … gt-18)

**Run date:** 2026-04-07 | **Resolved:** pending publication

### Prediction packet

| Rank | Hypothesis | Mechanism | Confidence | Falsifier |
|------|------------|-----------|------------|-----------|
| H1 | **Next “Law of …” or Part-II style method episode** | Series may resume **pattern** after capstone | low | New arc entirely |
| H2 | **War outcome / theater update** (Iran, Gulf, Israel) | #17–#18 are war-heavy; **events** may force continuation | med | Deliberate pivot away from Mideast |
| H3 | **Domestic US / election–institution game** | Trump frame → **constitutional or civil conflict** extension | med | Foreign-only |
| H4 | **New book/volume bridge** (announcement or meta) | End of run sometimes **meta** | low | Substantive topic only |

### Resolution

- **Actual:** _(Fill when Game Theory #19 is published: title + one-line thesis.)_
- **Scores:** _(pending)_
- **Adjustment:** _(pending)_

---

## Merge log (skill appendix)

| Merge | Rounds absorbed | Notes |
|-------|-----------------|-------|
| M3 | 1–3 | Life examples → boundary/migration |
| M6 | 4–6 | Finance institutions → U.S. hegemon “rules” episode |
| M9 | 7–9 | Ideology + hot war → named laws |
| M12 | 10–12 | Escalation → eschatology → epistemic/deep layer |
| M15 | 13–15 | Proximity → macro return → regional primacy thesis |
| M18 | 16–17 + capstone | Leadership + reset + commodity/order synthesis |
