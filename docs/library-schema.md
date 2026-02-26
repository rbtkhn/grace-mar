# LIBRARY Schema

**Purpose:** Governs the LIBRARY component — a record of what has shaped the mind and what we might want to return to in future media consumption.

**Dual role:**
1. **Lookup** — Books, reference works, and media Grace-Mar can draw on when answering questions. The system queries LIBRARY first before falling back to CMC or full LLM lookup.
2. **Mind-shaping record** — A catalog of influential and return-worthy media: books, videos, references. What entered awareness; what to revisit.

**See also:** [architecture.md](architecture.md), [id-taxonomy.md](id-taxonomy.md), EVIDENCE § I. READING LIST

---

## Relationship to Reading List

| Component | Purpose |
|-----------|---------|
| **EVIDENCE Reading List (READ-*)** | Books Grace-Mar has *consumed* — evidence of what she's read |
| **LIBRARY** | Record of what shaped the mind + lookup sources. Books, reference works, videos. What to query for answers; what to come back to. |

A book can appear in both. LIBRARY includes lookup sources (encyclopedias, story collections, CMC) and media that shaped the mind (videos watched, performances).

---

## Entry Format

Each LIBRARY entry uses the **LIB-** prefix.

```yaml
entries:
  - id: LIB-0001
    title: "Example Book Title"
    author: "Author Name"
    isbn: ""                      # optional: 10- or 13-digit ISBN (for lookup, disambiguation)
    type: book                    # book | story | article | reference | video | other
    volume: ""                    # for type: story — the volume that contains this story
    status: active                # active | deprecated
    scope: []                     # optional: topics this source covers (for query routing)
    read_status: unread           # read | unread — has Grace-Mar consumed this?
    read_id: null                 # optional: READ-XXXX if also in Reading List (evidence link)
    source: manual                # manual | path | url (for future RAG/indexing)
    pd_url: ""                    # optional: Project Gutenberg, Wikisource, etc.
    added_at: 2026-02-XX
    notes: ""                     # optional
```

---

## Fields

| Field | Required | Description |
|-------|----------|-------------|
| **id** | Yes | LIB-NNNN (4-digit zero-padded) |
| **title** | Yes | Full title |
| **author** | No | Author or editor (omit for reference works) |
| **isbn** | No | 10- or 13-digit ISBN (with or without hyphens). Use for catalog lookups, disambiguation, future RAG. Older or non-trade books may omit. |
| **type** | Yes | `book`, `story`, `article`, `reference`, `video`, `other` |
| **volume** | No | For `type: story` — the book/collection that contains this story (e.g. "Usborne Illustrated Grimm's Fairy Tales") |
| **status** | Yes | `active` (queryable) or `deprecated` (excluded from lookup) |
| **scope** | No | List of topics (e.g. `[space, science, animals]`) for query routing |
| **read_status** | Yes | `read` or `unread` — has Grace-Mar consumed this? Default `unread` for new entries. |
| **read_id** | No | READ-XXXX if this book is in EVIDENCE Reading List (evidence link when consumed) |
| **source** | Yes | `manual` (no indexed content yet), `path`, or `url` for future RAG |
| **pd_url** | No | URL to complete public domain text (Project Gutenberg, Wikisource) — for retrieval and RAG |
| **added_at** | Yes | ISO date when added |
| **notes** | No | Free-form notes |

---

## pd_url Notes

- For books based on public domain works: add URL to Project Gutenberg or Wikisource.
- Use for: direct retrieval, RAG indexing, faster lookup, reduced LLM knowledge leak.
- Author pages (e.g. `gutenberg.org/ebooks/author/37` for Dickens) used for "Complete" collections.

## ISBN Notes

- Store digits with or without hyphens. Normalize to ISBN-13 when both formats exist.
- Use for: catalog lookups (Open Library, WorldCat), disambiguation between editions, future RAG indexing.

---

## Lookup Order

When Grace-Mar receives a "look it up" request (Telegram bot):

1. **Query LIBRARY** (active entries only) — LLM checks if question can be answered from LIBRARY sources (books, reference, video scope) by scope
2. **If found** → Answer from LIBRARY, rephrase in Grace-Mar's voice (REPHRASE_PROMPT)
3. **If not found** (LIBRARY_MISS) → Fall back to CMC, then full LOOKUP_PROMPT, then REPHRASE

Videos in LIBRARY contribute scope for routing (e.g. Coppélia video → ballet questions); the LLM draws on documented knowledge of that content.

---

## Governance

- LIBRARY entries are added only through the gated pipeline or explicit user action
- Deprecating a source: set `status: deprecated`; do not delete (history preserved)
- New entries get `added_at`; optional `evidence_tier` if linked to READ-*

---

## ID Allocation

LIB-* IDs are allocated sequentially. Next ID = max(LIB-*) + 1.

---

*Last updated: February 2026*
