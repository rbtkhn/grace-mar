# Forecast Receipts

This directory stores receipt records for forecast runs.

A forecast receipt is a legibility object, not a Record update.

Its purpose is to show:

- that a forecast run occurred
- which lane produced it
- which source series was used
- which artifact file was written
- which method was selected
- whether the run succeeded or failed

Forecast receipts are WORK-layer metadata.
They may support observability, audit, and operator review.
They do not update SELF, SELF-LIBRARY, SKILLS, or EVIDENCE directly.

Naming suggestion:

- `forecast_run.<series_name>.<YYYY-MM-DDTHH-MM-SSZ>.json`

Example:

- `forecast_run.operator_daily_messages.2026-04-12T18-30-00Z.json`
