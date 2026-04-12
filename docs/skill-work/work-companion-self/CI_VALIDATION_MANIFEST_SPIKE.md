# CI validation manifest spike

**Status:** Spike artifact shipped as [`config/ci_validation_manifest.yaml`](../../../config/ci_validation_manifest.yaml) (human-maintained mirror of [`scripts/ci_validation_inventory.py`](../../../scripts/ci_validation_inventory.py)).

**Goal:** Optionally drive both **GitHub Actions** and **`scripts/validate.py`** from one manifest to eliminate CI/orchestrator drift.

**Next steps (operator):**

1. Estimate cost of refactoring `.github/workflows/test.yml` to invoke a small runner that reads this YAML (or generated JSON).
2. Decide: keep Python inventory as sole source of truth **or** codegen from YAML at commit time.
3. If abandoned, keep YAML as documentation-only and rely on `tests/test_validate_cli.py` + inventory module.
