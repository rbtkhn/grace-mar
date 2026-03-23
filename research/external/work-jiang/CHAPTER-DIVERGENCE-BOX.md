# Chapter-end divergence box (Volume II — Civilization, Part I)

Use at the **end of each Part I chapter** that corresponds to a **Civilization** lecture (book chapters `civ01`… when defined; until then, curated transcript files `lectures/civilization-NN-*.md`).

## Purpose

Close each chapter with **clearly flagged** points where **Jiang’s stated claim** is **compared** to a **named mainstream or specialist** view—so readers see what is at stake interpretively **before** Part II ([`book/PART-II-CIVILIZATION-DIVERGENCE.md`](book/PART-II-CIVILIZATION-DIVERGENCE.md)) expands the comparison.

This is **not** a prediction box. Civilization does **not** use `prediction-tracking/registry/predictions.jsonl` for chapter-end handoff.

## Source of truth

- **Registry:** `divergence-tracking/registry/divergences.jsonl`
- **Per-chapter IDs:** When `metadata/book-architecture.yaml` (or a future Volume II chapter list) includes `divergence_ids` for Civilization chapters, list them there. Until then, **filter** the JSONL by `lecture_ref` matching the chapter’s `lectures/civilization-*.md` path.

## Template (prose)

Add a subsection titled **Divergence (this lecture)** (or equivalent). For each `divergence_id` tied to that lecture:

1. **ID** — `div-…` (stable slug from the registry)
2. **One sentence** — fair paraphrase of `jiang_claim` (or quote sparingly with pointer to transcript).
3. **One line** — **Mainstream anchor** (who counts as “mainstream” here) + **divergence_type** (`empirical`, `interpretive`, `pedagogical_compression`, `normative`) when known.

## Part II

After the **last Civilization chapter** in Part I, **Part II — Divergence** does **not** adjudicate forecasts. It **deepens** the divergence rows: evidence, alternative schools, and **where the lecture’s framing is idiosyncratic vs. widely shared**. See [`book/PART-II-CIVILIZATION-DIVERGENCE.md`](book/PART-II-CIVILIZATION-DIVERGENCE.md).

The chapter-end box is **not** the full divergence chapter; it is the **handoff list** from exposition to Part II’s **historiographic** comparison.
