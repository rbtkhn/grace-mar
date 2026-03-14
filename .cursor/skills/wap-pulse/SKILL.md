---
name: wap-pulse
description: Generate a work-american-politics pulse with campaign status, blockers, doc freshness, gate rhythm, content queue state, and next actions. Use when checking WAP readiness, preparing the weekly brief, asking what is stale, or requesting a territory status sweep.
---

# WAP Pulse

Use this skill when the operator wants a territory-specific status pass instead of a full repo warmup.

## Default command

```bash
python3 scripts/operator_wap_pulse.py -u grace-mar
```

## Optional brief preview

When the operator also wants to see the top of the next scaffold:

```bash
python3 scripts/operator_wap_pulse.py -u grace-mar --brief-preview
```

## What to return

Keep the response focused on:

- upcoming dates
- blockers and stale docs
- brief readiness
- content queue state
- pending WAP gate items
- next actions

## Guardrails

- This is a WORK-territory surface, not a second queue.
- Do not turn WAP observations into Record edits without the normal gate flow.
- If blockers are all doc-freshness issues, say that plainly instead of overstating urgency.

## Related files

- `docs/operator-skills.md`
- `docs/skill-work/work-american-politics/workspace.md`
- `docs/skill-work/work-american-politics/brief-source-registry.md`
- `docs/skill-work/work-american-politics/content-queue.md`
