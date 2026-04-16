# Batch-analysis with history (wrapper) — implementation note

This file documents **`scripts/strategy_batch_analysis_with_history.py`** (in-repo). Regenerate the bundle after updating snapshot or historical `.md` artifacts.

**Purpose:** Read `batch-analysis-snapshot.json`, load compact historical lines from `historical-expert-context/` for both experts in a pair (per-month `/<expert_id>/<YYYY-MM>.md` when the full window is present, else rollup `/<expert_id>-<start>-to-<end>.md`), emit one markdown bundle under `artifacts/skill-work/work-strategy/batch-analysis-with-history/`.

**Run (after script exists):**

```bash
python3 scripts/strategy_batch_analysis_with_history.py \
  --pair scott-ritter,daniel-davis \
  --history-start 2026-01 \
  --history-end 2026-03 \
  --dry-run

python3 scripts/strategy_batch_analysis_with_history.py \
  --pair scott-ritter,daniel-davis \
  --history-start 2026-01 \
  --history-end 2026-03 \
  --apply
```

**Prerequisites:** Generate historical artifacts for each expert in the pair:

```bash
python3 scripts/strategy_historical_expert_context.py \
  --expert-id scott-ritter --start-segment 2026-01 --end-segment 2026-03 --apply
python3 scripts/strategy_historical_expert_context.py \
  --expert-id daniel-davis --start-segment 2026-01 --end-segment 2026-03 --apply
```

For **Jan–Apr** (or any month where `strategy-expert-<id>-thread.md` has a `## YYYY-MM` segment), use the same command with `--end-segment 2026-04` and align `--history-end` on the wrapper with that window.

**Snapshot schema:** The wrapper should read **`batch_analysis_refs`** (not `rows`) from the snapshot JSON, and filter rows where both expert slugs appear in **`expert_ids`** or in the serialized row.
