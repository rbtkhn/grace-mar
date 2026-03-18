# Boundary: SELF-KNOWLEDGE vs SELF-LIBRARY

**Purpose:** Canonical ontology for identity-facing vs reference-facing Record content. **Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md).

**See also:** [glossary.md](glossary.md), [library-integration.md](library-integration.md), [cmc-routing.md](cmc-routing.md).

---

## Rule (one line)

**SELF-KNOWLEDGE is identity-facing. SELF-LIBRARY is reference-facing. CIV-MEM is a governed sub-library inside SELF-LIBRARY, not part of SELF-KNOWLEDGE.**

*Glossary, README, architecture, and CMC routing quote this rule; do not paraphrase for enforcement text.*

---

## Definitions

| Term | Meaning |
|------|---------|
| **SELF** | The canonical **identity surface** of the fork: personality, style, values, preferences, boundaries, narrative continuity, post-seed IX-A/B/C. |
| **SELF-KNOWLEDGE** | The **identity-facing knowledge** in SELF — what the companion knows *about herself*: biographical continuity, preferences, values, identity-relevant facts (including facts she learned that matter to *who she is* in-character). Physically: primarily `self.md` IX-A (and seed sections), not domain corpora. |
| **SELF-LIBRARY** | The **governed reference layer** attached to the fork: structured return-to sources, domain shelves, and scoped lookup entries. Physically: `users/[id]/self-library.md` (Entries YAML) plus navigator docs under `SELF-LIBRARY/`. **Not identity.** |
| **CIV-MEM** | **Civilizational-memory domain** — historical, geopolitical, cultural, and related **reference material** carried as LIB rows + hybrid corpus paths. A **sub-library of SELF-LIBRARY**, not an extension of SELF-KNOWLEDGE. |

---

## Migration rules (for operators and analysts)

1. **Identity stays in SELF** — who she is, what she prefers, how she speaks, personal continuity → SELF / SELF-KNOWLEDGE (gate as today).
2. **Reference domains go to SELF-LIBRARY** — governed corpora, return-to sources, structured domain notes → `self-library.md` (gate when perimeter shifts).
3. **CIV-MEM is never identity** — do not store civilization-scale reference *as* IX-A merely because she can use it in lookup. IX-A may record *that she engaged with* a topic (identity-relevant); the **corpus** lives in SELF-LIBRARY / CIV-MEM.
4. **Review burden differs** — SELF-KNOWLEDGE merges shape in-character truth; SELF-LIBRARY merges shape what sources the Voice may draw on. Use **proposal_class** on candidates to separate review intent (see [identity-fork-protocol.md](identity-fork-protocol.md) §3.5).

---

## Routing (CMC)

When CIV-MEM is installed in-repo, **routing to CMC** is routing into the **CIV-MEM domain of SELF-LIBRARY** — a reference lookup path — **not** routing to a separate identity authority. See [cmc-routing.md](cmc-routing.md).

---

## Export model

Logical shape (see `scripts/export_fork.py`):

- `self` — full identity markdown (or summary).
- `self_knowledge` — IX-A (and optional IX-B/C slices) as explicit logical bucket.
- `self_library` — library raw + `civ_mem` sub-object (LIB ids whose scopes indicate civ-mem).

---

## Validation

- **`scripts/validate-integrity.py`** (default CI path) runs IX-A boundary checks via `collect_identity_library_violations` — failures block integrity pass. Also validates `proposal_class` when present on gate candidates; optional `--require-proposal-class` for strict queues.
- **`scripts/validate_identity_library_boundary.py`** — same IX-A rules standalone (exit 1 if violations).
