# Route recommendations (derived receipts)

Markdown **advisory** receipts from [`scripts/recommend_route.py`](../../scripts/recommend_route.py).

**Purpose:** Thin, heuristic “which lane fits this task?” notes — **not** a router, orchestrator, or gate substitute. Receipts sit outside the gated Record; see [`docs/route-recommendation.md`](../../docs/route-recommendation.md).

**Rebuild:** Run on demand:

```bash
python3 scripts/recommend_route.py -t "Your task …" [--lane-hint work-strategy] [--stdout]
```

Default write path: `artifacts/route-recommendations/YYYY-MM-DD/<HHMMSS>-<slug>.md`. Omit the file with `--stdout --no-write` for chat paste only.

**Policy:** Outputs are rebuildable snapshots; staleness equals “rerun.” Do not merge into Record from this artifact alone.
