---
name: gate-review-pass
preferred_activation: gate review
description: "Read-only RECURSION-GATE review pass: ordered recommendations, duplicate/stale hints, escalation signals—companion decides; never merge into SELF/EVIDENCE/prompt or run process_approved_candidates without explicit companion approval and per-candidate id+summary echo (AGENTS). Triggers: review gate backlog, pending CANDIDATE-XXXX, what to approve defer or investigate next, gate-review-pass."
---

# Gate Review Pass

**Preferred activation (operator):** say **`gate review`**.

Use this skill when the operator wants a structured review pass over pending candidates without taking action yet.

## Default command

```bash
python3 scripts/operator_gate_review_pass.py -u grace-mar
```

## Territory filters

Use a narrower review lens when needed:

```bash
python3 scripts/operator_gate_review_pass.py -u grace-mar --territory companion
python3 scripts/operator_gate_review_pass.py -u grace-mar --territory work-politics
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
- Keep companion and work-politics items distinct when that affects review.
- Treat duplicate hints as prompts to verify, not proof that a candidate should be rejected.

## Related files

- `docs/operator-skills.md`
- `users/grace-mar/recursion-gate.md`
- `scripts/recursion_gate_review.py`
