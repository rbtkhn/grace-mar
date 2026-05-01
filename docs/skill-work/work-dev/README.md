# work-dev

**Template mirror:** [companion-self `work-dev/README.md`](https://github.com/rbtkhn/companion-self/blob/main/docs/skill-work/work-dev/README.md) — grace-mar merges former work-build-ai here; reconcile opening sections when syncing portable doctrine.

**Objective:** Connect Grace-Mar (Record + Voice) with OpenClaw (personal agent workspace) so the Record feeds OpenClaw's identity layer, session continuity spans both systems, and OpenClaw artifacts can feed the grace-mar pipeline — with the companion always as gate.

This territory **merges** the former **work-build-ai** (same scope, same invariants). All work-build-ai content lives here; references elsewhere may still say "work-build-ai" for legacy links.

---

## Purpose

| Role | Description |
|------|-------------|
| **Record as identity source** | Export **SELF** (Record) → OpenClaw `user.md` or `SOUL.md` (their filenames) so the agent has the companion **self** / identity layer. Constitution prefix from INTENT. |
| **Session continuity** | OpenClaw reads SESSION-LOG, RECURSION-GATE, EVIDENCE before starting work. |
| **Artifacts as evidence** | OpenClaw outputs → "we did X" → pipeline. User invokes; operator stages; companion approves. |
| **Staging automation** | OpenClaw skill/cron can stage to RECURSION-GATE. Stage only; never merge. |

**Invariant:** The companion is always the gate. OpenClaw can stage; it cannot merge into the Record. This is non-negotiable: OpenClaw or downstream systems must never become control-grid infrastructure that centralizes identity or removes human approval. Companion sovereignty over the Record is preserved regardless of integration depth.

**Comprehension lock-in:** Enterprise stacks are racing to host *synthesis* (who-knows-what-across-systems) inside vendor runtimes — understanding that does not export cleanly. Grace-Mar’s counter at companion scale: **approved Record + export** (USER.md, PRP, manifest) so identity and documented understanding stay **portable** and **gate-kept**, not trapped in one agent’s memory. See [design-notes §2.5](../../design-notes.md#25-control-grid-vs-grace-mar--sovereignty-as-positioning) and [implementable-insights §10](../../implementable-insights.md#10-comprehension-lock-in-vs-companion-owned-synthesis).

### Work-template pattern library (optional)

Cross-territory WORK architecture (tiers, optional scaffolds): [work-template/README.md](../work-template/README.md). Adopt incrementally per that README.

**Canonical daily / operator surface** for this lane remains **[workspace.md](workspace.md)** — current state, blockers, and next actions live there first. For substantive **technical proposals**, consider appending a **Reality Sprint Block** ([reality-sprint-block.md](../reality-sprint-block.md)) so the smallest testable path stays visible.

**Optional judgment layer:** **[WORK-LEDGER.md](WORK-LEDGER.md)** — compounding index for watches and heuristics with **links** into integration docs; not a replacement entrypoint, not Record truth, instantiated from [work-template/WORK-LEDGER.md](../work-template/WORK-LEDGER.md).

---

## Current operator step

Use this order when actively working on the territory:

1. Open [workspace.md](workspace.md) for the current state and canonical file map.
2. Check [integration-status.md](integration-status.md) before assuming a capability is operational.
3. Read [known-gaps.md](known-gaps.md) before claiming provenance, benchmark, or continuity coverage.
4. Use [provenance-checklist.md](provenance-checklist.md) when validating export or handback behavior.
5. Use [economic-benchmarks.md](economic-benchmarks.md) only with its current instrumentation labels in mind.
6. For agent eval posture on Voice, run `python scripts/run_counterfactual_harness.py` (includes anchoring-stress probes CF-ANCH-*).
7. For **how evals are packaged as product** (operator + partner narrative), read [quality-gates-narrative.md](quality-gates-narrative.md).
8. For **session continuity as explicit steps** (files / scripts / CI vs implicit memory), read [session-continuity-contract.md](session-continuity-contract.md).
9. For **audit continuity as the safety story** (visible pipeline state vs “trust the chat”), read [safety-story-ux.md](safety-story-ux.md).
10. For **long-form tech media** (podcasts, keynotes) translated into integration + offers vocabulary — not as specs — read [external-signals.md](external-signals.md) and the shared table in [../work-strategy/external-tech-scan.md](../work-strategy/external-tech-scan.md). Example ingest: [research-no-priors-karpathy-end-of-coding.md](research-no-priors-karpathy-end-of-coding.md) (No Priors / Karpathy — agents, claws, auto-research).
11. For **focus intervals** inside the 2-hour design constraint (Pomodoro-style timeboxing, optional lesson prompt line), see [pomodoro-and-timeboxing.md](pomodoro-and-timeboxing.md).

---

## Primitive routing

Use the smallest WORK primitive that clarifies the job. These are advisory discipline surfaces, not Record truth and not gate approval.

| When the work feels like... | Start with | Why |
|-----------------------------|------------|-----|
| A non-trivial agent task, public-facing output, strategy synthesis, or delegation handoff | [templates/job-brief.md](templates/job-brief.md) | Clarifies objective, audience, success criteria, evidence, and acceptance check before execution. |
| A creative, visual, motion, or design artifact | [templates/creative-brief.md](templates/creative-brief.md) and [creative-pipeline.md](creative-pipeline.md) | Keeps taste, references, constraints, and visual proof together. |
| Code or system behavior with implementation details | [templates/specification-precision.md](templates/specification-precision.md) | Separates what must be built from examples, non-goals, and verification. |
| Vocabulary drift, hidden scope expansion, or documented-only claims | [ubiquitous-language-and-tracer-bullets.md](ubiquitous-language-and-tracer-bullets.md) | Names canonical terms and proves the thinnest end-to-end path before expanding. |
| A coding-agent recommendation that needs judgment lenses | [conductor-proposal-lenses.md](conductor-proposal-lenses.md) | Frames proposal quality and tradeoffs without turning the lens into an action menu. |

If two primitives seem to apply, pick one primary owner and link the other as supporting context. Do not stack templates just to feel thorough.

---

## Contents

**Grouping is navigational only; it does not change authority, ownership, or merge behavior.**

### Overview

| Doc / file | Purpose |
|------------|---------|
| **This README** | Objective, scope, and principles for work-dev (includes former work-build-ai). |

### Diagnostics / control plane

| Doc / file | Purpose |
|------------|---------|
| **[gap-classification.md](gap-classification.md)** | Severity / status vocabulary for [known-gaps.md](known-gaps.md). |
| **[claim-proof-standard.md](claim-proof-standard.md)** | Implemented capabilities must cite tests, scripts, receipts, or demos. |
| **[../../doctrine-drift-radar.md](../../doctrine-drift-radar.md)** | **Doctrine Drift Radar** — read-only drift audit for high-leverage authority and governance slips across scripts, docs, and derived artifacts. |
| **[../../counterfactual-fork-simulator.md](../../counterfactual-fork-simulator.md)** | **Counterfactual Fork Simulator** — scratch-only governance foresight report for proposed changes before they enter the normal gate path. |
| **[../../authority-values.md](../../authority-values.md)** | **Authority Values** — shared vocabulary for non-authority fields used by diagnostics, portable emulation, counterfactual simulation, interface artifacts, and agent surfaces. |
| **[agent-sprawl-control-plane.md](agent-sprawl-control-plane.md)** | **Agent Sprawl Control Plane** — registry and read-only audit layer for agent-like surfaces, authority boundaries, receipts, and consolidation opportunities. |
| **[diagnostics-control-plane.md](diagnostics-control-plane.md)** | **Diagnostics Control Plane** — map of work-dev diagnostic tools including Doctrine Drift Radar, Counterfactual Fork Simulator, Agent Sprawl Control Plane, Workbench, Interface Artifacts, and Claim-Proof. |
| **[path-placement-cleanup-investigation.md](path-placement-cleanup-investigation.md)** | **Path placement cleanup investigation** — factual note on the missing placement/path-friction artifacts and the narrower formatting scope confirmed in this checkout. |
| **[known-gaps.md](known-gaps.md)** | Work-dev small-seams backlog: concise inefficiencies, partials, and hardening follow-ups. |
| **[three-compounding-loops.md](three-compounding-loops.md)** | Record vs WORK vs CI — how compounding works in each loop and how they must interact (gate, no draft-as-truth). |
| **[templates/job-brief.md](templates/job-brief.md)** | **WORK job brief** — advisory pre-execution contract for non-trivial agent tasks, public-facing outputs, strategy synthesis, writing work, and drift-prone delegation. |
| **[ubiquitous-language-and-tracer-bullets.md](ubiquitous-language-and-tracer-bullets.md)** | **Ubiquitous Language + Tracer-Bullet Plans** — WORK-only primitive for shared vocabulary, forbidden claims, and the smallest end-to-end proof path before broader implementation. Template: [templates/language-and-tracer-bullet-plan.md](templates/language-and-tracer-bullet-plan.md). |
| **[compound-loop.md](compound-loop.md)** | **Compound work loop** — Plan → Execute → Review → Compound → Gate for coding-agent work; compound notes are WORK-only; gate is the only path toward Record candidates. |
| **[compound-gate-export.md](compound-gate-export.md)** | **Gate candidate export** — read-only `artifacts/work-dev-compound-gate-candidates.md` from `gate_candidate` notes; not approval; `python3 scripts/export_work_dev_compound_gate_candidates.py`. |
| **[compound-dashboard.md](compound-dashboard.md)** | **Compound dashboard** — generated operator view of compound notes, refresh/export status, stale/duplicate hints, and related paths; `python3 scripts/build_work_dev_compound_dashboard.py` → `artifacts/work-dev-compound-dashboard.md`. |
| **[work-dev-derived-markdown-authority.md](work-dev-derived-markdown-authority.md)** | **YAML `recordAuthority` / `gateEffect` on compound derived markdown** under `artifacts/work-dev-compound-*.md` (not the JSON interface-artifact schema). |
| **[provenance-checklist.md](provenance-checklist.md)** | Repeatable verification path for export, handback, and audit integrity. |
| **[record-diff-queue.md](../../record-diff-queue.md)** | **Record Diff Queue** (GAP-011): unified review surface for pending governed-state changes; standardized diff cards (old/new/evidence/confidence/conflict/recommended action); template-portable renderer + instance gate adapter. |

### Portability / runtime / external agents

| Doc / file | Purpose |
|------------|---------|
| **[persistence-and-memory-surfaces.md](persistence-and-memory-surfaces.md)** | What persists where (gate, MEMORY, vendor agents, exports) vs outcome-agent dimensions; assumption-labeled efficiency note. |
| **[delegation-spec-external-agents.md](delegation-spec-external-agents.md)** | External outcome agents: dimension map, 7-section delegation outline, copy-paste evaluation prompt (operator WORK). |
| **[openclaw-integration.md](../../openclaw-integration.md)** | Full integration guide — export, continuity, handback, staging, permission summary. |
| **[INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md)** | **One-loop spec:** read order → export → stage-only → merge; script index; companion gate invariant. |
| **[integration-status.md](integration-status.md)** | Implemented vs partial vs documented-only status table for the integration. |
| **[session-continuity-contract.md](session-continuity-contract.md)** | Continuity as **explicit contract**: which files, which scripts, what CI proves — **not** “the agent remembers.” |
| **[../../portability/emulation/README.md](../../portability/emulation/README.md)** | Portable emulation contract layer: behavior specs and authority-bounded bundle doctrine for foreign runtimes. |
| **[agentic-environment-principles.md](agentic-environment-principles.md)** | **Environment-first:** policy + continuity + gate + observability before prompt; canonical Record files before clever retrieval; **§5** local-private stacks (**a** residency/roles, **b** bounded execution, **c** pipeline vs agent memory). |
| **[agent-surface-template.yaml](agent-surface-template.yaml)** | **Agent surface axes** (runtime / orchestration / interface) + Grace-Mar trust fields; optional **`agent_species`** (`coding_harness`, `dark_factory`, `auto_research`, `workflow_orchestration`). CLI: `python scripts/work_dev/agent_surface_checklist.py`; `--validate` checks structure and species when set. |
| **[control-plane/capability-contract-template.yaml](control-plane/capability-contract-template.yaml)** | **Capability contract template** (GAP-008): schema, auth, failure policy, cost, rate limits, governance, receipt shape — standardized shape for any integration or tool surface. |
| [control-plane/capability-contract-openclaw-export.yaml](control-plane/capability-contract-openclaw-export.yaml) | Capability contract: OpenClaw identity export (`openclaw_hook.py`). |
| [control-plane/capability-contract-openclaw-stage.yaml](control-plane/capability-contract-openclaw-stage.yaml) | Capability contract: OpenClaw stage-only handback (`openclaw_stage.py`). |
| [control-plane/capability-contract-sandbox-dry-run.yaml](control-plane/capability-contract-sandbox-dry-run.yaml) | Capability contract: Sandbox DryRunBackend (mock; testing governance loop). |
| [control-plane/capability-contract-sandbox-docker.yaml](control-plane/capability-contract-sandbox-docker.yaml) | Capability contract: Sandbox LocalDockerBackend (planned; not yet implemented). |
| **[sandbox-adapter-spec.md](sandbox-adapter-spec.md)** | **Sandbox adapter layer** (GAP-010): governance wrapper for external sandbox runtimes (E2B, Daytona, Docker); authority classes, receipt emission, compute ledger integration, backend protocol. |

### Workbench / interface artifacts / generated views

| Doc / file | Purpose |
|------------|---------|
| **[workbench/README.md](workbench/README.md)** | **Workbench Harness** — run / inspect / revise / **workbench receipt** for generated UIs, CLIs, and scripts; `recordAuthority` and `gateEffect` are **none**; not action receipts or merge receipts. |
| **[interface-artifacts/README.md](interface-artifacts/README.md)** | **Interface Artifact Protocol** — generated operator-facing views and prototypes as a first-class derived layer; defines what these artifacts are and what authority they do not have. |
| **[derived-regeneration.md](derived-regeneration.md)** | Repo-owned derived regeneration roadmap and phase-1 foundation: change detector, regeneration entrypoint, rebuild receipts, and ranked next phases. |
| **[workbench/SCRIPT-USAGE.md](workbench/SCRIPT-USAGE.md)** | **Workbench** CLIs: `new_workbench_receipt.py`, `validate_workbench_receipt.py` (create/validate JSON; no gate). |
| **[creative-pipeline.md](creative-pipeline.md)** | Governed UI / motion / 3D workflow: creative brief, `users/grace-mar/DESIGN.md`, `scripts/validate-design-md.py`, artifacts under `users/grace-mar/artifacts/creative/`. |

### Build / automation / scripts / CI

| Doc / file | Purpose |
|------------|---------|
| **[implementation-ledger.md](implementation-ledger.md)** | Narrative spine for capability/gap machine artifacts (`artifacts/work-dev/*.json`). |
| **[capability-registry.md](capability-registry.md)** | Integration ids ↔ surfaces (aligns with gap `related_integration_ids`). |
| **[verification-runs/](verification-runs/README.md)** | Manual/script verification receipts. |
| **[PARALLEL-MACRO-ACTIONS.md](PARALLEL-MACRO-ACTIONS.md)** | Non-interfering parallel agent branches; `scripts/integration_macro_actions.py`. |
| **[operator_depth_hint.py](../../../scripts/operator_depth_hint.py)** | When pipeline velocity (approvals / merges in a rolling window) crosses tiers, emit a harness hint toward depth docs; `operator_daily_warmup` prints a one-liner summary. Operator-only; not part of the Record. |
| **[git-branch-hygiene.md](git-branch-hygiene.md)** | **Local git** branch snapshot: merge vs delete vs no action; wired into [coffee](../../../.cursor/skills/coffee/SKILL.md) Step 1 — **not** the same as menu **A** (template/boundary). |
| **[cursor-vscode-grace-mar-tasks.json](cursor-vscode-grace-mar-tasks.json)** | Snippet to merge into local `.vscode/tasks.json` — re-entry stack + `--receipt` tasks. |
| **[skills-portable/](../../../skills-portable/README.md)** | **Portable Cursor skills** (manifest + cores); sync into `.cursor/skills/` via `python3 scripts/sync_portable_skills.py` (`--verify`, `--dry-run`). Full procedure: `.cursor/skills/portable-skills-sync/SKILL.md`. |
| **[skill-candidates.md](../../../skills-portable/skill-candidates.md)** | **Skill discovery** backlog (one-line pointers); ladder continues in `_drafts/` then manifest ([README § Discovery ladder](../../../skills-portable/README.md)). |
| **[harness-replay-work-politics-demo.md](harness-replay-work-politics-demo.md)** | Harness replay walkthrough for a **work-politics** gate merge (audit tooling; territory doc links to [work-politics](../work-politics/README.md)). |

### Research notes / technical exploration

| Doc / file | Purpose |
|------------|---------|
| **[external-signals.md](external-signals.md)** | Moonshots / GTC–class discourse → **work-dev** lens (OpenClaw, enterprise trust, inference economics, portability); links shared [external-tech-scan](../work-strategy/external-tech-scan.md). |
| **[agent-memory-pgvector-spec.md](agent-memory-pgvector-spec.md)** | **Persistent agent memory (Postgres 16+ / pgvector):** flaw-fix DDL + RLS + revisions + hybrid (RRF) + reflection governance + dual-repo scope; SQL in [sql/agent_memory_v1_initial.sql](sql/agent_memory_v1_initial.sql). WORK only — not Record. |
| **[research-orchestra-ai-research-skills.md](research-orchestra-ai-research-skills.md)** | Orchestra Research AI Research Skills — WORK-only integration note and Autoresearch adapter packet: a safe research scaffold for sources, dated notes, and possible gate-candidate drafts, **not** an autonomous research-agent claim or Record authority. Templates: [wrapper](templates/autoresearch-wrapper.md), [run note](templates/autoresearch-run-note.md), [gate candidate example](templates/autoresearch-gate-candidate-example.md), [operator checklist](templates/autoresearch-operator-checklist.md). |
| **[research-moonshots-237.md](research-moonshots-237.md)** | Research notes from Moonshots #237 (Alex Finn) — identity, memory, security, hierarchy, actionable takeaways. |
| **[research-no-priors-karpathy-end-of-coding.md](research-no-priors-karpathy-end-of-coding.md)** | No Priors / Karpathy — agents, claws, auto-research, “end of coding”; transcript in [work-dev transcripts](../../../research/external/work-dev/transcripts/); work-dev alignment table + guardrails. |
| **[research-agent-readable-writable-commerce.md](research-agent-readable-writable-commerce.md)** | McKinsey / agent commerce / “agent readable & writable” stack; transcript in [work-dev research](../../../research/external/work-dev/transcripts/); positioning + guardrails. |
| **[lessons-openclaw-skills-video.md](lessons-openclaw-skills-video.md)** | Notes from OpenClaw skills / output-quality video. |
| **[lessons-perplexity-computer-video.md](lessons-perplexity-computer-video.md)** | Notes from Perplexity Comet/agent-skills video. |
| **[lessons-deepseek-insider-self-improving-agents.md](lessons-deepseek-insider-self-improving-agents.md)** | Notes from DeepSeek Insider (self-improving agents, bounded session). |
| **[lessons-solo-founder-ai-video.md](lessons-solo-founder-ai-video.md)** | Notes from solo-founder / AI talent video. |

### Product / business / positioning

| Doc / file | Purpose |
|------------|---------|
| **[economic-benchmarks.md](economic-benchmarks.md)** | Benchmarks for cost, value flow, and gate health — priority five and full set. |
| **[quality-gates-narrative.md](quality-gates-narrative.md)** | Evals as **product**: “green = within boundary” map (harness, integrity, continuity CI, gate health) + partner one-liner; future dashboard concept. |
| **[safety-story-ux.md](safety-story-ux.md)** | **Safety story** as product: visible pending/approved, receipts, staged vs merged — audit continuity as primary comfort, not admin trivia. |
| **[positioning-governed-state-os.md](positioning-governed-state-os.md)** | **Positioning:** "governed state OS" framing, companion-first vs infrastructure-first strategic fork, six-layer gap map, accepted external framings. |
| **[offers.md](offers.md)** | First-pass business-layer offers and commercial framing. |
| **[target-registry.md](target-registry.md)** | Buyer segments for the future company path. |
| **[proof-ledger.md](proof-ledger.md)** | Reusable proof lines from internal work and future client work. |
| **[engagement-model.md](engagement-model.md)** | How work should be packaged commercially. |
| **[delivery-playbook.md](delivery-playbook.md)** | Default service delivery phases. |
| **[agent-reliability-playbook.md](agent-reliability-playbook.md)** | Agent failure modes (tails, reasoning vs action, anchoring, guardrails) and four-layer mitigation. |
| **[variation-types.md](variation-types.md)** | Factorial stressor templates for evals across client workflows. |
| **[claude-code-wat-crosswalk.md](claude-code-wat-crosswalk.md)** | WAT / agentic-IDE practice mapped to delivery, reliability, gate, and handover. |
| **[unit-economics-one-pager.md](unit-economics-one-pager.md)** | **Unit economics:** what one companion instance costs (LLM tokens, storage, operator time, scale projections) from live compute-ledger data. |
| **[brief-ai-ambition-six-unlocks.md](brief-ai-ambition-six-unlocks.md)** | One-pager: ambition frame vs cost-reduction, Jevons paradox, six people-focused unlocks for boards/leadership. |
| **[brief-claude-1m-context-context-rot.md](brief-claude-1m-context-context-rot.md)** | Reference: Claude 1M context (Opus/Sonnet 4.6), context rot, eight-needle test, when to clear, pricing. |
| **[partner-channel.md](partner-channel.md)** | Borrowed-authority / partner path for growth. |
| **[objection-log.md](objection-log.md)** | Market-learning and positioning feedback loop. |
| **[crypto-roadmap.md](../../crypto-roadmap.md)** | Cross-cutting roadmap for using cryptocurrency as an authority, settlement, and access layer. |
| **[actionable-features-and-insights.md](actionable-features-and-insights.md)** | Product/UX feature backlog and copy snippets (polyphonic cognition, OpenClaw-adjacent); links to work-politics protocol docs. |
| **[capability-statement-assistant-brain.md](capability-statement-assistant-brain.md)** | Federal-style capability one-pager for assistant-brain / polyphonic cognition offer. |
| **[competitor-research-assistant-brain-judgment-testing.md](competitor-research-assistant-brain-judgment-testing.md)** | Competitor scan: multi-perspective / judgment-testing products vs assistant brain. |

### Local workspace / lane maintenance

| Doc / file | Purpose |
|------------|---------|
| **[workspace.md](workspace.md)** | Canonical operator entrypoint: current state, blockers, next actions, and file map. |
| **[workspace-hygiene.md](workspace-hygiene.md)** | Local-only temp/cache/audit clutter classes and commit hygiene guidance; docs-only, no cleanup command. |
| **[WORK-LEDGER.md](WORK-LEDGER.md)** | Optional **judgment / compounding** index (watches, heuristics, framing list) — pointers into workspace + integration docs; scaffold from [work-template/WORK-LEDGER.md](../work-template/WORK-LEDGER.md). |
| **[work-dev-sources.md](work-dev-sources.md)** | Authorized sources list (channels / podcasts) for operator framing; not integration truth. |
| **[work-dev-history.md](work-dev-history.md)** | Append-only **operator log** for this lane (ingests, integration milestones); not Record — see [work-modules-history-principle.md](../work-modules-history-principle.md). |
| **[dev-notebook/work-dev/journal/README.md](dev-notebook/work-dev/journal/README.md)** | **Dev journal** ( [work notebook](dev-notebook/README.md) → work-dev lane) — short daily **reflection** on work-dev learning/building (parallel to [cici-notebook](../work-cici/cici-notebook/README.md)); [Day 1](dev-notebook/work-dev/journal/2026-04-09-day-01.md), [Day 2](dev-notebook/work-dev/journal/2026-04-11-day-02.md); [daily-dev-journal-inbox](dev-notebook/work-dev/journal/daily-dev-journal-inbox.md) (rolling buffer; fold at **`dream`**; prune when long). Pointer: [dev-journal/README.md](dev-journal/README.md) — not Record, not a substitute for history or workspace. |
| **[dev-notebook/README.md](dev-notebook/README.md)** | **Work notebook** (`dev-notebook/`) — multi-lane **prompts and spec vault** ([Cici Phase 1 (work-cici/)](dev-notebook/work-cici/cici-phase-1-git-first-governed-state-prompt.md), [work-strategy/ shell](dev-notebook/work-strategy/README.md)); not the rolling day-scale strategy/cici trees. |
| **[pomodoro-and-timeboxing.md](pomodoro-and-timeboxing.md)** | Optional Pomodoro-style focus intervals inside the ~2-hour design ceiling; Record-derived lesson timebox line; WORK only. |
| **[google-workspace-cli-operator.md](google-workspace-cli-operator.md)** | Optional **Google Workspace CLI** for operator continuity (Sheets/Drive); not Record; local secrets; attach `gws-cli-recipes` rule when using `gws`. |
| **[operator-heartbeat-external-model-prompt.md](operator-heartbeat-external-model-prompt.md)** | Portable **non-repo** operator prompt (accurate gate/staging vs merge); use when no `AGENTS.md` / harness. |

### Other / legacy

| Doc / file | Purpose |
|------------|---------|
| **[work-modules-sources-principle.md](../work-modules-sources-principle.md)** | Cross-territory convention: each `work-*` module has a `*-sources.md` list. |

---

## Authority reminder

**work-dev** is a **WORK** lane. Its diagnostics, artifacts, receipts, and reports
do not update canonical Record unless separately routed through the governed
review path. Generated diagnostics are not approval. **Workbench receipts** are
not evidence truth. **External runtimes** do not gain merge authority.

---

## Principles

1. **Companion sovereignty** — Merge authority stays with the companion. OpenClaw stages; companion approves.
2. **Knowledge boundary** — Voice responses use only what is documented in the Record. No LLM inference into identity facts.
3. **Stage-only automation** — OpenClaw skills may read, analyze, and stage candidates. They may not merge into SELF, EVIDENCE, or prompt.
4. **Session continuity** — **Contract, not vibes:** read `session-log.md`, `recursion-gate.md`, and recent `self-evidence.md` (or run `continuity_read_log.py` / `harness_warmup.py` as documented). Do not assume the agent remembers; see [session-continuity-contract.md](session-continuity-contract.md).
5. **Handback provenance** — Inbound staging includes advisory constitutional check against INTENT; events emitted for audit.
6. **Portable synthesis** — Merge-approved truth in-repo; refresh exports after merges so OpenClaw never becomes the only place “who the companion is” lives.
7. **Agent reliability** — Do not treat chain-of-thought or internal traces as audit. For consequential agent work outside the companion Voice, use **tail scenarios**, **factorial variations**, and **deterministic checks** (see [agent-reliability-playbook.md](agent-reliability-playbook.md)).
8. **Visible safety state** — Users fear **silent failure**; foreground **pending vs approved**, **receipts**, **last merge**, **OpenClaw staged vs Record merged** — not chat-only reassurance. See [safety-story-ux.md](safety-story-ux.md).

---

## Quick Reference

**Export identity:**
```bash
python integrations/openclaw_hook.py --user grace-mar --format md+manifest --emit-event
```

**Handback (stage only):**
```bash
python integrations/openclaw_stage.py --user grace-mar --text "we explored X in OpenClaw"
python integrations/openclaw_stage.py --user grace-mar --artifact ./outputs/session-note.md
```

---

## Business path

Use this order when the question is how work-dev could become a real company rather than just a territory:

1. Open [offers.md](offers.md) and choose the first sellable diagnostic or architecture pass.
2. Confirm the target segment in [target-registry.md](target-registry.md).
3. Pull proof lines from [proof-ledger.md](proof-ledger.md).
4. Check [engagement-model.md](engagement-model.md) before inventing pricing or retainers.
5. Use [delivery-playbook.md](delivery-playbook.md) to keep implementation bounded.
6. Use [partner-channel.md](partner-channel.md) for borrowed-authority growth paths.
7. Log real objections in [objection-log.md](objection-log.md).
8. For **partner-facing safety framing** (silent-failure class, inspectable state), pull lines from [proof-ledger.md](proof-ledger.md) and [safety-story-ux.md](safety-story-ux.md).

---

## Cross-references

Other work territories (e.g. [work-politics](../work-politics/README.md)) share the same RECURSION-GATE and companion-approval rule; they use territory tags for batch merge (e.g. `--territory work-politics`).

- [OpenClaw Integration Guide](../../openclaw-integration.md) — Full spec
- [Crypto roadmap](../../crypto-roadmap.md) — authority, settlement, and access layer
- [Architecture](../../architecture.md) — Record structure, harness
- [AGENTS.md](../../../AGENTS.md) — Knowledge boundary, gated pipeline
- [INTENT](../../intent-template.md) — Constitutional context for handback
