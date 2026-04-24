# Workbench preflight

Read-only, **no Record writes**, **no gate staging**, **no merge path**. The preflight is an **operator convenience**: it checks that the Workbench pilot **documentation**, **example receipts**, **committed visualizer fixture JSON**, and (by default) **generated-fixture parity** with the live generator are in a good state before you commit or demo.

## What it checks

- **Core Workbench docs** are present: README, `WORKBENCH-RECEIPT-SPEC`, `VISUAL-INSPECTION-PROTOCOL`, `CANDIDATE-COMPARISON-PROTOCOL`.
- **Strategy workbench visualizer** pilot files are present: README, `GENERATED-FIXTURE.md`, HTML, `strategy-notebook-visualizer.fixture.json`.
- **Fixture JSON** parses and has the expected top-level keys, including `recordAuthority: "none"` and `gateEffect: "none"`, a non-empty `truthScope` string, and `nodes` / `edges` lists.
- **Each fixture node** has `id`, `label`, `kind`, `path`, `description`, and `authority: "work-only"`.
- **Each fixture edge** has `source`, `target`, and `relation`. If an edge references a node `id` that is not in the `nodes` list, the preflight **warns** (by default) — useful when the generator later adds **intentional** external references. Use `--strict` to treat those warnings as failures.
- **Example receipts** in `workbench/examples/*.json` with `receiptKind: "workbench"` are validated with the same rules as `validate_workbench_receipt.py` (no duplicated hand-maintained spec).
- **Freshness (default on):** runs `python3 scripts/work_strategy/generate_strategy_notebook_visualizer_fixture.py --check` so the on-disk committed fixture matches what the generator would write (modulo the generator’s time normalization for `generatedAt`).

## What it does **not** check

- It does **not** prove that screenshots, HTML, or fixtures describe **true** external or strategic facts. Structure and workbench **boundaries** only.
- It does **not** replace CI, the recursion gate, or single-file `python3 scripts/work_dev/validate_workbench_receipt.py` for ad-hoc receipts outside `examples/`.
- It does **not** read or write `users/grace-mar/self.md`, `self-archive.md`, `self-library.md`, or `recursion-gate.md`.

## Commands (repo root)

```bash
python3 scripts/work_dev/preflight_workbench.py
python3 scripts/work_dev/preflight_workbench.py --strict
python3 scripts/work_dev/preflight_workbench.py --skip-freshness
python3 scripts/work_dev/preflight_workbench.py --json
```

- **`--strict`** — fixture edge “missing node id” **warnings** fail the run.
- **`--skip-freshness`** — do not run the strategy fixture generator `--check` (offline or when you only care about static checks).
- **`--json`** — one JSON object on stdout (suitable for tooling); exit code still reflects pass/fail.

Exit **0** only when all **required** checks pass (and, with `--strict`, when there are no edge id warnings). Exit **nonzero** on any required failure.

## Visualizer smoke test

Optional **read-only** static check on the strategy-notebook workbench **HTML** only (it does not run a browser, does not load the network, and does not certify any strategic or external truth). It only asserts that the committed visualizer is still a substantial static document with the expected `fetch(… strategy-notebook-visualizer.fixture.json …)` hook, Workbench boundary language, and UI affordance markers, and that no CDN / framework / package-manager drift appeared in the file.

```bash
python3 scripts/work_dev/smoke_strategy_visualizer.py
python3 scripts/work_dev/smoke_strategy_visualizer.py --json
```

- **`--json`** — one JSON object on stdout (suitable for tooling). Exit code still reflects pass/fail.
- **`--strict`** — if the file is at least the minimum size but still suspiciously few lines, treat that as a failure (not the default; see script help).
