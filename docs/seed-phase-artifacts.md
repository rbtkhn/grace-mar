# Seed Phase — Artifacts

**Companion-Self template · Artifact index**

These files are **pre-activation formation outputs**. They are **not** the live Record (`self.md`, `self-evidence`, IX files). After activation, instance repos use the **gated pipeline** to merge evidence into the Record.

---

## Canonical layout

Two reference trees in this repo:

| Tree | Purpose |
|------|---------|
| `users/_template/seed-phase/` | Scaffold: placeholders for new runs. |
| `users/demo/seed-phase/` | Synthetic completed example for docs, validation, and UI demos. |

---

## File set

| File | Stage(s) | Role |
|------|----------|------|
| `seed-phase-manifest.json` | All | Index: versions, status, artifact paths, optional changelog. |
| `seed_intake.json` | 0 | Intake, constraints, education focus, completion metrics; optional **`cursor_operator_profile`** (IDE + Cursor rules preset intent for the instance — see [cursor-pack-from-seed.md](cursor-pack-from-seed.md)). |
| `seed_intent.json` | 0 (parallel) | Operating purpose, supported/unsupported workflows, review-required and human-only zones, activation success criteria — see [seed-phase-intent.md](seed-phase-intent.md). |
| `seed_identity.json` | 1 | Identity scaffold + confidence. |
| `seed_curiosity.json` | 2 | Curiosity scaffold + confidence. |
| `seed_pedagogy.json` | 3 | Pedagogy scaffold + confidence. |
| `seed_expression.json` | 4 | Expression scaffold + confidence. |
| `seed_memory_contract.json` | 5 | Memory governance contract + confidence (classes, regions, provenance). |
| `memory_ops_contract.json` | 5 | **MemoryOps** layer: taxonomy (episodic/semantic/…), retention policies, export/RTBF rights, drift protection — complements `seed_memory_contract.json`; validated by `seed-memory-ops-contract.v1.json`. |
| `seed_trial_report.json` | 6 | Trial results, stability and safety scores. |
| `seed_readiness.json` | 7 | Gate decision, stage_completion, blocking/non-blocking issues. |
| `seed_confidence_map.json` | 7 | Aggregated confidence_map + band constants. |
| `work_dev_seed.json` | (parallel) | Development / technical-systems context seed; governs promotion into `users/<id>/work-dev.md`. |
| `work_business_seed.json` | (parallel) | Business / commercial / venture context seed; governs promotion into `users/<id>/work-business.md`. |
| `seed_constitution.json` | (derived) | Offline-synthesized constitution from other seed JSON (`scripts/generate-constitution.py`); optional input to Voice self-critique via `runtime_config.json` — not merged into SELF without the gated pipeline. |
| `seed_dossier.md` | 7 | Human-readable summary for sign-off. |

**Naming:** JSON files use **snake_case** on disk. JSON Schemas in `schema-registry/` use **kebab-case** with `.v1.json` suffix (e.g. `seed-intake.v1.json` validates `seed_intake.json`; `seed-intent.v1.json` validates `seed_intent.json`; `work-dev-seed.v1.json` validates `work_dev_seed.json`; `work-business-seed.v1.json` validates `work_business_seed.json`).

---

## work-dev seed artifact

`work-dev` (the user module `work-dev.md`) is a **seeded work-layer module**, not a preloaded doctrine file.

It begins **blank** in the template and is populated only when seed-survey evidence (or explicit input / governed updates) indicates that development or technical systems work is relevant to the user.

**Status semantics**

- `uninitialized` — no approved seed content has been promoted into `work-dev.md` yet.
- `initialized` — approved seed outputs have been promoted into `work-dev.md`.

**Evidence semantics** (`evidence_basis`)

- `none` — no seed evidence recorded yet.
- `seed_survey` — populated from seed survey responses.
- `explicit_user_input` — populated directly from explicit user statements.
- `mixed` — both channels contributed.

**Promotion path**

1. Collect seed survey responses into `seed-phase/work_dev_seed.json`.
2. Validate against `schema-registry/work-dev-seed.v1.json`.
3. Approve during seed readiness / activation workflow.
4. Promote approved content into `work-dev.md`.
5. Set `status` to `initialized` in the seed artifact and reflect the same in the markdown module.

**Boundary notes**

- `work-dev.md` is a **user module** under `users/<id>/`.
- It is **not** the operator-facing `docs/skill-work/work-dev/` tree (integration, OpenClaw, exports).
- It is **not** `self-skill-work`, which tracks **skill claims** rather than development-context preferences.

**Schema note:** `work_dev_seed.json` uses `additionalProperties: false`; new keys require a schema version bump.

---

## work-business seed artifact

`work-business` (the user module `work-business.md`) is a **seeded work-layer module**, not a preloaded doctrine file.

It begins **blank** in the template and is populated only when seed-survey evidence (or explicit input / governed updates) indicates that business, market, or commercial context matters for this companion.

**Status semantics**

- `uninitialized` — no approved seed content has been promoted into `work-business.md` yet.
- `initialized` — approved seed outputs have been promoted into `work-business.md`.

**Evidence semantics** (`evidence_basis`)

- `none` — no seed evidence recorded yet.
- `seed_survey` — populated from seed survey responses.
- `explicit_user_input` — populated directly from explicit user statements.
- `mixed` — both channels contributed.

**Promotion path**

1. Collect seed survey responses into `seed-phase/work_business_seed.json`.
2. Validate against `schema-registry/work-business-seed.v1.json`.
3. Approve during seed readiness / activation workflow.
4. Promote approved content into `work-business.md`.
5. Set `status` to `initialized` in the seed artifact and reflect the same in the markdown module.

**Boundary notes**

- `work-business.md` is a **user module** under `users/<id>/`.
- It is **not** the operator-facing `docs/skill-work/work-business/` tree (research docs, Grace Gems, deep dives).
- It is **not** `self-skill-work`, which tracks **skill claims** rather than commercial-context preferences.

**Schema note:** `work_business_seed.json` uses `additionalProperties: false`; new keys require a schema version bump.

---

## JSON Schemas

Each artifact has a schema under [schema-registry/](https://github.com/rbtkhn/companion-self/tree/main/schema-registry). See [schema-record-api.md](schema-record-api.md) § Seed-phase artifact schemas.

---

## Validation

```bash
python3 scripts/validate-seed-phase.py users/demo/seed-phase
python3 scripts/validate-seed-phase.py users/_template/seed-phase --allow-placeholders
```

See [seed-phase-validation.md](seed-phase-validation.md).

---

## Regenerating the dossier

```bash
python3 scripts/generate-seed-dossier.py users/demo/seed-phase
```

---

*See [seed-phase.md](seed-phase.md) for the top-level protocol.*
