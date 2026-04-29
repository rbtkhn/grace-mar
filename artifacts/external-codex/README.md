# External codex neighborhood (`artifacts/external-codex/`)

**Derived WORK receipts** — structural adjacency around a path inside a checked-out external codex (default: `research/repos/civilization_memory`). **Not** Record truth, **not** upstream canon.

## SSOT

- **Doc:** [`docs/skill-work/work-dev/external-codex-explorer.md`](../../docs/skill-work/work-dev/external-codex-explorer.md)
- **Schema:** [`schema-registry/external-codex-neighborhood-report.v1.json`](../../schema-registry/external-codex-neighborhood-report.v1.json)
- **Builder:** [`scripts/build_external_codex_neighborhood.py`](../../scripts/build_external_codex_neighborhood.py)

## JSON vs Markdown companion

| Artifact | Role |
|----------|------|
| **`{stem}.json`** | Machine-readable report: `neighbors` (with `reason`, `section`, …), `likely_family`, `suggested_next_inspection`, optional `subject_title`. Stable for scripts and tests. |
| **`{stem}.neighborhood.md`** | Human-readable companion (same run; **`--write-md`**). Same deterministic facts; grouped headings for scanning. **Not** a second source of truth—regenerate from the builder when in doubt. |

Default outputs under this bucket root are typically **gitignored**; committed **`examples/`** holds illustrative JSON + Markdown only.

## Policy

- Regenerate after checkout updates when you care about freshness.
- **Do not** treat either artifact as canonical for the external repo—upstream governance wins.
