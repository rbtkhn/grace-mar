# Workflow observability thresholds (human guidance)

These thresholds are **recommendations for human review**, not automation hooks. They do **not** merge gate candidates or change prompts without operator/companion decisions.

| Signal | Suggested threshold | Suggested human action |
|--------|---------------------|-------------------------|
| Low acceptance rate over repeated review cycles | Many proposals stay `proposed` / `under_review` while similar `changeType` items accumulate | Audit templates, validator noise, or scope clarity—not “force approve.” |
| High median review cycles (lane) | `reviewCycles` median high vs peer lanes in friction report | Friction audit: gate copy, reviewer checklist, or split change size. |
| Excessive context cost per accepted output | Median tokens high with low acceptance in same lane | Compression or retrieval redesign **proposal**; compare [context-budgeting.md](runtime/context-budgeting.md). |
| High retrieval miss rate | Miss share elevated in context-efficiency report | Retrieval tuning or corpus coverage review—not silent routing changes. |
| Consistently high-leverage workflows | Same `workflowType` appears in leverage candidates repeatedly | Candidate for stronger defaults or reusable templates—**still** requires explicit promotion. |

## What not to do

- Do not wire these thresholds to auto-merge or auto-reject.
- Do not treat observability JSON as Record truth.

See [workflow-observability.md](workflow-observability.md).
