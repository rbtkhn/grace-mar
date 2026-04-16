# Operator Rhythm

Real operating rhythm for the operator.

## Boundary

This file records actual work rhythm as observed, reported, or elicited.
It is a WORK artifact, not identity truth.

## What belongs here

- realistic day rhythm
- realistic week rhythm
- realistic month rhythm
- common reentry patterns
- interruption windows
- times best suited for: strategy, writing, maintenance, review, low-cognition admin
- common closeout patterns
- known mismatch between ideal schedule and actual schedule

## Day rhythm

*Source: cadence telemetry (work-cadence-events.md), 12 days of data through 2026-04-16.*

- Activity spans ~18 hours per day (UTC 12 through UTC 06 next day).
- Quiet window: UTC 07–11 (likely sleep / offline).
- Heaviest event clusters: UTC 00 (29 events), UTC 04–05 (16+13 events), UTC 14–15 (11+13 events).
- Average ~16 events/day across all cadence kinds.
- Multiple coffee reorientations per day (~6 per day average) — not a single morning start; work is punctuated by frequent resets.
- Thanks pauses appear between work blocks (avg ~3 per day), marking topic transitions without full closeout.
- Dream typically once per day, near end of the work cycle.
- Bridge used for session transfers (~1 per day when active).

*(Operator: fill in local timezone and clock-hour labels when reviewing.)*

## Week rhythm

- Monday:
- Tuesday:
- Wednesday:
- Thursday:
- Friday:
- Weekend:

*(No clear weekday vs weekend pattern visible in current telemetry — 12 days of data is too short. Fill in from experience.)*

## Reentry patterns

*Source: cadence telemetry + session observation.*

- Typical interruption types: context switches between WORK lanes (strategy → dev → cadence → strategy); Cursor thread boundaries (new thread = cold start).
- What helps fast reentry: `coffee` with prior-event synthesis (Recent rhythm); `bridge` transfer prompt pasted into new thread; `thanks` park line as anchor.
- What causes slow reentry: cold Cursor thread with no warmup; long gap between sessions without a bridge or dream; multiple pending gate candidates creating decision load at reentry.

## Energy and cognition

*Source: session observation (to be confirmed by operator).*

- Best for strategy: extended uninterrupted blocks (visible as long coffee-to-thanks spans); wire harvests and notebook weaving happen in these windows.
- Best for writing: not yet observed separately from strategy — may overlap.
- Best for cleanup: shorter blocks between coffee resets; cadence telemetry fixes, script enhancements, and template alignment happen in these windows.
- Worst windows for deep work: *(fill in from experience)*

## Cadence implications

*Source: telemetry pattern + session observation.*

- Coffee should emphasize: fast reorientation — the operator uses coffee as a reset, not a planning ceremony; the Recent rhythm line and menu are the load-bearing parts.
- Dream should emphasize: bounded maintenance — the operator does not want open-ended consolidation; integrity and governance checks, handoff written, done.
- Bridge is most useful when: switching Cursor threads mid-day or carrying context across a gap longer than a thanks pause.

## Interaction style (observed)

- Short prompts: single letters ("a", "b", "d"), single words ("thanks"), or brief directives ("do you agree with any of this").
- Menu-driven: the operator selects from labeled options rather than writing long instructions.
- Hypothesis-first: floats proposals and evaluations, expects the agent to assess before implementing.
- Plan-then-execute: uses Plan mode to design, then switches to Agent mode with "implement the plan."
- Compression: prefers one-sentence answers over paragraphs; tightened the thanks SKILL to enforce "one sentence maximum."

## Notes

- Keep this grounded in real pattern, not aspiration.
- Current data covers 12 days (2026-04-05 through 2026-04-16). Patterns may shift with more data.
- The high coffee frequency (~6/day) is a feature, not a bug — it reflects genuine punctuated workflow, not indecision.
