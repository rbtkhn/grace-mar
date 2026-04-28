# Unified validation CLI (`scripts/validate.py`)

Read-only orchestrator: runs existing validation scripts via subprocess. Does **not** modify `self.md`, `self-archive.md`, `recursion-gate.md`, or merge candidates.

## Usage

Global options **before** the subcommand:

```bash
python scripts/validate.py --user grace-mar ci
python scripts/validate.py --json fast
python scripts/validate.py --user grace-mar full
```

## Subcommands

| Command | Purpose |
|---------|---------|
| `ci` | Parity with `.github/workflows/test.yml` validation steps (no pytest): canonical paths, integrity (`--require-proposal-class`), template sync contract, governance, structured governance files (`validate_structured_files.py`), work-dev control plane. |
| `fast` | Cheap local checks: paths, identity/library boundary, IX evidence refs, governance, structured governance files (`validate_structured_files.py`). |
| `full` | Same as `ci` plus `measure_growth_and_density.py`. |
| `expensive` | `measure_uniqueness.py` (OpenAI). **Skipped** if `OPENAI_API_KEY` is unset (exit code 0, status `skipped`). |
| `experimental` | `validate_skills.py`, `validate-seed-phase.py` on `users/_template/seed-phase`. |

## Structured governance files

Standalone parse/link pass (also runs inside `ci` / `fast` via [`scripts/ci_validation_inventory.py`](../scripts/ci_validation_inventory.py)):

```bash
python scripts/validate_structured_files.py
```

## `--user` semantics

- **Required** for checks that target `users/<id>/` (paths, integrity, boundaries, evidence refs, growth). The effective user is passed through to those scripts.
- **Ignored** for repo-wide tools (governance, structured governance files, template sync contract, work-dev control plane, seed-phase template path). The CLI still accepts `--user` for a consistent interface; metadata in `--json` output includes `user_scope` per step.

Default user: `GRACE_MAR_USER_ID`, else `grace-mar` if that directory exists, else `_template`.

## Exit codes

- **0** — All steps `pass` or `skipped`.
- **1** — Any step `fail`, `timeout`, or `error`.

The orchestrator runs **all** steps in the group (no fail-fast), then exits **1** if any step failed.

## JSON output (`--json`)

Emits `validation-run.v1` to **stdout** only. Human progress lines go to **stderr** when not using `--json`.

Fields include: `schema_version`, `run_id`, `mode`, `user`, `overall_status`, `checks[]` (each with `argv`, `exit_code`, `duration_ms`, `status`, `user_scope`, `user_effective`, truncated stdout/stderr), `summary`, optional `template_pin` from `template-source.json`.

## CI parity

`ci` mode matches **Tests** workflow validation steps in [`.github/workflows/test.yml`](../.github/workflows/test.yml). [`.github/workflows/governance.yml`](../.github/workflows/governance.yml) uses `validate-integrity.py --json` and template sync `--json`; output modes differ but the same scripts run—use `ci` for local parity with the main test pipeline.

## Template repo (companion-self)

Ship the same `scripts/validate.py` and `scripts/ci_validation_inventory.py` contract in **companion-self**; subset of checks may be unavailable—missing scripts surface as step `error`. See [validate-cli-inventory](skill-work/work-companion-self/validate-cli-inventory.md).
