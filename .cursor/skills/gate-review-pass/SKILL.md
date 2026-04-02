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

For each candidate, show **only the review-essential fields**:

- **id** and one-line **summary**
- **source_exchange** or **source** (grounding evidence)
- **suggested_entry** (what would be merged)
- **age** (days since timestamp — flag if >14 days)
- **risk_tier** from the review script (quick_merge_eligible / review_batch / manual_escalate)
- **duplicate_hints** if any

Do **not** show pipeline plumbing by default: `channel_key`, `signal_type`, `priority_score`, `profile_target`, `prompt_section`, `prompt_addition`, `mind_category`. These are available in the file if the operator asks.

Then give a recommendation per candidate:

- approve now
- investigate duplicates
- manual escalation (explain why)
- stale — review or reject
- defer or batch review

## Guardrails

- This workflow does not approve, reject, or merge anything by itself.
- Keep companion and work-politics items distinct when that affects review.
- Treat duplicate hints as prompts to verify, not proof that a candidate should be rejected.
- Rejected candidates are auto-swept to Processed on the next `coffee` run — no manual cleanup needed.

## Related files

- `docs/operator-skills.md`
- `users/grace-mar/recursion-gate.md`
- `scripts/recursion_gate_review.py`
