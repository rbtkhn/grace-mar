# work-build-ai delivery playbook

First-pass delivery model for the `work-build-ai` business layer.

Use this file to turn the territory's thesis into a repeatable services method.

---

## Default phases

| Phase | Purpose | Typical output |
|------|---------|----------------|
| **1. Diagnostic** | Understand stack, pain, lock-in / provenance risks; **inventory tail + high-stakes workflows** (where average accuracy hides failure) | Diagnostic memo + tail list |
| **2. Architecture proposal** | Define `record` vs `runtime` boundary, target contract, and **autonomy tiers** (what the agent may do alone vs shadow vs human-only) | Architecture summary + autonomy matrix |
| **3. Bounded implementation** | Build one agreed workflow or integration surface | One delivered surface, not a giant platform |
| **4. Audit and provenance check** | Verify behavior, handback, approval boundaries; **deterministic consistency checks** (stated analysis vs action); **sample passed runs** for false negatives; optional **factorial pilot** on one workflow ([variation-types.md](variation-types.md)) | Validation notes + any new eval cases |
| **5. Handoff / next-step plan** | Make the system usable after the sprint | Operator notes and next recommended actions |

**Reliability reference:** [agent-reliability-playbook.md](agent-reliability-playbook.md).

---

## What not to do

- do not sell a sprawling transformation before proving one bounded surface
- do not let implementation outrun the client's ability to understand the contract
- do not confuse runtime continuity with canonical truth

---

## Guardrail

The delivery method should keep human control and auditability visible throughout the engagement, not just at the end.
