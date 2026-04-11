# Cadence ↔ governance bridge

**Purpose:** Connect **ritual telemetry** ([work-cadence-events.md](work-cadence-events.md)) with **governance pressure** (pending gate work) without confusing cadence with merge authority.

## Scripts

- [audit_cadence_rhythm.py](../../scripts/audit_cadence_rhythm.py) — rhythm summary (existing).
- **`--pressure-report`** — writes `artifacts/work-cadence/cadence-pressure-report.json`, combining rhythm + `status: pending` counts in [`users/grace-mar/recursion-gate.md`](../../../users/grace-mar/recursion-gate.md).

## Authority

**Cadence** does not approve candidates. **Companion** approves merges through **RECURSION-GATE** per [AGENTS.md](../../AGENTS.md). Pressure metrics are **diagnostic** only.

## See also

- [cadence-pressure-signals.md](cadence-pressure-signals.md)
- [WORK-LAYER-HARDENING-ROADMAP.md](../WORK-LAYER-HARDENING-ROADMAP.md)
