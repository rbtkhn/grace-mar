# ADR 0001 — Future optional `users/` directory layout

**Status:** Proposed (not implemented)  
**Date:** 2026-03-21  
**Context:** Repo layout refactor; `users/grace-mar/` remains **flat** per [canonical-paths.md](../canonical-paths.md).

## Decision (deferred)

A future migration **might** introduce subfolders under `users/<id>/` (e.g. `identity/`, `evidence/processed/`) for operator ergonomics or large binary layout. That would require:

1. **RFC** agreed with companion and operator — canonical filenames (`self.md`, `self-evidence.md`, `recursion-gate.md`, …) stay authoritative **names**; only **directory** placement may change.
2. **One-shot migration script** updating every consumer: `scripts/process_approved_candidates.py`, `bot/`, `apps/`, tests, and CI.
3. **Coordinated release** with git tag and changelog; no partial migration.

## Non-goals (this ADR)

- No change to on-disk paths until the RFC is approved and tooling exists.
- No change to the **gated merge** rule or companion sovereignty.

## Consequences

- New instances should continue to use **`users/_template/`** as a **documentation-only** mirror of required filenames until a migration ships.
