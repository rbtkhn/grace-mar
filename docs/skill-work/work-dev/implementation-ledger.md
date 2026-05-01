# work-dev — implementation ledger

**Purpose:** Narrative spine for **what is real** in the work-dev territory — complements machine JSON under `artifacts/work-dev/` and [known-gaps.md](known-gaps.md).

**Authority:** **Not** Record. Integration truth lives in docs + tests + scripts cited in [capability-registry.md](capability-registry.md).

## How to read this

1. **Operator gaps** — [known-gaps.md](known-gaps.md) is the lightweight human table for `GAP-WD-*` docs / ergonomics / authority-hardening follow-ups.
2. **Control-plane gaps** — `docs/skill-work/work-dev/control-plane/known_gaps.yaml` and the generated view under `generated/` retain historical `BUILD-AI-GAP-*` ids for integration reliability work such as tail scenarios, handback analysis, and autonomy tiers.
3. **Machine export** — `artifacts/work-dev/known-gaps.json` validates against [schemas/work_dev/known_gaps.schema.json](../../schemas/work_dev/known_gaps.schema.json); expand export coverage over time.
4. **Capabilities** — `artifacts/work-dev/capability-status.json` uses [integration_status.schema.json](../../schemas/work_dev/integration_status.schema.json); ids align with gap `related_integration_ids` where possible.
5. **Proof** — [claim-proof-standard.md](claim-proof-standard.md) + `proof_ledger` schema.

## Cadence

Update when closing gaps or changing integration posture — same session as JSON when possible.
