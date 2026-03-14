---
name: handoff-check
description: Generate a stop/resume handoff summary with recent commits, meaningful local work, runtime noise, gate continuity, and a suggested re-entry prompt. Use when ending a session, resuming work after a break, or checking what is safe to ignore before committing or pushing.
---

# Handoff Check

Use this skill when the operator wants to pause or resume work without losing the active thread.

## Default command

```bash
python3 scripts/operator_handoff_check.py -u grace-mar
```

## What to return

Summarize:

- recently committed work
- meaningful local changes still in progress
- runtime-only noise that should stay uncommitted
- WAP continuity if relevant
- the best next re-entry prompt

## Guardrails

- Distinguish runtime noise from real local work before recommending any commit or push.
- This is a summary workflow only. Do not stage, commit, or merge as part of the handoff.
- If local changes mix unrelated threads, say so clearly.

## Related files

- `docs/operator-skills.md`
- `docs/development-handoff.md`
- `users/grace-mar/recursion-gate.md`
