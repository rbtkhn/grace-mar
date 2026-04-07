# Weak Signal Nursery

**Companion-Self template -- Holding space for immature observations**

---

## Purpose

Not everything should be either ignored or promoted. The nursery is the space between: observations that are interesting but not yet ready for governed state. It makes restraint intelligible by explaining *why* each claim is still provisional and *what* would change that.

---

## What the nursery is

A **view** over the Seed Registry, not a separate store. Claims with status `observed`, `weak_signal`, or `recurring` are nursery residents. The nursery report adds computed explanations drawn from the promotion threshold engine.

---

## What each nursery card shows

For every resident claim:

| Surface | What it answers | Example |
|---------|----------------|---------|
| **Why it is interesting** | What was observed, in what category | "Observed 3 times in curiosity category, recurring across 3 sessions" |
| **Why it is still a seed** | Which promotion thresholds are unmet | "insufficient recurrence (1 observation, need 2)" |
| **What would mature this** | Required evidence to cross promotion threshold | "2 more sessions, evidence from non-identical contexts" |
| **What would falsify this** | What evidence would weaken or contradict the claim | "explicit statement contradicting this claim" |
| **Whether it affects behavior yet** | Does this claim influence soft exploration without entering governed state | "no (not yet influencing recommendations)" |
| **When to review again** | Expiry review date or computed deadline | "2026-05-06" |

---

## "What seeds are shaping behavior already?"

Important distinction: some nursery claims may influence **soft exploration** without entering governed state.

| May influence | May not influence |
|---------------|-------------------|
| Question suggestions | Durable profile fields |
| Curiosity prompts | Identity statements |
| Topic exploration order | External actions |
| Session activity ideas | Governed preferences |

A claim at `recurring` or `candidate` status *may* shape soft exploration. A claim at `observed` or `weak_signal` *should not* shape anything yet. The nursery report flags this explicitly.

---

## Script

```bash
python3 scripts/seed_nursery_report.py -u demo
python3 scripts/seed_nursery_report.py --seed-id seed-demo-003
python3 scripts/seed_nursery_report.py --json
```

---

## Example output

```
seed-demo-003: "says they want to be an astronaut" (identity)
  Status: weak_signal
  Why interesting: Observed 2 time(s) in identity category; Recurring across 2 session(s) over 19 day(s)
  Still a seed because: conflicting evidence (1 contradiction(s)); sensitivity tier requires operator flag
  Would mature with: explicit operator confirmation; contradiction resolution or preservation note
  Would falsify with: existing contradictions: seed-demo-004; explicit statement contradicting this claim
  Affects behavior: no (not yet influencing recommendations)
  Review by: 2026-03-05
```

---

## Cross-references

- [seed-registry.md](seed-registry.md) -- Claim lifecycle and storage
- [seed-promotion-thresholds.md](seed-promotion-thresholds.md) -- Rules that determine nursery exit
- [seed-timeline.md](seed-timeline.md) -- Formation chronology for individual claims
- [seed-phase-doctrine.md](seed-phase-doctrine.md) -- "The system may assist formation, but may not silently define the companion"
