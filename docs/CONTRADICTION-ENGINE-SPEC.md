# CONTRADICTION-ENGINE-SPEC

**Companion-Self template ·** implementation-ready engineering spec  
**Purpose:** define a first-class contradiction and change-review engine for instances that upgrades conflict handling from a passive flag into a governed identity-diff workflow.  
**Scope:** recursion-gate (queue), review UI, merge logic, temporal validity, and audit events.  
**Non-Goal:** replace the canonical queue, bypass the human gate, or introduce autonomous merge authority.

**Primary sources:**  
- [README.md](../README.md)
- [change-review.md](change-review.md) — governed self-revision doctrine (v1); this spec **operationalizes** that doctrine (queue-integrated objects, UI, merge, audit)
- [contradiction-policy.md](contradiction-policy.md) — contradiction classes and resolution policy under change review
- [change-types.md](change-types.md) — canonical proposal scopes
- [change-review-lifecycle.md](change-review-lifecycle.md) — proposal-to-decision lifecycle
- [approval-inbox-spec.md](approval-inbox-spec.md)
- [contradiction-resolution.md](contradiction-resolution.md)
- [identity-fork-protocol.md](identity-fork-protocol.md)
- [instance-patterns.md](instance-patterns.md)

**Reference implementation:** [Grace-Mar CONTRADICTION-ENGINE-SPEC](https://github.com/rbtkhn/grace-mar/blob/main/docs/CONTRADICTION-ENGINE-SPEC.md) — concrete paths, scripts, and gate-review-app wiring.

---

## 1. Goal

Turn contradiction handling into a first-class review flow that answers:

**How should the identity model change in light of new evidence?**

This engine must:
- detect when a staged candidate materially conflicts with an active SELF or skill claim
- render a structured “before / proposed / after” diff
- require an explicit human resolution type
- preserve full history
- update active state deterministically after approval
- keep all actions audit-visible

This is a **review and merge-governance layer**, not a replacement memory system.

---

## 2. Architectural Constraints (MUST PRESERVE)

The engine must preserve these rules (see [long-term-objective.md](long-term-objective.md), [identity-fork-protocol.md](identity-fork-protocol.md)):

- the agent may stage; it may not merge
- the **canonical queue** remains the instance’s staging surface (`recursion-gate.md` with markdown blocks, or `recursion-gate.json` per [instance-patterns.md](instance-patterns.md)—one queue, one truth)
- candidate `status: pending | approved | rejected` (or equivalent) remains canonical
- approved candidates remain in queue until merge runs
- all review actions remain audit-visible (e.g. `pipeline-events.jsonl` where the instance uses it)
- derived UI fields and helper artifacts are allowed
- no second source of truth may be introduced

Contradiction handling must therefore be implemented as:

1. canonical staged candidate in queue  
2. derived contradiction analysis object  
3. explicit operator resolution  
4. deterministic merge into canonical profile/history files

---

## 3. Problem Statement

Contradiction surfacing is useful but often incomplete.

Today instances may:
- run an advisory conflict check before merge
- surface flags on candidates
- require human resolution at the gate

But the operator may still see primarily a **candidate**, not an **identity change decision**.

The real decision is:
> “Does this new evidence reinforce, refine, contextualize, contradict, or replace the current model of the person?”

This spec formalizes that distinction.

---

## 4. Product Definition

A **contradiction** becomes a **first-class identity-diff object** when:

- there is an active existing claim in SELF (unified or split: self-knowledge, self-identity, self-curiosity, self-personality) or skill containers
- a staged candidate materially overlaps the same domain, topic, or trait
- the relationship is not best explained as simple reinforcement or duplication
- a human reviewer would reasonably need to decide how the active model should change

---

## 5. Relation Classification Model

Classify each staged candidate against relevant active entries:

### 5.1 `reinforcement` — standard path; optional confidence append  
### 5.2 `duplicate` — duplicate hint; no contradiction workflow unless override  
### 5.3 `refinement` — contextual merge path  
### 5.4 `contradiction` — full workflow; quick merge disabled; explicit resolution before merge  

---

## 6. Canonical vs Derived Data

### 6.1 Canonical
Per instance layout (see [instance-patterns.md](instance-patterns.md)):

- `users/<id>/recursion-gate.md` **or** `users/<id>/recursion-gate.json`
- SELF: `self.md` and/or `self-knowledge.md`, `self-identity.md`, `self-curiosity.md`, `self-personality.md`
- `self-evidence.md`
- skill files as used (`self-skill-think.md`, etc.)
- `pipeline-events.jsonl` (or instance audit log)

### 6.2 Derived
Sidecar artifacts, e.g.:

- `users/<id>/derived/conflicts/CONFLICT-0001.json`
- `users/<id>/derived/conflict-index.json`

Prefer **gitignore** on `users/*/derived/`. Rebuild from queue + profile. Never outrank canonical files.

---

## 7. Contradiction Object Schema

Same field model as Grace-Mar reference. Example:

```json
{
  "conflict_id": "CONFLICT-0007",
  "candidate_id": "CANDIDATE-0142",
  "status": "pending_review",
  "profile_target": "IX-C",
  "mind_category": "personality",
  "existing_entry_id": "PER-0018",
  "existing_claim_text": "fearful of swimming in deep water",
  "incoming_summary": "joined swim team confidently",
  "relationship_type": "contradiction",
  "conflict_strength": 0.91,
  "recommended_resolution": "growth",
  "operator_decision": null
}
```

**Required:** `conflict_id`, `candidate_id`, `status`, `existing_entry_id`, `incoming_summary`, `relationship_type`, `conflict_strength`, `recommended_resolution`.  
**Optional:** `prompt_impact`, `confidence_delta`, `incoming_excerpt`, `operator_note`, `resolved_by`.

**Alignment with change-review:** [`identity-diff.v1.json`](../schema-registry/identity-diff.v1.json) is the governed **before/after** envelope for proposals. Map conceptually: existing vs incoming narrative → `before` / `after` objects; `conflict_id` / `candidate_id` / evidence ids → `evidenceRefs` and linkage from a parent [change proposal](../schema-registry/change-proposal.v1.json). Instances may keep **CONFLICT-*** sidecars for detection/triage while rendering or exporting an `identity-diff` for the operator-facing diff step.

---

## 8. Scoring Model

Three scores: **existing claim confidence**, **incoming evidence confidence**, **conflict strength** (each 0.00–1.00). **Confidence delta** for triage and inbox ordering.

---

## 9. Resolution Types

Fixed vocabulary (see [contradiction-resolution.md](contradiction-resolution.md)):

`growth` | `correction` | `context` | `reject_new` | `exception`

Merge behaviors: supersession with history, correction without developmental framing, dual context, reject new, exception / limited scope.

---

## 10. Temporal Validity Model

Support `valid_from`, `valid_until`, `superseded_by`, `active`, `resolution`, `resolution_note` on affected entries. Active state at time T: `valid_from <= T` and (`valid_until` null or `> T`).

---

## 11. Review UI Requirements

**Before** (claim, id, confidence, refs, dates) · **Proposed** (summary, excerpt, reasons, recommended resolution, strength) · **After** (preview of active claims, supersession, prompt impact) · **Actions** (resolution type, note, approve/reject/defer, confirm prompt delta).

---

## 12. Queue and Risk Rules

Contradictions are **not** quick-merge eligible. Default **manual_escalate**. Derived UI fields (`has_conflict_markers`, `conflict_strength`, etc.) unless written into queue by explicit schema upgrade.

---

## 13. API Surface

Expose on the **instance operator review layer** (web inbox, gate dashboard API). Illustrative endpoints:

- `GET /api/review/conflicts` — filter unresolved  
- `GET /api/review/conflicts/<id>` — full payload  
- `GET /api/review/preview/<candidate_id>` — merge preview  
- `POST /api/review/conflicts/<id>/resolve` — decision + optional approve + prompt delta flag  
- `GET /api/review/history` — resolved events  

Grace-Mar maps these to `gate-review-app` / inbox; new instances implement per stack.

---

## 14. Merge Logic

Staging → detection vs active Record → classification → if contradiction, generate `CONFLICT-*` → human resolution → merge (queue, SELF/skill files, evidence, temporal fields, prompt, audit) → archive conflict summary.

---

## 15. Audit Events

Append lifecycle events to instance audit log (e.g. `conflict_detected`, `conflict_resolved`, `identity_superseded`, `prompt_delta_applied`). Additive; do not replace queue state.

---

## 16. Dashboard Requirements

Operator dashboard should add contradiction metrics, saved views (`likely_growth`, `likely_correction`, etc.), and distinct conflict cards (collapsed + expanded before/proposed/after).

---

## 17. Prompt Safety Rule

Never silently change Voice/emulation prompt. Preview prompt impact; operator must explicitly allow prompt update; audit whether delta applied.

---

## 18. File and Script Additions (instance)

- This spec  
- Reference: Grace-Mar [CONTRADICTION-ENGINE-FLOW](https://github.com/rbtkhn/grace-mar/blob/main/docs/CONTRADICTION-ENGINE-FLOW.md), [conflict-object.schema.json](https://github.com/rbtkhn/grace-mar/blob/main/docs/schemas/conflict-object.schema.json)  
- Optional: `scripts/build_conflict_index.py`, `resolve_conflict.py`, `render_conflict_cards.py`  
- `users/<id>/derived/conflicts/` (gitignored)  
- Extend gate parser, merge tooling, dashboard generators per instance

---

## 19–21. Phases, MVP, Principle

**Phases:** (1) detection + sidecars + counts, (2) review UI + resolution + prompt preview, (3) temporal merge, (4) analytics.  
**MVP:** classify → CONFLICT object → cards → required resolution → supersession metadata → lifecycle events.  
**Principle:** **Never ask the operator to approve a raw candidate when the real question is how the identity model should change.**

---

*Template: companion-self. Reference implementation: [grace-mar](https://github.com/rbtkhn/grace-mar).*
