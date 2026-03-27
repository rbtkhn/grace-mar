# Contradiction Policy

Companion-Self template · Contradiction classification and resolution policy

---

## Purpose

This document defines how materially important conflicts are classified during change review.

Not every new observation is a contradiction.
Some updates are refinements, contextual clarifications, or normal growth.

The goal is to classify change precisely enough that the instance can decide well without flattening all revision into a generic “memory update.”

---

## Core rule

When new evidence conflicts with governed state, do **not** silently overwrite the prior state.

Instead:

1. classify the conflict
2. preserve prior state and evidence
3. route the item through change review
4. record a decision
5. apply the resulting governed state change only after review

---

## Contradiction classes

### 1. Direct contradiction

The new evidence materially opposes the prior governed claim.

Example:
- prior state: prefers direct answers
- new evidence: repeated successful interactions show the learner disengages unless guided Socratically

This usually requires explicit review.

---

### 2. Refinement

The prior state was broadly correct, but the new evidence makes it more precise.

Example:
- prior state: likes concise explanations
- new evidence: likes concise explanations for facts, but more scaffolded ones for math

Refinement usually preserves the old claim in narrowed form.

---

### 3. Expansion

The new evidence adds a durable new capability, interest, or condition without negating the prior state.

Example:
- prior state: strong interest in stories
- new evidence: also shows durable interest in hands-on experiments

Expansion is not usually a contradiction, but may still require review if it changes teaching strategy or boundaries.

---

### 4. Deprecation

A prior rule, preference, or policy should no longer be active.

Example:
- prior state: a startup pedagogy rule used during seed
- new evidence: post-activation governance has replaced it

Deprecation should preserve history and pointer references.

---

### 5. Ambiguity

The system lacks enough evidence to determine whether the change is contradiction, refinement, or context shift.

Ambiguity should usually be deferred rather than merged.

---

### 6. Policy collision

The new change conflicts with an explicit policy, safety rule, memory boundary, or guardian/operator constraint.

Policy collisions are high-risk and should never be merged silently.

---

### 7. Template-instance collision

A template upgrade or schema-level change conflicts with established instance-level governed state.

This should open review instead of overwriting instance truth.

---

## Resolution types

A reviewed contradiction may resolve as:

- **growth** — old state was true then; new state reflects development
- **correction** — old state was wrong and is corrected
- **context** — both states hold in different settings or scopes
- **reject_new** — new evidence is insufficient or inappropriate
- **exception** — both states coexist as a documented edge case
- **supersede** — governed state should be replaced, with history preserved
- **defer** — more evidence or human review is needed

Instances may map these to local merge behavior, but should preserve the semantic distinction.

---

## Blocking vs non-blocking

### Blocking contradictions
These should halt automatic merge into governed state until review:

- safety or boundary conflicts
- memory governance conflicts
- guardian/operator policy conflicts
- template-instance collisions affecting active governed state
- direct contradictions in identity or pedagogy with meaningful downstream effects

### Non-blocking contradictions
These may remain staged or advisory unless local policy escalates them:

- low-confidence ambiguity
- low-impact preference drift
- narrow expression refinements
- contextual clarifications with low risk

---

## Preservation rule

Unresolved contradiction should be preserved without forced synthesis.

The system may defer, annotate, or constrain the active state, but should not pretend certainty where review has not actually resolved the issue.

---

## Human review triggers

Human review is strongly recommended when:

- the change affects a high-trust interaction mode (e.g. sensitive or policy-bound contexts)
- the change alters boundaries or safety posture
- the change materially affects identity or pedagogy
- the confidence delta is large
- the evidence is sparse but the proposed change is high-impact
- a template upgrade collides with instance-governed state

---

## Policy priority order

When conflicts stack, resolve in this order:

1. safety and guardian/operator constraints
2. memory-governance rules
3. durable identity commitments
4. pedagogy and education rules
5. curiosity and expression preferences
6. low-impact presentation refinements

---

Companion-Self template · Contradiction policy v1
