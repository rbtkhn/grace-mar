# Cadence pressure signals

**Machine artifact:** `artifacts/work-cadence/cadence-pressure-report.json` (via `audit_cadence_rhythm.py --pressure-report`).

## Signals (v1)

| Signal | Meaning |
|--------|---------|
| `cadence_drift` | Rhythm summary discipline is `DRIFT` |
| `high_gate_pending` | More than five `status: pending` substrings in recursion-gate.md |
| `high_coffee_volume` | Coffee event count > 25 in window (reorientation load) |

Extend as needed; keep definitions versioned alongside `schemaVersion` in JSON.

**Not** Record truth.
