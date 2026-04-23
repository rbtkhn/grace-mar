# Strategy notebook — derived artifacts (WORK)

Rebuildable outputs from [docs/skill-work/work-strategy/strategy-notebook/](../../docs/skill-work/work-strategy/strategy-notebook/). **Not** canonical; [runtime-vs-record.md](../../../docs/runtime-vs-record.md).

| Path | Produced by | Policy |
|------|-------------|--------|
| `receipts/strategy-notebook-receipts.jsonl` | `strategy_page.py`, `compile_strategy_view.py`, … | **Append-only** trace lines; default **gitignored** |
| `graph.json` | `scripts/build_strategy_notebook_graph.py` | Derived **page / expert / watch** graph; delete and rebuild |
| `views/*.json` | Same builder | **watch-clusters**, **expert-convergence** summaries |

See [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-TRACE-CONTRACT.md) and [GRAPH-SCHEMA.md](../../docs/skill-work/work-strategy/strategy-notebook/GRAPH-SCHEMA.md).
