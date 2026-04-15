# work-dev workspace

Canonical operator entrypoint for the `work-dev` territory.

Use this file when you want one place to understand:

- what parts of the Grace-Mar ↔ OpenClaw integration are real today
- what is only documented or aspirational
- where provenance or observability is weak
- how the territory could become a real business
- what should be checked next

## Related territory: template sync (not OpenClaw)

**[`work-companion-self`](../work-companion-self/README.md)** — grace-mar ↔ companion-self drift, `template_diff.py`, manifest audits, upstream PRs. Use that folder for **template governance**; use **this** folder for **OpenClaw / exports / continuity / CI**. See also [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md).

---

## Current state summary

| Area | Current state |
|------|---------------|
| **Identity export** | Implemented through `integrations/openclaw_hook.py` and the runtime bundle export path |
| **Stage-only handback** | Implemented through `integrations/openclaw_stage.py` → `/stage` |
| **Pipeline-level export audit** | Implemented via `runtime_compat_export` events and harness events |
| **Constitution advisory event** | Implemented via `intent_constitutional_critique` event emission |
| **End-to-end provenance** | Implemented: OpenClaw payload (source=openclaw_stage) flows as staging_meta into gate; candidate blocks carry candidate_source, artifact_*, constitution_*; recursion_gate_review parses them for review/benchmarks |
| **Session continuity** | **Contract:** [session-continuity-contract.md](session-continuity-contract.md) — files + `continuity_read_log.py` + CI (`tests/test_continuity_read_log.py`); not “agent remembers.” Live JSONL append when script invoked; OpenClaw startup wiring still operator-side |

---

## Canonical files

| File | Role |
|------|------|
| `README.md` | Territory doctrine, scope, and invariants |
| `../work-companion-self/README.md` | Template sync, audit reports, reconciliation-code audit guidance |
| `INTEGRATION-PROGRAM.md` | Single-page OpenClaw ⟷ Grace-Mar loop (read / export / stage / merge) |
| `PARALLEL-MACRO-ACTIONS.md` | Parallel macro-action branches + merge order discipline |
| `three-compounding-loops.md` | Record vs WORK vs CI loops — how compounding works and where drafts must not become canon |
| `integration-status.md` | Honest implemented/partial/documented-only status table |
| `known-gaps.md` | Current spec-to-implementation gaps and suggested fixes |
| `provenance-checklist.md` | Repeatable verification path for export, handback, and audit |
| `economic-benchmarks.md` | Metrics and instrumentation reality |
| `../../openclaw-integration.md` | Full integration guide and architecture-level contract |
| `research-moonshots-237.md` | Research notes and ecosystem framing |
| `research-no-priors-karpathy-end-of-coding.md` | No Priors / Karpathy — agents, claws, auto-research; links to work-dev transcripts + work-dev takeaways |
| `research-agent-readable-writable-commerce.md` | McKinsey / agent commerce / readable-writable stack; transcript under `research/external/work-dev/transcripts/` |
| `offers.md` | Business-layer offers and commercial framing |
| `target-registry.md` | Buyer segments for the business layer |
| `proof-ledger.md` | Reusable proof lines for client or partner conversations |
| `session-continuity-contract.md` | Explicit continuity steps vs implicit memory (files, scripts, CI) |
| `safety-story-ux.md` | Visible pipeline state as user-facing safety story (pending/approved, receipts, staged vs merged) |
| `external-signals.md` | Transcript/keynote-class discourse → work-dev lens (OpenClaw, trust, inference); pairs with work-strategy `external-tech-scan.md` |
| `work-dev-sources.md` | Authorized sources list for work-dev framing (not integration truth); see [work-modules-sources-principle.md](../work-modules-sources-principle.md); parallel: [../work-politics/work-politics-sources.md](../work-politics/work-politics-sources.md) |
| `../work-career/README.md` | **AI career prep (operator lane):** manual job JSON/CSV, skill worksheet, opportunity-review template; `scripts/work_career/` — not Record truth |
| `creative-pipeline.md` | **Agent-augmented creative workflow:** brief template, `DESIGN.md`, `scripts/validate-design-md.py`, artifacts under `users/grace-mar/artifacts/creative/` — not Record truth until gated |
| `agentic-environment-principles.md` | Environment-first debugging; §5 **a/b/c** (residency + roles, bounded runtime, pipeline vs local memory) |
| `agent-surface-template.yaml` | Structured checklist: runtime / orchestration / interface + Grace-Mar trust; optional `agent_species`; `scripts/work_dev/agent_surface_checklist.py` |
| `managed-agent-design.md` | Think-lane design: persistent-agent lifecycle using existing primitives (sandbox adapter, agent-surface-template, gate); operator runbook; steward boundary review |
| `engagement-model.md` | Commercial packaging and sequencing |
| `delivery-playbook.md` | Service delivery phases |
| `claude-code-wat-crosswalk.md` | WAT / agentic IDE ↔ delivery, reliability, handover |
| `partner-channel.md` | Borrowed-authority / partner growth path |
| `objection-log.md` | Positioning and market-learning log |
| `../../crypto-roadmap.md` | Future authority, settlement, and access layer across territories |
| `harness-replay-work-politics-demo.md` | Example **work-politics** `CANDIDATE-*` replay ([work-politics](../work-politics/README.md) territory); audit tooling |
| `actionable-features-and-insights.md`, `capability-statement-assistant-brain.md`, `competitor-research-assistant-brain-judgment-testing.md`, `lessons-openclaw-skills-video.md`, `lessons-perplexity-computer-video.md`, `lessons-deepseek-insider-self-improving-agents.md`, `lessons-solo-founder-ai-video.md` | Assistant-brain / agent-product operator notes; link to polyphonic protocol docs in [work-politics](../work-politics/README.md) |

---

## Operator path

0. When debugging agent vs repo behavior, read `agentic-environment-principles.md` (environment before prompt).
1. Open `integration-status.md` to see what is implemented, partial, or only documented.
2. Read `known-gaps.md` before assuming a workflow is operational.
3. Use `provenance-checklist.md` when validating export, handback, or merge-followthrough behavior.
4. Check `economic-benchmarks.md` before claiming observability or benchmark coverage.
5. Update `integration-status.md` and `known-gaps.md` after any real test or implementation change.

---

## Business layer

This territory now has three lanes:

| Lane | Purpose |
|------|---------|
| **Doctrine** | Why the territory exists and what it believes about portable, governed AI systems |
| **Operator** | What is real today, what is partial, and what needs verification |
| **Business** | What the future company would sell, to whom, and how delivery could work |

Use the business lane when the question is not "is this implemented?" but "how could this become a client-services company?"

Crypto belongs adjacent to these lanes as a future **authority / settlement / access** layer, not as a prerequisite for current operator work.

---

## Current blockers

| Blocker | Why it matters |
|---------|----------------|
| ~~**Handback provenance is not preserved cleanly into `recursion-gate.md`**~~ | Resolved: OpenClaw payload sets candidate_source + artifact/constitution fields in gate (handback_server + core + recursion_gate_review). |
| **Benchmark docs overstate current instrumentation** | Mitigated: `economic-benchmarks.md` distinguishes automatic pipeline emission vs manual/derivation; re-audit after hook changes |
| **Live continuity JSONL is opt-in** | CI verifies script + files; `scripts/openclaw_session_continuity.sh` logs then execs the command; habit still required if not wired into OpenClaw |

---

## Next actions

1. ~~Preserve OpenClaw-specific provenance end-to-end from `openclaw_stage.py` through `/stage` into staged candidates.~~ Done.
2. ~~Mark benchmark rows as instrumented, manual, planned, or blocked instead of implying they all exist today.~~ Done (see `economic-benchmarks.md` definitions and tables).
3. ~~CI wiring for `continuity_read_log.py`~~ Done (`tests/test_continuity_read_log.py`). ~~Optional: OpenClaw startup wrapper~~ `scripts/openclaw_session_continuity.sh` appends JSONL then runs the rest of the command.
4. ~~Refresh stale derived exports (`manifest.json`, `llms.txt`, `intent_snapshot.json`, `fork-manifest.json`, PRP, runtime bundle). Validator flags these; run `refresh_derived_exports.py` after confirming no Record changes are pending.~~ Done (2026-04-12: `refresh_derived_exports.py -u grace-mar`; commit `3a17caf`).
5. ~~Pick only between BUILD-AI-GAP-005 and BUILD-AI-GAP-006 as the next blocker~~ — Incremental slice landed: matrix `--check` + pytest drift on `handback_tail_stress.matrix.md`, optional `staged_risk_tier` narrative guard in `validate_handback_analysis.py` (commit `aa1417c`). Both gaps remain `partial` (client tail YAMLs; full semantic alignment; wiring `staged_risk_tier` from `/stage` when ready). **Choose next wedge:** **GAP-007** (progressive autonomy — shadow JSONL + `evaluate_autonomy_tiers.py` vs `tier_thresholds.yaml`, `partial`; dashboard/CI hook still open; see `autonomy/tier_policy.md`) when scope expansion is live; **OB1 chunking** (#6) when bridge exporter / PR4 is queued; **risk-mitigation template** (#7) for cross-territory hygiene without new instrumentation.
6. OB1 chunking spike — when demand materializes: export one real `self.md` under each strategy, measure retrieval precision, pick the winner. Blocking prerequisite for the bridge exporter (PR 4). See `docs/integrations/ob1/architecture.md` § Known technical risks.
7. Apply risk-mitigation template (success criteria, sustainment, deprecation, scope creep) to remaining uncovered territories: `work-politics`, `work-civ-mem`, `work-xavier`. Template: `docs/skill-work/work-template/README.md` § Risk-mitigation checklist.

---

## Guardrail

This workspace is for operator truth, not marketing truth. If a capability is only documented, say so plainly.
