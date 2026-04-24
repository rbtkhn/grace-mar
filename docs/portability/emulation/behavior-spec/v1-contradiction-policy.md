# Portable Emulation Contradiction Policy v1

## Core rule

- Contradictions **MUST** be surfaced, not silently resolved.

## Allowed actions

- A foreign runtime **MAY** identify possible contradictions.
- A foreign runtime **MAY** emit contradiction proposals.
- A foreign runtime **MAY** recommend review actions.

## Forbidden actions

- A foreign runtime **MUST NOT** decide canonical contradiction resolution.
- A foreign runtime **MUST NOT** collapse old and new claims into one approved truth.
- A foreign runtime **MUST NOT** silently discard uncertainty.

## Minimum contradiction payload

When a contradiction is detected, preserve:

- old claim
- new claim
- evidence or source references
- uncertainty level
- recommended review action

Contradiction handling remains **proposal-only** until the source repo reviews the result.
