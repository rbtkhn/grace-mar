# work-dev — gap classification

**Purpose:** Shared vocabulary for [known-gaps.md](known-gaps.md) and `artifacts/work-dev/known-gaps.json`.

## Severity (operator)

| Level | Meaning |
|-------|---------|
| **S0** | Safety / authority / provenance — fix before scaling agent scope |
| **S1** | Core operator workflow broken or misleading |
| **S2** | Missing polish; workaround exists |
| **S3** | Future / nice-to-have |

## Status (schema enum)

Maps to `known_gaps.schema.json`: `open`, `closed`, `planned`, `partial`.

## Remediation paths

- **Doc-only** — Clarify README; no code.
- **Script** — Add validator or logging.
- **Integration** — Touch bot / gate / external system.
