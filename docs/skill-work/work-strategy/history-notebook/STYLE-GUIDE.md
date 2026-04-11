# History Notebook — Style Guide

Chapter format and conventions for the History Notebook. This file is the reference for writing and reviewing chapters.

---

## Public / operator boundary

Chapter markdown files are **public-facing output**. They must never reference:
- CIV-MEM file names (`CIV-CORE-PERSIA`, `MEM-PERSIA-*`, etc.)
- Internal skill paths (`skills-portable/_drafts/...`)
- Doctrine IDs (`CIV-DOCTRINE-PERSIA`)
- Any operator infrastructure

Public-facing sources cite historical authors and works (Herodotus, Ferdowsi, Plutarch, etc.). Operator-facing metadata (CIV-MEM source_refs, linked_skills, PH source_ids) lives in `book-architecture.yaml` and `cross-book-map.yaml` only.

---

## Chapter format (6 sections)

Each chapter is ~500–1000 words. Sections appear in this order:

### 1. Sources

Public-facing historical source attribution.

> **Sources:** Herodotus, Xenophon's *Cyropaedia*, Plutarch, Ferdowsi's *Shahnameh* (c. 1010), the Cyrus Cylinder.

### 2. Axioms

Numbered list of core strategic patterns, tagged inline with `[pattern:X]`.

> 1. **Sovereignty as sacred** — Autonomy is absolute. Dependency equals suffocation. `[pattern:sovereignty]`
> 2. **Continuity through compression** — Persia does not recover from shocks; it densifies. `[pattern:compression]` `[pattern:endurance]`

### 3. Formation dimensions (Durant)

2–3 sentences each on the constitutive dimensions of this civilization in this era. Inspired by Durant's "synthetic history" — showing government, religion, education, and economics operating simultaneously.

Include only the dimensions that are load-bearing for this civilization-era; not all three are required.

- *Education / narrative* — how the civilization trains loyalty, self-understanding, and historical imagination
- *Religion / legitimacy* — sacred language, prophecy, or moral architecture as political resource
- *Economic structure* — material base, extraction model, or production logic that sustains the formation

Draft formation dimensions *before* the compressed narrative. The dimensions are the constitutive evidence; the narrative is the arc they produce.

### 4. Compressed narrative

Dense analytical prose (~400–600 words). When describing civilizational transformation, explicitly distinguish:

- **Proximate cause** — what triggered it
- **Structural cause** — what made it vulnerable

This is Thucydides' core analytical move: "Sparta attacked not because of Corcyra but because Athens' growing power made war inevitable." Apply to every major rupture or regime change.

The two-word labels can appear inline or as a brief parenthetical:

> Alexander's campaign exploited this — **proximate cause:** decapitation of Darius III at Gaugamela triggered elite defection. **Structural cause:** the Achaemenid integration model had no shock absorber — local elites retained loyalty to a person, not an institution.

### 5. Contradictions

Tensions the historical record names, at two levels:

**Conceptual tensions** — opposing forces within the civilization itself:

> **Sovereignty vs. coalition.** Absolute sovereignty conflicts with the need for allies in sustained confrontation.

**Source tensions** (Gibbon) — where the historical record disagrees with itself or where a pattern claimed by one source is contradicted by another. Show the seam between accounts; don't flatten it:

> *Source tension:* Herodotus portrays Cyrus as a liberator (Cylinder); Xenophon's *Cyropaedia* treats him as an ideal ruler whose empire depended on personal virtue. The tension: was Achaemenid tolerance a systemic feature or a personal one?

### 6. Strategy relevance

When and why this chapter's patterns apply to present-day analysis. Includes at least one **strategic case**: a named historical moment (2–3 sentences) where the civilization's formation logic is visible in a decision.

The case should be concrete enough that a strategist can reason by analogy:

> **Strategic case — Carrhae (53 BCE).** Crassus invaded Parthia with 40,000 heavy infantry. Surena refused engagement on Roman terms — horse archers at range, feigned retreats, supply denial. The case demonstrates parity-mode logic: when the weaker force controls terrain and tempo, the stronger force's advantages become liabilities.

No internal skill or doctrine file references. The analysis speaks for itself.

---

## Cross-volume bridges (style convention)

When a chapter continues a civilization from a prior volume:
- The **opening sentence** of the compressed narrative explicitly connects backward, with a parenthetical cross-reference to the prior chapter ID.

When a chapter sets up a future volume:
- The **closing sentence** of Strategy Relevance connects forward.

First chapters of an arc don't need backward references; last chapters don't need forward references.

---

## Conventions

- **Sub-groupings are provisional** — they adjust as chapters are written and the book's argument sharpens
- Civilizations reappear across volumes: each chapter covers **only its era**, not the full arc
- **YAML-first:** `book-architecture.yaml` is the SSOT. Update it when adding or completing a chapter
- **Stable IDs:** Every chapter has an `hn-{vol}-{slug}` ID used in YAML, cross-references, and prose citations
- Pattern tags (`[pattern:X]`) appear inline in chapters **and** in `book-architecture.yaml` `pattern_tags`
- Cross-references between volumes use chapter IDs (`hn-i-rome`) not file paths
- **PH wiring:** When writing a new chapter, update `cross-book-map.yaml` (sole SSOT for PH ↔ HN links)

---

## Design lineage

| Source | Structural gift | How it appears in HN |
|--------|----------------|---------------------|
| **Durant** | Synthetic history — all dimensions simultaneously | Formation dimensions section |
| **Churchill** | Dramatic selectivity, short chapters, authorial voice | Compressed format (~800 words), opinionated prose |
| **Gibbon** | Irony, footnote-as-argument, analytical transparency | Source tensions in Contradictions |
| **Herodotus** | Ethnographic *logoi*, ring composition, unresolved perspectives | Formation dimensions as constitution-before-narrative; ring-style cross-volume bridges |
| **Thucydides** | "Possession for all time," speeches as case studies, proximate/structural cause | Strategy relevance with strategic case vignette; cause distinction in narrative |
