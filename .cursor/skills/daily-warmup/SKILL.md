---
name: daily-warmup
description: Generate a Grace-Mar morning coffee or daily operator warmup with gate state, WAP status, repo integrity, and top priorities. Use when starting a new thread, planning the day, asking what to work on next, or requesting a pulse check before implementation.
---

# Daily Warmup

Use this skill at the start of a work block when the operator wants a quick planning pass grounded in repo state.

## Run this first

```bash
python3 scripts/operator_daily_warmup.py -u grace-mar
```

If the work touches instance state and the thread does not already contain a warmup snapshot, also run:

```bash
python3 scripts/harness_warmup.py -u grace-mar
```

Paste or quote the warmup block so the thread carries the same continuity snapshot.

## What to return

Return a short operator brief with:

- top 3 priorities
- gate state and whether anything needs review now
- WAP blockers or next actions
- integrity status
- local worktree noise only if it matters for the next move

## Guardrails

- This is read-only planning. Do not merge or stage just because the warmup mentions candidates.
- If integrity fails, surface that before optional improvements.
- Treat `users/grace-mar/recursion-gate.md` and `self-evidence.md` as canonical, not the summary.

## Related files

- `docs/operator-skills.md`
- `docs/skill-work/work-political-consulting/workspace.md`
