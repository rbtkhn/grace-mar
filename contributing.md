# Contributing

This repository is primarily a **live cognitive-fork instance** (grace-mar) with a gated pipeline. External contributions are welcome for **code and docs**; changes to the **Record** (identity, evidence, gate) follow companion rules.

**Filename conventions:** [docs/naming-convention.md](docs/naming-convention.md) (lowercase docs, reserved `AGENTS.md`, OpenClaw export path).

## Before you start

1. Read [AGENTS.md](AGENTS.md) — knowledge boundary, sovereign merge rule, file-update protocol, and what assistants may not do.
2. For system design: [docs/architecture.md](docs/architecture.md), [docs/identity-fork-protocol.md](docs/identity-fork-protocol.md).
3. Canonical on-disk paths: [docs/canonical-paths.md](docs/canonical-paths.md) (lowercase `users/<id>/self.md`, etc.).
4. **Public-facing tone** (README, outbound copy, example tokens): [docs/contributing-public-copy.md](docs/contributing-public-copy.md).

## Record and pipeline (critical)

- **Do not** edit `users/*/self.md`, `self-evidence.md`, `recursion-gate.md`, `bot/prompt.py`, or PRP outputs by hand for “real” merges. Stage candidates; the companion approves; merges run via `python scripts/process_approved_candidates.py --apply` (see AGENTS.md).
- Commits that touch gated paths should include **`[gated-merge]`** in the message (or mention `process_approved_candidates`) if your [pre-commit](.pre-commit-config.yaml) commit-msg hook is installed.

## Code layout (after repo refactor)

- Flask apps: [apps/](apps/) (`miniapp_server.py`, `gate-review-app.py`, `metrics-dashboard.py`).
- Run from repository root so `REPO_ROOT` resolves to the checkout.
- Optional: [deployment/README.md](deployment/README.md) for Docker / Render / Procfile notes.

## Python package (optional)

The repo includes a minimal installable package under [src/grace_mar/](src/grace_mar/) ([pyproject.toml](pyproject.toml)):

```bash
pip install -e .
grace-mar warmup -u grace-mar --compact
```

Mini App / bot dependencies are optional: `pip install -e ".[miniapp]"` (see `[project.optional-dependencies]` in `pyproject.toml`). Most scripts still run with `python scripts/...` without an editable install.

**Reflection cycle (operator):** `pip install -e ".[reflect]"` — see [docs/reflection-cycle.md](docs/reflection-cycle.md). `grace-mar reflect -u grace-mar --dry-run` writes `users/<id>/reflection-proposals/` only; `--append` stages candidates into `recursion-gate.md`.

## Performance

- Budgets and tier meanings: [docs/perf-budgets.md](docs/perf-budgets.md).
- Local check against committed baselines: `python scripts/run_perf_suite.py --tier 1 -u grace-mar --check-baseline` (run before releases or after changing `scripts/recursion_gate_review.py`, `bot/retriever.py`, or `scripts/perf/baselines.json`).

## Questions

Open a discussion or issue on [GitHub](https://github.com/rbtkhn/grace-mar) for tooling and docs; instance-specific Record content is not something to “fix” without the companion’s process.
