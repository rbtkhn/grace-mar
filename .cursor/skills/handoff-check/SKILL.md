---
name: handoff-check
description: Run operator_handoff_check.py for RECURSION-GATE pending, Predictive History night closeout, commits, worktree noise, re-entry prompt — read-only. On **good night**, this script is **daily-warmup Step 1**; **Step 2** is the fixed **A–E** night menu in daily-warmup § *Good night — multiple choice*. Also use when resuming work or checking safe-to-ignore before commit/push.
---

# Handoff Check

Use this skill when the operator wants to pause or resume work without losing the active thread.

**Preset — good night:** When the operator says **good night** (session end), the agent runs **good night Step 1** (this command + summary) then **good night Step 2** (A–E menu) — see [daily-warmup/SKILL.md](../daily-warmup/SKILL.md) § **Good night** and § *Good night — multiple choice (A–E required)*. On follow-up turns, **A–D** runs the track then **re-offers the full A–E menu** until **E** ends the night session.

**Good morning (related):** After **A–D**, **re-offer the full A–E morning menu** each turn until **E** — same loop as good night; see [daily-warmup/SKILL.md](../daily-warmup/SKILL.md) § *Good morning — multiple choice (A–E required)*.

## Default command

```bash
python3 scripts/operator_handoff_check.py -u grace-mar
```

## What to return

Summarize:

- **RECURSION-GATE** — pending totals (work-politics vs companion), listed items if any (script caps long queues), and the script’s **proposed** processing steps (`operator_gate_review_pass` → approve/reject in-file → `process_approved_candidates.py`); remind that **merge requires companion approval**
- **Predictive History (work-jiang)** — **`## Predictive History — night closeout`**: where the lane rests, suggested first lever tomorrow, rotating **Spark** (edit `research/external/work-jiang/metadata/warmup-sparks.yaml`), optional rebuild ritual; still read-only / not Record
- recently committed work
- meaningful local changes still in progress
- **`## Derived / export churn`** — PRP, manifest, ledger, etc. (regenerate or batch-commit vs editorial work)
- runtime-only noise that should stay uncommitted
- work-politics continuity if relevant
- the best next re-entry prompt

## Guardrails

- Distinguish runtime noise from real local work before recommending any commit or push.
- This is a summary workflow only. Do not stage, commit, or merge as part of the handoff.
- If local changes mix unrelated threads, say so clearly.

## Related files

- `docs/operator-skills.md`
- `docs/development-handoff.md`
- `users/grace-mar/recursion-gate.md`
