# Narrative Feedback Loop Ledger

**Purpose:** Convergence Ledger for rolling daily-brief analysis. Tracks companion signals and agent interpretations with explicit decisions and follow-up tests.

**Boundary:** WORK-only process memory. This file is not Record truth and does not bypass gated pipeline rules.

---

## Entry Template

```markdown
### NARR-YYYYMMDD-XX
- timestamp: YYYY-MM-DD HH:MM UTC
- domain: work-strategy|work-politics|work-dev|mixed
- companion_signal: "<what the companion/operator emphasized>"
- agent_interpretation: "<assistant narrative synthesis or recommendation>"
- decision: accept|defer|reject
- rationale: "<1-3 lines explaining why>"
- confidence: high|medium|low
- impact: high|medium|low
- next_test: "<observable test for next run>"
- review_by: YYYY-MM-DD (required when decision=defer)
- supersedes: NARR-YYYYMMDD-XX (optional)
- source_briefs:
  - daily-brief-YYYY-MM-DD.md
  - daily-brief-YYYY-MM-DD.md
```

## Required decision rules

- `accept`: includes one concrete operational implication.
- `defer`: must include `review_by`.
- `reject`: include one short contradiction reason.
- If no `next_test`, do not log unless `impact=high`.

---

## Active Ledger

<!-- Add newest entries at top -->

### NARR-20260331-01
- timestamp: 2026-03-31 18:00 UTC
- domain: work-strategy
- companion_signal: "Need narrative skill to improve content creation and recursive learning."
- agent_interpretation: "Convergence Ledger v2 should be the default operating model for skill-narrative."
- decision: accept
- rationale: "Improves continuity and auditability while preserving companion authority."
- confidence: high
- impact: high
- next_test: "Run next 3-brief synthesis using this schema and verify at least one output is adopted."
- review_by: n/a
- supersedes: n/a
- source_briefs:
  - daily-brief-2026-03-27.md
  - daily-brief-2026-03-28.md
  - daily-brief-2026-03-31.md

---

## Weekly Defer Sweep

Use this block in the weekly sweep. Move resolved items to Archive.

```markdown
### SWEEP-YYYY-MM-DD
- reviewed_deferred: <count>
- closed: <ids>
- extended: <ids + new review_by>
- promoted: <ids + reason>
- notes: "<what changed in the model this week>"
```

---

## Archive

Move closed entries here with original IDs intact.
