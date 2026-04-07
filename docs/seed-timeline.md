# Seed Timeline

**Companion-Self template -- Formation chronology for seed claims**

---

## Purpose

The Seed Timeline shows how a companion forms over time. For each seed claim, it reconstructs a chronological narrative from the append-only registry: when it first appeared, when recurrence began, when contradictions appeared, when confidence rose or fell, and when it was promoted, rejected, or expired.

This is one of the most compelling product surfaces in the system. It makes identity formation visible and legible.

---

## How it works

Since `seed-registry.jsonl` is append-only (every status change appends a new snapshot line), the full formation history is already stored. The timeline script reads all snapshots for a given `seed_id` and emits a sequence of events.

---

## Event types

| Event | Icon | Meaning |
|-------|------|---------|
| `first_observed` | `+` | Claim first appeared in the registry |
| `new_observation` | `o` | Additional observation recorded |
| `status_change` | `>` | Status transitioned (e.g. observed -> recurring) |
| `contradiction_appeared` | `!` | Conflicting evidence detected |
| `confidence_rose` | `^` | Confidence score increased |
| `confidence_fell` | `v` | Confidence score decreased |

---

## Example

```
  Timeline: seed-demo-005
  Claim: "reads chapter books independently"
  ----------------------------------------------------------------------
  2026-01-20 13:00:00  [+] first_observed            Claim first seen  (conf=0.15 rec=0.15)
  2026-01-27 14:00:00  [o] new_observation            observation #2    (conf=0.38 rec=0.38)
  2026-01-27 14:00:00  [>] status_change              observed -> weak_signal  (conf=0.38 rec=0.38)
  2026-02-05 15:00:00  [o] new_observation            observation #3    (conf=0.55 rec=0.55)
  2026-02-05 15:00:00  [>] status_change              weak_signal -> recurring  (conf=0.55 rec=0.55)
  2026-02-15 14:00:00  [o] new_observation            observation #4    (conf=0.68 rec=0.68)
  2026-02-15 14:00:00  [>] status_change              recurring -> candidate   (conf=0.68 rec=0.68)
```

---

## Seed Diff View

When a claim changes status, `emit_seed_diff.py` can produce an identity-diff JSON capturing the exact transition. These diffs use `category: "seed_transition"` and `sourceType: "seed"` in the identity-diff schema, and are renderable by the existing Record Diff Queue renderer.

Each diff captures:
- Before/after status
- Change summary with observation count and time span
- Confidence delta
- Recommended action (accept/defer/reject)
- Why it matters (human-readable impact statement)

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/seed_timeline.py` | Reconstruct formation timeline from registry history |
| `scripts/emit_seed_diff.py` | Emit identity-diff JSON on status transition |

---

## Cross-references

- [seed-registry.md](seed-registry.md) -- Claim lifecycle and append-only storage
- [seed-nursery.md](seed-nursery.md) -- Why claims stay in nursery
- [record-diff-queue.md](record-diff-queue.md) -- Diff rendering for governed changes
