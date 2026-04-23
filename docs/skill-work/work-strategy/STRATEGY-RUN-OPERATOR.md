# Strategy run — operator use

## Commands

From repo root:

```bash
# Start a run for a calendar day (resolves inbox, month days.md, raw-input/YYYY-MM-DD/)
python3 scripts/strategy_run.py start --date YYYY-MM-DD --intent eod

# Optional: name the session kind (default: eod_strategy)
python3 scripts/strategy_run.py start --date YYYY-MM-DD --intent eod --session-type eod_strategy

# Point at a copy of the notebook (tests / alternate tree)
python3 scripts/strategy_run.py start --date YYYY-MM-DD --notebook-dir /path/to/strategy-notebook
```

Output prints `run_id` (e.g. `stratrun-20260416-abc12def`) and paths to **state** and **start receipt**.

```bash
python3 scripts/strategy_run.py inspect --run-id stratrun-20260416-abc12def
python3 scripts/strategy_run.py resume --run-id stratrun-20260416-abc12def   # same summary; no file writes
python3 scripts/strategy_run.py complete --run-id stratrun-20260416-abc12def
```

If the run is in status `failed`, `complete` refuses unless you pass **`--force`** (marks completed anyway; use sparingly).

## Artifacts (derived, gitignored by default)

| Path | Content |
|------|---------|
| `artifacts/strategy-runs/<run_id>/state.json` | Lane, intent, `target_date`, `status`, resolved **inputs** (paths + exists flags), `proposed_outputs` (null until you add sidecars), `receipt_refs`, `warnings` |
| `artifacts/run-receipts/<run_id>-start.json` | Receipt for `start` |
| `artifacts/run-receipts/<run_id>-complete.json` | Receipt for `complete` |

## Report (optional)

```bash
python3 scripts/build_strategy_run_report.py
python3 scripts/build_strategy_run_report.py --limit 20 --output artifacts/strategy-run-report.md
```

## Applying judgment (not automated here)

- **`days.md` / `strategy-page` / threads:** This wrapper does **not** paste prose. After you have thesis and shape, you still edit Markdown or run **`scripts/strategy_page.py`** (and similar) **explicitly** if you want machine-assisted scaffolds; those tools emit the **trace JSONL** described in the notebook trace contract, which is a **different** grain from the run envelope.
- **Proposals (future or manual):** Valid JSON for `strategy-day-proposal` / `strategy-page-proposal` can be saved under a path you record in `state.json`’s `proposed_outputs` (v1 may leave both null until you add automation).

## Page operation names

| Proposal `operation` | Notebook [PAGE-UPDATE-CONTRACT](strategy-notebook/STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md) |
|---------------------|----------------------------------|
| `new` | Aligns with **APPEND** (new page scaffold) / fresh block |
| `append` | Add under existing page block where applicable |
| `refine` | Maps to **REFINE** / substantive edit to an existing page |

## See also

- [docs/run-contract.md](../../run-contract.md)
- [STRATEGY-RUN-ARCHITECTURE.md](STRATEGY-RUN-ARCHITECTURE.md)

**Tests / isolated runs:** Set environment variable `STRATEGY_RUN_ARTIFACT_ROOT` to a temporary directory that mirrors repo layout (`artifacts/`, optional `docs/.../strategy-notebook/`) so scripts do not write under the real repo — used by `tests/test_strategy_run.py`.
