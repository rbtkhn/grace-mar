# Skill-work-curate-library

**Objective:** Curate and maintain Grace-Mar's self-library — the Record's curated lookup sources (books, videos, reference works).

This submodule supports WORK and the Record by documenting **how** to curate self-library, what it feeds (lookup, RAG), and how it stays aligned with the companion's knowledge and curiosity.

---

## Purpose

| Role | Description |
|------|-------------|
| **Lookup** | Books, reference works, and media the Voice can draw on when answering questions. The bot queries LIBRARY first (LIBRARY_LOOKUP_PROMPT) before CMC or full LLM lookup. |
| **Mind-shaping record** | A catalog of influential and return-worthy media — what has shaped the mind and what to revisit. |

self-library is **gated**: entries enter through the pipeline (staging → companion approval → merge). No autonomous additions.

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Objective, scope, and curation principles for skill-work-curate-library. |
| **[library-schema](../../library-schema.md)** | Entry format (LIB-NNNN), fields (title, scope, status, type), dual role (lookup vs mind-shaping). |

---

## Curation principles

1. **Alignment with Record** — Scope and topics should align with IX-A (knowledge), IX-B (curiosity), and skills edge. New entries can extend the edge but should not drift far from documented interests.
2. **Lookup quality** — Active entries must be usable for lookup: clear scope, correct type (reference, book, story, video).
3. **Deprecation** — When a source is superseded or no longer relevant, set `status: deprecated`; do not delete. Preserves provenance.
4. **Gated pipeline** — Additions pass through PENDING-REVIEW. Companion approves before merge into self-library.

---

## Cross-references

- [Architecture](../../architecture.md) — LIBRARY in the Record
- [ID taxonomy](../../id-taxonomy.md) — self-library container
- [Bot core](../../../bot/core.py) — `_library_lookup`, `_load_library`, LIBRARY_LOOKUP_PROMPT
- [Export curriculum](../../../scripts/export_curriculum.py) — includes library titles in curriculum_profile.json
