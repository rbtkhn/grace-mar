# Change Types

Companion-Self template · Governed change scopes

---

## Purpose

This document defines the major scopes of change that may enter change review.

The goal is to keep change proposals legible and comparable across instances.

---

## Canonical change scopes

### identity
Durable self-description, role commitments, boundaries, values, or relationship stance.

### curiosity
Durable topic priorities, question style, exploration depth, or inquiry limits.

### pedagogy
Teaching method, scaffolding strategy, correction style, pace, encouragement style, or anti-spoonfeeding rules.

### expression
Writing cadence, length norms, examples, formatting preferences, or tone envelope.

### memory_governance
Retention rules, provenance rules, deletion rules, sensitive-category handling, editable vs protected regions.

### safety
Boundaries, refusals, guardian constraints, restricted domains, escalation rules.

### preference
Durable user-facing likes, dislikes, or recurring response preferences that materially affect operation.

### upgrade_collision
A template or schema change that collides with instance-level governed state.

---

## Multi-scope proposals

A single proposal may affect more than one scope, but it should still name one **primary** scope.

Example:
A pedagogy change that also alters expression should usually be filed as `pedagogy` with secondary notes about expression.

---

## Scope discipline

Do not use generic or catch-all scopes when a more precise one exists.

Good classification improves:
- auditability
- human review
- merge logic
- future analytics across instances

---

Companion-Self template · Change scopes v1
