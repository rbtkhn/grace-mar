# Seed Phase — Validation

**Companion-Self template**

Seed phase artifacts are **JSON Schema–backed**. Use the validator before claiming readiness or merging bootstrap docs that depend on demo data.

---

## Requirements

- Python **3.10+**
- Package: **`jsonschema`** (Draft 2020-12 support)

```bash
pip install jsonschema
```

---

## Commands

**Strict mode** (CI and `users/demo/seed-phase`):

```bash
python3 scripts/validate-seed-phase.py users/demo/seed-phase
```

**Placeholder mode** (`users/_template/seed-phase`): validates file presence, JSON parse, and manifest consistency; **skips** full schema validation so `TODO` strings and incomplete enums are allowed.

```bash
python3 scripts/validate-seed-phase.py users/_template/seed-phase --allow-placeholders
```

---

## What the validator checks

1. Expected files exist (see script `REQUIRED_FILES`).
2. Each file parses as JSON (where applicable).
3. Unless `--allow-placeholders`: each JSON instance validates against its schema in `schema-registry/`.
4. `seed-phase-manifest.json` lists artifact keys matching the standard set (including `work_business_seed`, `work_dev_seed` → matching `.json` filenames).
5. `seed_dossier.md` exists (non-empty).

Optional fields such as **`seed_intake.json.cadence_preference`** still validate strictly when present; omitting them is allowed.

---

## Regenerate dossier (demo)

```bash
python3 scripts/generate-seed-dossier.py users/demo/seed-phase
```

---

## Reuse in instance repos

Copy `scripts/validate-seed-phase.py`, `schema-registry/seed-*.v1.json`, and point the script at your instance’s seed directory (same filenames). Keep **seed artifacts outside** merged Record paths until activation policy is met.

---

*See [seed-phase-artifacts.md](seed-phase-artifacts.md).*
