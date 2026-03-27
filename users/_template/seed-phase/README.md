# Seed Phase Artifact Set

This directory contains the **canonical artifact layout** produced before a new companion instance is activated.

These files are **scaffold-only** in `_template/`: placeholders and `TODO` values. In an instance repo, the corresponding files are produced during seed phase and reviewed before activation.

**Not the live Record** — see [docs/seed-phase-artifacts.md](../../../docs/seed-phase-artifacts.md).

Validate (lenient):

```bash
python3 scripts/validate-seed-phase.py users/_template/seed-phase --allow-placeholders
```
