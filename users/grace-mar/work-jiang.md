# work-jiang — grace-mar

Operator project — **Jiang** (separate from SKILLS). See [skill-think](skill-think.md), [skill-write](skill-write.md), [work-alpha-school](work-alpha-school.md).

## Purpose

**Deliver a book and/or website** under the multivolume title **Predictive History** (one volume per lecture series) that articulates and analyzes **Jiang’s unique philosophy** — clear enough for readers to understand the system, and analytic enough to show how claims connect and where they meet the world. Current repo tranche: **Volume 1 — Geo-Strategy**.

**Canonical library index:** The book is catalogued in [self-library](self-library.md) as **LIB-0149** (SELF-LIBRARY is reference-facing; the working manuscript and research corpus stay under `research/external/work-jiang/` until material is merged through the gate).

**Method (operator work, not Voice knowledge until merged through the gate):**

1. **Lecture transcripts** — primary text: systematic capture and close reading of his talks (e.g. channel pulls under `research/external/youtube-channels/predictive-history/`), tagged and excerpted for themes, definitions, and internal consistency.
2. **[CIV-MEM](../../docs/skill-work/work-civ-mem/README.md)** — civilizational / strategic / governance vocabulary and frames from the civilization_memory stewardship lane: use as an **analytic lattice** (conditions, seams, multi-perspective structure) to organize and stress-test philosophical claims without collapsing them into politics alone.
3. **Current-events scans** — periodic passes (news, briefs, operator skills such as pulse/search workflows) to **ground** the philosophy: where the abstract system meets concrete episodes, and what would need to be said in a given moment.

Nothing in this file is Record truth for the Voice until merged through the gated pipeline. Human-gated.

**Membrane (normative):** [research/external/work-jiang/README.md § Boundaries](../../research/external/work-jiang/README.md#boundaries-membrane) — research corpus vs Record, candidates vs quotes, validators as gate.

---

## Context objectives

- Maintain a **canonical transcript set** and a working **outline / thesis map** for the book or site.
- Run **civ-mem-informed analysis** on clusters of transcript material (themes, tensions, dependencies).
- Run **current-events tie-ins** as optional chapters or “applications” sections — never shipped without explicit approval.
- Separate **exposition** (what Jiang’s philosophy holds) from **analysis** (how it compares, where it strains, what it predicts).

---

## WORK Container

<!-- WORK-JIANG-CONTAINER-START -->
```yaml
status: OUTLINE_ACTIVE
edge: "Philosophy book + site; transcript-driven; civ-mem lattice; current-events grounding"
gaps: []
notes: "See research/external/work-jiang/STATUS.md and BOOK-ARCHITECTURE.md for live production state. Geo-Strategy series resumed 2026-03-23; geo-13+ pending ingest."
```
<!-- WORK-JIANG-CONTAINER-END -->

---

## WORK GOALS

Objectives for this lane. Gated; evidence-linked when captured.

```yaml
work_goals:
  near_term: []
  horizon:
    - "Published book and/or website articulating Jiang's philosophy with transcript-backed analysis"
  source: null
```

---

## LIFE MISSION REF

Life mission lives in SELF (identity, values). WORK goals may align when this lane touches the companion.

```yaml
life_mission_ref: "self.md § VI VALUES (life_mission)"
```

---

## Operator schedule (Jiang lane)

- **Lecture series order (Predictive History / book work):** (1) **Geo-Strategy** — curated in `research/external/work-jiang/lectures/` (`geo-strategy-*.md`). (2) **Civilization** — second series; **transcript intake in progress** — add curated files as `civilization-*.md`, register `civ-*` sources in `metadata/sources.yaml`, same pipeline as Geo-Strategy ([WORKFLOW-transcripts.md](../../research/external/work-jiang/WORKFLOW-transcripts.md) § Multi-series; channel pulls under `research/external/youtube-channels/predictive-history/`).

---

## RESEARCH / ARTIFACTS

Repo-local material (operator research; not Voice knowledge until merged):

- [work-jiang (research)](../../research/external/work-jiang/README.md) — curated lecture notes + transcripts
  - [Transcript intake & analysis workflow](../../research/external/work-jiang/WORKFLOW-transcripts.md) — acquire, normalize, structured extraction, CIV-MEM passes, memo template
  - [Influence tracking](../../research/external/work-jiang/influence-tracking/README.md) — longitudinal views/likes/comment counts via `scripts/snapshot_youtube_video_metrics.py` + optional monthly notes
  - [Prediction tracking](../../research/external/work-jiang/prediction-tracking/README.md) — forecast-like claims in `registry/predictions.jsonl`; resolve vs dated evidence (orthogonal to “influence”)
  - [Divergence tracking](../../research/external/work-jiang/divergence-tracking/README.md) — where claims differ from **named** mainstream/consensus views; `registry/divergences.jsonl`
  - Examples: [Geo-Strategy #1 — Iran strategy matrix (2024-04-24)](../../research/external/work-jiang/lectures/geo-strategy-01-iran-strategy-matrix-2024-04-24.md); [#2 — Christian Zionism & Middle East](../../research/external/work-jiang/lectures/geo-strategy-02-christian-zionism-middle-east-conflict.md); [#3 — Empire & financialization](../../research/external/work-jiang/lectures/geo-strategy-03-how-empire-is-destroying-america.md); [#4 — Saudi Arabia vs Iran](../../research/external/work-jiang/lectures/geo-strategy-04-saudi-arabia-trump-card-against-iran.md); [#5 — Trump 2024 / Haley VP hypothesis](../../research/external/work-jiang/lectures/geo-strategy-05-why-trump-will-win-nikki-haley-vp.md); [#6 — Imperial hubris & shock-and-awe](../../research/external/work-jiang/lectures/geo-strategy-06-americas-imperial-hubris.md); [#7 — Raisi helicopter / IRGC scenario](../../research/external/work-jiang/lectures/geo-strategy-07-who-killed-iranian-president-ebrahim-raisi.md); [#8 — Iran trap / invasion scenario](../../research/external/work-jiang/lectures/geo-strategy-08-the-iran-trap.md); [#9 — Putin / putinism & consumerism thesis](../../research/external/work-jiang/lectures/geo-strategy-09-putins-war-for-the-soul-of-russia.md); [#10 — Putin strategic imagination / Stalin game-theory](../../research/external/work-jiang/lectures/geo-strategy-10-putins-strategic-imagination.md); [#11 — Second American Civil War thesis](../../research/external/work-jiang/lectures/geo-strategy-11-the-second-american-civil-war.md); [#12 — Psychohistory / hope & modeling (END)](../../research/external/work-jiang/lectures/geo-strategy-12-psychohistory-the-science-of-imagining-the-future.md)
  - Book/site production: [STATUS](../../research/external/work-jiang/STATUS.md), [BOOK-ARCHITECTURE](../../research/external/work-jiang/BOOK-ARCHITECTURE.md), [THESIS-MAP](../../research/external/work-jiang/THESIS-MAP.md), [CHAPTER-QUEUE](../../research/external/work-jiang/CHAPTER-QUEUE.md), [CONCEPT-DICTIONARY](../../research/external/work-jiang/CONCEPT-DICTIONARY.md), [CLAIMS-OVERVIEW](../../research/external/work-jiang/CLAIMS-OVERVIEW.md), [evidence-packs](../../research/external/work-jiang/evidence-packs/); comparative layer: [QUOTE-BANK](../../research/external/work-jiang/QUOTE-BANK.md), [COUNTER-READINGS](../../research/external/work-jiang/COUNTER-READINGS.md), [INTELLECTUAL-CHRONOLOGY](../../research/external/work-jiang/INTELLECTUAL-CHRONOLOGY.md)
- `research/external/youtube-channels/predictive-history/` — machine transcripts + `index.json` for channel pulls
- [work-civ-mem](../../docs/skill-work/work-civ-mem/README.md) — stewardship surface for civilization_memory; use for analytic frames and CIV-MEM ↔ text crosswalks
  - [CIV-MEM lens (work-jiang)](../../research/external/work-jiang/CIV-MEM-LENS.md) — lattice mapped to lectures + registries; CMC as reference, not Record
