# work-dream

**Purpose:** Operator-facing doctrine, boundaries, and evolution history for Grace-Mar's `dream` ritual — the end-of-day consolidation pass. The executable trigger surface lives in [.cursor/skills/dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md).

**Not** Record truth. **Not** MEMORY. **Not** a second merge path.

---

## Role

| Role | Description |
|------|-------------|
| **Consolidation architecture** | Defines the shape of end-of-day maintenance: memory normalization, integrity, governance, contradiction digest, artifact drafts. |
| **Night-to-morning handoff** | Documents the `last-dream.json` data contract that bridges dream output to coffee Step 1. |
| **Boundary surface** | Explains what belongs in WORK-only docs/history versus what must escalate to `RECURSION-GATE`. |
| **Choreography with coffee** | Holds the rationale for the dream→coffee pairing: sequence, timing, data flow. |

---

## Relationship to `dream`

- **`dream` skill** = executable ritual contract, trigger behavior, script commands, return shape, guardrails.
- **`work-dream` territory** = prose home for rationale, boundaries, history, and evolution of the ritual.

This split mirrors `work-coffee`:

- the skill should stay optimized for invocation and agent behavior
- the territory should hold the longer-form doctrine and lane-specific history

---

## Gate threshold

`work-dream` is **WORK-only by default**.

Keep changes in docs/history only when they are about:

- maintenance semantics (what dream checks, in what order)
- strict mode behavior and when to use it
- handoff contract shape (`last-dream.json` fields)
- contradiction digest integration
- dream→coffee choreography

Stage to **`users/grace-mar/recursion-gate.md`** only when a `work-dream` insight would change governed behavior, such as:

- durable prompt or policy behavior
- changes to how integrity/governance checks affect the Record
- new artifact types that cross into Record territory

This territory never creates a second merge path. `RECURSION-GATE` remains the membrane.

---

## Script topology

```
auto_dream.py
  ├─ maintain_self_memory()        normalize self-memory.md
  ├─ validate-integrity.py         integrity checks (--json)
  ├─ governance_checker.py         governance scan
  ├─ contradiction_digest.py       derived contradiction digest
  │    └─ write_artifact_drafts()  optional artifact drafts
  ├─ emit_pipeline_event.py        maintenance event
  └─ _write_last_dream_handoff()   writes last-dream.json
```

**Bundle:** `operator_end_of_day.py` runs `auto_dream.py` then `operator_handoff_check.py` — night-side counterpart to `operator_reentry_stack.py`.

**Strict mode:** `--strict` tightens integrity parity, contradiction classification, and failure states. Same ritual, sharper posture. Use at end of week or after unusual maintenance events.

---

## Handoff contract

`last-dream.json` (written to `users/grace-mar/`) contains:

| Field | Type | Purpose |
|-------|------|---------|
| `generated_at` | ISO timestamp | When dream ran |
| `ok` | boolean | Overall pass/fail |
| `integrity_ok` | boolean | Integrity check result |
| `governance_ok` | boolean | Governance check result |
| `self_memory_changed` | boolean | Whether memory was normalized |
| `reviewable_count` | int | Reviewable items in contradiction digest |
| `contradiction_count` | int | Contradictions found |
| `artifact_draft_count` | int | Artifact drafts generated |
| `promotable_draft_count` | int | Drafts ready for promotion |
| `followups` | string[] | Human-readable follow-up items for morning |

Coffee Step 1 (`operator_daily_warmup.py`) reads this file and renders a **"Last dream (night handoff)"** block. The file is classified as runtime noise in `operator_handoff_check.py` — it does not need to be committed.

---

## Continuity and trail

`work-dream` does **not** replace any existing continuity surface.

- **Raw continuity:** `users/<id>/session-transcript.md`
- **Lane breadcrumbs:** `docs/skill-work/work-dream/work-dream-history.md`
- **Optional continuity memory:** `users/grace-mar/self-memory.md`
- **Governed durable changes:** `users/grace-mar/recursion-gate.md`

---

## Adjacent surfaces

- [.cursor/skills/dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md)
- [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md)
- [docs/skill-work/work-coffee/README.md](../work-coffee/README.md)
- [scripts/auto_dream.py](../../../scripts/auto_dream.py)
- [scripts/operator_end_of_day.py](../../../scripts/operator_end_of_day.py)

---

## Scope boundaries

In scope:

- end-of-day consolidation architecture
- maintenance semantics and strict mode
- contradiction digest integration
- handoff contract design
- dream→coffee choreography
- night-side operator ergonomics

Out of scope:

- morning re-entry or orientation (that's coffee)
- Record merges or prompt edits without the gate
- generic repo hygiene (coffee B / handoff-check)
- work-politics or other territory content
