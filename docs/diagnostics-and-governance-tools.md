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

### Doctrine Drift Radar

- **Question:** Does the current repo violate stated doctrine?
- **Authority:** read-only audit
- **Writes:** no
- **Typical command/path:** [`doctrine-drift-radar.md`](doctrine-drift-radar.md),
  `python3 scripts/audit_doctrine_drift.py`
- **Use when:** after adding scripts, schemas, authority language, or new
  runtime surfaces

### Counterfactual Fork Simulator

- **Question:** Would a proposed future change introduce drift,
  contradiction, or follow-up work?
- **Authority:** advisory / scratch-only
- **Writes:** `artifacts/counterfactual-simulations/` only
- **Typical command/path:**
  [`counterfactual-fork-simulator.md`](counterfactual-fork-simulator.md),
  `python3 scripts/simulate_counterfactual_fork.py --proposal <file>`
- **Use when:** before accepting broad or authority-sensitive changes

### Agent Sprawl Control Plane

- **Question:** Are agent-like surfaces overlapping, unreceipted, or
  authority-confused?
- **Authority:** read-only registry / audit
- **Writes:** no
- **Typical command/path:**
  [`skill-work/work-dev/agent-sprawl-control-plane.md`](skill-work/work-dev/agent-sprawl-control-plane.md),
  `python3 scripts/work_dev/audit_agent_sprawl.py`
- **Use when:** adding a new agent, runtime, harness, adapter, or
  automation surface
- **Operator scan:** use the generated Agent Surfaces Table
  (`python3 scripts/work_dev/render_agent_surfaces_table.py`) for a readable
  inventory; the JSON registry and `audit_agent_sprawl.py` remain authoritative
  for surface semantics and authority.

### Workbench

- **Question:** Does a generated artifact run or behave under inspection?
- **Authority:** artifact-behavior only
- **Writes:** receipts / artifacts only
- **Typical command/path:**
  [`skill-work/work-dev/workbench/README.md`](skill-work/work-dev/workbench/README.md)
- **Use when:** testing generated HTML, React, SVG, CLI, or script artifacts

### Interface Artifact Protocol

- **Question:** Is this generated operator-facing artifact bounded and
  non-canonical?
- **Authority:** WORK-only / derived artifact
- **Writes:** metadata / artifacts only
- **Typical command/path:**
  [`skill-work/work-dev/interface-artifacts/README.md`](skill-work/work-dev/interface-artifacts/README.md)
- **Use when:** creating dashboards, visualizers, review cockpits, or
  prototype views

### Portable Emulation Contract

- **Question:** Can a foreign runtime emulate Grace-Mar without gaining
  merge authority?
- **Authority:** read-only Record context; proposal-only return
- **Writes:** exported bundle / proposal envelope only
- **Typical command/path:**
  [`portability/emulation/README.md`](portability/emulation/README.md)
- **Use when:** exporting Grace-Mar behavior to external agents or runtimes

### Claim-Proof Standard

- **Question:** Is a claimed capability supported by test, script, receipt,
  or demo?
- **Authority:** capability-description audit
- **Writes:** status / proof artifacts only
- **Typical command/path:**
  [`skill-work/work-dev/claim-proof-standard.md`](skill-work/work-dev/claim-proof-standard.md)
- **Use when:** marking a feature implemented or capability-complete

### Observability

- **Question:** Are proposals, statuses, validation results, touched
  surfaces, and stale reviews visible?
- **Authority:** inspection only
- **Writes:** reports only
- **Typical command/path:** [`observability.md`](observability.md)
- **Use when:** reviewing governance state

### Workflow Observability

- **Question:** Which workflows are expensive, stale, high-friction, or
  effective?
- **Authority:** inspection only
- **Writes:** workflow reports / events
- **Typical command/path:** [`workflow-observability.md`](workflow-observability.md)
- **Use when:** improving process rather than content

### Gate Board

- **Question:** What is pending, blocked, ready, approved, rejected, or
  merged?
- **Authority:** generated view only
- **Writes:** generated board
- **Typical command/path:** [`gate-board.md`](gate-board.md),
  `python3 scripts/build_gate_board.py`
- **Use when:** reviewing gate queue state

### Harness Replay

- **Question:** What audit context exists for a staged proposal, export, or
  event?
- **Authority:** replay / inspection only
- **Writes:** replay report
- **Typical command/path:** [`harness-replay.md`](harness-replay.md),
  `python3 scripts/replay_harness_event.py ...`
- **Use when:** reconstructing what happened

### Action Receipts

- **Question:** What happened during a meaningful operation?
- **Authority:** audit trail only
- **Writes:** receipt JSON / logs
- **Typical command/path:** [`action-receipts.md`](action-receipts.md)
- **Use when:** making meaningful operations inspectable

### Context Budgeting

- **Question:** What context was included, excluded, or escalated?
- **Authority:** context-assembly receipt
- **Writes:** budget receipts
- **Typical command/path:** [`runtime/context-budgeting.md`](runtime/context-budgeting.md),
  `python3 scripts/prepared_context/build_budgeted_context.py ...`
- **Use when:** managing context depth and recovery

### Retrieval-Miss Ledger

- **Question:** What did retrieval fail to surface?
- **Authority:** retrieval-improvement log
- **Writes:** miss ledger
- **Typical command/path:** [`retrieval-miss-ledger.md`](retrieval-miss-ledger.md),
  `python3 scripts/runtime/log_retrieval_miss.py ...`
- **Use when:** search or context retrieval fails

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

For the shared vocabulary behind repeated authority fields, see
[`authority-values.md`](authority-values.md).

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
