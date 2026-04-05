# Change Review Lifecycle

Companion-Self template · Proposal-to-decision flow

---

## Purpose

This document defines the canonical lifecycle for materially important post-seed changes.

The lifecycle should be stable even if specific instances implement different tools or UI layers.

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
