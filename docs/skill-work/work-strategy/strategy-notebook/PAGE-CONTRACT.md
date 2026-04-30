# Page contract — strategy notebook
<!-- word_count: 372 -->

WORK only; not Record.

**Purpose:** A **one-screen link hub**. Normative spec lives in the files below; do not duplicate long excerpts here.

## Center of gravity

- **`strategy-page` blocks** (marker-fenced in expert **thread** journal layers) are the **primary analytical unit** — portable by stable `id=` across experts and months.
- **Thread file(s)** are **temporally limited — one file per calendar month:** **`experts/<expert_id>/<expert_id>-thread-YYYY-MM.md`** (journal + machine layer for that month only). **Legacy:** a single **`experts/<expert_id>/thread.md`** may still hold multiple **`## YYYY-MM`** segments until migrated.
- **Month continuity** in the thread **journal layer** (above the machine markers) is **bookended synthesis** from that month’s thread-embedded pages when you fill it in: **lede** after `## YYYY-MM`, **`strategy-page`** bodies dated in the month, optional **closer** — see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Thread* and [strategy-expert-template.md](strategy-expert-template.md#thread-template). Read-only inventory: `python3 scripts/list_strategy_pages_by_month.py --year-month YYYY-MM` (optional `--expert-id`, `--chronicle-snippets`, `--json`).

## Page-thread binding

**Expert surfaces are siblings, not a hierarchy:** **Thread / Continuity** tracks temporal narrative and analytical continuity; **Pages / Work Product** are focused expert-associated analytical objects. Strengthen the bond through a small bidirectional index while preserving different purposes.

**Standalone refined pages** should carry these appendix bullets when adopted:

```markdown
- **Thread file:** [experts/<expert_id>/<expert_id>-thread-YYYY-MM.md](experts/<expert_id>/<expert_id>-thread-YYYY-MM.md)  <!-- or legacy thread.md -->
- **Thread month:** `YYYY-MM`
- **Thread role:** `new-thesis` | `update` | `contradiction` | `falsifier` | `synthesis` | `carry-forward`
- **Continuity delta:** One sentence naming what this page changes, clarifies, or carries forward in the expert continuity.
```

**Thread month segments** should carry a compact page index when adopted:

```markdown
### Pages / Work Product

- YYYY-MM-DD - [Page title](<page path>)
  role: carry-forward
  delta: One sentence saying what the page contributes to continuity.
```

The thread index **does not duplicate** the page. It answers: *why does this page matter to this expert's temporal continuity?*

## Where the rules live

| Topic | Document / tool |
|-------|-----------------|
| Fence syntax, page template | [strategy-page-template.md](strategy-page-template.md) |
| Refined page scaffold (all experts) | [refined-page-template.md](refined-page-template.md) + per-expert `*-page-template.md` stub |
| Thread layers (journal vs machine), parse contract | [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Thread](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology) |
| `watch=` and multi-expert duplicate pages | [watches/README.md](watches/README.md) (page format) |
| Validation | From repo root: `python3 scripts/validate_strategy_pages.py` — [validate_strategy_pages.py](../../../../scripts/validate_strategy_pages.py) |
| Machine **`### Page references`** | [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology) (machine layer) |
| Bundled read-only multi-expert snapshots | [compiled-views/README.md](compiled-views/README.md) — **derived**, not SSOT |
| Trace and receipts (script runs) | [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](STRATEGY-NOTEBOOK-TRACE-CONTRACT.md) |
| Page update operations (script / propose) | [STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md](STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md) |
| Derived graph (rebuild) | [GRAPH-SCHEMA.md](GRAPH-SCHEMA.md), `build_strategy_notebook_graph.py` |

## Multi-expert pages

When several experts address the same page, the **same `id=`** appears in each expert’s **thread file for that month** (see [watches/README.md](watches/README.md)). This is **intentional** duplication for per-lane reading; **not** multiple competing sources of truth.

## Refined pages (standalone `*-page-*.md`)

**SSOT stack:** **[`raw-input/`](raw-input/README.md)** = literal capture; **refined page** = default handle for **`thread` / `days.md` / analysis** (see [refined-page-template.md](refined-page-template.md) **SSOT hierarchy**). **Target** **~3000** words, **~70–80%** in **`### Verbatim`**; [`refined_page_word_budget.py`](../../../../scripts/strategy/refined_page_word_budget.py).

**Distinct from** thread-embedded **`strategy-page`** fences: standalone files under **`experts/<expert_id>/`** (**Verbatim** / Reflection / Foresight; link to **`raw-input/`** in **`### Appendix`**). **Multiple refined pages for the same publication date are allowed** for every expert: default **`<expert_id>-page-YYYY-MM-DD.md`**, or **`<expert_id>-page-YYYY-MM-DD-<slug>.md`** when splitting by primary capture (`<slug>` from the **`raw-input`** stem). **Alternatively,** one file may consolidate same-day captures with **A / B / C** Verbatim blocks as defined in [refined-page-template.md](refined-page-template.md). Normative detail: [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) (split ingest / refined pages), the same **refined-page-template.md**, and each expert’s thin **`*-page-template.md`** compat stub.
