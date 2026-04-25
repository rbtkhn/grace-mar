# Agent Sprawl Control Plane

**Status:** read-only audit and registry layer for work-dev.

## Definition

Agent Sprawl Control Plane is a registry and audit layer for agent-like
surfaces already present in Grace-Mar. Its job is not to create new
agents. Its job is to make existing or planned surfaces legible enough
to ask:

- do we already have something that does this
- do two surfaces overlap unnecessarily
- does this surface have a receipt trail
- does this surface have a capability contract
- does this surface imply authority it should not have

The control plane is therefore **inventory first, governance second, expansion last**.

## Why agent sprawl matters

More agents are not automatically more intelligence.

Uncontrolled agent multiplication creates:

- duplicated state
- repeated tool calls
- overlapping write paths
- rising cost without clear gain
- receipt gaps
- authority confusion
- doctrine drift

Grace-Mar should prefer governed routing, capability contracts,
receipts, and clear authority boundaries over unconstrained runtime
proliferation.

## What counts as an agent surface

For this control plane, an **agent surface** is any repo-described
surface that behaves like an agent, runtime, delegator, or
operator-facing execution wrapper.

This includes:

- coding harness
- external runtime
- bot
- workflow orchestrator
- auto-research process
- sandboxed execution backend
- portable emulation runtime
- interface artifact generator
- workbench runner
- external handback agent
- read-only audit or simulator surfaces that shape governance decisions

## What does not count

These are adjacent, but not agent surfaces by themselves:

- canonical Record files
- `recursion-gate.md`
- EVIDENCE entries
- one-off markdown notes
- raw exported artifacts without a runtime or orchestration role
- ordinary scripts that do not expose an ongoing surface, delegation wrapper, or agent-like control loop

## Authority model

The control plane does not create authority. It records and audits authority that other surfaces already claim.

Phase 1 assumptions:

- canonical Record write authority must never be granted to an agent surface
- merge authority must remain `none`
- stage effects must stay explicit (`none`, `stage-only`, or `advisory-only`)
- receipts should exist for implemented and partial surfaces unless the surface is a pure read-only audit
- capability contracts should exist for implemented and partial
  integrations unless a registry row explicitly marks a narrow exemption

## Registry fields

Each registry row records:

- `id`
- `name`
- `status`
- `category`
- `reads`
- `writes`
- `canonical_record_access`
- `merge_authority`
- `gate_effect`
- `receipt_required`
- `capability_contract`
- `owner_lane`
- `notes`

Phase 1 also permits narrow optional fields:

- `receipt_required_exempt` — explicit escape hatch for surfaces that
  are intentionally inventoried before a receipt policy is in place
- `capability_contract_exempt` — explicit escape hatch for surfaces
  that are intentionally tracked without a capability contract yet

## Audit checks

The Phase 1 audit checks for:

- duplicate ids
- missing required fields
- invalid status/category values
- `merge_authority != none`
- invalid `canonical_record_access`
- invalid `gate_effect`
- implemented/partial non-audit surfaces without `receipt_required: true`
- implemented/partial integrations missing a capability contract unless explicitly exempt
- multiple surfaces in the same category writing to overlapping paths

Overlapping writes are a **warning**, not an automatic failure. The
point is to surface sprawl and duplication risk early.

## Failure modes

- duplicated surfaces drift apart while claiming the same role
- two runtimes can write or stage through overlapping paths without a clear owner
- tool access exists without receipts
- an implemented surface is live but undocumented in contracts
- advisory tooling is mistaken for execution authority
- merge authority or Record authority leaks into agent surfaces
- category proliferation hides that three wrappers are doing the same job

## Recommended actions

Recommended action vocabulary for the control plane:

- `keep`
- `consolidate`
- `route-through-existing`
- `add-capability-contract`
- `add-receipt`
- `restrict-authority`
- `sandbox`
- `retire`
- `needs-review`

These are operator recommendations, not automatic actions.

## Relationship to existing surfaces

### `agent-surface-template.yaml`

The template defines comparison axes for runtime placement,
orchestration, interface channels, and Grace-Mar trust fields. The
sprawl control plane is narrower: it turns those judgments into a small
registry and audit layer.

### Capability contracts

Capability contracts are the strongest machine-readable statement of
what an integration promises. The sprawl registry should point at them
whenever a surface is implemented or partial.

### Portable emulation

Portable emulation is a bounded runtime surface. The control plane
tracks it as a runtime class that must stay non-authoritative and
non-merging.

### Interface artifacts

Interface artifacts are WORK-only derived surfaces. The control plane
tracks them because they can still create sprawl when multiple artifact
generators overlap or begin implying more authority than they possess.

### Workbench

Workbench is an inspection and receipt layer, not a merge path. The
control plane tracks it as a runner/audit-adjacent surface whose
receipts are about artifact behavior, not Record truth.

### Doctrine Drift Radar

Doctrine Drift Radar asks whether the current repo already violates
boundary doctrine. Agent Sprawl Control Plane asks whether the surface
inventory itself is becoming redundant, under-receipted, or
authority-confused.

### Counterfactual Fork Simulator

Counterfactual Fork Simulator is advisory foresight for proposed
changes. Agent Sprawl Control Plane is inventory and overlap control for
current/planned surfaces. One is about hypothetical consequence; the
other is about control-plane hygiene.

### External-agent delegation

External-agent delegation defines how to hand work to outside outcome
agents without confusing their memory or outputs with Record truth. The
control plane turns those surfaces into auditable rows.

### OpenClaw integration

OpenClaw export and OpenClaw stage are already the clearest examples of
why this layer matters: one surface exports, another stages, both emit
receipts, neither may merge.

## Phase 1 posture

This is read-only control-plane work.

It does **not**:

- create new agents
- orchestrate agents
- auto-consolidate surfaces
- modify canonical Record files
- modify `recursion-gate.md`

It only inventories, classifies, and audits the surfaces Grace-Mar already has or already describes.
