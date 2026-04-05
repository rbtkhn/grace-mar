# Classical Republican and English Constitutional Idiom in a Thirty-Two Unit Founding Corpus: A Dual-Method Report

**Working paper (internal research).** This text is operator-facing documentary analysis. It is **not** companion Record, Voice knowledge, or gated SELF content.  
**Version:** 2026-04-05 (rubric); lexical replication 2026-04-05 / 2026-04-06 (see §5.2).  
**Repository artifact:** `docs/skill-work/work-strategy/founding-influences-graeco-roman-vs-english.md`; lexical pipeline: `scripts/founding_lexical_compare.py`.

---

## Abstract

Scholarly accounts of the American founding often stress either British imperial–constitutional argument or neo-classical and Montesquieu-inflected “republican” design language. This report does not resolve that debate causally; it **operationalizes** it on a **fixed canon** of thirty-two primary units (imperial crisis through selected *Federalist* and Anti-Federalist essays) using two complementary methods: (1) a **frozen three-lens ordinal rubric** (0–10 classical-republic lean per unit), and (2) **preregistered lexical counts** of classical-republic proxy lemmas versus two distinct English legal proxies (imperial–constitutional/colonial–legal; rights/common-law/adjudication). Aggregate rubric means show a **low classical lean** in the pre-independence band (mean 3.64), a **high classical lean** in the *Federalist* sample (7.19), and an **intermediate** Anti-Federalist band (3.93). Lexical rates align directionally: crisis-era texts exhibit dense imperial–English lemma use; *Publius* exhibits high classical-proxy density and sparse imperial–English lemmas, while still registering substantial **second-list** English (law, constitution, court) density—so headline “GR versus English” contrasts **depend on which English list** is paired with the classical proxy. The report records edition families, limitations (host noise, short excerpts, list sensitivity), and **counter-archive** gaps (Loyalist, Indigenous, enslaved petitioners, etc.). A supplementary in-repository index probe found **no usable overlap** with founding-specific queries without re-indexing.

**Keywords:** American founding; civic humanism; Montesquieu; *Federalist*; Anti-Federalist; content analysis; lexicon; digital editions

---

## 1. Introduction

The question whether American revolutionary and constitutional discourse was “more Roman” or “more English” embeds a category error if posed as a forced choice. Historians have long described a **composite** idiom: Anglo-American opposition themes, common-law expectations, and imperial–parliamentary reference braided with classical exempla and Enlightenment political vocabulary (Bailyn; Wood; Pocock). Empirical traction nonetheless requires **bounded texts** and **explicit coding rules**.

This report examines **thirty-two** primary documents spanning roughly 1765–1788. It asks, at a **descriptive** level: (a) How does a transparent ordinal rubric distribute “classical-republic lean” across crisis texts, confederation and convention materials, *Publius*, and selected Anti-Federalists? (b) How do **token-level** counts of preregistered lemma families vary across the same units, and how stable are contrasts when a **second English proxy list** is substituted?

The analysis is **reproducible** where the pipeline is scripted; the rubric remains **interpretive** and would benefit from a second coder. No claim is made about the **causal weight** of Rome versus Westminster in actors’ minds, nor about representativeness beyond the chosen canon.

---

## 2. Historiography and expectations

**Bernard Bailyn** (*The Ideological Origins of the American Revolution*) emphasizes a **synthesized** Anglo-American opposition vocabulary in which classical and modern strands already intermingle. **Gordon S. Wood** (*The Creation of the American Republic*) tracks **republican** language in tension with **liberal** and **English legal** habits across Confederation and ratification. **J.G.A. Pocock** (*The Machiavellian Moment*) situates **civic humanist** concerns (virtue, corruption, temporal horizon) within an Atlantic pattern often **woven into** rather than replacing Whig argument.

**Working expectations** (checked against instruments in §5–6, not as statistical hypotheses):

1. Mass-legible **imperial-crisis** texts skew toward **English-leaning** rubric scores and high **imperial–constitutional/colonial** lemma rates.  
2. **Constitutional design** discourse—especially the sampled *Federalist* essays—scores **high** on classical-republic lean and on classical-proxy lemmas relative to the first English list.  
3. **Overlap / fusion** appears as **mid-range** scores on pamphlets and structural texts (Articles, mid-tier convention pieces).  
4. Lexical **English** measures should **shift** when grievance-adjacent imperial vocabulary is distinguished from **rights/court/constitution** vocabulary.

---

## 3. Corpus, editions, and canon stability

### 3.1 Edition families

Primary wording is drawn from a **single family** of digital hosts per genre:

| Use | Source |
|-----|--------|
| Papers, congressional materials, many state texts | Founders Online (National Archives), https://founders.archives.gov/ |
| Imperial crisis instruments, Articles, Northwest Ordinance (where hosted), many *Federalist* pages | Avalon Project, https://avalon.law.yale.edu/subject_menus/18th.asp |
| Numbered *Federalist* / Anti-Federalist parallels, convention excerpts | *Founders’ Constitution* (University of Chicago Press), https://press-pubs.uchicago.edu/founders/ |

Anti-Federalist attributions follow a **standard anthology** (e.g. Kenyon) where pseudonym-to-author notes are required; transcribed text follows Chicago / Founders Online ecosystems.

### 3.2 Canon

The **baseline** corpus comprises **thirty-two** units: eighteen instruments and speeches from imperial crisis through transmittal of the Constitution, nine *Federalist* numbers, and five Anti-Federalist essays (Brutus I–II, Federal Farmer I–II, Centinel I). A pass against an **in-repository civilization-memory index** (cluster and row-targeted queries) produced **no add/swap**: founding-specific recall in that index was **low**, and hits were **orthogonal** to the question under study. The **final canon** remained **identical** to the baseline. Index echoes, where they occur, reflect **internal library structure**, not historical salience in eighteenth-century Philadelphia.

---

## 4. Methodology

### 4.1 Phase A: Ordinal rubric (2026-04-05-v1)

For each primary unit and for each of **three lenses**, a **Greco-Roman / classical-republic lean** score was assigned on **0–10**:

| Score | Interpretation |
|------:|----------------|
| 0 | Predominantly English constitutional, common-law, Whig, or imperial–parliamentary idiom |
| 5 | Deliberately balanced or fused within the same passages |
| 10 | Predominantly classical republican, Montesquieu–Polybius chain, Roman institutional or exemplary language |

**Lenses**

| Lens | Coding focus |
|------|----------------|
| Rhetoric | Personae, exempla, virtue/corruption/faction diction vs. rights, petitions, king-in-parliament framing |
| Institutional | Senate, mixed government, separation vs. jury, precedent, charter machinery |
| Legal / constitutional machinery | Abstract republican theory vs. English-style rights lists, confederal legal practice |

**Excluded** from mandatory row coverage (noted narratively only): formal “education” scoring; **Gothic/Saxon liberty myth** as distinct from **Blackstone/Coke** common-law idiom (see §6.3).

The **row mean** is the arithmetic mean of the three lenses. Inter-coder reliability was **not** measured; ±1–2 points per cell is a plausible band. **Ordinal ordering** across bands is treated as more robust than absolute levels.

### 4.2 Phase B: Preregistered lexical counts

Phase B **complements** Phase A with **token-level** measures. It is **not** argument-structure parsing; it counts whole-token matches (regex `[a-z]{3,}` after HTML stripping) per 1,000 tokens.

**Lists** (disjoint sets; frozen in `scripts/founding_lexical_compare.py`):

- **GR_LEX** (n=39): classical-republic / design-discourse proxy (*republic*, *senate*, *faction*, *virtue*, *tyranny*, *legislature*, *democracy*, …).  
- **EN_LEX** (n=24): **British imperial–constitutional and colonial–legal** lemmas (*crown*, *king*, *parliament*, *colonies*, *taxation*, *charter*, *jury*, *petition*, *governor*, *subjects*, …)—**Westminster-and-empire institutional vocabulary**, not limited to the lemma *grievance*.  
- **EN2_LEX** (n=33): **rights / common-law / adjudication** lemmas (*law*, *liberty*, *rights*, *constitution*, *court*, *trial*, *habeas*, …).

**Metrics:** raw hits; **GR/1k**, **EN/1k**, **EN2/1k**; **GR/(GR+EN)** and **GR/(GR+EN2)** = share of hits from the classical list within the union of classical plus the relevant English list (document-level; bucket tables report **means of document-level shares**).

**Sources** per unit are enumerated in **`FOUNDING_CANON`** in the script (Avalon, National Archives constitution transcript, Chicago Founders’ Constitution, Wikisource, Project Gutenberg, constitution.org for Virginia Resolves). **Row 3** (*Letters from a Farmer*) aggregates **twelve** Wikisource letter URLs before tokenization. **Replication:** `python3 scripts/founding_lexical_compare.py` (optional `--json`).

---

## 5. Findings

### 5.1 Rubric: document-level scores and aggregates

**Table 1** reports the three-lens scores and row means for all thirty-two units.

**Table 1. Classical-republic lean (0–10) by lens and primary unit**

| # | Primary unit | Rhet | Inst | Legal | Avg |
|---|----------------|-----|-----|-------|-----|
| 1 | Virginia Resolves (1765) | 3 | 3 | 4 | 3.3 |
| 2 | Declaration of Rights and Grievances, Stamp Act Congress (1765) | 3 | 3 | 5 | 3.7 |
| 3 | *Letters from a Farmer in Pennsylvania* (1767–68) | 3 | 2 | 4 | 3.0 |
| 4 | Massachusetts Circular Letter (1768) | 2 | 2 | 3 | 2.3 |
| 5 | *Summary View of the Rights of British America* (1774) | 5 | 4 | 6 | 5.0 |
| 6 | First Continental Congress: Declaration and Resolves (1774) | 3 | 3 | 4 | 3.3 |
| 7 | Continental Association (1774) | 2 | 2 | 4 | 2.7 |
| 8 | Olive Branch Petition (1775) | 1 | 2 | 4 | 2.3 |
| 9 | Declaration of Causes and Necessity of Taking Up Arms (1775) | 4 | 4 | 5 | 4.3 |
| 10 | *Common Sense* (1776) | 6 | 5 | 5 | 5.3 |
| 11 | Declaration of Independence (1776) | 5 | 4 | 6 | 5.0 |
| 12 | Virginia Declaration of Rights (1776) | 4 | 3 | 3 | 3.3 |
| 13 | Articles of Confederation (1777 / 1781) | 5 | 6 | 5 | 5.3 |
| 14 | Northwest Ordinance (1787) | 4 | 4 | 6 | 4.7 |
| 15 | Virginia Plan (1787) | 7 | 8 | 6 | 7.0 |
| 16 | New Jersey Plan (1787) | 5 | 5 | 5 | 5.0 |
| 17 | Constitution of the United States (1787) | 6 | 7 | 6 | 6.3 |
| 18 | Washington, Letter of Transmittal (1787) | 4 | 4 | 5 | 4.3 |
| 19 | *The Federalist* No. 1 | 6 | 6 | 6 | 6.0 |
| 20 | *The Federalist* No. 10 | 7 | 8 | 7 | 7.3 |
| 21 | *The Federalist* No. 37 | 6 | 7 | 6 | 6.3 |
| 22 | *The Federalist* No. 39 | 7 | 7 | 7 | 7.0 |
| 23 | *The Federalist* No. 47 | 8 | 8 | 8 | 8.0 |
| 24 | *The Federalist* No. 48 | 8 | 8 | 7 | 7.7 |
| 25 | *The Federalist* No. 51 | 8 | 8 | 7 | 7.7 |
| 26 | *The Federalist* No. 63 | 7 | 9 | 6 | 7.3 |
| 27 | *The Federalist* No. 78 | 7 | 7 | 8 | 7.3 |
| 28 | Anti-Federalist “Brutus” I | 3 | 4 | 4 | 3.7 |
| 29 | Anti-Federalist “Brutus” II | 3 | 4 | 4 | 3.7 |
| 30 | Anti-Federalist “Federal Farmer” I | 4 | 5 | 4 | 4.3 |
| 31 | Anti-Federalist “Federal Farmer” II | 4 | 5 | 4 | 4.3 |
| 32 | Anti-Federalist “Centinel” I | 3 | 4 | 4 | 3.7 |

**Table 2. Mean rubric scores by corpus slice**

| Slice | Mean GR-lean (0–10) | Note |
|-------|---------------------|------|
| Rows 1–12 (imperial crisis → independence) | **3.64** | Complement ≈ 6.36 on 0–10 scale as crude “English-lean” proxy |
| Rows 1–18 (through transmittal) | **4.24** | Convention-era texts raise the mean |
| Rows 19–27 (*Federalist*) | **7.19** | Strong design- and theory-leaning classical idiom |
| Rows 28–32 (Anti-Federalist) | **3.93** | Closer to English-rights and consolidation anxieties on rubric |
| **All 32** | **5.02** | Near parity when *Federalist* cluster averages with crisis + opposition |

**Ordering robustness:** Crisis band < Anti-Federalist sample < *Federalist* sample on mean classical lean.

### 5.2 Lexical phase: rates by unit and bucket means

**Table 3** gives token counts and EN_LEX / GR rates per matrix row (replication date 2026-04-05 for transcribed numerics; bucket means aligned with script run 2026-04-06).

**Table 3. Lexical hits per unit (Phase B)**

| # | N tokens | GR | EN | GR/1k | EN/1k | GR/(GR+EN) |
|---|---------:|---:|---:|------:|------:|-----------:|
| 1 | 1074 | 8 | 63 | 7.45 | 58.66 | 0.113 |
| 2 | 575 | 4 | 44 | 6.96 | 76.52 | 0.083 |
| 3 | 26502 | 57 | 599 | 2.15 | 22.60 | 0.087 |
| 4 | 1005 | 9 | 36 | 8.96 | 35.82 | 0.200 |
| 5 | 5437 | 24 | 107 | 4.41 | 19.68 | 0.183 |
| 6 | 1449 | 12 | 56 | 8.28 | 38.65 | 0.176 |
| 7 | 1624 | 8 | 33 | 4.93 | 20.32 | 0.195 |
| 8 | 4675 | 18 | 83 | 3.85 | 17.75 | 0.178 |
| 9 | 2182 | 16 | 42 | 7.33 | 19.25 | 0.276 |
| 10 | 5444 | 1 | 8 | 0.18 | 1.47 | 0.111 |
| 11 | 1332 | 14 | 19 | 10.51 | 14.26 | 0.424 |
| 12 | 706 | 9 | 2 | 12.75 | 2.83 | 0.818 |
| 13 | 2759 | 18 | 14 | 6.52 | 5.07 | 0.562 |
| 14 | 2317 | 29 | 24 | 12.52 | 10.36 | 0.547 |
| 15 | 759 | 19 | 1 | 25.03 | 1.32 | 0.950 |
| 16 | 920 | 4 | 1 | 4.35 | 1.09 | 0.800 |
| 17 | 3975 | 49 | 10 | 12.33 | 2.52 | 0.831 |
| 18 | 456 | 2 | 0 | 4.39 | 0.00 | 1.000 |
| 19 | 1298 | 12 | 0 | 9.24 | 0.00 | 1.000 |
| 20 | 2396 | 58 | 1 | 24.21 | 0.42 | 0.983 |
| 21 | 2196 | 11 | 2 | 5.01 | 0.91 | 0.846 |
| 22 | 2024 | 51 | 5 | 25.20 | 2.47 | 0.911 |
| 23 | 2222 | 132 | 6 | 59.41 | 2.70 | 0.957 |
| 24 | 1522 | 60 | 1 | 39.42 | 0.66 | 0.984 |
| 25 | 1537 | 50 | 0 | 32.53 | 0.00 | 1.000 |
| 26 | 2411 | 51 | 2 | 21.15 | 0.83 | 0.962 |
| 27 | 2376 | 33 | 1 | 13.89 | 0.42 | 0.971 |
| 28 | 1496 | 19 | 12 | 12.70 | 8.02 | 0.613 |
| 29 | 2006 | 5 | 2 | 2.49 | 1.00 | 0.714 |
| 30 | 1703 | 11 | 1 | 6.46 | 0.59 | 0.917 |
| 31 | 219 | 3 | 2 | 13.70 | 9.13 | 0.600 |
| 32 | 625 | 7 | 2 | 11.20 | 3.20 | 0.778 |

**Table 4. Mean lexical rates by slice (including EN2); script replication 2026-04-06**

| Slice | n | Mean GR/1k | Mean EN/1k | Mean EN2/1k | Mean GR/(GR+EN) | Mean GR/(GR+EN2) |
|-------|---|------------|------------|-------------|-----------------|------------------|
| Rows 1–12 | 12 | **6.48** | **27.32** | **20.71** | **0.237** | **0.232** |
| Rows 13–18 | 6 | **10.86** | **3.39** | **18.65** | **0.782** | **0.348** |
| Rows 19–27 | 9 | **25.56** | **0.93** | **18.94** | **0.957** | **0.547** |
| Rows 28–32 | 5 | **9.31** | **4.39** | **22.69** | **0.724** | **0.361** |
| All 32 | 32 | **13.11** | **11.83** | **20.14** | **0.618** | **0.363** |

**Pooled interpretation (all thirty-two units):** among tokens matching **GR_LEX ∪ EN_LEX**, the **mean document-level** classical share **GR/(GR+EN)** is **0.618** (~**62%** classical-proxy hits vs ~**38%** imperial–constitutional/colonial-proxy hits **within that hit set**—not as a fraction of all tokens).

**Ad hoc bipartition (rows 1–18 + 28–32 vs 19–27):** mean GR/1k **8.24** vs **25.56**; mean EN/1k **16.09** vs **0.93**; mean EN2/1k **20.60** vs **18.94**; mean GR/(GR+EN) **0.485** vs **0.957**; mean GR/(GR+EN2) **0.290** vs **0.547**.

### 5.3 Sensitivity: EN_LEX versus EN2_LEX (constant GR_LEX)

**Table 5.** Δ share = mean GR/(GR+EN2) − mean GR/(GR+EN) over units in the slice.

| Slice | Mean EN/1k | Mean EN2/1k | Mean GR/(GR+EN) | Mean GR/(GR+EN2) | Δ share |
|-------|------------|-------------|-----------------|------------------|--------:|
| Rows 1–12 | 27.32 | 20.71 | 0.237 | 0.232 | −0.005 |
| Rows 13–18 | 3.39 | 18.65 | 0.782 | 0.348 | −0.434 |
| Rows 19–27 | 0.93 | 18.94 | 0.957 | 0.547 | −0.410 |
| Rows 28–32 | 4.39 | 22.69 | 0.724 | 0.361 | −0.363 |
| All 32 | 11.83 | 20.14 | 0.618 | 0.363 | −0.255 |

The **crisis band** is **stable** across English lists on classical **share** (Δ ≈ 0). **Design and ratification** discourse scores **high EN2/1k** even when **EN/1k** is low for *Publius*; **GR/(GR+EN2)** therefore **falls sharply** relative to **GR/(GR+EN)**. *Federalist* No. **78** drives part of the EN2 signal (judicial vocabulary). The contrast confirms **list dependence**: “English” is not a single lexical column.

**Concordance with Phase A:** High **EN_LEX** density and low **GR/(GR+EN)** in rows 1–12 align with rubric mean **3.64**. High **GR/1k** and low **EN_LEX** in *Federalist* rows align with rubric **7.19**. Anti-Federalist rows sit **between** on both instruments (**3.93**; intermediate EN_LEX and GR shares).

---

## 6. Discussion

### 6.1 Composite inheritance

Elite revolutionary argument rarely staged a clean **Rome against Westminster**. The materials support a **Whig-republican composite**: imperial–parliamentary and colonial-legal language for **legitimacy within empire** and for **rights claims against metropolitan policy**; classical and especially **Montesquieu-inflected** language for **republican legitimacy** and **institutional design** after the break.

### 6.2 Period and genre variation

**Imperial crisis through independence (rows 1–12):** Rubric means skew **English-leaning**; charter, association, petition, and reconciliation genres carry **parliamentary and common-law** expectations, alongside **tyranny** and natural-law tropes that can be mediated through early modern rather than narrowly “Roman” channels.

**Design and ratification (rows 15–27 on rubric; *Federalist* cluster lexical):** *Publius* scores **high** on classical lean and on **GR/1k**; the **Constitution** text mixes **Latin institutional labels** with **English-derivative** criminal-procedure guarantees.

**Anti-Federalists (rows 28–32):** On the rubric they appear **more “English”** than *Publius* in the sense of **rights**, **judiciary**, and **consolidation** anxieties framed in familiar **liberty-and-law** idioms rather than the “extended republic” synthesis.

### 6.3 Anglo-Saxon myth versus common-law practice

**Gothic or “Saxon” freeholder myth** (antiquarian, often rhetorically thin) should not be **collapsed** with **Blackstone, Coke, and common-law practice**, which carried **institutional** force. Rubric “English-lean” scores track **petition, rights, jury, parliamentary** frames **without** assuming speakers believed a literal **Saxon forest** utopia. Where this report refers broadly to **English** influence, it means the **Whig–legal complex**, with Saxon myth as at most one **optional** ingredient.

### 6.4 Hypothesis checklist (ordinal)

| Expectation | Assessment |
|-------------|------------|
| Revolutionary mass-legible case more English-leaning | **Supported** (mean **3.64**, rows 1–12) |
| Design discourse stronger classical / Montesquieu presence | **Supported** (*Federalist* mean **7.19**) |
| ~55–70% “English complement” on crude linear scale for revolutionary band | **In band** (~64% complement); interpret as ordinal sketch |
| Fusion / overlap | **Supported** (mid scores on pamphlets, Articles, etc.) |

---

## 7. Limitations and future research

**Rubric:** Single coder; no κ; relative **order** preferred over point estimates.

**Lexicon:** Frozen lists miss inflections and semantics; **frequency ≠ salience**. **Host boilerplate** differs across Avalon, Wikisource, Gutenberg, Chicago, Archives. ***Common Sense* (row 10)** under-maps GR/EN on these lists (edition + vocabulary mismatch); the rubric still rates it mid-high classical lean—treated as **instrument gap**, not absence of idiom. **Federal Farmer II** is a **short** Chicago excerpt (**~219** tokens)—unstable rates. Many *Federalist* essays have **zero EN_LEX** hits, inflating **GR/(GR+EN)**; **EN2** must be read alongside **GR/1k**.

**Corpus:** The thirty-two units **center Patriot continental and federal print**. They **omit** or underrepresent Loyalist, Indigenous diplomatic, enslaved petitioners’ legal voice, women’s political petitions, non-elite formats, 1789 Bill of Rights legislative history, and full state ratifying debates unless the canon is extended.

**Future work:** Second rater; expand **FOUNDING_CANON**; strip main-content HTML per host; offline **pytest** on `analyze()`; optional re-index of project notes for CIV-MEM-style probes after **founding-oriented** ingest.

---

## 8. Conclusion

On a **transparent thirty-two-unit canon** and **two frozen instruments**—ordinal rubric plus preregistered lexicons—the American founding texts examined here **vary systematically by period and genre**: **imperial-crisis** discourse scores **English-leaning** on the rubric and loads **imperial–constitutional/colonial** lemmas; ***Federalist*** selections score **high** classical lean and **high classical-proxy density**, while still registering substantial **rights/court/constitution** English under **EN2_LEX**. **Anti-Federalist** samples occupy an **intermediate** position on both measures. The pattern supports **historiographical fusion** theses more than a **binary** “classical *or* English” replacement narrative, provided **“English”** is **disaggregated** lexically. All proportions are **canon- and instrument-bound**; they describe **this text set**, not “America” as a whole.

---

## References

Bailyn, Bernard. *The Ideological Origins of the American Revolution.* Cambridge, MA: Belknap Press of Harvard University Press.

Kenyon, Cecilia M., ed. *The Antifederalists.* Indianapolis: Bobbs-Merrill, 1966. (Anthology reference for Anti-Federalist attribution practice.)

Pocock, J.G.A. *The Machiavellian Moment: Florentine Political Thought and the Atlantic Republican Tradition.* Princeton: Princeton University Press.

Wood, Gordon S. *The Creation of the American Republic, 1776–1787.* Chapel Hill: University of North Carolina Press.

*The Founders’ Constitution.* Ed. Philip B. Kurland and Ralph Lerner. Chicago: University of Chicago Press. Online: https://press-pubs.uchicago.edu/founders/.

National Archives. Founders Online. https://founders.archives.gov/.

Yale Law School. *The Avalon Project: Eighteenth Century Documents.* https://avalon.law.yale.edu/subject_menus/18th.asp.

---

## Appendix A. Supplementary index probe (in-repository)

**Index:** `docs/civilization-memory/.cache/inrepo_index.json`  
**Tooling:** `scripts/build_civmem_inrepo_index.py`; `query_inrepo_civmem()`.

| Query id | Query (abbrev.) | Top hit(s) | Overlap | Assessment |
|----------|-----------------|------------|---------|------------|
| cluster_classical | mixed government senate virtue … montesquieu faction | Unrelated lens document | 1 | Orthogonal |
| cluster_english | common law magna carta whig … 1689 | Manuscript / mind profile | 1 | Orthogonal |
| row_stamp_act | Stamp Act Congress … 1765 | Unrelated briefs | 1 | Orthogonal |
| row_association | Continental Association … 1774 | — | 0 | No hit |
| row_olive | Olive Branch … 1775 | — | 0 | No hit |
| row_fed10 | Federalist faction extended republic madison | Unrelated insights doc | 1 | Orthogonal |
| row_brutus | Brutus anti-federalist judiciary | — | 0 | No hit |

**Conclusion:** No meaningful founding-specific proportion can be read from this index **without** ingesting founding-oriented notes and rebuilding the index.

---

## Document history

| Element | Version / date |
|---------|----------------|
| Rubric | 2026-04-05-v1 |
| Lexical numerics (Tables 3–5) | Aligned with `founding_lexical_compare.py` runs 2026-04-05 / 2026-04-06 |
| Report structure | Academic reformulation (same substantive content), 2026-04-06 |
| Location | Moved from `docs/skill-work/work-cadence/` to **`docs/skill-work/work-strategy/`**, 2026-04-06 |
