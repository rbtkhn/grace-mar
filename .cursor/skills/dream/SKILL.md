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
- before handing the system forward to tomorrow's `coffee`

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
python3 scripts/auto_dream.py
```

For the stricter maintenance variant:

```bash
python3 scripts/auto_dream.py --strict
```

Alternative via swarm bridge (same underlying logic):

```bash
python3 auto-research/swarm/orchestrator.py dream
```

**End-of-day bundle (optional):** To run dream + handoff-check in one pass (night-side equivalent of `operator_reentry_stack.py`):

```bash
python3 scripts/operator_end_of_day.py -u grace-mar
```

The ritual should:

1. normalize `self-memory.md`
2. run integrity checks
3. run governance checks
4. refresh the derived contradiction digest
5. prepare governed artifact drafts if needed
6. emit one maintenance summary/event

`dream --strict` is the same ritual in a sharper maintenance posture: stricter integrity parity, stricter contradiction classification, clearer failure states, and fail-fast closeout when checks do not pass. It does not change companion-facing tone, canonical memory surfaces, or merge authority.

This is a maintenance pass, not a merge pass.

**Morning handoff:** When `apply=True` (the default), dream writes `users/grace-mar/last-dream.json` — a compact summary that tomorrow's `coffee` Step 1 (`operator_daily_warmup.py`) automatically picks up and displays as **"Last dream (night handoff)"**. This closes the choreography gap: coffee knows what dream found without the operator carrying it across threads.

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

Tonight's pass cleaned continuity and left no governed follow-up items.
```

Or, when something needs attention:

```md
## Dream

- self-memory changed: yes
- integrity: pass
- governance: pass
- contradiction digest: reviewable 2, contradiction 1
- artifact drafts: 1 prepared

Tonight's pass surfaced one contradiction worth governed review tomorrow; nothing was merged automatically.
```

## Guardrails

- Do not create a new canonical memory surface.
- Do not treat strict mode as a global prompt override.
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
`dream` settles continuity, checks integrity, and prepares tomorrow's state.

Multiple `coffee` sessions per day are normal.
Usually one `dream` session per day is normal.

`coffee` should feel like a sip.
`dream` should feel like sleep.

## Cadence choreography

`coffee`, `dream`, and `bridge` form Grace-Mar's cadence triad:

| Time | Ritual | What it does |
|------|--------|-------------|
| **Morning** | `coffee` (work-start) | Read dream handoff, grounding scripts, A–H menu |
| **During day** | `coffee` (reorientation) | Re-sip as needed — many per day is normal |
| **End of day** | `dream` | Memory normalization, integrity, governance, contradiction digest |
| **Session close** | `bridge` | Seal repos (commit/push), synthesize transfer prompt for next session |

**Dream's role is maintenance, not session closure.** Dream settles continuity and writes the handoff artifact. It does not commit, push, or produce a transfer prompt. If the operator is also closing the Cursor session, `bridge` follows dream.

| Scenario | Path |
|----------|------|
| End of day + closing session | `dream` then `bridge` |
| End of day, keeping session | `dream` alone |
| Mid-day, closing session | `bridge` alone (no dream needed) |

**One-command bundle:** `python3 scripts/operator_end_of_day.py -u grace-mar` runs dream + handoff-check. If also closing the session, say `bridge` afterward.

**Morning pickup:** `operator_daily_warmup.py` reads `last-dream.json` and displays follow-ups from last night's dream — contradictions to review, artifact drafts to promote, integrity/governance status.

For the full decision tree including signing-off **`coffee`** (lightweight alternative to bridge), see [bridge SKILL.md](../bridge/SKILL.md).

## Cadence audit

Each successful dream run appends one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. This is automatic — no operator action required.

## Related files

- `docs/skill-work/work-dream/README.md` — territory doctrine and boundaries
- `docs/skill-work/work-dream/work-dream-history.md` — design history (architecture changes, not per-run telemetry)
- `docs/skill-work/work-cadence/work-cadence-events.md` — per-run cadence telemetry
- `.cursor/skills/coffee/SKILL.md` — morning-side counterpart
- `.cursor/skills/bridge/SKILL.md` — session-scale handoff
