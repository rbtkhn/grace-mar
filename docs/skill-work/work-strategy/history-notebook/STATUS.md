# History Notebook — STATUS (WORK only)

**Single SSOT** for **“next `hn-*` chapters to draft.”** Strategy-notebook [meta.md](../strategy-notebook/chapters/) should **link here**, not maintain a parallel queue.

## Volume priority (operator — pick one primary lane first)

- [ ] **Vol V — Contemporary** (same-day strategy relevance): `hn-v-america-hegemonic`, `hn-v-china-modern`, `hn-v-russia-modern`, `hn-v-persia-modern`
- [ ] **Vol I — Problem spine** (comparative ancient mechanisms): `hn-i-v1-01` … `hn-i-v1-20`

**Active choice (edit when you commit):** _e.g. “Primary: Vol I spine through v1-05; Vol V when contemporary judgment dominates.”_

## Distillation queue (ordered)

Reorder as **`HN gap:`** lines from strategy-notebook accumulate. Stub ids must exist in [book-architecture.yaml](book-architecture.yaml).

1. `hn-i-v1-01` — Legitimacy After Conquest (planned)
2. `hn-i-v1-02` — Civilizational Endurance Under Defeat (planned)
3. `hn-i-v1-03` — When Power Changes Shape (planned)
4. _(extend or replace per operator; add Vol V ids when that lane is primary)_

## Monthly strip (habit)

Once per month (manual):

1. Search strategy-notebook for **`### History resonance`** and **`HN gap:`** lines.
2. Count: **Tier 1** `hn-*` cites vs **deferred** vs **gap lines**.
3. Reorder **Distillation queue** above from the gap backlog.
4. Optional: run `python3 scripts/validate_strategy_hn_citations.py` (warns on unknown `hn-*` tokens).

**Target:** rising share of Tier 1 over time as chapters land.

## Coverage coupling (cross-book-map)

When you bump a row in [cross-book-map.yaml](cross-book-map.yaml) from **`stub` → `partial`**, add **at least one** strategy-notebook **`### History resonance`** line that month (pointer + mechanism) so PH/HN coverage advances show up in fast judgment.

## Related

- [README.md](README.md) — book model and LIB-0156
- [STRATEGY-NOTEBOOK-ARCHITECTURE § Parallel to History notebook](../strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#parallel-to-history-notebook-lib-0156)
- [validate_cross_book.py](../../../scripts/validate_cross_book.py) — PH ↔ HN map validation
