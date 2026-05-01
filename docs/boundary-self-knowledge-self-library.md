# Boundary: SELF-KNOWLEDGE vs SELF-LIBRARY

**Purpose:** Canonical ontology for identity-facing vs reference-facing Record content. **Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md).

**See also:** [glossary.md](glossary.md), [library-integration.md](library-integration.md), [cmc-routing.md](cmc-routing.md), [self-library-domains.md](self-library-domains.md) (Library Domain Registry — canonical index of reference domains).

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

## SELF-KNOWLEDGE Growth Shape

SELF-KNOWLEDGE should grow as **sparse, gated, identity-facing IX-A**: what the companion has actually learned, can use in-character, and has approved as part of the Record. SELF-LIBRARY may grow much richer as reference infrastructure, but library richness is not a reason to bulk-promote source facts into IX-A. Prefer one well-evidenced knowledge claim over many mirrored shelf entries; if a domain mainly improves lookup, keep it in SELF-LIBRARY.

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

## Boundary Review Queue

Operational surface for **classification at the identity/library boundary**: hints on gate candidates, inbox display, future reclassify + audit. See [boundary-review-queue.md](boundary-review-queue.md).

## Validation

- **`scripts/validate-integrity.py`** (default CI path) runs IX-A boundary checks via `collect_identity_library_violations` — failures block integrity pass. Also validates `proposal_class` when present on gate candidates; CI uses `--require-proposal-class` for `grace-mar` so every **pending** candidate must declare `proposal_class`.
- **`scripts/validate_identity_library_boundary.py`** — same IX-A rules standalone (exit 1 if violations).
- **`scripts/process_approved_candidates.py --apply`** — after merging approved candidates **in memory**, runs the same IX-A rules on the merged `self.md` preview; violations **block the write** (merge aborts before disk update). Shared rules live in `scripts/identity_library_boundary_rules.py` (also used by `recursion_gate_review` boundary hints).
