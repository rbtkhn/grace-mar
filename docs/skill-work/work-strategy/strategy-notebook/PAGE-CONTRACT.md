# Page contract — strategy notebook

WORK only; not Record.

**Purpose:** A **one-screen link hub**. Normative spec lives in the files below; do not duplicate long excerpts here.

## Center of gravity

- **`strategy-page` blocks** (marker-fenced in expert **`thread.md`** journal layers) are the **primary analytical unit** — portable by stable `id=` across experts and months.
- **Thread file(s)** (`experts/<expert_id>/thread.md` or monthly `*-thread-YYYY-MM.md`) are **containers and continuity lanes**: month segments, machine extraction, and embedded pages.

## Where the rules live

| Topic | Document / tool |
|-------|-----------------|
| Fence syntax, page template | [strategy-page-template.md](strategy-page-template.md) |
| Thread layers (journal vs machine), parse contract | [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Thread](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology) |
| `watch=` and multi-expert duplicate pages | [watches/README.md](watches/README.md) (page format) |
| Validation | From repo root: `python3 scripts/validate_strategy_pages.py` — [validate_strategy_pages.py](../../../../scripts/validate_strategy_pages.py) |
| Machine **`### Page references`** | [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology) (machine layer) |
| Bundled read-only multi-expert snapshots | [compiled-views/README.md](compiled-views/README.md) — **derived**, not SSOT |

## Multi-expert pages

When several experts address the same page, the **same `id=`** appears in each expert’s `thread.md` (see [watches/README.md](watches/README.md)). This is **intentional** duplication for per-lane reading; **not** multiple competing sources of truth.
