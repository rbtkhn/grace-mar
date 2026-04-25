# Diagnostics and Governance Tools

## Purpose

Grace-Mar uses multiple read-only or derived diagnostic tools to keep
recursive self-improvement bounded, inspectable, and human-governed.
These tools do not merge the Record, do not approve changes on their
own, and do not mutate canonical state simply by being run.

The core distinction is:

- **Current-state diagnostics** ask: "Is the repo already drifting or
  broken?"
- **Counterfactual diagnostics** ask: "Would this proposed change
  introduce drift or breakage?"
- **Artifact diagnostics** ask: "Does this generated artifact behave as
  claimed?"
- **Agent diagnostics** ask: "Are agent-like surfaces duplicating,
  escalating authority, or lacking receipts?"
- **Governance diagnostics** ask: "Are candidates, proposals, receipts,
  and gates visible enough for review?"

## Tool map

| Tool | Question it answers | Authority | Writes? | Typical command/path | Use when |
|------|----------------------|-----------|---------|----------------------|----------|
| **Doctrine Drift Radar** | Does the current repo violate stated doctrine? | read-only audit | no | [`doctrine-drift-radar.md`](doctrine-drift-radar.md), `python3 scripts/audit_doctrine_drift.py` | after adding scripts, schemas, authority language, or new runtime surfaces |
| **Counterfactual Fork Simulator** | Would a proposed future change introduce drift, contradiction, or follow-up work? | advisory / scratch-only | `artifacts/counterfactual-simulations/` only | [`counterfactual-fork-simulator.md`](counterfactual-fork-simulator.md), `python3 scripts/simulate_counterfactual_fork.py --proposal <file>` | before accepting broad or authority-sensitive changes |
| **Agent Sprawl Control Plane** | Are agent-like surfaces overlapping, unreceipted, or authority-confused? | read-only registry / audit | no | [`skill-work/work-dev/agent-sprawl-control-plane.md`](skill-work/work-dev/agent-sprawl-control-plane.md), `python3 scripts/work_dev/audit_agent_sprawl.py` | adding a new agent, runtime, harness, adapter, or automation surface |
| **Workbench** | Does a generated artifact run or behave under inspection? | artifact-behavior only | receipts / artifacts only | [`skill-work/work-dev/workbench/README.md`](skill-work/work-dev/workbench/README.md) | testing generated HTML, React, SVG, CLI, or script artifacts |
| **Interface Artifact Protocol** | Is this generated operator-facing artifact bounded and non-canonical? | WORK-only / derived artifact | metadata / artifacts only | [`skill-work/work-dev/interface-artifacts/README.md`](skill-work/work-dev/interface-artifacts/README.md) | creating dashboards, visualizers, review cockpits, or prototype views |
| **Portable Emulation Contract** | Can a foreign runtime emulate Grace-Mar without gaining merge authority? | read-only Record context; proposal-only return | exported bundle / proposal envelope only | [`portability/emulation/README.md`](portability/emulation/README.md) | exporting Grace-Mar behavior to external agents or runtimes |
| **Claim-Proof Standard** | Is a claimed capability supported by test, script, receipt, or demo? | capability-description audit | status / proof artifacts only | [`skill-work/work-dev/claim-proof-standard.md`](skill-work/work-dev/claim-proof-standard.md) | marking a feature implemented or capability-complete |
| **Observability** | Are proposals, statuses, validation results, touched surfaces, and stale reviews visible? | inspection only | reports only | [`observability.md`](observability.md) | reviewing governance state |
| **Workflow Observability** | Which workflows are expensive, stale, high-friction, or effective? | inspection only | workflow reports / events | [`workflow-observability.md`](workflow-observability.md) | improving process rather than content |
| **Gate Board** | What is pending, blocked, ready, approved, rejected, or merged? | generated view only | generated board | [`gate-board.md`](gate-board.md), `python3 scripts/build_gate_board.py` | reviewing gate queue state |
| **Harness Replay** | What audit context exists for a staged proposal, export, or event? | replay / inspection only | replay report | [`harness-replay.md`](harness-replay.md), `python3 scripts/replay_harness_event.py ...` | reconstructing what happened |
| **Action Receipts** | What happened during a meaningful operation? | audit trail only | receipt JSON / logs | [`action-receipts.md`](action-receipts.md) | making meaningful operations inspectable |
| **Context Budgeting** | What context was included, excluded, or escalated? | context-assembly receipt | budget receipts | [`runtime/context-budgeting.md`](runtime/context-budgeting.md), `python3 scripts/prepared_context/build_budgeted_context.py ...` | managing context depth and recovery |
| **Retrieval-Miss Ledger** | What did retrieval fail to surface? | retrieval-improvement log | miss ledger | [`retrieval-miss-ledger.md`](retrieval-miss-ledger.md), `python3 scripts/runtime/log_retrieval_miss.py ...` | search or context retrieval fails |

## Diagnostic selection guide

- Use **Doctrine Drift Radar** for current repo doctrine violations.
- Use **Counterfactual Fork Simulator** before accepting proposed
  changes.
- Use **Agent Sprawl Control Plane** before adding new agent-like
  surfaces.
- Use **Workbench** for generated executable or visual artifacts.
- Use **Interface Artifact Protocol** before creating operator-facing
  generated views.
- Use **Portable Emulation Contract** before exporting behavior to
  foreign runtimes.
- Use **Claim-Proof Standard** before declaring a capability
  implemented.
- Use **Observability**, **Gate Board**, and **Harness Replay** when
  reviewing governance state.

## Authority ladder

These tools sit on different authority rungs:

- **read-only audit** — inspects repo state and reports findings
- **advisory scratch report** — models possible consequences without
  approving them
- **derived artifact** — generated operator-facing view or bounded
  runtime output
- **receipt** — structured trace of what happened during an operation
- **proposal envelope** — durable-change suggestion that still requires
  governed review
- **gate candidate** — staged item awaiting human approval
- **approved merge** — the governed merge path that updates canonical
  Record

Only the governed merge path updates canonical Record.

## Common failure modes

- treating an advisory report as approval
- treating a Workbench receipt as evidence truth
- treating an interface artifact as Record
- letting a foreign runtime merge
- adding agents without a registry entry
- duplicating audit logic without linking it
- using generated dashboards as a source of truth
- ignoring retrieval misses
- allowing stale proposals to remain invisible

## Recommended default sequence for risky changes

For a risky change:

1. Run **Counterfactual Fork Simulator**
2. Run **Doctrine Drift Radar**
3. Run **Agent Sprawl audit**, if the change is agent- or
   runtime-related
4. Run **Workbench**, if the change is artifact-, script-, or UI-related
5. Apply **Claim-Proof**, if the capability claim changes
6. Route durable change through **gate review**

## Local deterministic diagnostics

```bash
python3 scripts/run_deterministic_diagnostics.py
```

Diagnostics help make review legible. They do not merge, do not approve,
and do not mutate canonical Record on their own.
