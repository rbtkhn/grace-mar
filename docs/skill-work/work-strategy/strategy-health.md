# work-strategy — health interpretation

**Companion doc** to [observability.md](observability.md), `artifacts/work-strategy/strategy-observability.json`, and (when generated) carry-stack aggregates under `runtime/work-strategy/observability/` from [`summarize_carry_receipts.py`](../../../scripts/work_strategy/summarize_carry_receipts.py).

## Green / yellow / red (heuristic)

### Structure signals

| Signal | Healthy | Investigate |
|--------|---------|-------------|
| Open decision points | Few, intentional | Many stale `open` without notebook movement |
| Authorized sources YAML | Growing toward parity with [work-strategy-sources.md](work-strategy-sources.md) | Stalled count vs markdown "Total: N sources" |
| Promotion policy | Present | Missing file |

### Reflection quality signals

| Signal | Healthy | Yellow | Red |
|--------|---------|--------|-----|
| **avg_sections_per_entry** | >=3.5 (Signal + Judgment + Links + Open) | 2.5-3.5 — some sections skipped | <2.5 — entries lack minimum structure |
| **avg_links_per_entry** | >=2 — judgment is cited | 1-2 — thin sourcing | <1 — judgment detached from sources |
| **inbox_pending_lines** | 0-30 — normal accumulation | 30-50 — weave soon | >50 — prune or weave overdue |
| **open_carry_forward** (relative to entries) | <50% — threads are being resolved | 50-75% — some debt | >75% — Open sections accumulating unresolved work |
| **promotion_date_mentions** | >0 after first month — notebook feeding STRATEGY | 0 for 2-3 weeks — check if arcs are stabilizing | 0 over a full month with active notebook — promotion habit stalled |

### What these measure (and what they don't)

- **avg_sections** measures **completeness of structure**, not quality of reasoning. A bad entry with all four sections scores 4.0. But consistently missing sections signals that the pass is skipping steps.
- **avg_links** measures **citation discipline**. Judgment with no Links cannot be traced or verified.
- **inbox_pending** measures **conversion rhythm**. High backlog means the inbox is accumulating without being synthesized into notebook judgment.
- **open_carry** measures **thread hygiene**. Some carry-forward is healthy (active threads). Too much means Open is becoming a junk drawer.
- **promotion_date_mentions** is a coarse proxy. It catches date strings in STRATEGY.md — not whether promotions were meaningful.

## Actions

- Run [build_strategy_observability.py](../../../scripts/build_strategy_observability.py) after ladder or sources changes, or periodically to check health.
- Use [WORK-LAYER-HARDENING-ROADMAP.md](../WORK-LAYER-HARDENING-ROADMAP.md) for full work-plane sequencing.
- If judgment quality signals go yellow, the most common fix is a **weave session** (inbox -> `days.md`) and an **Open thread audit** (close or defer stale items).
