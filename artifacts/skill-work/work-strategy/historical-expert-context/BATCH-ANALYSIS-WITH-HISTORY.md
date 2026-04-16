# Batch-analysis with history (wrapper) — implementation note

This file documents **`scripts/strategy_batch_analysis_with_history.py`** (in-repo). Regenerate the bundle after updating snapshot or historical `.md` artifacts.

**Purpose:** Read `batch-analysis-snapshot.json`, load compact historical lines from `historical-expert-context/*.md` for both experts in a pair, emit one markdown bundle under `artifacts/skill-work/work-strategy/batch-analysis-with-history/`.

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

**Snapshot schema:** The wrapper should read **`batch_analysis_refs`** (not `rows`) from the snapshot JSON, and filter rows where both expert slugs appear in **`expert_ids`** or in the serialized row.
