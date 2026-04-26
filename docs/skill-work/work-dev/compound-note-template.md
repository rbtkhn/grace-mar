# Compound note template

Copy the **YAML front matter** and section skeleton into a new file under `compound-notes/`, or use `scripts/new_work_dev_compound_note.py`.

---

**Example front matter:**

```yaml
---
date: YYYY-MM-DD
work_lane: work-dev
title:
source_pr:
source_commit:
affected_files: []
problem_type:
reusable_pattern:
self_catching_test: unknown
gate_candidate: false
record_status: work-only
---
```

# Compound Note: <title>

## Context

(What was being built or fixed; link to issue/PR if any.)

## What happened

(Factual sequence: what the agent and operator did.)

## Reusable lesson

(One or more patterns or rules worth reusing in future sessions.)

## Failure pattern

(What broke or nearly broke; class of error.)

## Self-catching test

Would the current Grace-Mar system catch this issue next time?

Choose one:

- yes
- no
- only-if-invoked-manually
- only-after-gate-promotion
- unclear

## Candidate follow-up

(Optional: tests, docs, or counterfactual run to schedule.)

## Gate recommendation

**Default:** No gate action. This note remains a **work-only** learning artifact.

If promotion to Record-related change is *recommended*, set `gate_candidate: true` in front matter and explain the **rationale and risk** here—still **not** a merge until the normal gate process runs.
