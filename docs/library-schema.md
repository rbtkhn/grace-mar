# LIBRARY Schema

**Purpose:** Governs the LIBRARY component — a curated store of approved sources Grace-Mar may return to for lookup, canon, and influence.

**Three lanes:**
1. **Reference** — Lookup-first sources Grace-Mar can draw on when answering questions.
2. **Canon** — Approved books, stories, and collections that belong in Grace-Mar's long-term intellectual world.
3. **Influence** — Media that has already shaped Grace-Mar's taste, curiosity, knowledge, or personality.

**See also:** [architecture.md](architecture.md), [id-taxonomy.md](id-taxonomy.md), EVIDENCE § I. READING LIST

---

## Relationship to Reading List

| Component | Purpose |
|-----------|---------|
| **EVIDENCE Reading List (READ-*)** | Books Grace-Mar has *consumed* — evidence of what she's read |
| **LIBRARY** | Curated return-to store of references, canon works, and influential media |

A book can appear in both. LIBRARY is not only a reading log. It includes lookup sources, approved canon, and influential media.

---

## Entry Format

Each LIBRARY entry uses the **LIB-** prefix.

```yaml
entries:
  - id: LIB-0001
    title: "Example Book Title"
    author: "Author Name"
    isbn: ""                      # optional: 10- or 13-digit ISBN (for lookup, disambiguation)
    lane: canon                   # reference | canon | influence
    type: book                    # book | story | article | reference | video | audio | other
    volume: ""                    # for type: story — the collection/container title
    status: active                # active | deprecated | archived
    scope: []                     # optional: topics this source covers (for query routing)
    engagement_status: planned    # planned | in_progress | consumed | recurring | available | trusted | primary
    read_id: null                 # optional: READ-XXXX if also in Reading List (evidence link)
    lookup_priority: low          # preferred | high | medium | low | none
    source: manual                # manual | path | url (for future RAG/indexing)
    url: ""                       # optional: canonical website, repository, or source page
    pd_url: ""                    # optional: Project Gutenberg, Wikisource, etc.
    shelf_intent: ""              # optional: canon | working_reference | operator_book | active_study | temporary_aid
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
| **lane** | Yes | `reference`, `canon`, or `influence` |
| **type** | Yes | `book`, `story`, `article`, `reference`, `video`, `audio`, `other` |
| **volume** | No | For `type: story` — the collection or source volume containing the story |
| **status** | Yes | `active`, `deprecated`, or `archived` |
| **scope** | No | List of topics (e.g. `[space, science, animals]`) for query routing |
| **engagement_status** | Yes | Current relationship to the source: `planned`, `in_progress`, `consumed`, `recurring`, `available`, `trusted`, or `primary` |
| **read_id** | No | READ-XXXX if this book is in EVIDENCE Reading List (evidence link when consumed) |
| **lookup_priority** | No | `preferred` (sorts above all other priorities in library summary), `high`, `medium`, `low`, or `none` |
| **source** | Yes | `manual` (no indexed content yet), `path`, or `url` for future RAG |
| **url** | No | Canonical website, repository, or source page for the entry |
| **pd_url** | No | URL to complete public domain text (Project Gutenberg, Wikisource) — for retrieval and RAG |
| **shelf_intent** | No | What role the entry plays: `canon`, `working_reference`, `operator_book`, `active_study`, or `temporary_aid`. See [Shelf Intent](#shelf-intent) below. |
| **added_at** | Yes | ISO date when added |
| **notes** | No | Free-form notes |
| **maturity** | No | 1–3 scale for content difficulty; see [Maturity](#maturity) below. Mirrors lesson difficulty. |

---

## Lane Semantics

### `reference`
Lookup-first sources Grace-Mar may actively consult when answering questions.

Examples:
- encyclopedias
- atlases
- codices
- trusted reference videos

### `canon`
Approved cultural works that belong in Grace-Mar's long-term library, whether or not already consumed.

Examples:
- fairy tales
- myths
- classic stories
- story collections

### `influence`
Media already shaping Grace-Mar's tastes, curiosity, knowledge, or personality.

Examples:
- watched ballet performances
- bedtime music
- repeatedly returned-to videos
- important consumed books

---

## Maturity

Optional **maturity** field (1–3) aligns LIBRARY with lesson difficulty. Same scale is used in [lesson-rules-config](../skill-work/lesson-rules-config.yaml) for LLM lesson scope.

| Value | Label | Description |
|-------|-------|-------------|
| **1** | Early/young | Picture books, early readers, simple vocabulary |
| **2** | Intermediate | Retellings, short chapter books, edge Lexile |
| **3** | Advanced | Full texts, older literature, SAT-prep tier |

Lesson generator uses this scale to scope activity difficulty and to instruct which LIBRARY maturity to draw from for reading activities.

---

## Lookup Priority

Optional routing signal for runtime lookup.

| Value | Meaning |
|-------|---------|
| **high** | First-stop source when scope matches |
| **medium** | Useful secondary source |
| **low** | Valid but not preferred for runtime lookup |
| **none** | Preserved for canon/influence, not used for active lookup routing |

---

## Shelf Intent

Optional field describing the entry's operational role in the library.

| Value | Meaning |
|-------|---------|
| **canon** | Durable cultural or intellectual fixture; long-term retention; rarely reviewed for freshness. |
| **working_reference** | Actively consulted for lookup; reviewed when scope or accuracy changes. |
| **operator_book** | Operator-authored analytical corpus (e.g. Predictive History, strategy notebook, journals). Reference-facing; does not bypass gate for identity claims. |
| **active_study** | Currently being read, studied, or ingested; temporary elevated priority; review when engagement ends. |
| **temporary_aid** | Short-lived utility (e.g. a one-off reference for a specific task); archive candidate after use. |

When omitted, the entry's role is inferred from `lane` and `scope`. The field is most useful for operator books and entries with non-obvious retention expectations.

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

1. Query active LIBRARY entries with `lane: reference` first
2. Then use active `canon` entries when relevant by scope
3. `influence` entries may inform tone, taste, or known exposure, but are not primary lookup sources unless explicitly intended
4. If no match is found (`LIBRARY_MISS`) → fall back to CMC, then full LOOKUP_PROMPT, then REPHRASE

Videos in LIBRARY can still contribute scope for routing, but the lane makes clear whether they are lookup sources, canon objects, or documented influences.

---

## Governance

- LIBRARY entries are added only through the gated pipeline or explicit user action
- Deprecating a source: set `status: deprecated`; do not delete (history preserved)
- Archiving a source: set `status: archived`; keep for history
- New entries get `added_at`; optional `evidence_tier` if linked to READ-*
- Canon and influence entries may remain active even when not primary lookup sources

---

## ID Allocation

LIB-* IDs are allocated sequentially. Next ID = max(LIB-*) + 1.

---

*Last updated: April 2026*
