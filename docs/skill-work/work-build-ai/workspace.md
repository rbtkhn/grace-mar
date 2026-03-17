# work-build-ai workspace

Canonical operator entrypoint for the `work-build-ai` territory.

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
| **Session continuity enforcement** | Documented and recommended, but not verified by a repo-local runtime hook |

---

## Canonical files

| File | Role |
|------|------|
| `README.md` | Territory doctrine, scope, and invariants |
| `integration-status.md` | Honest implemented/partial/documented-only status table |
| `known-gaps.md` | Current spec-to-implementation gaps and suggested fixes |
| `provenance-checklist.md` | Repeatable verification path for export, handback, and audit |
| `economic-benchmarks.md` | Metrics and instrumentation reality |
| `../../openclaw-integration.md` | Full integration guide and architecture-level contract |
| `research-moonshots-237.md` | Research notes and ecosystem framing |
| `offers.md` | Business-layer offers and commercial framing |
| `target-registry.md` | Buyer segments for the business layer |
| `proof-ledger.md` | Reusable proof lines for client or partner conversations |
| `engagement-model.md` | Commercial packaging and sequencing |
| `delivery-playbook.md` | Service delivery phases |
| `partner-channel.md` | Borrowed-authority / partner growth path |
| `objection-log.md` | Positioning and market-learning log |
| `../../crypto-roadmap.md` | Future authority, settlement, and access layer across territories |

---

## Operator path

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
| **Benchmark docs overstate current instrumentation** | Makes it too easy to confuse desired observability with actual emitted data |
| **Session continuity is checklist-level, not verified runtime behavior** | Weakens one of the territory's stated core roles |

---

## Next actions

1. ~~Preserve OpenClaw-specific provenance end-to-end from `openclaw_stage.py` through `/stage` into staged candidates.~~ Done.
2. Mark benchmark rows as instrumented, manual, planned, or blocked instead of implying they all exist today.
3. Decide whether continuity should remain checklist-based or gain a verifiable startup/logging surface.

---

## Guardrail

This workspace is for operator truth, not marketing truth. If a capability is only documented, say so plainly.
