# Analysis: Grace-Mar Self-Knowledge (IX-A)

**Purpose:** Analyze the **self-knowledge** dimension (IX-A) of the Grace-Mar Record — scope, sources, evidence linkage, and alignment with the companion-self model.

**Source:** `users/grace-mar/self.md` § IX-A. KNOWLEDGE.  
**Canonical definition:** Facts that entered awareness through observation (agents.md, ID-TAXONOMY, CONCEPTUAL-FRAMEWORK). Self-knowledge = self.md IX-A; standard label **self-knowledge**.

**Date:** 2026-02-26

---

## 1. Scope and Counts

| Metric | Value |
|--------|--------|
| **IX-A entries** | 36 (LEARN-0001 through LEARN-0036) |
| **Evidence-linked** | 36/36 (every entry has `evidence_id: ACT-XXXX`) |
| **Provenance** | Mix: `curated_by: user` (early); `provenance: human_approved` (from LEARN-0026 onward, plus some earlier) |
| **Date range** | 2026-02-19 to 2026-02-24 |

All entries conform to the protocol: facts only, traceable to an activity (ACT-*). No claim without evidence.

---

## 2. Topic Clusters

Self-knowledge in the Record clusters as follows:

| Cluster | LEARN IDs | Count | Representative topics |
|---------|-----------|--------|------------------------|
| **US history / presidents** | 0001, 0006, 0007, 0027 | 4 | George Washington, Lincoln (hat, 16th president, Emancipation), John Adams |
| **Space / solar system** | 0002, 0003, 0012, 0013–0023 | 13 | Jupiter Great Red Spot, Mars/Olympus Mons, no reptiles on Jupiter; Mercury–Pluto, Moon, Asteroid Belt (school workbook) |
| **Gemstones / minerals** | 0004, 0005, 0030 | 3 | Gemstones (shiny, rare); gemstones vs stones; diamond hardest |
| **Ballet / classical music** | 0008, 0009, 0026, 0035, 0036 | 5 | Nutcracker, Schubert D845, Swan Lake, Bach Goldberg Variations, Tchaikovsky Andante cantabile |
| **Books / media** | 0010, 0028, 0033 | 3 | The Wild Robot (Roz), Land Before Time 2 (Chomper), The Fox and the Hound (Tod, Copper) |
| **Biology / nature** | 0011, 0034 | 2 | Reptiles (scales, eggs, cold-blooded); extinct |
| **Culture / place** | 0024, 0029, 0031, 0032 | 4 | Egyptian pharaoh/King Tut; Tomb of Pakal (Palenque); Lunar New Year; Vietnamese food/pho |
| **Other** | 0025 | 1 | Black holes (gravity, light) |

**Observations:**
- **Space** dominates (13 entries), largely from one school workbook (ACT-0013) — one artifact, many facts; protocol allows multiple LEARN entries per ACT when distinct facts.
- **Presidents, ballet/music, and culture/place** show variety of sources: bot lookup, conversation, KBCP probes, companion report.
- **Reptiles** appear in both knowledge (LEARN-0011) and curiosity (IX-B); **gemstones** in knowledge and curiosity. No conflict — knowledge = “learned”; curiosity = “drawn to.” Same topic can sit in both dimensions.

---

## 3. Sources of Knowledge (Evidence Types)

| Source type | ACT range / examples | LEARN count | Notes |
|-------------|----------------------|-------------|--------|
| **Bot lookup** (user asked, system looked up, approved) | ACT-0001–0012 | 12 | First pipeline batches; user-initiated lookups |
| **School worksheet** | ACT-0013 (solar system), ACT-0014 (pharaoh), ACT-0037 (extinction) | 13 | LEARN-0013–0023 (one ACT), 0024, 0034 |
| **Bot conversation** (expressed/shared, no lookup) | ACT-0016, 0029–0031 | 4 | Black holes, Lunar New Year, pho, Fox and the Hound |
| **KBCP (Knowledge Boundary Calibration Probe)** | ACT-0022–0026 | 5 | Swan Lake, John Adams, Land Before Time 2, Tomb of Pakal, diamond |
| **Companion report** (“we listened”, “we did”) | ACT-0038, 0039 | 2 | Bach Goldberg, Tchaikovsky Andante cantabile |

Evidence linkage is consistent: every LEARN entry has exactly one `evidence_id` pointing to self-evidence.md § V. ACTIVITY LOG. Some ACTs support multiple LEARN entries (e.g. ACT-0013 → LEARN-0013 through LEARN-0023); that is by design (one artifact, many facts).

---

## 4. Schema and Provenance

- **Required fields per entry:** `id`, `date`, `topic`, `source`, `her_understanding`, `evidence_id`.
- **Optional:** `curated_by: user`, `provenance: human_approved`. Newer entries tend to include `provenance: human_approved` (File Update Protocol).
- **No scope/constraint** on any IX-A entry in the current set; optional per IDENTITY-FORK-PROTOCOL / KNOWLEDGE-BOUNDARY-FRAMEWORK when a belief has a boundary.

---

## 5. Downstream Consumption

| Consumer | How IX-A is used |
|----------|-------------------|
| **SYSTEM_PROMPT (bot/prompt.py)** | Section “YOUR KNOWLEDGE (from observations)” — compressed bullet list. Not a 1:1 dump of all 36 LEARN entries; summarized by topic (e.g. “George Washington as first president, John Adams as 2nd, Abraham Lincoln as 16th”). |
| **ANALYST_PROMPT** | Dedup list and “Known topics” plus “IX-A. Knowledge (post-seed)” bullets so analyst does not re-stage existing knowledge. |
| **PRP (export_prp.py)** | PRP embeds a compressed knowledge section; source is self.md (IX-A/B/C). |
| **scripts/metrics.py** | `RecordCompleteness.ix_a` = count of `id: LEARN-NNNN` in self.md (36). Reported in pipeline health. |

**Prompt sync:** The ANALYST “IX-A. Knowledge (post-seed)” block in prompt.py is a maintained summary. If new LEARN entries are merged into self.md but the prompt section is not updated, the Voice and analyst dedup can drift. Per File Update Protocol, prompt and SELF must be updated together on merge.

---

## 6. Alignment with Companion-Self and Protocol

| Criterion | Status |
|----------|--------|
| **Self-knowledge = IX-A** | ✅ ID-TAXONOMY and CONCEPTUAL-FRAMEWORK: self-knowledge is self.md IX-A. |
| **Evidence linkage** | ✅ Every LEARN entry has `evidence_id`. |
| **Knowledge boundary** | ✅ Only documented facts; no LLM leak. Sources are bot lookup, conversation, school, KBCP, companion report. |
| **Gated pipeline** | ✅ All entries merged after staging and approval (SESSION-LOG and SELF-ARCHIVE reflect this). |
| **Provenance** | ✅ `curated_by: user` or `provenance: human_approved` present. |

---

## 7. Summary

- **Grace-Mar self-knowledge (IX-A)** consists of **36 evidence-linked facts** (LEARN-0001–LEARN-0036) across space, US history, gemstones, ballet/music, books/media, biology, and culture/place.
- **Sources** are diverse: bot lookups, school worksheets, conversation, KBCP probes, and companion reports. Each entry traces to an ACT-* in EVIDENCE.
- **Protocol and companion-self alignment:** Evidence linkage, knowledge boundary, and gated merge are satisfied. Downstream (prompt, PRP, metrics) consume IX-A in compressed form; keeping prompt and SELF in sync on merge remains important.

---

*Analysis based on users/grace-mar/self.md § IX-A, self-evidence.md, bot/prompt.py, scripts/metrics.py, and agents.md / ID-TAXONOMY.*
