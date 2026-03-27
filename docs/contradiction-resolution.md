# Contradiction Resolution

**Purpose:** Define how instances handle conflicts between new evidence and existing SELF / skill claims. Preserve history instead of overwriting; require explicit human resolution at the gate.

**Status:** Template specification, with **Grace-Mar** advisory conflict detection implemented (`bot/conflict_check.py`, `bot/conflict_rules.yaml`) before RECURSION-GATE append.

**See also:** [change-review.md](change-review.md) (governed self-revision doctrine entrypoint), [contradiction-policy.md](contradiction-policy.md), [CONTRADICTION-ENGINE-SPEC.md](CONTRADICTION-ENGINE-SPEC.md) (governed identity-diff workflow, UI, merge, audit), [contradiction-timeline.md](contradiction-timeline.md), [identity-fork-protocol.md](identity-fork-protocol.md); [companion-self mirror](https://github.com/rbtkhn/companion-self/blob/main/docs/contradiction-resolution.md).

---

## Principle

When new evidence contradicts an existing claim, do **not** overwrite. Instead:

1. Surface the conflict  
2. Preserve both the old claim and the new evidence  
3. Record the companion’s (or delegated human’s) resolution  
4. Optionally supersede the old claim with a resolution pointer  

---

## Resolution Record Format

When a conflict is resolved, record (shape may live in self-archive or dimension files per instance):

```yaml
superseded_entry:
  id: LEARN-0024
  original_claim: "fearful of swimming"
  superseded_at: 2026-02-25
  superseded_by: ACT-0015
  resolution: growth
  resolution_note: "Overcame fear; joined swim team. Growth, not contradiction."
```

### Resolution Types

| Type | Meaning |
|------|---------|
| **growth** | Old claim was true then; new evidence shows development |
| **correction** | Old claim was wrong; new evidence corrects it |
| **context** | Both true in different contexts; clarify scope |
| **reject_new** | Reject new evidence; keep old claim |
| **exception** | Edge case; document why both coexist |

---

## Conflict detection (Grace-Mar — implemented)

The pipeline runs `bot/conflict_check.py` before appending to RECURSION-GATE. It:

1. Compares new personality candidates to existing SELF traits (seed + IX-C)
2. Flags contradictions using `bot/conflict_rules.yaml` (e.g., dependent vs independent)
3. Appends `conflicts_detected` to the candidate YAML; the operator sees the flag in RECURSION-GATE
4. Does **not** block staging — surfaces for user resolution (approve / reject / merge)

Rules are editable in `conflict_rules.yaml`. V1 covers personality opposites only; knowledge / curiosity checks can be added later.

On resolution (when the user approves), add `superseded_by` / `superseded_entry` per the format above.

**Other instances:** Before merge, an instance may run an **advisory** conflict check per [instance-patterns.md](https://github.com/rbtkhn/companion-self/blob/main/docs/instance-patterns.md) § conflict check. Surface for resolution; do not block staging unless instance policy requires it.

---

## Temporal Validity (future)

Resolved claims may gain `valid_from`, `valid_until`, `superseded_by`. Fork state at time T: entries where `valid_from <= T` and `valid_until` is null or `> T`. See CONTRADICTION-ENGINE-SPEC §10.

---

## Example (Grace-Mar)

**Before (conflict detected):**

- SELF IX-C: "Fearful of swimming (deep water) — WRITE-0003"
- New candidate: "Joined swim team — observed at pool"

**After resolution (type: growth):**

- Old entry gets `superseded_by: ACT-0015`, `resolution: growth`
- New entry: PER-0002 "Overcame swimming fear; joined team — ACT-0015"
- History preserved: both the fear and the growth are in the record

---

*Template doc aligned with companion-self (March 2026); Grace-Mar implementation notes preserved.*
