# Page contract — strategy notebook

WORK only; not Record.

**Purpose:** A **one-screen link hub**. Normative spec lives in the files below; do not duplicate long excerpts here.

## Center of gravity

- **`strategy-page` blocks** (marker-fenced in expert **`thread.md`** journal layers) are the **primary analytical unit** — portable by stable `id=` across experts and months.
- **Thread file(s)** (`experts/<expert_id>/thread.md` or monthly `*-thread-YYYY-MM.md`) are **containers and continuity lanes**: month segments, machine extraction, and embedded pages.
- **Month continuity** in the thread **journal layer** (above the machine markers) is **bookended synthesis** from that month’s thread-embedded pages when you fill it in: **lede** after `## YYYY-MM`, **`strategy-page`** bodies dated in the month, optional **closer** — see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Thread* and [strategy-expert-template.md](strategy-expert-template.md#thread-template). Read-only inventory: `python3 scripts/list_strategy_pages_by_month.py --year-month YYYY-MM` (optional `--expert-id`, `--chronicle-snippets`, `--json`).

## Where the rules live

| Topic | Document / tool |
|-------|-----------------|
| Fence syntax, page template | [strategy-page-template.md](strategy-page-template.md) |
| Thread layers (journal vs machine), parse contract | [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Thread](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology) |
| `watch=` and multi-expert duplicate pages | [watches/README.md](watches/README.md) (page format) |
| Validation | From repo root: `python3 scripts/validate_strategy_pages.py` — [validate_strategy_pages.py](../../../../scripts/validate_strategy_pages.py) |
| Machine **`### Page references`** | [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology) (machine layer) |
| Bundled read-only multi-expert snapshots | [compiled-views/README.md](compiled-views/README.md) — **derived**, not SSOT |
| Trace and receipts (script runs) | [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](STRATEGY-NOTEBOOK-TRACE-CONTRACT.md) |
| Page update operations (script / propose) | [STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md](STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md) |
| Derived graph (rebuild) | [GRAPH-SCHEMA.md](GRAPH-SCHEMA.md), `build_strategy_notebook_graph.py` |

## Multi-expert pages

When several experts address the same page, the **same `id=`** appears in each expert’s `thread.md` (see [watches/README.md](watches/README.md)). This is **intentional** duplication for per-lane reading; **not** multiple competing sources of truth.
