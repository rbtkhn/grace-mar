# Harness Event Replay — product spec (north star)

Grace-Mar treats **Voice as model + harness** and expects debugging to separate **model limit, prompt gap, pipeline miss, or tool/context issue** ([architecture.md](architecture.md)). The system is split into **record, runtime, audit, and policy** lanes—not one opaque memory store. The audit lane already anchors concrete files: `pipeline-events.jsonl`, `merge-receipts.jsonl`, `compute-ledger.jsonl`, `harness-events.jsonl`, `fork-manifest.json` ([harness-inventory.md](harness-inventory.md)). That layout is the architectural placeholder for **causal replay**.

**Harness Event Replay** (full vision) reconstructs *why* a specific **answer**, **staged proposal**, or **merge recommendation** happened by replaying the **prompt context**, **active runtime aids**, **routing decisions**, **evidence references**, **validator results**, and **gate actions** that shaped the outcome. It is a **causal debugger** for the harness—not a generic log viewer.

Grace-Mar is a **governed cognitive fork**: the Record exposes **SELF, SELF-LIBRARY, SKILLS, and EVIDENCE** as first-class surfaces, and profile changes flow through **signal detection → candidate staging → review → integration**. When something goes wrong, the question is not only “what did the model think?” but **which part of the harness produced this outcome?** ([conceptual framework / AGENTS guardrails](conceptual-framework.md))

Ontology work (SELF-KNOWLEDGE vs SELF-LIBRARY, CIV-MEM routing) makes replay especially valuable for **boundary** questions:

- Why was this filed under SELF instead of SELF-LIBRARY?
- Why did CIV-MEM routing fire?
- Why was this treated as identity-facing rather than reference-facing?

[boundary-review-queue.md](boundary-review-queue.md) helps decide **where** things should go; Harness Event Replay explains **why** the system thought they should go there. Together they form a strong core for the next phase.

---

## What full replay should show (per event)

For any **event ID** (once the envelope exists end-to-end):

| Layer | Examples |
|-------|----------|
| **Input** | Message or operator action that triggered the event |
| **Runtime bundle** | What was active at the time (compat export, handback metadata) |
| **Routing / classification** | Analyst path, `proposal_class`, territory, boundary hints |
| **Evidence** | ACT lines, evidence tier, links consulted |
| **Prompt / policy** | Surfaces in force (`intent.md`, PRP slices, prompt sections) |
| **Candidate outputs** | Staged YAML, diffs, confidence where recorded |
| **Validators** | `validate-integrity`, governance_checker, boundary warnings |
| **Human gate** | Approve / reject / defer, inbox state |
| **Outcome** | Final write targets, non-write, or receipt + checksum |

---

## Three replay modes

### 1. Answer replay

**Question:** “Why did Grace-Mar say this?”

Reconstruct: user input; loaded **record** snippets; loaded **runtime** snippets; routing path; tool / lookup results; **prompt assembly**; model output; post-processing.

This is the highest-trust surface for the **live companion** experience. **Today:** transcript tail and session logs are partial; full prompt assembly is not persisted unless product logging adds it.

### 2. Proposal replay

**Question:** “Why was this candidate written to `recursion-gate.md`?”

Reconstruct: source signal; classifier / analyst output; proposed category; evidence links; diff target; confidence; validator warnings; how the approval inbox displayed it.

Best for **misclassification** and **bad staging**. **Today:** `replay_harness_event.py` + gate YAML + pipeline rows approximate this for a **candidate ID**, minus classifier internals unless logged.

### 3. Merge replay

**Question:** “Why did this change land in SELF, SELF-LIBRARY, or SKILLS?”

Reconstruct: approved candidate; reviewer action; `process_approved_candidates` actions; files touched; merge receipt; optional git commit trail.

Best for **governance**. **Today:** merge receipts + harness merge events + pipeline `applied` events cover much of this path.

---

## Minimal implementation shape (future envelope)

A single **append-only event envelope** across pipeline steps would unify correlation. Sketch (fields evolve with implementation):

```json
{
  "event_id": "evt_20260320_001",
  "event_type": "proposal_stage",
  "fork_id": "grace-mar",
  "timestamp": "2026-03-20T14:12:03Z",
  "input_ref": "msg_abc123",
  "record_refs": ["users/grace-mar/self.md#IX-A"],
  "library_refs": ["users/grace-mar/self-library.md#CIV-MEM"],
  "runtime_refs": ["memory.md#tail"],
  "policy_refs": ["intent.md"],
  "routing": {
    "classifier": "cmc-routing",
    "decision": "SELF_LIBRARY.CIV_MEM",
    "confidence": 0.87
  },
  "candidate_ref": "recursion-gate.md#CANDIDATE-0047",
  "validator_refs": ["validate-integrity.py:warn_boundary"],
  "review_action": null,
  "outcome": "staged"
}
```

A **replay viewer** (CLI or static page) resolves this envelope into a **human-readable timeline**. Implementation can start **without** a giant observability dashboard.

---

## UI shape (incremental)

Start with a **single event page** (or markdown report):

- **Header:** event type, time, fork, outcome  
- **Timeline:** input → routing → evidence → prompt context → output → validation → review  
- **Panels:** Record, Library, Runtime, Policy  
- **Diff box:** what changed or would have changed  
- **Why box:** short natural-language explanation (generated or templated)

---

## Current implementation vs north star

| Capability | Today (`scripts/replay_harness_event.py`) | North star |
|------------|-------------------------------------------|------------|
| Proposal / merge correlation | Candidate ID + gate YAML + pipeline + harness + receipts | Same, plus cross-step refs (`parent_event_id`, etc.) |
| Answer replay | Not built; transcript optional | Full prompt assembly + routing + tools |
| Validator linkage | Manual follow-up | `validator_refs` in envelope |
| Event ID | **`event_id`** on new `pipeline-events.jsonl` and `harness-events.jsonl` lines (`evt_YYYYMMDD_HHMMSS_<hex>`), plus **`fork_id`**, **`envelope_version`**, optional **`replay_mode`** (`proposal` \| `merge` \| `gate` \| `debate` \| `dyad` \| `policy`) | Richer envelope with `record_refs`, `routing`, … |
| Staged → merge chain | **`parent_event_id`** on `applied` / `approved` / `rejected` lines when a matching prior **`staged`** row has **`event_id`**; **`candidate_ref`** (`recursion-gate.md#CANDIDATE-…`) on staged, gate, and applied | Full graph in one envelope |
| Merge batch (harness) | **`applied_pipeline_event_ids`** and **`staged_parent_event_ids`** on `merge_applied` (after per-candidate `applied` lines are written) | Single batch points at pipeline ids |

Emitted by: `scripts/emit_pipeline_event.py`, `bot/core.emit_pipeline_event`, `scripts/harness_events.append_harness_event`, `scripts/process_approved_candidates.py` (`append_pipeline_event`). Older JSONL lines omit these fields; readers should treat them as optional.

Operational doc: [harness-replay.md](harness-replay.md).

---

## Why this matters

Institutional memory lives in **approved Record artifacts** and **git + gated pipeline + small auditable core**—not session-only vendor memory. Harness Event Replay makes that design **inspectable**, not only asserted in prose.

**Priority:** High—improves **trust**, **debuggability**, and **governance clarity** together.

---

## Related

- [harness-replay.md](harness-replay.md) — CLI replay (audit + gate)  
- [boundary-review-queue.md](boundary-review-queue.md) — boundary classification product  
- [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md) — SELF vs SELF-LIBRARY  
- [harness-inventory.md](harness-inventory.md) — lanes and audit files  
- [architecture.md](architecture.md) — harness and boundaries  
