# Thread contract â€” strategy-codex
<!-- word_count: 392 -->

WORK only; not Record.

**Purpose:** Shared hub for the thread side of the canonical bundle. Normative detail lives in the files below; do not duplicate long excerpts here.

## Center of gravity

- **Threads** are the month-bounded continuity surface; **pages** are the portable analytical objects; **raw-input** is the literal SSOT.
- The canonical thread shape lives in [strategy-expert-template.md](strategy-expert-template.md#thread-template).
- Month continuity in the journal layer is a short bookended synthesis of that monthâ€™s `strategy-page` set.

## Thread-page binding

**Author surfaces are siblings, not a hierarchy:** **Thread / Continuity** tracks temporal narrative and analytical continuity; **Pages / Work Product** are focused author-associated analytical objects. Keep a small bidirectional index, but do not duplicate the page.

**Monthly thread files** use these continuity bullets in the machine index:

```markdown
### Pages / Work Product

- YYYY-MM-DD - [Page title](<page path>)
  role: carry-forward
  delta: One sentence saying what the page contributes to continuity.
```

**Thread month segments** should stay compact:

- one file per month when possible
- `thread.md` only while migrating
- journal prose above machine extraction
- page index in machine output, not page prose repeated in full

**Thread-embedded `strategy-page` blocks** are the main analytical pages for the month. Use the fence shape in [strategy-expert-template.md](strategy-expert-template.md#strategy-page-template), and keep the month file as the continuity container.

**Drafting flow:** thread composition should be driven by that monthâ€™s page set, with a compact continuity summary and lifted quotes only when they support the month narrative.

**Machine extraction:** keep the script-managed block between the `<!-- strategy-author-thread:start -->` and `<!-- strategy-author-thread:end -->` comments.

## Where the rules live

| Topic | Document / tool |
|-------|-----------------|
| Thread scaffold | [strategy-expert-template.md#thread-template](strategy-expert-template.md#thread-template) |
| Thread-embedded page fence | [strategy-expert-template.md#strategy-page-template](strategy-expert-template.md#strategy-page-template) |
| Month-to-month continuity rules | [STRATEGY-NOTEBOOK-ARCHITECTURE.md Â§ Thread](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology) |
| Page vs thread hub | [NOTEBOOK-CONTRACT.md](NOTEBOOK-CONTRACT.md) |
| Validation | From repo root: `python3 scripts/validate_strategy_pages.py` â€” [validate_strategy_pages.py](../../../../scripts/validate_strategy_pages.py) |
| Machine **`### Page references`** | [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology) (machine layer) |
| Trace and receipts (script runs) | [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](STRATEGY-NOTEBOOK-TRACE-CONTRACT.md) |
| Page update operations (script / propose) | [STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md](STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md) |

## Multi-author pages

When several authors address the same page, the **same `id=`** appears in each authorâ€™s **thread file for that month** (see [watches/README.md](watches/README.md)). This is intentional duplication for per-lane reading, not multiple competing sources of truth.

## Thread month segments

**Canonical layout:** one month file per author when possible; legacy `thread.md` only while migrating.
