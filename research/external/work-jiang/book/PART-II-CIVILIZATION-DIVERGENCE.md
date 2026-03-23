# Part II — Divergence (Civilization)

**Predictive History, Volume II — Civilization**  
**As of:** 2026-03-23 (UTC)  
**Source registry:** [`divergence-tracking/registry/divergences.jsonl`](../divergence-tracking/registry/divergences.jsonl)  
**Lens doc:** [`divergence-tracking/README.md`](../divergence-tracking/README.md)

Volume II is **not** a forecast corpus. Its second movement is **historiography and divergence**: where Jiang’s classroom claims sit relative to **named** mainstream, contested, or specialist positions—without treating “consensus” as moral truth or “heterodoxy” as automatic virtue.

---

## 1. What Part II is (and is not)

| Part II is | Part II is not |
|------------|----------------|
| A **second pass** after Part I (lecture-faithful chapters) | A duplicate of Geo-Strategy **Part II — predictions** |
| **Comparative**: lecture claim ↔ field anchor ↔ evidence notes | A hit-rate scoreboard for ancient history |
| Explicit about **divergence_type** (empirical, interpretive, pedagogical_compression, normative) | Pretending every simplification is a “falsification” |
| **Tension-preserving** when schools disagree | Forcing one “winner” per topic |

**Orthogonal to** [`PART-II-GEO-STRATEGY.md`](PART-II-GEO-STRATEGY.md): predictions measure **forecast fit**; divergence measures **interpretive fit** with how disciplines usually frame the same material.

---

## 2. Method (how to read and write)

1. **Scope “mainstream”** — Always tag **whose** mainstream (field, period, institution). See the hard rule in [`divergence-tracking/README.md`](../divergence-tracking/README.md).
2. **Pull from the registry** — Prefer rows whose `lecture_ref` points at `lectures/civilization-*.md` (or add rows as the book is drafted). Use `divergence_id`, `jiang_claim`, `mainstream_summary`, `strength`, `divergence_type`.
3. **Primary and specialist sources** — For empirical rows (dates, archaeology, text criticism), cite **handbooks, museum timelines, standard editions**, or peer-reviewed work—not only encyclopedia summaries.
4. **Pedagogical compression** — When the lecture is **compressed for class**, label it `pedagogical_compression` in the registry; Part II explains the tradeoff, not a “gotcha.”
5. **Synthesis** — Close Part II with **cross-chapter themes** (e.g. myth vs. history, elite overproduction, Roman vs. Greek “soul”) and **where tensions persist** in the field as well as in the lecture arc.

---

## 3. Handoff from Part I

Each Part I chapter ends with a **Divergence (this lecture)** box (see [`CHAPTER-DIVERGENCE-BOX.md`](../CHAPTER-DIVERGENCE-BOX.md)): `divergence_id` + short paraphrase. That box is the **handoff list** into Part II’s deeper comparison—not the full analysis.

---

## 4. Master divergence pass (placeholder)

When the registry is populated for Civilization lectures, replace this section with a **table or per-lecture subsections** (like the Geo-Strategy scorecard, but **qualitative**): `divergence_id` | Lecture | Claim (short) | Type | Divergence (summary) | Notes.

Until then, **Part II is a procedure and a target**: add rows to `divergences.jsonl`, rebuild indexes if used, and extend this file as the **consolidated** divergence chapter for the volume.

---

## 5. Relation to other work-jiang tools

- **CIV-MEM** — Optional cross-tags for civilizational objects (institutions, seams). See [`CIV-MEM-LENS.md`](../CIV-MEM-LENS.md).
- **Influence tracking** — Measures **attention** (views/likes); divergence does **not** validate claims by popularity.
- **Prediction tracking** — Civilization lectures generally do **not** feed `predictions.jsonl`; do not merge the two registries.
