---
name: dream
preferred_activation: dream
description: "Grace-Mar night-close maintenance ritual. Primary trigger: dream. Dream is the end-of-day consolidation pass: a bounded maintenance ritual that settles continuity, checks integrity and governance, refreshes contradiction visibility, and prepares governed follow-up without merge authority. Usually one dream session per day."
---

# Dream

**Preferred activation (operator):** say **`dream`**.

`dream` is not another work-start ritual. `dream` is the **end-of-day consolidation pass**.

Its purpose is to help the system settle, compress, and prepare for tomorrow. A dream session does not try to push work forward aggressively. It closes the day by cleaning continuity, checking integrity, refreshing contradiction visibility, and surfacing any governed follow-up that tomorrow may need.

Normally there is only one `dream` session per day, near the end of the day. Extra `dream` runs are allowed, but they are exceptional rather than the norm.

## Design intent

`dream` should feel like closure, settling, and quiet integration. It should not feel like another stimulant or another planning sprint. Because `dream` is a consolidation ritual, it should be bounded, calm, and trustworthy: enough maintenance to reduce entropy, but never so much autonomy that it blurs governance or begins acting like a second operator.

## Success condition

A `dream` succeeds if, after using it, the system feels quieter, cleaner, and better prepared for tomorrow.

Its success condition is not dramatic change. Its success condition is that continuity is lighter, integrity is confirmed, contradiction visibility is refreshed, and no ungated mutation has occurred.

## Cadence

`dream` is normally a once-per-day closeout ritual.

Typical use:
- near the end of the day
- after the last substantial work block
- before sleep or final sign-off
- before handing the system forward to tomorrow’s `coffee`

Extra runs are allowed when needed, especially for:
- dry-run inspection
- recovery after an unusual maintenance event
- explicit operator request

But the default pattern is:
- many `coffee` sessions are normal
- one `dream` session is normal

## Step 1 — Automated actions

Run the bounded maintenance pass:

```bash
python3 auto-research/swarm/orchestrator.py dream
```

Equivalent direct script:

```bash
python3 scripts/auto_dream.py
```

The ritual should:

1. normalize `self-memory.md`
2. run integrity checks
3. run governance checks
4. refresh the derived contradiction digest
5. prepare governed artifact drafts if needed
6. emit one maintenance summary/event

This is a maintenance pass, not a merge pass.

## What to return

Return a short night-close brief with:

- `self-memory` changed: yes/no
- integrity: pass/fail
- governance: pass/fail
- contradiction digest: counts
- artifact drafts: none / count
- one sentence on what tomorrow inherits from this run

If nothing important changed, say so plainly. A quiet run is success.

## Example return shape

```md
## Dream

- self-memory changed: yes
- integrity: pass
- governance: pass
- contradiction digest: reviewable 0, contradiction 0
- artifact drafts: none

Tonight’s pass cleaned continuity and left no governed follow-up items.
```

Or, when something needs attention:

```md
## Dream

- self-memory changed: yes
- integrity: pass
- governance: pass
- contradiction digest: reviewable 2, contradiction 1
- artifact drafts: 1 prepared

Tonight’s pass surfaced one contradiction worth governed review tomorrow; nothing was merged automatically.
```

## Guardrails

- Do not create a new canonical memory surface.
- Do not bypass `recursion-gate.md`.
- Do not directly rewrite `self.md` or `self-archive.md`.
- Do not let `dream` become an autonomous merge agent.
- Prefer bounded maintenance over speculative semantic intervention.
- A quiet run is normal; do not manufacture significance.

## Relation to coffee

`coffee` and `dream` form a biological-cognitive pair.

- **`coffee`** = repeated framing dose
- **`dream`** = end-of-day consolidation pass

`coffee` restores orientation, clarity, and agency.  
`dream` settles continuity, checks integrity, and prepares tomorrow’s state.

Multiple `coffee` sessions per day are normal.  
Usually one `dream` session per day is normal.

`coffee` should feel like a sip.  
`dream` should feel like sleep.

## Canonical pairing

`coffee` and `dream` form Grace-Mar’s daily cognitive rhythm.

`coffee` is a repeatable sip of coherence. It is a lightweight reorientation ritual that can happen many times per day whenever orientation needs to be restored. Its success condition is improved orientation, not exhaustive completion.

`dream` is the end-of-day consolidation pass. It is a bounded maintenance ritual that usually happens once, settling continuity, checking integrity, refreshing contradiction visibility, and preparing governed follow-up without bypassing governance.

Together, `coffee` handles re-entry and `dream` handles closeout.
