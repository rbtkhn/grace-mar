# External codex explorer (`artifacts/external-codex/`)

**Derived WORK receipts** — structural maps over a checked-out external codex (default: `research/repos/civilization_memory`). **Not** Record truth, **not** upstream canon.

## Neighborhood vs family

| Mode | Question | Default output folder | Builder |
|------|-----------|------------------------|---------|
| **Neighborhood** | What sits **adjacent** to **one** subject path? | `artifacts/external-codex/` (flat JSON / `.neighborhood.md`) | [`scripts/build_external_codex_neighborhood.py`](../../scripts/build_external_codex_neighborhood.py) |
| **Family** | What **cluster** of files matches a **selector** (`civilization`, `file_class`), and how do members link **within** that cluster? | `artifacts/external-codex/families/` | [`scripts/build_external_codex_family_report.py`](../../scripts/build_external_codex_family_report.py) |

Shared deterministic helpers live in [`scripts/external_codex_common.py`](../../scripts/external_codex_common.py).

## SSOT

- **Doc:** [`docs/skill-work/work-dev/external-codex-explorer.md`](../../docs/skill-work/work-dev/external-codex-explorer.md)
- **Schemas:** [`schema-registry/external-codex-neighborhood-report.v1.json`](../../schema-registry/external-codex-neighborhood-report.v1.json), [`schema-registry/external-codex-family-report.v1.json`](../../schema-registry/external-codex-family-report.v1.json)
- **Builders:** neighborhood and family scripts as above

## JSON vs Markdown companions

| Artifact | Role |
|----------|------|
| **`{stem}.json`** | Machine-readable report (neighborhood or family schema). Stable for scripts and tests. |
| **Neighborhood:** **`{stem}.neighborhood.md`** | Human-readable companion (`--write-md`). Same deterministic facts as JSON. |
| **Family:** **`{stem}.family.md`** | Human-readable companion (`--write-md`). |

Default generated outputs under `artifacts/external-codex/` (including nested **`families/`** / **`neighborhood/`** when used) are typically **gitignored**; committed **`examples/`** holds illustrative JSON + Markdown only.

## Policy

- Regenerate after checkout updates when you care about freshness.
- **Do not** treat either artifact as canonical for the external repo—upstream governance wins.
