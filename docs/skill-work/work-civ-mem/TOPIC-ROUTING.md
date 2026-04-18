# Civ-mem topic routing (ROME-first)

**Purpose:** Auditable **topic → civilization → MEM** ordering before deep reads. Complements `suggest_civ_mem_from_relevance.py` (single-entity relevance spine) and `build_civmem_upstream_index.py query` (untargeted full-text).

**WORK only;** not Record.

## Quick start

```bash
python3 scripts/route_civ_mem_topic.py "Pope Leo Vatican France"
python3 scripts/route_civ_mem_topic.py "mosque Algiers dialogue" --expand-connections
python3 scripts/route_civ_mem_topic.py --profile latin_catholic_sphere "custom"
```

**Config:** [`config/civ_mem_topic_routes.yaml`](../../../config/civ_mem_topic_routes.yaml) — profiles, keywords, `rome_seed_files`, `routing_rules_version`.

## Behavior

1. **Profile match** — Keyword substring overlap against each profile’s `keywords` list; tie-break by `priority`. If overlap is zero, use `default_profile`.
2. **Civ order** — `primary_civ` then `secondary_civs` (e.g. ROME → FRANCE → AMERICA for `latin_catholic_sphere`).
3. **Per civ:**
   - If `MEM–RELEVANCE–<CIV>.md` exists under `research/repos/civilization_memory/content/civilizations/<CIV>/`, run `suggest_civ_mem_from_relevance.py <CIV>` (unless `--dry-run`).
   - If absent for **ROME**, list **ROME seeds** from config (Tier B until upstream adds `MEM–RELEVANCE–ROME.md`).
4. **`--expand-connections`** — Parse `MEM CONNECTIONS` in the **first** ROME seed file; list MEM ids (ROME-internal first, then others), capped by `max_cross_civ_edges`.

Re-check **`tier_a_relevance_entities`** and filesystem inventory when bumping the `civilization_memory` submodule.

## When to use vs other tools

| Tool | Use when |
|------|----------|
| `route_civ_mem_topic.py` | Mixed geography / papacy / Islam–Christian encounter; need **ordered** civs and ROME-first discipline |
| `suggest_civ_mem_from_relevance.py <X>` | You already fixed **X** and a relevance spine exists |
| `build_civmem_upstream_index.py query` | Exploratory search without a routing prior |

## Recursive improvement (no black boxes)

**Loop:** run router → open MEMs → weave Judgment / Links → record feedback → **human** edits YAML → bump `routing_rules_version`.

**Optional log:** `--log-decision` appends JSON lines to `artifacts/skill-work/work-civ-mem/routing-decisions.jsonl` (rebuildable).

### Operator one-liner feedback (grep-friendly)

| Pattern | Meaning |
|---------|---------|
| `routing:wrong_profile:<got>:<wanted>` | Classifier vs intended profile |
| `routing:missing_keyword:<profile>:<token>` | Add keyword to profile |
| `routing:seed_bad:<mem_id>` | Deprioritize seed |
| `routing:seed_good:<mem_id>` | Promote seed |
| `routing:civ_order:<c1>,<c2>,...` | Preferred civ order |
| `routing:upstream:pin_changed` | Submodule bump — re-inventory relevance files |

Agents **do not** auto-edit YAML from these lines without explicit operator / EXECUTE review.

**Optional ingest:** `python3 scripts/ingest_routing_feedback.py` (stdin or file args) appends normalized rows to `artifacts/skill-work/work-civ-mem/routing-feedback.jsonl`.

### Cadence

- After heavy strategy weeks: short YAML review.
- On submodule bump: re-run relevance inventory (which entities ship `MEM–RELEVANCE–*.md`).

## See also

- [`TRUMP-LEO-CIV-MEM-BARNES-DRILL.md`](../work-strategy/strategy-notebook/TRUMP-LEO-CIV-MEM-BARNES-DRILL.md) — manual ROME MEM picks
- [`CIV-MEM-TRI-FRAME-ROUTING.md`](../work-strategy/minds/CIV-MEM-TRI-FRAME-ROUTING.md)
- [`work-civ-mem/README.md`](README.md)
