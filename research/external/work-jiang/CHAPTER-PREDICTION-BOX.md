# Chapter-end prediction box (Part I)

Use at the **end of each Part I chapter** (Geo-Strategy lectures 1–12, book chapters `ch01`–`ch12`).

## Purpose

Close each chapter with **at least three** clearly stated forecast claims drawn from the registry, so readers see what Jiang’s argument implies for the near future **before** Part II evaluates the corpus as a whole.

## Source of truth

- **Registry:** `prediction-tracking/registry/predictions.jsonl`
- **Per-chapter IDs:** `metadata/book-architecture.yaml` → `book.chapters[].prediction_ids` (three IDs per chapter by default)

## Template (prose)

Add a subsection titled **Predictions (this lecture)** (or equivalent). For each `prediction_id` listed for that chapter:

1. **ID** — `jiang-GSNN-00x`
2. **One sentence** — paraphrase `claim_summary` from the registry (or quote sparingly with pointer to transcript).

Optional one line: **claim type** (`event`, `conditional`, `time_bounded`, `trend`, `interpretive`, `series_preview`, …) so Part II can reference scoring rules.

## Part II

After **Chapter 12**, Part II is a **deep web and news** pass over the same `prediction_id` rows: time-stamped, citable sources; **triangulation** (more than one independent line of evidence when the claim is high-stakes); and scoring that respects **claim type** (events vs conditionals vs trends vs interpretive claims—the last two may stay “not evaluable” unless you define metrics).

The chapter-end box is **not** the full scorecard; it is the **handoff list** from exposition to Part II’s **per-prediction adjudication** and **overall evaluation** of how the Geo-Strategy forecasts hold up together.
