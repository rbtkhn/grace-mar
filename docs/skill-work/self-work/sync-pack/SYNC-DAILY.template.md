# SYNC-DAILY (optional training mode)

Use this only for onboarding/training-heavy instances that benefit from one-page daily sync control.

Date: `YYYY-MM-DD`

## Territory A: {{territory_a}}
- status:
- score summary:
- top proposed updates:
- action today:

## Territory B: {{territory_b}}
- status:
- score summary:
- top proposed updates:
- action today:

## Combined next action
- top task:
- owner:
- done by:

## Staleness guardrail (optional)

If any sync log has no new row for > `{{staleness_days}}` days:
- mark `stale sync state: yes`
- run forced relevance scan before other optimization tasks

