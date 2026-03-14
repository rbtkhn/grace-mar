# Skill-work-curate-library

**Objective:** Curate and maintain Grace-Mar's self-library — the Record's curated return-to store of references, canon works, and influential media.

This submodule supports WORK and the Record by documenting **how** to curate self-library, what it feeds (lookup, RAG), and how it stays aligned with the companion's knowledge and curiosity.

---

## Purpose

| Role | Description |
|------|-------------|
| **Reference lane** | Lookup-first sources the Voice can draw on when answering questions. The bot queries LIBRARY reference sources first before CMC or full LLM lookup. |
| **Canon lane** | Approved stories, books, and collections that belong in Grace-Mar's long-term intellectual world. |
| **Influence lane** | Media that has already shaped Grace-Mar's taste, curiosity, knowledge, or personality. |

self-library is **gated**: entries enter through the pipeline (staging → companion approval → merge). No autonomous additions.

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Objective, scope, and curation principles for work-curate-library. |
| **[library-schema](../../library-schema.md)** | Entry format (LIB-NNNN), fields (`lane`, `type`, `engagement_status`, `lookup_priority`), and lane semantics. |

---

## Curation principles

1. **Alignment with Record** — Scope and topics should align with IX-A (knowledge), IX-B (curiosity), and skills edge. New entries can extend the edge but should not drift far from documented interests.
2. **Lane clarity** — Decide whether a source is primarily `reference`, `canon`, or `influence` before adding it. Do not collapse all three into one undifferentiated list.
3. **Lookup quality** — Active `reference` entries must be usable for lookup: clear scope, correct type, and appropriate `lookup_priority`.
4. **Deprecation** — When a source is superseded or no longer relevant, set `status: deprecated`; do not delete. Preserves provenance.
5. **Gated pipeline** — Additions pass through PENDING-REVIEW. Companion approves before merge into self-library.

---

## Cross-references

- [Architecture](../../architecture.md) — LIBRARY in the Record
- [ID taxonomy](../../id-taxonomy.md) — self-library container
- [Bot core](../../../bot/core.py) — `_library_lookup`, `_load_library`, LIBRARY_LOOKUP_PROMPT
- [Export curriculum](../../../scripts/export_curriculum.py) — includes library titles in curriculum_profile.json
