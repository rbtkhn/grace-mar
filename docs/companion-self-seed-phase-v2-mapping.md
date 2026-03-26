# Companion-self Seed Phase v2 ↔ Grace-Mar instance tools

**Purpose:** Align mental models between the **template** ([companion-self](https://github.com/rbtkhn/companion-self) Seed Phase v2) and **Grace-Mar**’s operator-facing [seed-phase-wizard.md](seed-phase-wizard.md) / `scripts/seed-phase-wizard.py`.

---

## Boundary

| Surface | Repo | Role |
|---------|------|------|
| Seed Phase v2 JSON artifacts | companion-self `users/_template/seed-phase/`, `users/demo/seed-phase/` | Pre-activation **formation** package; schemas in `schema-registry/seed-*.v1.json`. |
| `seed-phase-wizard.py` | grace-mar | Interactive **instance** bootstrap: `reflection-proposals/`, `users/<id>/seed/minimal-core.json`, `memory.md` tone — **does not** replace template seed JSON set. |

Neither replaces the other: the template defines **portable, validatable** artifacts; Grace-Mar defines **live operator workflow** under canonical instance paths.

---

## Mapping (conceptual)

| Template artifact | Grace-Mar analogue (today) | Notes |
|-------------------|----------------------------|--------|
| `seed_intake.json` | Wizard prompts + `minimal-core.json` fields | Future: optional export to template JSON from wizard. |
| `seed_identity.json` | `SEED-founding-intent.md` + SELF baseline (post-gate) | Template artifact is **pre**-Record; SELF merge is **post**-activation gate. |
| `seed_curiosity.json` | IX-B seeds via pipeline | Same separation: formation vs merged Record. |
| `seed_readiness.json` / dossier | Operator judgment + RECURSION-GATE | Template encodes **explicit** readiness JSON; instance may adopt when syncing docs. |

---

## Sync recommendation

When merging from companion-self ([MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md)):

1. Pull `docs/seed-phase*.md`, `schema-registry/seed-*.v1.json`, and validation scripts if instances should reuse them.
2. Do **not** overwrite `users/grace-mar/` with template seed-phase **demo** data.
3. Optionally add a `users/grace-mar/seed-phase/` (or repo-local) directory for a **real** run, validated with `validate-seed-phase.py` copied from template.

---

*Living note · update when wizard emits template-aligned JSON.*
