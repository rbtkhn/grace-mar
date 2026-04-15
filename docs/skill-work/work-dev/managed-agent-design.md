# Managed Agent Design (Think lane)

**Territory:** work-dev
**Status:** Design — not governance, not Record, not AGENTS.md amendment
**Date:** 2026-04-14

---

## Problem

Grace-Mar already supports operator-supervised AI assistants through the WORK execution layer (Cursor agents, OpenClaw headless mode, pipeline scripts). These are session-scoped: they start when the operator opens a thread, they end when the thread closes, and state lives in files.

The system does not yet have an explicit lifecycle model for agents that **persist across sessions** — email orchestrators, research monitors, scheduled digest builders, overnight data ingestion loops. These exist in the ecosystem today and will become routine. Without a lifecycle model, they will arrive as ad-hoc scripts with no governance envelope, receipt trail, or shutdown discipline.

This document scopes what "managed agent" means in this system's terms and maps it onto existing primitives. It does **not** create new governance surfaces, modify AGENTS.md, or assume multi-agent fleet orchestration.

---

## Existing coverage

The repo already has substantial agentic infrastructure. A managed-agent lifecycle should **use** these primitives, not duplicate them.

| Primitive | File | What it provides |
|-----------|------|------------------|
| Authority classes | [sandbox-adapter-spec.md](sandbox-adapter-spec.md) | Three tiers: `operator`, `agent_supervised`, `agent_autonomous` — with escalation rules, receipt emission, and Record-access controls |
| Environment principles | [agentic-environment-principles.md](agentic-environment-principles.md) | Debug order (environment before prompt), bounded execution (§5b), pipeline discipline (§5c: local memory is not the Record) |
| Agent surface template | [agent-surface-template.yaml](agent-surface-template.yaml) | Structured evaluation: runtime placement, orchestration, interface, Grace-Mar trust fields, `agent_species` |
| Runtime-vs-Record boundary | [runtime-vs-record.md](../../runtime-vs-record.md) | Canonical map: what is governed (SELF, SKILLS, EVIDENCE, SELF-LIBRARY) vs runtime-only (session paste, MEMORY, skill cards, observations ledger) |
| Governance unbundling | [governance-unbundling.md](../../governance-unbundling.md) | Routing (automatable) vs sensemaking (human) vs accountability (human) — agents may route; they may not sense-make or merge |
| Gated pipeline | [AGENTS.md](../../../AGENTS.md) §2 | Sovereign merge rule: stage to recursion-gate, companion approves, `process_approved_candidates.py --apply` |
| Compute ledger | [sandbox-adapter-spec.md](sandbox-adapter-spec.md) §Data shapes | Per-invocation cost and outcome tracking via `append_integration_ledger()` |
| Conceptual invariants | [conceptual-framework.md](../../conceptual-framework.md) §8, invariant 38 | WORK execution is instrumental (not a fourth triad seat); reactive now, agentic later; extra guardrail design required for agentic capabilities |

**What is missing:** An explicit lifecycle (spin-up → observe → pause → shutdown) and an operator runbook that ties these primitives together for persistent agents.

---

## Terminology

| This document says | Not this | Why |
|--------------------|----------|-----|
| managed agent | lobster, autonomous agent | "Managed" signals operator control; "autonomous" implies independence the system does not grant |
| work agent | agent with rights | Agents are WORK execution layer tools ([AGENTS.md](../../../AGENTS.md), [conceptual-framework.md](../../conceptual-framework.md) §8); they do not hold identity claims or governance standing |
| operator runbook | bill of rights / agent contract | Operational discipline is a human responsibility, not an agent entitlement |
| lifecycle | personhood / identity continuity | Agents have a lifecycle (create, run, pause, stop); they do not have identity continuity in the system's sense |

---

## Proposed lifecycle

A managed agent follows five phases. Each phase maps to an existing primitive.

```
Create ──► Run ──► Observe ──► Propose ──► Approve
  │          │        │           │           │
  ▼          ▼        ▼           ▼           ▼
manifest   sandbox   runtime    gate.md     merge
(YAML)    adapter    logs      (YAML)      script
```

### 1. Create

The operator fills out an `agent-surface-template.yaml` manifest for the agent, selecting:

- **`agent_species`** — one of the four existing values (`coding_harness`, `dark_factory`, `auto_research`, `workflow_orchestration`)
- **`runtime.placement`** — where the agent runs (local, cloud, hybrid)
- **`grace_mar.merge_requires_companion_gate`** — always `true` for managed agents
- **Purpose statement** — a concrete, documented reason for spinning up this agent (what WORK territory it serves, what it produces, how long it should run)

The manifest lives in the WORK territory and is **not** a Record artifact.

### 2. Run

The agent executes under one of the sandbox-adapter authority classes:

- **`agent_supervised`** — operator is in the loop; receipts reviewed post-hoc. Typical for Cursor agents, session-scoped helpers.
- **`agent_autonomous`** — restricted to pre-approved task types; no Record write; timeout enforced; receipts auto-flagged for review. Typical for overnight monitors, scheduled digest builders.

Every invocation produces a `SandboxReceipt` per the adapter spec. Cost rows append to the compute ledger.

### 3. Observe

Agent output stays **runtime-only** until explicitly staged:

- Logs → `runtime/observability/*.jsonl` (existing feed)
- Artifacts → WORK territory (e.g. `docs/skill-work/work-dev/agent-output/`)
- State files → agent-local storage (not the Record, not MEMORY)

Per [runtime-vs-record.md](../../runtime-vs-record.md): nothing produced by the agent is Record truth. Agent memory, caches, and intermediate state are runtime artifacts — rebuildable, prunable, not governed.

### 4. Propose

When an agent produces something worth preserving (a research finding, a capability observation, a draft artifact), the operator or a routing script stages it to `recursion-gate.md` using the standard YAML schema:

```yaml
### CANDIDATE-NNNN (agent output — [description])
status: pending
timestamp: YYYY-MM-DDTHH:MM:SSZ
channel_key: managed-agent
source: agent:[agent-name]
mind_category: IX-A | IX-B | IX-C
signal_type: knowledge | curiosity | personality
summary: [one line]
profile_target: [self.md section or self-archive.md]
suggested_entry: |
  [content]
```

The `channel_key: managed-agent` tag distinguishes agent-originated proposals from session, Telegram, or operator sources. The pipeline handles them identically.

### 5. Approve

Companion reviews and approves via the existing gate process. `process_approved_candidates.py --apply` merges. No special path for agent-originated candidates — same gate, same script, same companion authority.

---

## Operator runbook

Operational discipline for managed agents. These are **operator responsibilities**, not agent properties.

### Before spin-up

- [ ] Purpose documented in the manifest (what, why, how long, which WORK territory)
- [ ] Authority class selected (`agent_supervised` or `agent_autonomous`)
- [ ] Sandbox backend chosen and healthy (`health()` check passes)
- [ ] Compute budget estimated (cost ceiling in the ledger)
- [ ] Observability feed confirmed (JSONL path exists, dashboard accessible)

### During operation

- [ ] Receipts accumulating in `pipeline-events.jsonl` or `sandbox-receipts.jsonl`
- [ ] Compute ledger rows within budget
- [ ] No Record access beyond declared `record_access` level
- [ ] Periodic operator review of output artifacts (cadence depends on agent species)

### Pause

- [ ] Agent halted cleanly (no orphaned processes or connections)
- [ ] State files preserved (not deleted until explicitly retired)
- [ ] Summary of work-to-date written to WORK territory

### Shutdown

- [ ] Final summary log: what the agent accomplished, open questions, suggested follow-ups
- [ ] State files archived or deleted per operator judgment
- [ ] Compute ledger reconciled (total cost, total invocations, outcome quality)
- [ ] Any valuable output staged to recursion-gate or archived in WORK territory
- [ ] Manifest updated with shutdown date and reason

---

## What this does NOT do

- **Does not create a governance contract.** Agents do not have "rights" or "obligations" in the governance sense. They have operational requirements managed by the operator.
- **Does not modify AGENTS.md.** Layer 1 doctrine is unchanged. Agents remain the WORK execution layer.
- **Does not modify the recursion-gate template.** The existing YAML schema handles agent-originated proposals via `channel_key: managed-agent`.
- **Does not assume multi-agent fleet orchestration.** Per [sandbox-adapter-spec.md](sandbox-adapter-spec.md) principle 5: companion-scale first. Multi-agent coordination is deferred until the single-companion case is proven.
- **Does not grant agents identity continuity.** When an agent is forked, reset, or replaced, there is no obligation to carry forward "personality" or "learned capabilities." State preservation is an operator backup decision, not an agent right.
- **Does not position agents as triad members.** [Conceptual-framework.md](../../conceptual-framework.md) §8 is explicit: WORK execution is instrumental, not a fourth part of Mind + Record + Voice.

---

## Prerequisites before formalization

This design doc is a Think-lane artifact. Before it becomes a portable skill or formal spec:

1. **Single-companion case proven** — at least one real managed agent running under this lifecycle for >1 week, with receipts, ledger rows, and operator review.
2. **Boundary stress-test** — confirm that `agent_autonomous` authority class + existing observability feeds are sufficient for overnight/unattended operation.
3. **Operator feedback** — runbook tested in practice; gaps identified and patched.
4. **Discovery ladder entry** — when prerequisites 1–3 are met, add a row to `skills-portable/skill-candidates.md` pointing here.
5. **Eventual portable skill** — if the lifecycle proves repeatable, extract a `SKILL.md` via the standard discovery ladder.

---

## Steward review — boundary coherence

_Findings from a read-only pass across the four existing agentic governance surfaces, checking whether the managed-agent lifecycle exposes gaps or tensions._

### 1. conceptual-framework.md — invariant 38 + section 8

**Status: Holds.**

Invariant 38 ("reactive now, agentic later") distinguishes two meanings of "agentic": (1) WORK execution layer (in scope today), (2) agentic Voice (roadmap). Managed agents are squarely type (1) — they are WORK execution, not Voice. The invariant does not need updating; it already anticipates this use case.

Section 8's disambiguation is clear: "Do not conflate skill-work execution with agentic Voice." A managed agent running email digests is skill-work execution, not a Voice modality. The triad (Mind + Record + Voice) is not disturbed.

The status language guidance ("process microcopy must not anthropomorphize WORK execution") applies directly: managed-agent logs should say "agent completed task" not "agent decided" or "agent wants."

**Follow-up:** None required. The existing framing accommodates managed agents without modification.

### 2. sandbox-adapter-spec.md — authority classes + principle 5

**Status: Holds, with one minor observation.**

The three authority classes (`operator`, `agent_supervised`, `agent_autonomous`) map cleanly to managed-agent scenarios:

- Session-scoped helper → `agent_supervised`
- Overnight monitor → `agent_autonomous`
- Operator-driven ad-hoc → `operator`

Principle 5 ("companion-scale first; multi-agent fleet orchestration out of scope until single-companion case is proven") is the correct gate. The managed-agent lifecycle does not require fleet orchestration — it describes one agent at a time under one companion's authority.

**Observation:** The `agent_autonomous` class currently says "restricted to pre-approved task_types; no Record write; timeout enforced." For long-running agents (e.g. an overnight research monitor that runs for 8 hours), the `timeout_ms` field in `SandboxRequest` may need a "heartbeat" variant rather than a single wall-clock ceiling. This is a future implementation detail, not a spec gap — the spec already says "0 = backend default" which can accommodate long-running processes.

**Follow-up:** When the first real `agent_autonomous` long-running agent is deployed, confirm that timeout handling works for multi-hour processes. Add to `workspace.md` next actions if needed at that point.

### 3. agentic-environment-principles.md — sections 4 and 5

**Status: Holds.**

Section 4 ("resist agent mesh envy") directly applies. The managed-agent lifecycle intentionally avoids mesh topology — it is one agent, one operator, one gate. The section's framing ("highest-leverage moves stay boring: gate hygiene, continuity contract, lane scope, dashboard") describes exactly what the operator runbook covers.

Section 5's three operator rules (a: explicit data residency + role split; b: bounded execution for anything touching the repo; c: pipeline discipline — local memory is not the Record) all apply without modification to managed agents. Rule (c) is especially relevant: agent memory, caches, and state files are runtime artifacts, not Record truth.

**Follow-up:** When this design doc is committed, add a one-line cross-reference from `agentic-environment-principles.md` §Cross-references to `managed-agent-design.md`. This is a pointer, not a governance change.

### 4. agent-surface-template.yaml — agent_species

**Status: Holds.**

The four existing species cover managed-agent use cases:

| Use case | Species |
|----------|---------|
| Email orchestrator | `workflow_orchestration` |
| Research monitor | `auto_research` |
| Overnight data ingest | `dark_factory` |
| Cursor-supervised helper | `coding_harness` |

No new species value is needed. The template's Grace-Mar trust fields (`record_authority`, `staging_surface`, `merge_requires_companion_gate`, `continuity_contract`, `observability`) are sufficient to describe a managed agent's governance posture.

**Follow-up:** None required. If a genuinely novel agent pattern emerges that does not fit any species, that is the signal to extend — not before.

---

## Cross-references

- [sandbox-adapter-spec.md](sandbox-adapter-spec.md) — authority classes, receipts, compute ledger
- [agentic-environment-principles.md](agentic-environment-principles.md) — environment-first, bounded execution, pipeline discipline
- [agent-surface-template.yaml](agent-surface-template.yaml) — structured evaluation template
- [runtime-vs-record.md](../../runtime-vs-record.md) — canonical vs runtime boundary
- [governance-unbundling.md](../../governance-unbundling.md) — routing vs sensemaking vs accountability
- [conceptual-framework.md](../../conceptual-framework.md) — triad, invariant 38, §8 disambiguation
- [workspace.md](workspace.md) — work-dev operator entrypoint

---

## Revision log

| Date | Change |
|------|--------|
| 2026-04-14 | Initial design doc from managed-agent proposal analysis. Think lane; not governance. |
