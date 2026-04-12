# Export CLI — dual-repo inventory

**Purpose:** Track **unified export CLI** (`scripts/export.py`) parity between **grace-mar** (instance) and **companion-self** (template).

## Script parity

| Module | grace-mar `scripts/` | companion-self `scripts/` (at introduce) |
|--------|----------------------|------------------------------------------|
| `export.py` (dispatcher) | yes | yes (copy; same contract) |
| `export_fork.py` | yes | not present — promote via merge |
| `export_prp.py` | yes | not present |
| `export_user_identity.py` | yes | not present |
| `export_manifest.py` | yes | not present |
| `export_runtime_bundle.py` | yes | not present |

Update this table when the template gains modules.

## Local `companion-self/` under grace-mar

If `./companion-self/` is a **gitignored** local clone (see repo `.gitignore`), changes there are **not** part of the grace-mar commit. Ship the same `scripts/export.py` and `docs/EXPORT-CLI.md` to the **companion-self GitHub repo** in a separate PR, or copy from this doc tree after pulling grace-mar `main`.

## After parallel land (checklist)

- [x] `python scripts/export.py --help` works in **both** repos (grace-mar: full dispatch; companion-self: help; template clone has only `export.py` until modules are promoted).
- [x] Run `python scripts/template_diff.py` from grace-mar (2026-04-11: no `scripts/export.py` delta in manifest lock vs pinned paths; dispatcher not yet on `origin/main` — see below).
- [ ] Update `template-source.json` / `instance-contract.json` **`templateCommitTarget`** when companion-self **`main`** includes the unified export PR (pin the merge commit; then re-run `template_diff.py`).

**Upstream note:** `https://github.com/rbtkhn/companion-self` **`main`** did not yet contain `scripts/export.py` at last check; open work lives on branch **`feature/unified-export-cli`**. After that lands on **`main`**, complete the remaining checkbox and refresh audit outputs if the manifest gains `scripts/export.py` / `docs/EXPORT-CLI.md`.

See [EXPORT-CLI.md](../../EXPORT-CLI.md).
