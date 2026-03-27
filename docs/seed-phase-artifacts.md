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
| `seed_intake.json` | 0 | Intake, constraints, education focus, completion metrics. |
| `seed_identity.json` | 1 | Identity scaffold + confidence. |
| `seed_curiosity.json` | 2 | Curiosity scaffold + confidence. |
| `seed_pedagogy.json` | 3 | Pedagogy scaffold + confidence. |
| `seed_expression.json` | 4 | Expression scaffold + confidence. |
| `seed_memory_contract.json` | 5 | Memory governance contract + confidence. |
| `seed_trial_report.json` | 6 | Trial results, stability and safety scores. |
| `seed_readiness.json` | 7 | Gate decision, stage_completion, blocking/non-blocking issues. |
| `seed_confidence_map.json` | 7 | Aggregated confidence_map + band constants. |
| `seed_dossier.md` | 7 | Human-readable summary for sign-off. |

**Naming:** JSON files use **snake_case** on disk. JSON Schemas in `schema-registry/` use **kebab-case** with `.v1.json` suffix (e.g. `seed-intake.v1.json` validates `seed_intake.json`).

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
