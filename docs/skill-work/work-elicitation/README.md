# work-elicitation

**Objective:** Bounded WORK lane for extracting tacit operator knowledge into structured, review-first artifacts.

_Not:_ Record truth; not Voice knowledge; not a substitute for `users/<id>/self.md` or RECURSION-GATE queue.

---

## Purpose

This lane exists to solve the gap between:
- what the operator actually does,
- what the system can explicitly act on,
- and what downstream lanes need in order to be useful.

The target is not abstract self-description.
The target is operational clarity.

---

## Core questions

This lane tries to make five classes of tacit knowledge more explicit:

1. **Rhythms** — How does the operator actually work across day / week / month? What is the real pattern, not the idealized one?
2. **Recurring decisions** — What judgments recur? What makes a decision easy, hard, urgent, deferrable, or escalatable?
3. **Dependencies** — What people, systems, sources, and timing dependencies shape the work?
4. **Friction** — What repeatedly wastes attention, time, or momentum?
5. **Thresholds** — What counts as good enough? When should the system escalate, stop, continue, or ask?

---

## Boundary

- **WORK-only** drafts and operator notes live here.
- **Not** a second memory surface.
- **Not** direct merge authority into any other lane.
- **Yes** to structured operator workflow extraction.
- **Yes** to review-first artifacts that can inform cadence, strategy, think, and write.
- **Yes** to staged promotion or reuse after explicit review.
- **Promotion to Record / Voice:** only via **RECURSION-GATE** + companion approval + `process_approved_candidates.py` per [AGENTS.md](../../../AGENTS.md).

### Governing gate

Default: `users/<id>/recursion-gate.md` with `territory: work-elicitation` when staging companion-facing facts.

### Membrane (downstream lanes)

This lane may inform:
- `work-cadence`
- `work-strategy`
- `skill-think`
- `skill-write`

Downstream lanes consume elicitation outputs by reference or selective copy — not automatic propagation.

---

## Suggested workflow

1. Run a bounded elicitation pass.
2. Capture raw answers in a session note under `elicitation-sessions/`.
3. Compile answers into the five operator-working files.
4. Run a contradiction pass across layers (do stated rhythms match stated frictions? do thresholds contradict decision logic?).
5. Review and edit for usefulness.
6. Route selected lines into downstream lanes only if needed.

---

## Success criterion

This lane is successful when downstream work becomes easier because the operator's tacit patterns are more explicit and more reusable.

Elicitation outputs should be:
- concrete
- operational
- reviewable
- useful to a downstream lane

They should not become bloated autobiographical notes.

---

## Contents

| Doc / path | Role |
|------------|------|
| `README.md` | This file |
| `operator-rhythm.md` | Real operating rhythm |
| `operator-decisions.md` | Recurring judgment patterns and decision classes |
| `operator-dependencies.md` | People, systems, sources, and timing dependencies |
| `operator-frictions.md` | Recurring bottlenecks and energy drains |
| `operator-thresholds.md` | Escalation, sufficiency, review, and stop/continue thresholds |
| `work-elicitation-history.md` | Append-only operator trail |
| `elicitation-sessions/` | Optional raw or semi-structured session material |

---

## Related

- [work-template/README.md](../work-template/README.md) — full WORK pattern library (tiers, ledger, mapping)
- [work-template.md](../work-template.md) — new lane checklist
- [work-modules-history-principle.md](../work-modules-history-principle.md) — history log convention
- [work-menu-conventions.md](../work-menu-conventions.md) — operator menu conventions
- Upstream model: [OB1 Work Operating Model Activation](https://github.com/NateBJones-Projects/OB1/tree/main/recipes/work-operating-model-activation) — five-layer extraction framework (this lane diverges at layer 4: thresholds instead of institutional knowledge)
