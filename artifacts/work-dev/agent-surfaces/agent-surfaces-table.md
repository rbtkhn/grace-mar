# Agent Surfaces Table

Generated from `config/agent-surfaces.v1.json`.

This table is derived from the machine-readable Agent Sprawl Control Plane registry.
The JSON registry remains authoritative.
This table is not Record, not approval, not a merge path, and grants no authority.

## Summary

- Total surfaces: 10
- Implemented: 7
- Partial: 2
- Documented-only: 1
- Planned: 0
- Surfaces requiring receipts: 7
- Surfaces with capability contracts: 4
- Surfaces with merge authority: 0

## Surfaces

| ID | Name | Status | Category | Owner lane | Canonical Record access | Merge authority | Gate effect | Receipt required | Capability contract | Reads | Writes | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| auto-research | Auto-research swarm bridge | partial | auto_research | work-dev | none | none | none | true | — | auto-research/self-proposals/accepted/ <br> auto-research/swarm/ | auto-research/swarm/swarm-state.json <br> derived debate artifacts <br> shared artifact promotion path | Grounded in auto-research/swarm/README.md; partial operator-facing swarm bridge that reuses existing promotion helpers. |
| counterfactual-fork-simulator | Counterfactual Fork Simulator | implemented | read_only_audit | work-dev | read-only | none | advisory-only | false | — | repo working tree <br> proposal-like JSON input | artifacts/counterfactual-simulations/ | Grounded in docs/counterfactual-fork-simulator.md; advisory scratch-only simulation, not staging or merge. |
| doctrine-drift-radar | Doctrine Drift Radar | implemented | read_only_audit | work-dev | read-only | none | advisory-only | false | — | repo working tree <br> config/doctrine-rules.v1.json | — | Grounded in docs/doctrine-drift-radar.md; current-state doctrine audit only. |
| external-agent-delegation | External outcome-agent delegation | documented_only | delegation_protocol | work-dev | none | none | none | false | — | exports <br> warmup digests <br> operator task spec | WORK artifacts <br> gate candidates via existing shared paths | Grounded in docs/skill-work/work-dev/delegation-spec-external-agents.md; delegation policy, not a standalone governed integration. |
| interface-artifacts | Interface Artifact Protocol | implemented | interface_artifact_generator | work-dev | none | none | none | true | — | strategy-notebook markdown <br> lane docs <br> artifact metadata | artifacts/work-dev/interface-artifacts/ <br> artifacts/work-strategy/strategy-notebook/ | Grounded in docs/skill-work/work-dev/interface-artifacts/README.md; derived operator-facing surfaces only. |
| openclaw-export | OpenClaw identity export | implemented | external_runtime | work-dev | read-only | none | none | true | docs/skill-work/work-dev/control-plane/capability-contract-openclaw-export.yaml | users/[id]/SELF.md <br> users/[id]/EVIDENCE/ <br> users/[id]/session-log.md <br> users/[id]/INTENT.md | users/[id]/openclaw-user.md <br> users/[id]/runtime-bundle/ <br> users/[id]/intent_snapshot.json <br> pipeline-events.jsonl <br> harness-events.jsonl <br> users/[id]/compute-ledger.jsonl | Grounded in docs/openclaw-integration.md and the OpenClaw export capability contract. |
| openclaw-stage | OpenClaw stage-only handback | implemented | external_handback_agent | work-dev | none | none | stage-only | true | docs/skill-work/work-dev/control-plane/capability-contract-openclaw-stage.yaml | runtime/continuity/receipts/ <br> users/[id]/INTENT.md | users/[id]/recursion-gate.md <br> pipeline-events.jsonl <br> harness-events.jsonl <br> users/[id]/compute-ledger.jsonl | Grounded in docs/openclaw-integration.md and the OpenClaw stage-only capability contract. |
| portable-emulation | Portable emulation bundle surface | partial | portable_emulation_runtime | work-dev | read-only | none | none | true | docs/portability/emulation/README.md | users/[id]/SELF.md <br> users/[id]/EVIDENCE/ <br> users/[id]/SKILLS/ <br> users/[id]/INTENT.md | artifacts/portability/emulation/ | Grounded in docs/portability/emulation/README.md and behavior-spec docs; bounded export surface, not a merge path. |
| sandbox-adapter | Sandbox adapter layer | implemented | sandbox_adapter | work-dev | read-only | none | none | true | docs/skill-work/work-dev/control-plane/capability-contract-sandbox-dry-run.yaml | repo working tree <br> files_in hashes <br> sandbox requests | pipeline-events.jsonl <br> users/[id]/compute-ledger.jsonl | Grounded in docs/skill-work/work-dev/sandbox-adapter-spec.md and sandbox capability contracts; governance wrapper, not a merge path. |
| workbench | Workbench Harness | implemented | workbench_runner | work-dev | none | none | none | true | — | artifacts/work-dev/interface-artifacts/ <br> artifacts/work-strategy/strategy-notebook/ <br> repo working tree | artifacts/work-dev/workbench-receipts/ <br> artifacts/work-dev/workbench-screenshots/ | Grounded in docs/skill-work/work-dev/workbench/README.md; inspection layer for generated artifacts, not a merge path. |
