# Seed Phase — Validation

**Companion-Self template**

Seed phase artifacts are **JSON Schema–backed**. Use the validator before claiming readiness or merging bootstrap docs that depend on demo data.

---

## Requirements

- Python **3.10+**
- **`jsonschema`** (Draft 2020-12 support) for strict validation
- **`pytest`** + **`cryptography`** if you run the full seed-phase test suite (birth certificate tests)

```bash
pip install -r scripts/requirements-seed-phase.txt
```

Optional (not required for `validate-seed-phase.py`):

- **`plotly`** (+ **`kaleido`** for PNG) — confidence radar: `scripts/requirements-seed-phase-dashboard.txt`
- **`cryptography`** only — if you use signing without the bundle above: `scripts/requirements-seed-phase-signing.txt`

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
4. `seed-phase-manifest.json` lists artifact keys matching the standard set (including `seed_intent`, `memory_ops_contract`, `seed_constitution`, `work_business_seed`, `work_dev_seed` → matching `.json` filenames).
5. `seed_dossier.md` exists (non-empty).

---

## Regenerate dossier (demo)

```bash
python3 scripts/generate-seed-dossier.py users/demo/seed-phase
```

---

## Confidence dashboard (optional)

Reads `seed_confidence_map.json` and writes `confidence-report.html` under the seed-phase directory. PNG export requires **kaleido**; without it, HTML is still produced.

```bash
pip install -r scripts/requirements-seed-phase-dashboard.txt
python3 scripts/generate-confidence-report.py users/demo/seed-phase
```

---

## Birth certificate (optional)

Computes a deterministic **genesis hash** over all strict-validated JSON artifacts (see `scripts/seed_phase_artifacts.py` order), then writes `seed_birth_certificate.json` and `seed_birth_certificate.sig` (Ed25519).

- Production: pass **`--private-key`** to a PEM file containing an **Ed25519** private key, or set **`SEED_BIRTH_CERT_PRIVATE_KEY_PATH`**.
- Demos only: **`--insecure-generate-ephemeral-key`** (new key each run; signatures are not durable).

```bash
pip install -r scripts/requirements-seed-phase-signing.txt
python3 scripts/generate-birth-certificate.py users/demo/seed-phase --private-key /secure/path/ed25519.pem
```

`template_version` on the certificate is read from **`template-manifest.json`** at the repo root.

---

## Companion factory CLI (optional)

Creates **`output-dir/<instance_name>/`** by copying a **template** checkout, then seeds **`users/<instance_name>/seed-phase/`** from **`users/_template/seed-phase/`**. Use a clean **companion-self** template tree as `--template`; avoid pointing at a private instance repo if it contains live Record data you do not want duplicated.

```bash
python3 scripts/companion_factory.py new my-instance \
  --template /path/to/companion-self \
  --output-dir /path/to/parent
```

The command prints the exact **`validate-seed-phase.py`** invocation for the new tree.

---

## Constitution artifact (`seed_constitution.json`)

After strict validation succeeds, synthesize and validate the constitution JSON (deterministic, no LLM in the generator):

```bash
python3 scripts/generate-constitution.py users/demo/seed-phase
python3 scripts/validate-constitution.py users/demo/seed-phase
```

`validate-seed-phase.py` does **not** run the generator (avoid subprocess coupling in CI). Treat **generate → validate constitution** as a separate operator step when refreshing the artifact.

**Voice runtime:** Optional self-critique reads `users/<id>/seed-phase/seed_constitution.json` and repo-root `runtime_config.json` (`constitutional_critique.enabled`, default false). Nested **`voice_avatar`** (STT/TTS placeholders, avatar, `latency_mode`) is documented in [voice-runtime-config.md](voice-runtime-config.md). Metrics append to `users/<id>/<metrics_filename>` when logging is on (JSONL; may be ingested alongside other observability pipelines).

---

## Reuse in instance repos

Copy `scripts/validate-seed-phase.py`, `schema-registry/seed-*.v1.json`, and point the script at your instance’s seed directory (same filenames). Keep **seed artifacts outside** merged Record paths until activation policy is met.

---

*See [seed-phase-artifacts.md](seed-phase-artifacts.md).*
