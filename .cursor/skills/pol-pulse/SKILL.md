---
name: pol-pulse
preferred_activation: pol pulse
description: Generate a work-politics pulse with campaign status, blockers, doc freshness, gate rhythm, content queue state, and next actions. Use when checking work-politics readiness, preparing the weekly brief, asking what is stale, or requesting a territory status sweep.
---

# Work-politics pulse

**Preferred activation (operator):** say **`pol pulse`**.

Use this skill when the operator wants a territory-specific status pass instead of a full repo warmup.

## Default command

```bash
python3 scripts/operator_work_politics_pulse.py -u grace-mar
```

## Optional brief preview

When the operator also wants to see the top of the next scaffold:

```bash
python3 scripts/operator_work_politics_pulse.py -u grace-mar --brief-preview
```

## What to return

Keep the response focused on:

- upcoming dates
- blockers and stale docs
- brief readiness
- content queue state
- pending work-politics gate items
- next actions
- **High-stakes flag:** if the week’s work includes war powers, ethics/insider, high-claim cartel economy, or border + civil liberties messaging, note that **weekly brief §8** / `america-first-ky` stress-test may be required before ship (see `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md`).

## Guardrails

- This is a WORK-territory surface, not a second queue.
- Do not turn work-politics observations into Record edits without the normal gate flow.
- If blockers are all doc-freshness issues, say that plainly instead of overstating urgency.

## Related files

- `docs/operator-skills.md`
- `docs/skill-work/work-politics/workspace.md`
- `docs/skill-work/work-politics/weekly-brief-template.md`
- `docs/skill-work/work-politics/brief-source-registry.md`
- `docs/skill-work/work-politics/work-politics-sources.md` (§ Tucker Carlson Network → `research/external/youtube-channels/tucker-carlson-book/`)
- `docs/skill-work/work-politics/content-queue.md`
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md`
