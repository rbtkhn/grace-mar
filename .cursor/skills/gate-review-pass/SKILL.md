---
name: gate-review-pass
description: Generate a recommendation-oriented RECURSION-GATE review summary with quick-merge candidates, duplicate hints, stale items, and escalation signals. Use when reviewing pending candidates, checking gate backlog, or deciding what should be approved, deferred, or investigated next.
---

# Gate Review Pass

Use this skill when the operator wants a structured review pass over pending candidates without taking action yet.

## Default command

```bash
python3 scripts/operator_gate_review_pass.py -u grace-mar
```

## Territory filters

Use a narrower review lens when needed:

```bash
python3 scripts/operator_gate_review_pass.py -u grace-mar --territory companion
python3 scripts/operator_gate_review_pass.py -u grace-mar --territory wap
```

## What to return

Keep the output recommendation-oriented:

- approve now
- investigate duplicates
- manual escalation
- stale candidates
- defer or batch review

## Guardrails

- This workflow does not approve, reject, or merge anything by itself.
- Keep companion and WAP items distinct when that affects review.
- Treat duplicate hints as prompts to verify, not proof that a candidate should be rejected.

## Related files

- `docs/operator-skills.md`
- `users/grace-mar/recursion-gate.md`
- `scripts/recursion_gate_review.py`
