# Data layer roadmap

**Purpose:** Outline a path from markdown-as-database to a normalized data layer with markdown as export. This doc is design only; implementation is deferred until a later decision.

**Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md). Invariants (gated pipeline, Sovereign Merge Rule) remain unchanged.

---

## Current state

System state lives in **markdown files** under `users/[id]/`:

- **self.md** — identity, three-dimension mind (IX-A, IX-B, IX-C); YAML-like blocks.
- **self-evidence.md** — activity log (ACT-*, READ-*, WRITE-*, CREATE-*); structured blocks.
- **recursion-gate.md** — pipeline staging: candidates above `## Processed`, processed below.

**Consumers:** `bot/core.py`, `scripts/process_approved_candidates.py`, `scripts/recursion_gate_review.py`, `scripts/validate-integrity.py`, and others parse these files with regex/YAML-style extraction. That is transparent and git-friendly but brittle at scale: multiple parsers, regex drift, no single schema. Multi-user and automation would benefit from a single source of truth and typed schemas.

---

## Invariants (unchanged)

- **Sovereign Merge Rule:** Only the companion (or explicitly delegated human) may merge. The agent may stage; it may not merge. No autonomous merge path.
- **Merge semantics:** When we introduce a store, "merge" means: update store → regenerate markdown → commit. No direct markdown edits by the agent or by scripts other than the single regeneration path.
- **GRACE-MAR-CORE** and the gated pipeline remain the authority. Only `process_approved_candidates` (or its future equivalent) performs the merge operation.

---

## Phased approach (recommended if moving to a store)

### Phase A — Schema and read path

- Define JSON schemas (or SQLite tables) for: **SELF** (IX-A/B/C entries), **EVIDENCE** (ACT, READ, WRITE, CREATE), **recursion-gate** (candidates + processed).
- Add a **read-through** layer: if a JSON/SQLite file exists, use it; else parse markdown and (optional) write JSON once. No change yet to the write path; all writers continue to write markdown.

### Phase B — Write path for one surface

- Choose one surface (e.g. **recursion-gate** only): bot and scripts write only to the store; a single job regenerates `recursion-gate.md` from the store.
- Validate that all existing consumers (`process_approved_candidates`, operator gate snapshot, gate dashboard) still work against the regenerated file or are switched to read from the store.

### Phase C — Extend to SELF and EVIDENCE

- Same pattern for `self.md` and `self-evidence.md`: merge script updates the store and regenerates markdown. PRP and profile generation read from the store or from regenerated markdown.

---

## Alternative: minimal (no new store)

Do not introduce a structured store yet. Instead:

1. **Centralize parsing** in one module (e.g. `recursion_gate_review` is already shared by several scripts); ensure all readers use it.
2. **Single writer for recursion-gate:** Add one canonical writer for the gate file; all code that updates the gate calls it (no direct file writes from multiple places).
3. **Document** the canonical parser and writer so new code does not add new regex or ad-hoc writes. That reduces drift without a DB.

---

## Decision

Implementation of Phase A, B, C or of the minimal option is left to a later decision. This roadmap documents the current state, the invariants, and the options so that when we revisit, we can choose consistently.

---

## Success criteria (per phase gate)

Do not advance to the next phase without meeting the prior phase's criteria. If Phase A fails its criteria, reconsider whether the migration is worth pursuing at all.

| Phase | Metric | Target | How to measure |
|-------|--------|--------|----------------|
| **A** | Parser consolidation | 1 canonical parser per surface (gate, self, evidence) | Grep for regex/YAML extraction calls; count distinct parsers |
| **A** | Read-path correctness | 100% — store output matches markdown parse output for all existing files | Diff test: parse markdown → write to store → read from store → compare |
| **A** | Zero regressions | All existing consumers (`bot/core.py`, `process_approved_candidates.py`, `validate-integrity.py`) pass their test suites | Run existing tests against read-through layer |
| **B** | Write-path idempotency | Regenerated `recursion-gate.md` is byte-identical on repeated runs with no intervening changes | Run regeneration twice, diff output |
| **B** | Operator-invisible | Operator workflow unchanged — no new commands, no manual migration steps | Operator confirms during pilot |
| **C** | Full-surface parity | SELF and EVIDENCE regenerated markdown passes `validate-integrity.py` | Automated test |

### Sustainment

| Task | Cadence | What to check |
|------|---------|---------------|
| Parser drift audit | After any new script that reads gate/self/evidence | Is the new script using the canonical parser or adding ad-hoc regex? |
| Schema version check | After any structural change to self.md or self-archive.md | Does the store schema still match the markdown structure? |
| Regeneration fidelity | After any merge via `process_approved_candidates.py` | Does regenerated markdown match what the merge script produced? |

### Deprecation path

This roadmap may be abandoned if the minimal option (centralized parsing, no store) proves sufficient. In that case:

1. Delete any prototype store files (JSON/SQLite) if created during Phase A exploration.
2. Archive this roadmap to `docs/archived/data-layer-roadmap.md` with a note explaining why the migration was not pursued.
3. Ensure the minimal option's centralized parser is documented and all scripts use it.
4. No data is lost — markdown remains the source of truth throughout.

### Scope creep guardrail

This roadmap authorizes **schema definition and read/write path consolidation**. It does not authorize:

- **New data surfaces** (e.g. adding analytics tables, search indexes, or caches beyond the three core surfaces: gate, self, evidence)
- **External database dependencies** (e.g. Postgres, cloud-hosted stores) — the store is local-only (JSON or SQLite)
- **API layers** (e.g. REST/GraphQL endpoints for external consumers) — exports are handled by existing export scripts, not by a live API
- **Multi-user architecture** — this roadmap is for a single companion instance; multi-user is a different problem

Any of these requires a separate plan. Do not add them as "Phase D" to this roadmap.
