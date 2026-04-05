# Contradiction Resolution

**Purpose:** Define how instances handle conflicts between new evidence and existing SELF / skill claims. Preserve history instead of overwriting; require explicit human resolution at the gate.

**Status:** Template specification. Instances may implement advisory conflict checks before merge (see [instance-patterns.md](instance-patterns.md) § conflict check).

**See also:** [change-review.md](change-review.md) (governed self-revision doctrine entrypoint), [contradiction-policy.md](contradiction-policy.md) (classification during change review), [source-of-truth.md](source-of-truth.md), [conflict-resolution-order.md](conflict-resolution-order.md), [CONTRADICTION-ENGINE-SPEC.md](CONTRADICTION-ENGINE-SPEC.md) (governed identity-diff workflow, UI, merge, audit), [identity-fork-protocol.md](identity-fork-protocol.md)

---

## Principle

When new evidence contradicts an existing claim, do **not** overwrite. Instead:

1. Surface the conflict  
2. Preserve both the old claim and the new evidence  
3. Record the companion’s (or delegated human’s) resolution  
4. Optionally supersede the old claim with a resolution pointer  

---

## Resolution Record Format

When a conflict is resolved, record (shape may live in self-evidence or dimension files per instance):

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

## Conflict Detection (instance option)

Before merge, an instance may run an **advisory** conflict check: compare staged content to existing Record (e.g. IX-A, IX-B, IX-C). Surface for resolution; **do not block staging** unless instance policy explicitly requires it. The companion still decides at the gate.

Reference implementation: Grace-Mar `bot/conflict_check.py` + `bot/conflict_rules.yaml`.

---

## Temporal Validity (future)

Resolved claims may gain `valid_from`, `valid_until`, `superseded_by`. Fork state at time T: entries where `valid_from <= T` and `valid_until` is null or `> T`. See CONTRADICTION-ENGINE-SPEC §10.

---

*Template doc. Last updated: March 2026.*
