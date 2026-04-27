# Civ-mem topic routing (ROME-first)

**Purpose:** Auditable **topic → civilization → MEM** ordering before deep reads. Complements `suggest_civ_mem_from_relevance.py` (single-entity relevance spine) and `build_civmem_upstream_index.py query` (untargeted full-text).

**WORK only;** not Record.

## Quick start

```bash
python3 scripts/route_civ_mem_topic.py "Pope Leo Vatican France"
python3 scripts/route_civ_mem_topic.py "mosque Algiers dialogue" --expand-connections
python3 scripts/route_civ_mem_topic.py --profile latin_catholic_sphere "custom"
python3 scripts/route_civ_mem_topic.py "hormuz" --focus-config config/civ_mem_routing_focus.yaml
python3 scripts/route_civ_mem_topic.py "test" --no-focus
# MEM-only BFS (theology / lineage traces): connection-first walk to N distinct MEM files
python3 scripts/route_civ_mem_topic.py --profile theology_ra_trace "Law of One" --bfs-mem-target 50 --no-focus
python3 scripts/route_civ_mem_topic.py --profile theology_ra_trace "…" --bfs-mem-target 50 --bfs-max-depth 12 --bfs-neighbors-per-hop 32 --bfs-output artifacts/skill-work/work-civ-mem/bfs-log.json --no-focus
```

**Config:** [`config/civ_mem_topic_routes.yaml`](../../../config/civ_mem_topic_routes.yaml) — profiles, keywords, `rome_seed_files`, **`theology_seed_mems`** (multi-civ MEM rel paths for BFS), `routing_rules_version`.

**Optional routing focus:** [`config/civ_mem_routing_focus.yaml`](../../../config/civ_mem_routing_focus.yaml) — time-bounded `profile_overlap_bonus` and `sticky_keywords` (see **Routing focus** below).

**Trace contract:** [`topic-trace-contract.md`](topic-trace-contract.md) — topic traces are **WORK · DERIVED · NOT RECORD**, upstream is read-only, and structural analogy is not truth validation.

## Behavior

1. **Profile match** — Keyword substring overlap against each profile’s `keywords` list; tie-break by `priority`. If overlap is zero, use `default_profile`. If a **routing focus** file is loaded, in date range, and not disabled with `--no-focus`, add **integer bonuses**: per-profile `profile_overlap_bonus` plus per-entry `sticky_keywords` (substring match → bonus to named profile). Effective score = base overlap + those bonuses (disqualified profiles stay excluded).
2. **Civ order** — `primary_civ` then `secondary_civs` (e.g. ROME → FRANCE → AMERICA for `latin_catholic_sphere`).
3. **Per civ:**
   - If `MEM–RELEVANCE–<CIV>.md` exists under `research/repos/civilization_memory/content/civilizations/<CIV>/`, run `suggest_civ_mem_from_relevance.py <CIV>` (unless `--dry-run`).
   - If absent for **ROME**, list **ROME seeds** from config (Tier B until upstream adds `MEM–RELEVANCE–ROME.md`).
4. **`--expand-connections`** — Parse `MEM CONNECTIONS` in the **first** ROME seed file; list MEM ids (ROME-internal first, then others), capped by `max_cross_civ_edges`.
5. **`--bfs-mem-target N` (optional)** — If `N > 0`, run a **breadth-first** walk along **MEM CONNECTIONS** only. Visits distinct `MEM–*.md` files until `N` are collected or the queue / `--bfs-max-depth` is exhausted. Seeds = `theology_seed_mems` + profile merge of `rome_seed_files` when `merge_rome_bfs_seeds` is true (see `theology_ra_trace`) + optional `--bfs-seed-file` (one `CIV/MEM–….md` path per line). Neighbor fan-out per file: `--bfs-neighbors-per-hop` (default 24). **`--bfs-output PATH`** writes JSON (`visited`, `edges`, `civ_mem_HEAD`). Use `--bfs-no-rome-priority` to follow connection ids in document order instead of ROME-first.

Re-check **`tier_a_relevance_entities`** and filesystem inventory when bumping the `civilization_memory` submodule.

## When to use vs other tools

| Tool | Use when |
|------|----------|
| `route_civ_mem_topic.py` | Mixed geography / papacy / Islam–Christian encounter; need **ordered** civs and ROME-first discipline |
| `suggest_civ_mem_from_relevance.py <X>` | You already fixed **X** and a relevance spine exists |
| `build_civmem_upstream_index.py query` | Exploratory search without a routing prior |
| `route_civ_mem_topic.py` + `--bfs-mem-target` | Need **50+ MEM** file list along **graph edges** (theology / comparative lineage WORK) |

## Routing focus (forward-looking)

**Purpose:** Encode a **fortnight-scale prior** (e.g. “last 14 days’ strategy lanes stay hot next 14 days”) without editing the main routes file every day. Same **additive, integer** discipline as base overlap—easy to audit in git.

- **File:** [`config/civ_mem_routing_focus.yaml`](../../../config/civ_mem_routing_focus.yaml) — `focus_version`, `valid_from` / `valid_until` (UTC, inclusive; date-only means start/end of that calendar day in UTC), `profile_overlap_bonus`, `sticky_keywords`.
- **CLI:** `--focus-config PATH` (default: `config/civ_mem_routing_focus.yaml`), `--no-focus` to ignore the file (tests, A/B).
- **Stdout:** **Routing focus** section lists `focus_version`, validity window, whether any **non-zero** adjustment applied, and per-profile breakdown (`base` + `profile_bonus` + `sticky` → `effective`).
- **`--log-decision`:** JSONL rows gain `focus_version`, `focus_active`, `focus_applied` (true only if a non-zero bonus changed scores), `score_components` for the winning profile, `routing_fallback` when `default_profile` was used.

**Rollup (print-only):** After logging decisions, generate a pasteable snippet:

```bash
python3 scripts/suggest_routing_focus.py --days 14
```

Review the YAML comment header (`generated_from`, `modal_profile`, `rows_in_window`) before merging into `civ_mem_routing_focus.yaml`. Nothing writes focus YAML automatically.

**Cadence:** Rotate the validity window and bonuses after heavy strategy weeks; bump `focus_version` when the contract changes.

### Related patterns (not dependencies)

Industry tools use the same **building blocks** with different names: **search** stacks add **recency boosts** and **function scores** (e.g. Elasticsearch), **editorial elevation** for query-specific overrides (Apache Solr), **scheduled rules** on time windows (feature-flag products). This router stays **transparent**: additive integer overlap, human-edited YAML, no fused multiplicative scores.

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
