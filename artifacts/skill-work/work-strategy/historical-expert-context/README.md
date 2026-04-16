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

Reads only the human layer **above** `<!-- strategy-expert-thread:start -->` in `strategy-expert-<id>-thread.md`. Strips the backfill HTML block before parsing month headings.

## Use with batch-analysis (manual)

[`parse_batch_analysis.py`](../../../scripts/parse_batch_analysis.py) is unchanged. Paste the **Prompt-ready compact block** from the generated `.md` (fenced `text` section) into your batch-analysis prompt or scratch, **before** the canonical inbox line:

```text
historical-expert-context | scott-ritter | stance=... | tensions=... | provenance=...
`batch-analysis | YYYY-MM-DD | Ritter × Davis | ...`
```

Phase 2 (optional): a wrapper script that prepends compact blocks for each expert in a pair — only after this pilot proves useful.
