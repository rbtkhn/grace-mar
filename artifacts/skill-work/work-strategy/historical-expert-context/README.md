# Historical expert context (batch-analysis handoff)

WORK-only artifacts produced by [`scripts/strategy_historical_expert_context.py`](../../../scripts/strategy_historical_expert_context.py).

## Generate

```bash
python3 scripts/strategy_historical_expert_context.py \
  --expert-id scott-ritter \
  --start-segment 2026-01 \
  --end-segment 2026-03 \
  --dry-run

python3 scripts/strategy_historical_expert_context.py \
  --expert-id scott-ritter \
  --start-segment 2026-01 \
  --end-segment 2026-03 \
  --apply
```

**Range choice:** Use `--end-segment 2026-03` for **Q1-only** rollups, or `--end-segment 2026-04` (or later months as they exist in Segment 1) for **year-to-date** context through that calendar month. Wider ranges supersede narrower rollups for the same `<expert_id>` when you need Jan–Apr (or longer) in one file — older `*-2026-01-to-2026-03.md` artifacts may remain on disk until removed manually.

Reads only the human layer **above** `<!-- strategy-expert-thread:start -->` in `strategy-expert-<id>-thread.md`. Strips the backfill HTML block before parsing month headings.

## On-disk layout

| Artifact | Path |
|----------|------|
| Range rollup | `historical-expert-context/<expert_id>-<start>-to-<end>.md` (+ `.json`) |
| Per month | `historical-expert-context/<expert_id>/<YYYY-MM>.md` (+ `.json`) |

`--apply` writes **both** by default. Use `--no-rollup` or `--no-segment-files` to skip one side.

## Use with batch-analysis

[`parse_batch_analysis.py`](../../../scripts/parse_batch_analysis.py) is unchanged. For a **pair** plus **current snapshot rows**, use the wrapper (reads snapshot + two experts’ historical context, emits one bundle):

[`scripts/strategy_batch_analysis_with_history.py`](../../../scripts/strategy_batch_analysis_with_history.py) — see [`BATCH-ANALYSIS-WITH-HISTORY.md`](./BATCH-ANALYSIS-WITH-HISTORY.md). The wrapper **prefers** per-month files when **every** month in `--history-start` … `--history-end` exists under `historical-expert-context/<expert_id>/`; otherwise it uses the range rollup file.

**Manual paste (still valid):** copy the **Prompt-ready compact block** from a generated expert `.md` (fenced `text` section) into your batch-analysis prompt or scratch, **before** the canonical inbox line:

```text
historical-expert-context | scott-ritter | stance=... | tensions=... | provenance=...
`batch-analysis | YYYY-MM-DD | Ritter × Davis | ...`
```
