# Change Review

**Grace-Mar:** Mirror of the [companion-self template](https://github.com/rbtkhn/companion-self/blob/main/docs/change-review.md) (same path). Update when syncing; see [merging-from-companion-self.md](merging-from-companion-self.md).

Companion-Self template · Governed self-revision doctrine (v1 entrypoint)

---

## Purpose

Change review is the governed pipeline for materially important post-seed changes to a companion instance.

It exists to answer a different question from seed phase:

- **Seed phase:** how a companion is formed before activation
- **Change review:** how a companion changes after activation without silent drift

Change review makes meaningful self-revision visible, reviewable, and provenance-preserving.

---

## Why change review exists

A persistent companion should not evolve only by passive accumulation of memories or by silent overwrites to active files.

When new evidence materially affects identity, curiosity, pedagogy, expression, memory governance, safety rules, or durable preferences, the system should:

1. preserve the prior state
2. surface the proposed change
3. classify the nature of the change
4. record supporting evidence
5. require an explicit decision before governed state is updated

This keeps the companion coherent over time and preserves trust for operators, guardians, and future audits.

---

## Relationship to seed phase

Seed phase establishes the initial baseline before activation.

Change review begins **after activation** and governs significant revisions to that baseline.

Seed phase answers:
- who this companion is at the start
- what confidence exists at activation
- whether activation is allowed

Change review answers:
- what is changing now
- why it is changing
- whether the new evidence should refine, supersede, or be rejected
- how the change should be preserved in history

Seed phase and change review should remain separate subsystems.

---

## Relationship to the live Record

Change review is a governance layer around Record updates.

It does **not** replace the canonical queue, the identity fork protocol, or instance-specific merge logic.

Instead, it adds a review object around important changes so the instance can distinguish:

- a staged candidate
- a proposed identity or policy change
- a final decision
- an auditable state transition

The live Record remains the durable truth surface in the instance repo.
Change-review artifacts are review and audit objects, not replacements for the Record.

---

## When change review is required

Change review should be triggered for materially important changes, including:

- durable identity changes
- curiosity-priority changes
- pedagogy-style changes
- expression-style changes
- memory-governance changes
- safety or boundary changes
- durable preference changes
- template-upgrade collisions that affect governed state

Small ephemeral updates or ordinary session memory do not require change review unless instance policy says otherwise.

---

## Core review objects

A first-class change-review flow should include these objects:

- **proposal** — a structured statement of the proposed change
- **supporting evidence** — the evidence, interaction, or upgrade signal that triggered review
- **classification** — the type of contradiction or change
- **diff** — visible before / after comparison
- **decision** — approved, deferred, rejected, or superseded
- **event log** — audit-visible record of what happened and when

These objects may be implemented with JSON artifacts and a human-readable diff view.

---

## Review states

A proposal should move through these states:

- `proposed`
- `under_review`
- `approved`
- `deferred`
- `rejected`
- `superseded`

Instances may add local detail, but the high-level state model should remain stable across implementations.

---

## Decision rules

Change review follows these rules:

1. **No silent overwrite**
   Material state changes should not overwrite prior governed state without an explicit decision.

2. **Preserve provenance**
   Prior state, new evidence, and decision rationale should remain inspectable.

3. **One canonical review path**
   Instances may derive UI or helper files, but should keep one canonical review queue or queue-integrated review flow.

4. **Agent may stage; gate decides**
   The system may detect and stage a proposed change, but merge authority remains with the instance’s human gate and merge doctrine.

5. **History is preserved**
   A decision may supersede prior state, but should not erase the fact that prior state existed.

---

## Provenance requirements

Every materially important proposed change should preserve:

- prior state reference
- proposed state reference
- evidence reference(s)
- contradiction or change type
- confidence delta if available
- decision
- decision rationale
- timestamp(s)

Without provenance, change review loses most of its value.

---

## Integration with upgrades

Template upgrades must not silently override instance-level governed state.

If a template upgrade collides with instance identity, pedagogy, memory governance, safety rules, or prior seed outputs, the instance should open a change proposal rather than auto-merge the change into active governed state.

This is especially important for high-trust or education-oriented instances.

---

## Relationship to existing contradiction docs

This document is the doctrine entrypoint for governed self-revision.

Related documents may provide narrower or deeper treatment:

- contradiction resolution at the evidence / claim level
- engineering spec for identity-diff workflow
- approval inbox / review UI details
- identity fork merge rules

Those documents should remain aligned with this doctrine.

---

Companion-Self template · Change review v1
