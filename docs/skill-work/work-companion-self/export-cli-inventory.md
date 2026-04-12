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

- [ ] `python scripts/export.py --help` works in **both** repos (grace-mar: full dispatch; companion-self: help even if targets missing).
- [ ] Run `python scripts/template_diff.py` from grace-mar; if `scripts/export.py` is new vs upstream, record in **expected drift** or confirm intentional match.
- [ ] Update `template-source.json` / instance contract when companion-self commit is pinned (grace-mar).

See [EXPORT-CLI.md](../../EXPORT-CLI.md).
