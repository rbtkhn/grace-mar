# Continuity Observability

**Status:** WORK / runtime observability. **Not** Record. **Not** EVIDENCE. **Not** merge authority.

This surface tracks continuity-block events from OpenClaw handback enforcement without turning local runtime residue into durable truth by accident.

## Contract

| Field | Value |
|-------|-------|
| Source feed | `runtime/observability/continuity_blocks.jsonl` |
| Export command | `python scripts/work_dev/export_continuity_blocks.py` |
| Derived output | `artifacts/work-dev/continuity-observability/continuity-blocks.md` |
| Authority | WORK-derived operator review only |
| Gate effect | none |

`continuity_blocks.jsonl` is local runtime residue. The feed is useful because it shows when `/stage` was blocked for missing or invalid continuity receipts, but it is not durable state while it remains only in `runtime/`.

## Export Path

The exporter reads the local JSONL feed and writes a derived Markdown summary for operator review. Missing or empty feeds are valid states; the output should say that no continuity blocks were observed rather than failing.

The export path does not touch:

- `users/grace-mar/self.md`
- `users/grace-mar/self-archive.md`
- `users/grace-mar/recursion-gate.md`
- `users/grace-mar/session-log.md`
- `bot/prompt.py`

## Retention

Retention is still minimal: local runtime feed plus optional derived export. This moves toward durable observability only when an explicit export or retention path exists and is intentionally used. It does not make the local feed canonical.

## When This Changes

Treat continuity event logging as stronger than local residue only after one of these exists:

- an explicit recurring export path with reviewable artifacts
- a documented retention policy for the runtime feed
- a dashboard or receipt family that consumes the export without changing Record authority

Until then, the status remains `partial`.
