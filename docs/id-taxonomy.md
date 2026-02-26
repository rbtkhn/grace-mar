# ID Taxonomy

**Purpose:** Canonical reference for all identifier prefixes used in Grace-Mar. Ensures consistent naming and supports provenance, schema work, and tooling.

**See also:** [architecture.md](architecture.md), [pipeline-map.md](pipeline-map.md)

---

## Prefix Summary

| Prefix | Scope | Location | Description |
|--------|-------|----------|-------------|
| **ACT-** | Activity | self-evidence.md § V. ACTIVITY LOG | Raw activity records — bot exchanges, physical artifacts, lookups |
| **LEARN-** | Knowledge | self.md IX-A | Facts that entered awareness (post-seed) |
| **CUR-** | Curiosity | self.md IX-B | Topics that caught attention (post-seed) |
| **PER-** | Personality | self.md IX-C | Observed behavioral patterns (post-seed) |
| **CANDIDATE-** | Pipeline | pending-review.md | Staged signals awaiting approve/reject |
| **WRITE-** | Evidence | self-evidence.md § II. WRITING LOG | Writing samples, journals, stories |
| **READ-** | Evidence | self-evidence.md § I. READING LIST | Books, articles consumed |
| **CREATE-** | Evidence | self-evidence.md § III. CREATION LOG | Artwork, collages, creative output |
| **MEDIA-** | Evidence | self-evidence.md § IV. MEDIA LOG | Movies, shows, games (survey + mentions) |
| **LIB-** | Library | users/[id]/library.md | Approved lookup sources (query first before full LLM) |

---

## Standard capability labels (self-skill-*)

Canonical labels for the three SKILLS modules when referring to the self's capability layer (APIs, docs, cross-references):

| Standard label | Module | Location | Description |
|----------------|--------|----------|-------------|
| **self-skill-write** | WRITE | skills.md § WRITE Container | Production — journal, stories, explanations; primary data source for SELF linguistic style |
| **self-skill-read** | READ | skills.md § READ Container | Intake — comprehension, inference, vocabulary; feeds SELF interests and preferences |
| **self-skill-work** | WORK (BUILD container) | skills.md § BUILD Container | Making, planning, execution, creation; starts from zero, grows via pipeline |

Use these labels in prose, tooling, and external references where a single token is needed. The third module is named **WORK** in prose; in skills.md the section heading remains "BUILD Container" (internal identifier). Evidence prefixes (WRITE-, READ-, CREATE-, ACT-) are unchanged.

---

## Standard location labels (self-library, self-archive, self-memory)

Canonical labels for key self-scoped files (APIs, docs, cross-references):

| Standard label | File | Description |
|----------------|------|-------------|
| **self-library** | users/[id]/library.md | Curated lookup sources (books, reference works, videos); query-first for answers; gated pipeline |
| **self-archive** | users/[id]/self-archive.md | Gated log of approved activity (voice and non-voice); appended only on merge |
| **self-memory** | users/[id]/memory.md | Ephemeral session context — tone, recent topics, calibrations; not part of the Record; optional |

Use these with **self-skill-write**, **self-skill-read**, **self-skill-work** for a consistent self-scoped vocabulary.

---

## Companion self contains

The **companion self** (the documented self + the self that companions) is composed of these standard components. See [CONCEPTUAL-FRAMEWORK](conceptual-framework.md) (companion self).

| Component | Location | Description |
|-----------|----------|-------------|
| **self-knowledge** | self.md IX-A | Facts that entered awareness (post-seed knowledge) |
| **self-curiosity** | self.md IX-B | Topics that catch attention (post-seed curiosity) |
| **self-personality** | self.md IX-C | Observed behavioral patterns (post-seed personality) |
| **self-skill-write** | skills.md § WRITE Container | Production capability |
| **self-skill-read** | skills.md § READ Container | Intake/comprehension capability |
| **self-skill-work** | skills.md § BUILD Container | Making, planning, execution, creation |
| **self-archive** | self-archive.md | Gated log of approved activity |
| **self-library** | library.md | Curated lookup sources |
| **self-memory** | memory.md | Ephemeral session context (not part of Record) |
| **self-voice** | Voice / bot (e.g. bot/bot.py) | Queryable interface that speaks the Record when queried; renders self-skill-read, self-skill-write, self-skill-work (and the rest of the companion self) |

---

```
CANDIDATE-* (pending)
    │
    ├──[approved]──► ACT-* (new) + LEARN-* | CUR-* | PER-* (new)
    │
    └──[rejected]──► (no new IDs)

ACT-*
    │
    └──[referenced by]──► LEARN-*, CUR-*, PER-* (via evidence_id)

WRITE-*, CREATE-*, READ-*
    │
    └──[referenced by]──► SELF (seed/post-seed), SKILLS, activity_id in samples
```

---

## Format

- **ACT-NNNN** — 4-digit zero-padded (ACT-0001, ACT-0014)
- **LEARN-NNNN**, **CUR-NNNN**, **PER-NNNN** — 4-digit zero-padded
- **CANDIDATE-NNNN** — 4-digit zero-padded
- **WRITE-NNNN**, **READ-NNNN**, **CREATE-NNNN** — 4-digit zero-padded
- **MEDIA-NNNN** — 4-digit zero-padded

---

## Evidence References

Every post-seed SELF entry (IX-A, IX-B, IX-C) must have `evidence_id: ACT-XXXX` pointing to an existing Activity Log entry. This enforces:

- No claim without evidence
- LLM knowledge cannot leak (claims require user-approved source)
- Provenance is traceable

### Optional: scope / constraint (CMC-aligned)

IX entries (LEARN-, CUR-, PER-) may include an optional **scope** or **constraint** field: when the belief does not apply or would be invalid (e.g. "Only for pre-modern cases", "If X then this narrows"). Use when the candidate or analyst output implies a boundary. No backfill required. Improves auditability and aligns with CMC-style hard constraints per doctrine. See [NOTES-CMC-SUBSTANCE](notes-cmc-substance.md) §4, [IMPLEMENTABLE-OPTIMIZATIONS-FROM-CMC](implementable-optimizations-from-cmc.md) §3.

---

## Allocation

| ID type | Allocated by |
|---------|--------------|
| ACT-* | Integration step (when processing approved candidates) or manual evidence entry |
| LEARN-, CUR-, PER-* | Integration step (derived from CANDIDATE) |
| CANDIDATE-* | `bot/bot.py` `_next_candidate_id()` when analyst stages |
| LIB-* | Manual entry in LIBRARY |
| WRITE-, READ-, CREATE-* | Manual entry in EVIDENCE |
| MEDIA-* | Survey seed or manual entry |

---

*Last updated: February 2026*
