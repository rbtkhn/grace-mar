# Work-Dev Diagnostics Control Plane

Work-dev now contains a cluster of tools that keep fast iteration from
becoming agent sprawl, authority drift, or unverified capability claims.
This page maps that stack as a composition guide. It does **not** create
new authority, a new merge path, or a new agent.

## Stack

- **Doctrine Drift Radar** — current-state doctrine audit  
  See [../../doctrine-drift-radar.md](../../doctrine-drift-radar.md).
- **Counterfactual Fork Simulator** — scratch-only foresight before
  broad or authority-sensitive changes  
  See [../../counterfactual-fork-simulator.md](../../counterfactual-fork-simulator.md).
- **Agent Sprawl Control Plane** — registry and audit for agent-like
  surfaces  
  See [agent-sprawl-control-plane.md](agent-sprawl-control-plane.md).
- **Interface Artifact Protocol** — bounded doctrine for operator-facing
  generated views  
  See [interface-artifacts/README.md](interface-artifacts/README.md).
- **Workbench** — artifact execution and inspection loop  
  See [workbench/README.md](workbench/README.md).
- **Claim-Proof Standard** — proof bar before marking capabilities
  implemented  
  See [claim-proof-standard.md](claim-proof-standard.md).
- **Capability Contracts** — standardized integration/tool surface
  contract shape  
  See [control-plane/capability-contract-template.yaml](control-plane/capability-contract-template.yaml).
- **Sandbox Adapter Spec** — governance wrapper for sandbox execution
  surfaces  
  See [sandbox-adapter-spec.md](sandbox-adapter-spec.md).
- **Portable Emulation Contract** — authority-bounded export contract for
  foreign runtimes  
  See [../../portability/emulation/README.md](../../portability/emulation/README.md).

## How the stack composes

### New interface artifact

Interface Artifact Protocol -> Workbench -> Claim-Proof ->
Doctrine Drift Radar

Use this path when the change is a dashboard, visualizer, review
cockpit, or other generated operator-facing artifact. First bound the
artifact, then inspect its behavior, then decide whether any capability
claim now needs proof, then confirm the broader doctrine still holds.

### New agent or runtime surface

Agent Sprawl Control Plane -> Capability Contract -> Sandbox Adapter or
Portable Emulation -> Doctrine Drift Radar

Use this path when the change adds a harness, adapter, external runtime,
or automation surface. First confirm the repo actually needs a new
surface, then define the contract, then route the execution/export model
through the right bounded runtime doctrine, then check the whole repo
for drift.

### New proposal or broad change

Counterfactual Fork Simulator -> Doctrine Drift Radar -> gate review

Use this path when a change is broad, authority-sensitive, or likely to
touch multiple docs/scripts/surfaces. First ask what could go wrong,
then inspect the current state, then use the normal governed review
path.

### New claimed capability

Claim-Proof Standard -> tests / receipts / demos -> work-dev status

Use this path when a feature is being called implemented. The claim
needs proof artifacts; README prose alone is not enough.

## Decision table

| If you are doing this | Start here | Then run/check | Do not confuse with |
|---|---|---|---|
| Adding a new script | [../../counterfactual-fork-simulator.md](../../counterfactual-fork-simulator.md) if scope is broad; otherwise [../../doctrine-drift-radar.md](../../doctrine-drift-radar.md) | Doctrine Drift Radar, relevant tests, Claim-Proof if capability status changes | a successful script run is not by itself a merge or approval |
| Adding a new agent surface | [agent-sprawl-control-plane.md](agent-sprawl-control-plane.md) | Capability contract, sandbox or portable-emulation boundary, Doctrine Drift Radar | a new runtime surface is not automatically justified just because it can be built |
| Adding a generated UI or artifact | [interface-artifacts/README.md](interface-artifacts/README.md) | Workbench, then Claim-Proof if capability claims are affected | Workbench receipts are not evidence truth and artifacts are not Record |
| Adding an external runtime bridge | [../../portability/emulation/README.md](../../portability/emulation/README.md) or [sandbox-adapter-spec.md](sandbox-adapter-spec.md), depending on the runtime model | Capability contract, Agent Sprawl audit, Doctrine Drift Radar | foreign runtimes may propose; they may not merge |
| Marking a capability implemented | [claim-proof-standard.md](claim-proof-standard.md) | tests, receipts, verification runs, or demos | README prose alone is not proof |
| Reviewing a broad proposed change | [../../counterfactual-fork-simulator.md](../../counterfactual-fork-simulator.md) | Doctrine Drift Radar, then normal gate review | a counterfactual report is not approval |
| Debugging governance state | [../../doctrine-drift-radar.md](../../doctrine-drift-radar.md), [../../harness-replay.md](../../harness-replay.md), or [../../observability.md](../../observability.md) depending on the question | Gate Board, workflow observability, action receipts | generated reports are not the canonical source of truth |

## Non-goals

- not a new authority layer
- not a merge path
- not a replacement for tests
- not a replacement for human review
- not a new agent

The work-dev diagnostics control plane exists to keep iteration legible
and bounded. Governed merge remains the only path that updates canonical
Record.
