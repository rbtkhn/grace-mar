---
name: weekly-brief-run
description: Run the work-politics weekly brief workflow with readiness checks, blocker reporting, and scaffold generation. Use when preparing the weekly brief, checking if sources are fresh enough, or asking for a first-pass campaign brief.
---

# Weekly Brief Run

Use this skill when the operator wants a disciplined weekly brief routine rather than a raw generator call.

## Default command

```bash
python3 scripts/operator_weekly_brief_run.py -u grace-mar
```

## Override stale sources

When the operator explicitly wants a first-pass scaffold even though some sources need refresh:

```bash
python3 scripts/operator_weekly_brief_run.py -u grace-mar --allow-stale-sources
```

## Optional output file

When the operator wants the scaffold written to disk:

```bash
python3 scripts/operator_weekly_brief_run.py -u grace-mar --allow-stale-sources --output "tmp/wap-weekly-brief.md"
```

## What to return

Focus on:

- readiness verdict
- what still needs refresh
- territory blockers that affect the brief
- whether a scaffold was emitted
- human review requirements before use

## Guardrails

- Do not present the scaffold as final-use campaign output.
- If sources need refresh, say so before showing any generated brief.
- This is a WORK-territory workflow; Record changes still go through the gate.

## High-stakes guardrail stress-test (§8)

When the brief touches **war powers**, **congressional ethics / insider-trading**, **cartel-economy claims with legal bite**, or **border + civil liberties** in a volatile window, remind the operator to complete **§8** of the weekly template *before* treating copy as ship-ready:

- Framework: `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md`
- Paste template: `docs/skill-work/work-politics/america-first-ky/stress-test-brief-template.md`
- Dated scaffold: `python3 scripts/scaffold_stress_test_brief.py <issue-slug>` (optional `--dry-run` to preview path)

This is WORK-only documentation; it does not merge into the Record.

## Related files

- `docs/operator-skills.md`
- `docs/skill-work/work-politics/weekly-brief-template.md`
- `docs/skill-work/work-politics/brief-source-registry.md`
- `docs/skill-work/work-politics/content-queue.md`
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md`
