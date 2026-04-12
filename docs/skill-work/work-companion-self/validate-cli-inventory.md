# Validate CLI — dual-repo inventory

**Purpose:** Track **`scripts/validate.py`** parity between **grace-mar** (instance) and **companion-self** (template), mirroring [export-cli-inventory](export-cli-inventory.md).

## Script parity

| Component | grace-mar | companion-self |
|-----------|-----------|----------------|
| `scripts/validate.py` | yes | ship same contract |
| `scripts/ci_validation_inventory.py` | yes (source of truth for groups) | copy / sync |
| `docs/VALIDATE-CLI.md` | yes | adapt links (CI paths) |

## After template merge (checklist)

- [ ] `python scripts/validate.py --help` in both repos.
- [ ] Pin [`template-source.json`](../../../template-source.json) / [`instance-contract.json`](../../../instance-contract.json) to companion-self merge commit.
- [ ] Run `python3 scripts/template_diff.py` (see merge-from-template workflow).
- [ ] Confirm `ci` subcommand: template may omit instance-only scripts (`work_dev/validate_control_plane.py` etc.)—orchestrator must **error clearly** when a script path is missing.

## CI scope note

**grace-mar** [`.github/workflows/test.yml`](../../../.github/workflows/test.yml) runs the full validation sequence. **companion-self** CI may differ; document per-repo expectations in each repo’s `docs/VALIDATE-CLI.md`.
