# ID Taxonomy

**Purpose:** Canonical reference for all identifier prefixes used in Grace-Mar. Ensures consistent naming and supports provenance, schema work, and tooling.

**See also:** [architecture.md](architecture.md), [pipeline-map.md](pipeline-map.md)

---

## Prefix Summary

| Prefix | Scope | Location | Description |
|--------|-------|----------|-------------|
| **ACT-** | Activity | self-archive.md § V. ACTIVITY LOG | Raw activity records — bot exchanges, physical artifacts, lookups |
| **LEARN-** | Knowledge | self.md IX-A | Facts that entered awareness (post-seed) |
| **CUR-** | Curiosity | self.md IX-B | Topics that caught attention (post-seed) |
| **PER-** | Personality | self.md IX-C | Observed personality entries (post-seed): behavior, speech/style, emotional patterns, aesthetic tendencies, value expressions |
| **CANDIDATE-** | Pipeline | recursion-gate.md | Staged signals awaiting approve/reject |
| **WRITE-** | Evidence | self-archive.md § II. WRITING LOG | Writing samples, journals, stories |
| **READ-** | Evidence | self-archive.md § I. READING LIST | Books, articles consumed |
| **CREATE-** | Evidence | self-archive.md § III. CREATION LOG | Artwork, collages, creative output |
| **MEDIA-** | Evidence | self-archive.md § IV. MEDIA LOG | Movies, shows, games (survey + mentions) |
| **LIB-** | Library | users/[id]/self-library.md | Approved library entries spanning references, canon works, and influential media |

---

## Standard capability labels (self-skill-*)

Canonical labels for the Record-bound SKILLS modules when referring to the companion's capability layer (APIs, docs, cross-references):

| Standard label | Module | Location | Description |
|----------------|--------|----------|-------------|
| **self-skill-write** | WRITE | self-skills.md § WRITE Container | Production — journal, stories, explanations; primary data source for SELF linguistic style |
| **self-skill-think** | THINK | self-skills.md § THINK Container | Intake, learning, comprehension (multimodal); feeds SELF interests and preferences |

Use these labels in prose, tooling, and external references where a single token is needed. The Record-bound skill modules are **THINK** (intake, learning, comprehension) and **WRITE** (production, expression). Evidence prefixes (WRITE-, READ-, CREATE-, ACT-) are unchanged; READ-nnn feeds the THINK container (Reading List).

### Work layer labels

Canonical labels for the separate work / execution layer:

| Standard label | Scope | Location | Description |
|----------------|-------|----------|-------------|
| **work-territory** | Reusable execution domain | `docs/skill-work/work-*/` | A self-contained work domain such as `work-dev`, `work-politics`, or `work-human-teacher` |
| **work-context** | Instance-specific work state | `users/[id]/work-*.md` | Live instance work files such as `work-alpha-school.md`, `work-jiang.md`; separate from SKILLS |

**Historical compatibility:** `BUILD` remains an internal legacy term attached to older docs, evidence, and analyses. `CREATE-*` and `ACT-*` remain valid evidence IDs and are not renamed by this taxonomy change.

---

## Standard location labels (self-library, self-archive, self-memory)

Canonical labels for key self-scoped files (APIs, docs, cross-references):

| Standard label | File | Description |
|----------------|------|-------------|
| **self-library** | users/[id]/self-library.md | **SELF-LIBRARY** — reference-facing governed domains (not SELF-KNOWLEDGE); **CIV-MEM** = sub-library (scopes + corpus); gated pipeline |
| **self-archive** | On-disk **`self-archive.md`** | **Canonical EVIDENCE file:** full activity log + **`self-archive.md` § VIII** (gated approved). **Chronological** across entries; **expansive, multicategory, multimodal** (typed sections, ids, media, artifacts). Optional `self-evidence.md` = compatibility pointer only. |
| **self-memory** | users/[id]/memory.md | **Short / medium / long** horizons for continuity (see [memory-template.md](memory-template.md)); **governance-ephemeral** = outside gated Record, rotatable — **not** “short-term only”; **chronological** prose; **narrower** than self-archive (no multicategory evidence spine); optional; Voice loads short→long with caps |

Use these with **self-skill-write** and **self-skill-think** for a consistent self-scoped vocabulary. Use **work-territory** / **work-context** when referring to the separate execution layer.

### Capitalization and format

Use these rules everywhere docs list companion-self components (the `self-*` standard labels).

| Kind | Rule | Examples |
|------|------|----------|
| **Standard labels** | Lowercase, hyphenated, **bold** when listing components | **self-knowledge**, **self-identity**, **self-curiosity**, **self-personality**, **self-skill-think**, **self-skill-write**, **self-archive**, **self-library**, **self-memory**, **self-voice** |
| **Formal Record surfaces** (disambiguation) | ALL CAPS with hyphen | **SELF-KNOWLEDGE** (identity-facing IX-A), **SELF-LIBRARY** (reference-facing `self-library.md`), **SELF** (identity + IX in `self.md`), **SELF-ARCHIVE** (gated approved log — `self-archive.md` § VIII; full EVIDENCE on disk) |
| **On-disk paths** | Monospace, always lowercase filenames | `self.md`, `self-identity.md` (optional split surface), `self-library.md`, `self-evidence.md`, `self-archive.md` |
| **Planned WORK coordination** | Not part of companion self; same label shape as other `self-*` files | **`self-work`** → `users/[id]/self-work.md` (operator coordination; **not** SELF-KNOWLEDGE) |

**Do not** use sentence case (**Self-voice**) or mixed-case (**Self-Knowledge**) for standard labels. **Voice** and **Record** remain capitalized when meaning the product interfaces (triadic cognition / triad), not as `self-voice` spelled with two capitals.

---

## Companion self contains

The **companion self** (the documented self + the self that companions) is composed of these standard components. See [CONCEPTUAL-FRAMEWORK](conceptual-framework.md) (companion self).

| Component | Location | Description |
|-----------|----------|-------------|
| **self-knowledge** | self.md IX-A | **SELF-KNOWLEDGE** — identity-facing facts; from observation, READ-nnn, teaching. Domain corpora → **SELF-LIBRARY** / CIV-MEM, not IX-A dumps. See [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md). |
| **self-identity** | self-identity.md (optional) | Durable identity commitments — boundaries, role-level commitments, long-horizon direction — when an instance uses the split surface; gated like the rest of the Record. See [canonical-paths.md](canonical-paths.md), [identity-fork-protocol.md](identity-fork-protocol.md). |
| **self-curiosity** | self.md IX-B | Topics that catch attention (post-seed curiosity) |
| **self-personality** | self.md IX-C | Observed, evidence-linked personality entries (post-seed personality); contradiction-preserving rather than trait-test style |
| **self-skill-write** | self-skills.md § WRITE Container | Production capability |
| **self-skill-think** | self-skills.md § THINK Container | Intake, learning, comprehension capability |
| **self-archive** | `self-archive.md` (full file) | **EVIDENCE** — chronological, **multicategory** activity spine + § VIII gated approved (voice + non-voice) |
| **self-library** | self-library.md | Curated return-to store of references, canon works, and influential media |
| **self-memory** | memory.md | Short/medium/long continuity; **non-Record** and prunable (not “only session-length”); **chronological** prose; narrower than EVIDENCE / self-archive |
| **self-voice** | Voice / bot (e.g. bot/bot.py) | Queryable interface that speaks the Record when queried; renders self-skill-think, self-skill-write, and the rest of the companion self |

**Adjacent but separate:** work territories and instance work contexts may use full LLM/tool capability and may produce artifacts or staged candidates, but they are not part of the self-skill taxonomy and do not automatically enter the Record.

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

### Optional: richer `PER-*` metadata

`PER-*` entries may also include optional metadata when the observation benefits from more structure:

- `facet` — `behavioral_tendency`, `emotional_pattern`, `interpersonal_posture`, `aesthetic_tendency`, `value_expression`, or `style_marker`
- `evidence_strength` — `single_signal`, `repeated_pattern`, or `cross_context`
- `stability` — `emerging`, `recurring`, or `stable`
- `valence` — `attraction`, `aversion`, `mixed`, or `neutral`
- `tension_with` — other `PER-*` ids or short notes indicating preserved tension

These are optional enrichment fields, not a schema migration requirement. The core invariant stays the same: `PER-*` is an observed, evidence-linked, human-approved entry in `IX-C`.

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

*Last updated: March 2026*
