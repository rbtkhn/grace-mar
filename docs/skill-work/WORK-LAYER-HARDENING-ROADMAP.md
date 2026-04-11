# Work-layer hardening roadmap (grace-mar)

**Purpose:** Single **dependency order** for bringing WORK lanes closer to Record-adjacent discipline **without** changing companion merge authority. **Not** Record truth.

**Authority:** Promoted watches, decision recommendations, and lane metrics are **WORK artifacts**. **SELF / EVIDENCE / prompt** change only through **RECURSION-GATE** and companion approval ([AGENTS.md](../../AGENTS.md)).

## Recommended sequence

| Phase | Focus | Key artifacts |
|-------|--------|----------------|
| 1 | Strategy promotion + decision points | [promotion-ladder.md](work-strategy/promotion-ladder.md), [decision-points/](work-strategy/decision-points/), [watch-promotion-rules.md](work-strategy/watch-promotion-rules.md), [promotion-policy.json](work-strategy/promotion-policy.json); extend [decision-point-template.md](work-strategy/decision-point-template.md) |
| 2 | Sources machine legibility | [authorized-sources.yaml](work-strategy/authorized-sources.yaml), [source-tiers.md](work-strategy/source-tiers.md), `schemas/work_strategy/`, [validate_work_strategy_sources.py](../../scripts/validate_work_strategy_sources.py) |
| 3 | Strategy observability | [observability.md](work-strategy/observability.md), [strategy-health.md](work-strategy/strategy-health.md), `artifacts/work-strategy/strategy-observability.json`, [build_strategy_observability.py](../../scripts/build_strategy_observability.py) |
| 4 | work-dev implementation ledger | [implementation-ledger.md](work-dev/implementation-ledger.md), [capability-registry.md](work-dev/capability-registry.md), `artifacts/work-dev/` JSON aligned with [schemas/work_dev/](../../schemas/work_dev/) |
| 5 | Proof-backed claims | [claim-proof-standard.md](work-dev/claim-proof-standard.md), [verification-runs/](work-dev/verification-runs/), [verify_work_dev_claims.py](../../scripts/verify_work_dev_claims.py) |
| 6 | Cadence ↔ governance | [cadence-governance-bridge.md](work-cadence/cadence-governance-bridge.md), [cadence-pressure-signals.md](work-cadence/cadence-pressure-signals.md), `artifacts/work-cadence/cadence-pressure-report.json`, extends [audit_cadence_rhythm.py](../../scripts/audit_cadence_rhythm.py) |
| 7 | Lane contracts | [work-lane-contract.md](work-lane-contract.md), [work-lane-minimum-standard.md](work-lane-minimum-standard.md), [work-template/](work-template/), [validate_work_lane_contracts.py](../../scripts/validate_work_lane_contracts.py) |
| 8 | Work-lanes dashboard | [build_work_lanes_dashboard.py](../../scripts/build_work_lanes_dashboard.py), `artifacts/work-lanes-dashboard.json` (UI optional) |

## Cross-links

- Strategy synthesis stack: [strategy-notebook/SYNTHESIS-OPERATING-MODEL.md](work-strategy/strategy-notebook/SYNTHESIS-OPERATING-MODEL.md) (L4 promotion).
- work-modules sources principle: [work-modules-sources-principle.md](work-modules-sources-principle.md).
