# Forecast Artifacts

This directory stores WORK-layer forecast outputs.

These files are:

- provisional
- rebuildable
- decision-support oriented
- not canonical Record truth

Recommended contents:

- one JSON forecast artifact per run
- optional markdown summary per run
- links to receipts when available

Naming suggestion:

- `series_name.YYYY-MM-DD.v1.json`
- `series_name.YYYY-MM-DD.summary.md`

Example:

- `operator_daily_messages.2026-04-12.v1.json`
- `operator_daily_messages.2026-04-12.summary.md`

Rule: Forecast artifacts may support planning and review, but they do not update Record surfaces directly.

See [docs/skill-work/work-forecast/README.md](../../docs/skill-work/work-forecast/README.md).
