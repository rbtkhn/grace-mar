# Change Review Lifecycle

Companion-Self template · Proposal-to-decision flow

---

## Purpose

This document defines the canonical lifecycle for materially important post-seed changes.

The lifecycle should be stable even if specific instances implement different tools or UI layers.

---

## Persistence model (layers → review)

End-to-end ordering for **material** changes (complements the numbered lifecycle below):

1. **Evidence** — raw or staged source material ([Evidence Layer](evidence-layer.md))
2. **Prepared context** — normalized or structured inputs for reasoning ([Prepared Context Layer](prepared-context-layer.md))
3. **Proposal artifact** — the first **formal persisted review object** is typically a Change Proposal v1 JSON file in `review-queue/proposals/` (see [state-proposals.md](state-proposals.md))
4. **Review** — classification, diff, human or policy gate
5. **Merge or reject** — governed state updates only after an explicit decision; no silent overwrite

Narrative stage docs: [pipeline/evidence-to-proposal.md](pipeline/evidence-to-proposal.md), [pipeline/proposal-to-review.md](pipeline/proposal-to-review.md), [pipeline/review-to-merge.md](pipeline/review-to-merge.md). Reference flow across layers: [evidence-to-context-pipeline.md](evidence-to-context-pipeline.md).

**Observability:** Operators should be able to see **where each proposal sits** in this lifecycle (e.g. via `review-queue/` artifacts and optional [observability reports](observability.md)).

**Authority:** Transition into governed state should respect the [authority map](authority-map.md). **Action receipts** may be used to make lifecycle transitions inspectable without substituting for the Record ([action-receipts.md](action-receipts.md)).

---

## Lifecycle

### 1. Detect

A possible governed change is detected from one or more sources:

- staged interaction evidence
- operator note
- guardian note
- policy signal
- seed artifact re-interpretation
- template upgrade collision
- validation output

Detection does not change governed state by itself.

**Prepared context:** Review inputs may be produced from [prepared context](prepared-context-layer.md) artifacts (summaries, bundles, structured drafts). Prepared context itself is **not** governed state until a proposal is accepted and merged through this lifecycle or the gate.

---

### 2. Propose

The system creates or prompts creation of a structured proposal containing:

- scope
- prior state reference
- proposed state reference
- supporting evidence
- contradiction or change type
- initial risk estimate
- initial confidence delta if available

The item enters review in `proposed` state.

---

### 3. Classify

The proposal is classified using contradiction policy.

Typical classifications:
- contradiction
- refinement
- expansion
- deprecation
- ambiguity
- policy collision
- template-instance collision

Classification should happen before merge.

---

### 4. Render diff

A visible before / after comparison is generated.

At minimum, the diff should show:
- prior governed state
- proposed governed state
- what evidence triggered the change
- what kind of contradiction or change is being claimed

This is the most important operator-facing surface in the flow.

---

### 5. Review

The proposal is reviewed by the governing human gate or instance-defined review path.

Review may:
- approve
- defer
- reject
- supersede an earlier proposal

High-impact user-facing or policy-colliding changes should not bypass this step.

---

### 6. Decide

A decision record is created with:
- decision status
- rationale
- blocking issues, if any
- follow-up actions, if any
- references to affected governed files or objects

No governed merge should occur without this decision step.

---

### 7. Merge or preserve

If approved, the change is merged according to instance doctrine.

If deferred or rejected, the active governed state remains unchanged.

In all cases:
- prior state remains historically visible
- proposal and decision remain auditable
- event history remains inspectable

---

### 8. Log

Every major lifecycle action should appear in an event log, for example:
- proposal created
- proposal classified
- diff generated
- decision made
- merge applied
- proposal superseded
- merge reverted

---

## Non-goals

This lifecycle does not:
- replace the canonical staging queue
- grant autonomous merge authority to the agent
- flatten all memory updates into governance events
- erase prior governed state

---

Companion-Self template · Change-review lifecycle v1
