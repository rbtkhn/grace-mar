# Contradiction Resolution

**Purpose:** Define how to handle conflicts between new evidence and existing SELF/SKILLS claims. Preserves history instead of overwriting; requires explicit user resolution.

**Status:** Specification for approved improvement #2 (Contradiction surfacing). Conflict detection in staging is implemented (`bot/conflict_check.py`, `bot/conflict_rules.yaml`).

**See also:** [anti-cheating.md](anti-cheating.md), [agents.md](../agents.md) (immutability rules)

---

## Principle

When new evidence contradicts an existing claim, do **not** overwrite. Instead:

1. Surface the conflict
2. Preserve both the old claim and the new evidence
3. Record the user's resolution
4. Optionally supersede the old claim with a resolution pointer

---

## Resolution Record Format

When a conflict is resolved, record:

```yaml
superseded_entry:
  id: LEARN-0024                    # or CUR-*, PER-*
  original_claim: "fearful of swimming"
  superseded_at: 2026-02-25
  superseded_by: ACT-0015           # evidence that contradicted
  resolution: growth                # user-chosen resolution type
  resolution_note: "Overcame fear; joined swim team. Growth, not contradiction."
```

### Resolution Types

| Type | Meaning |
|------|---------|
| **growth** | The new evidence shows development; old claim was true then, new is true now |
| **correction** | The old claim was wrong; new evidence corrects it |
| **context** | Both can be true in different contexts; keep both with clarification |
| **reject_new** | User rejects the new evidence; keep old claim |
| **exception** | Edge case; document why both coexist |

---

## Conflict Detection (Implemented)

The pipeline runs `bot/conflict_check.py` before appending to RECURSION-GATE. It:

1. Compares new personality candidates to existing SELF traits (seed + IX-C)
2. Flags contradictions using `bot/conflict_rules.yaml` (e.g., dependent vs independent)
3. Appends `conflicts_detected` to the candidate YAML; user sees the flag in RECURSION-GATE
4. Does **not** block staging — surfaces for user resolution (approve/reject/merge)

Rules are editable in `conflict_rules.yaml`. V1 covers personality opposites only; knowledge/curiosity checks can be added later.

On resolution (when user approves), add `superseded_by` / `superseded_entry` per the format above.

---

## Temporal Validity (Future)

When temporal validity layer (#3) is implemented, resolved claims get:

- `valid_from: 2026-02-19`
- `valid_until: 2026-02-25` (or `superseded_by` reference)
- `superseded_by: LEARN-0025` (the new claim that replaces this one)

The fork state at time T is computed by filtering entries where `valid_from <= T` and `valid_until` is null or `> T`.

---

## Example

**Before (conflict detected):**

- SELF IX-C: "Fearful of swimming (deep water) — WRITE-0003"
- New candidate: "Joined swim team — observed at pool"

**After resolution (type: growth):**

- Old entry gets `superseded_by: ACT-0015`, `resolution: growth`
- New entry: PER-0002 "Overcame swimming fear; joined team — ACT-0015"
- History preserved: both the fear and the growth are in the record

---

*Last updated: February 2026*
