# Workbench — script usage

Run commands from the **repository root** unless you use absolute paths.

These scripts only create or validate **workbench** inspection receipts under [WORKBENCH-RECEIPT-SPEC.md](WORKBENCH-RECEIPT-SPEC.md). They do **not** write to the recursion-gate, do **not** merge into the Record, and do **not** stage candidates. A receipt is a log of **artifact behavior** under stated commands and inspection—not proof of external facts.

- **Generator:** `scripts/work_dev/new_workbench_receipt.py` — JSON on disk, defaults `receiptKind: "workbench"`, `status: "draft"`, `recordAuthority: "none"`, `gateEffect: "none"`.
- **Validator:** `scripts/work_dev/validate_workbench_receipt.py` — exit `0` if the file matches the spec; non-zero on errors.
- **Preflight (pilot chain):** `scripts/work_dev/preflight_workbench.py` — read-only; rolls up docs, visualizer, fixture, `examples/*`, and optional generator `--check`. See [PREFLIGHT.md](PREFLIGHT.md).

**CLI mapping:** `--candidate-id` populates `artifactCandidateLabel` (a free label for A/B runs, **not** a `CANDIDATE-nnnn` gate id).

**List flags:** You may repeat flags (`--paths-touched` twice) and/or use comma-separated values in one string.

## Generator example

```bash
python3 scripts/work_dev/new_workbench_receipt.py \
  --artifact-type react \
  --candidate-id A \
  --source-prompt-ref docs/skill-work/work-dev/workspace.md \
  --paths-touched docs/example/App.tsx,docs/example/index.html \
  --commands-run "npm install" \
  --commands-run "npm run build" \
  --launch-command "npm run preview" \
  --inspection-method manual_screenshot \
  --status draft
```

With no `--output`, the file is written to:

`artifacts/work-dev/workbench-receipts/workbench-YYYYMMDD-HHMMSS.json`

(UTC clock in the filename; `receiptId` defaults to `wb-YYYYMMDD-HHMMSS` in the same second.)

## Validator example

```bash
python3 scripts/work_dev/validate_workbench_receipt.py \
  docs/skill-work/work-dev/workbench/examples/strategy-notebook-visualizer-receipt.example.json
```

On success, stdout prints `ok: workbench receipt is valid` and the process exits `0`.

## What these scripts are not

- **Not** gate automation — no YAML candidates, no `process_approved_candidates`.
- **Not** EVIDENCE or SELF — receipts stay in `artifacts/…` or a path you choose with `--output` (the generator refuses to write to `users/**/self.md`, `self-archive.md`, `self-library.md`, or `recursion-gate.md` by basename).

## Also see

- [README.md](README.md) — Workbench doctrine and link table.
