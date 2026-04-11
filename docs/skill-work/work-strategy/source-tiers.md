# work-strategy — source trust tiers

**Purpose:** Align **structured** sources ([authorized-sources.yaml](authorized-sources.yaml)) with **ingest** behavior ([daily-brief-config.json](daily-brief-config.json) feed `tier` 1–3).

**Not** Record truth. **WORK** lane hygiene only.

## Tier meanings

| Tier | Meaning | Typical use |
|------|---------|-------------|
| **1** | Primary data, primary docs, or methodology-heavy reference | Datasets (ACLED), official releases when used as fact source |
| **2** | Established outlets / analysis shops | Most daily brief rows, defense and foreign-affairs press |
| **3** | Long-tail, noisy, or auxiliary feeds | Higher duplication risk; cap in `ingest_caps` |

`trust_tier` in YAML is **review hygiene**, not epistemic score. Pair with **`bias_scope`** notes.

## Phased enforcement

1. **Warn** — `validate_work_strategy_sources.py` + optional `sync_strategy_sources.py --check` in CI advisory mode.
2. **Brief citation** — When daily briefs carry `source_ids: []` frontmatter (future), validate references exist in YAML.
3. **Strict** — Fail CI if outside-material briefs lack authorized id (operator opt-in).

See [WORK-LAYER-HARDENING-ROADMAP.md](../WORK-LAYER-HARDENING-ROADMAP.md).
