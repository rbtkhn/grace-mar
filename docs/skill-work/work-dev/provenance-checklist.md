# work-dev provenance checklist

Repeatable verification path for the core `work-dev` invariant:

OpenClaw may export and stage, but it must remain stage-only and auditable.

---

## Export check

1. Run:
   `python integrations/openclaw_hook.py --user grace-mar --format md+manifest --emit-event`
2. Confirm a `runtime_compat_export` event appears in `users/grace-mar/pipeline-events.jsonl`.
3. Confirm harness audit also records the export if harness events are enabled.

## Handback check

1. Run:
   `python integrations/openclaw_stage.py --user grace-mar --text "we explored X in OpenClaw"`
2. Confirm the request succeeds and stages a candidate.
3. Confirm an `intent_constitutional_critique` event appears with `advisory_clear` or `advisory_flagged`.

## Gate candidate check

1. Open `users/grace-mar/recursion-gate.md`.
2. Confirm a new pending candidate exists before `## Processed`.
3. Check whether OpenClaw-specific provenance survived into the candidate block:
   - source marker
   - artifact metadata if applicable
   - constitutional advisory context if applicable
4. If provenance is missing or only visible in events, update `known-gaps.md`.

## Review-path check

1. Run any queue review surface that depends on provenance.
2. Confirm the candidate can be distinguished as OpenClaw-sourced without guesswork.
3. If not, treat OpenClaw-specific benchmark rows as blocked or partial.

## Merge-followthrough check

1. After a real approved merge, confirm whether downstream docs or metrics can still attribute the result to the OpenClaw path.
2. If attribution disappears after merge, note the break in `known-gaps.md`.

---

## Guardrail

If provenance cannot survive from export/handback through review and merge, the integration is operationally weaker than the doctrine implies.
