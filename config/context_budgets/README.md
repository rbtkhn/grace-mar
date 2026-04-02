# Context budgets

JSON files here cap **operator ritual paste size** and dream **write-path** payloads. Operator scaffolding only; not Record truth.

| File | Consumers |
|------|-----------|
| `coffee.json` | `operator_daily_warmup.py` — collapsed Last dream lines, optional civ-mem/rollup lines, session tail depth |
| `dream.json` | `auto_dream.py`, `dream_civmem_echoes.py` — civ-mem echo limits, specificity gate, rollup allow, suppress analogies when checks fail |

**Reserved (not enforced in v1):** `default_visible_budget_lines`, `default_visible_budget_chars` — for future whole-warmup caps or audit targets.

**Reserved (v2):** `max_rollup_lines` — rollup line truncation is not implemented yet; do not add to JSON expecting enforcement.

**Semantics:** `min_civ_mem_overlap` applies to **index overlap counts** from `query_inrepo_civmem`. `require_specific_civ_mem_token` is a **query-side** specificity gate (see `docs/skill-work/work-dream/README.md`).
