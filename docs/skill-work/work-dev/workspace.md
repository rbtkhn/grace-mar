# work-dev workspace

Canonical operator entrypoint for the `work-dev` territory.

Use this file when you want one place to understand:

- what parts of the Grace-Mar ↔ OpenClaw integration are real today
- what is only documented or aspirational
- where provenance or observability is weak
- how the territory could become a real business
- what should be checked next

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
| `agentic-environment-principles.md` | Environment-first debugging: policy + continuity + gate + observability before prompt; canonical files before clever retrieval; “boring” high-leverage work |
| `agent-surface-template.yaml` | Structured checklist: runtime / orchestration / interface + Grace-Mar trust; `scripts/work_dev/agent_surface_checklist.py` |
| `engagement-model.md` | Commercial packaging and sequencing |
| `delivery-playbook.md` | Service delivery phases |
| `claude-code-wat-crosswalk.md` | WAT / agentic IDE ↔ delivery, reliability, handover |
| `partner-channel.md` | Borrowed-authority / partner growth path |
| `objection-log.md` | Positioning and market-learning log |
| `../../crypto-roadmap.md` | Future authority, settlement, and access layer across territories |

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
| **Live continuity JSONL is opt-in** | CI verifies script + files; appending to `continuity-log.jsonl` on each OpenClaw session still requires wrapper or habit |

---

## Next actions

1. ~~Preserve OpenClaw-specific provenance end-to-end from `openclaw_stage.py` through `/stage` into staged candidates.~~ Done.
2. ~~Mark benchmark rows as instrumented, manual, planned, or blocked instead of implying they all exist today.~~ Done (see `economic-benchmarks.md` definitions and tables).
3. ~~CI wiring for `continuity_read_log.py`~~ Done (`tests/test_continuity_read_log.py`). Optional: OpenClaw startup wrapper for real JSONL appends each session.

---

## Guardrail

This workspace is for operator truth, not marketing truth. If a capability is only documented, say so plainly.
