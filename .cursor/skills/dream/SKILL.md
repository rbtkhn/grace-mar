---
name: dream
preferred_activation: dream
description: "Grace-Mar night-close maintenance ritual. Primary trigger: dream. Dream is the end-of-day consolidation pass: a bounded maintenance ritual that settles continuity, checks integrity and governance, refreshes contradiction visibility, and prepares governed follow-up without merge authority. Before auto_dream.py runs, synthesize the previous eight events from work-cadence-events.md into **Recent rhythm** prose (no cadence-tail jargon or timestamps in chat). Usually one dream session per day."
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

## Step 0 — Recent rhythm (before Step 1 scripts)

**Read first** — `auto_dream.py` (and `operator_end_of_day.py`) append a new **`dream`** line when the pass completes successfully, so the log must be read **before** those commands if the rhythm read is to exclude this run.

1. Open **`docs/skill-work/work-cadence/work-cadence-events.md`**. Below `_(Append below this line.)_`, collect lines matching `- **YYYY-MM-DD HH:MM UTC** — kind (user) …`.
2. Take the **last 8** such lines already in the file. If there are fewer than eight, use what exists; if none, **Recent rhythm:** _(no prior events)_ in the reply.
3. **Synthesize in plain prose** — a **short paragraph** (or a few tight sentences), **grounded in the eight lines**: which rituals appeared, what **differed** (bridge commit refs, coffee modes, thanks **park** lines, prior dream ok/fail). **Companion-facing UX:** **do not** use the phrase **cadence tail** in chat; **do not** put **dates, UTC, or clock times** in this prose. **Do not** open with a wall of raw `key=value`; weave **specifics** into sentences (short shas, park text, integrity/governance in ordinary words). **Avoid** generic closure talk with no tie to those events. Script output below still carries the full machine snapshot.
4. Hold this synthesis for **What to return** — it belongs **at the top** of the night-close brief, before `self-memory` / integrity lines.

If the file is missing or empty below the anchor, note that under **Recent rhythm** and continue.

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

**Morning handoff:** When `apply=True` (the default), dream writes `users/grace-mar/last-dream.json` — a compact summary that tomorrow's `coffee` Step 1 (`operator_daily_warmup.py`) automatically picks up and displays as **"Last dream (night handoff)"**. This closes the choreography gap: coffee knows what dream found without the operator carrying it across threads. The JSON includes **`agent_surface.cursor_model`** (same meaning as bridge/harvest **Agent surface** / cadence **`cursor_model=`**): pass **`--cursor-model`** to `auto_dream.py` or set **`CURSOR_MODEL`** in the environment when running from a context that knows the Cursor UI label; otherwise **`unknown`**.

## What to return

Return a short night-close brief with:

- **Recent rhythm:** (synthesis from Step 0 — always first; never label this **cadence tail**)
- `self-memory` changed: yes/no
- integrity: pass/fail
- governance: pass/fail
- contradiction digest: counts
- artifact drafts: none / count
- **When present in `last-dream.json`:** coffee **24h rollup** (runs, mode mix, optional **menu picks** from `coffee_pick` cadence lines), **three execution paths** with **suggested index**: Steward when this run’s **integrity or governance failed**, else Steward when **gate pending > `max_pending_candidates`** (from `config/fork-config.json`), else **calendar mod-3** on tomorrow’s yearday; **`tomorrow_inherits`** one-liner (operational hint only); **civ-mem echoes** (default **one** hit above overlap threshold — each carries **“Analogy candidate only — not evidence, not recommendation, not Record”**; cite the disclaimer)
- one sentence on what tomorrow inherits from this run

If nothing important changed, say so plainly. A quiet run is success.

## Example return shape

```md
## Dream

- Recent rhythm: (e.g. two work-start coffees, a thanks pause with a short park line, then bridge with two short commit refs)
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

- Recent rhythm: (compressed rhythm from Step 0, no timestamps in chat)
- self-memory changed: yes
- integrity: pass
- governance: pass
- contradiction digest: reviewable 2, contradiction 1
- artifact drafts: 1 prepared

Tonight's pass surfaced one contradiction worth governed review tomorrow; nothing was merged automatically.
```

## Governance doctrine (soft boundary)

**Suggestions** emitted by dream (execution path index, `tomorrow_inherits`, civ-mem echoes, coffee rollup) are **operational hints only**. They do **not** establish truth, priority, or policy, and must **never** substitute for gate review, integrity status, companion approval, or operator judgment. Cadence and handoff files are **not** a shadow Record.

## Strict halt and `last-dream.json`

When **`auto_dream.py --strict`** halts because integrity or governance failed, a **new** `last-dream.json` is **not** written (the previous file, if any, is left unchanged). Morning pickup may show an **older** handoff until the next successful dream. Rotation overrides, civ-mem echoes, and rollup fields apply to **successful** writes only.

---

## Strict halt repeats — doc-only loop

If **strict** dream halts for the **same** integrity or governance **reason** more than once, the fix is usually **operational** (refresh exports, resolve parity, adjust config) — not a gate merge.

**Recursive tightening:** Add **one** bullet to **this skill** (e.g. under *Step 1* or this section) or to `docs/skill-work/work-dream/README.md` describing the recurring cause and the **first** recovery step. Do not use this loop to bypass companion merge authority.

---

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

`coffee`, `dream`, and `bridge` form Grace-Mar's cadence triad; **`thanks`** is a **light pause** (telemetry + optional park line + synthesis of prior two events — see [.cursor/skills/thanks/SKILL.md](../thanks/SKILL.md)).

| Time | Ritual | What it does |
|------|--------|-------------|
| **Morning** | `coffee` (work-start) | Read dream handoff, grounding scripts, A–E menu |
| **During day** | `coffee` (reorientation) | Re-sip as needed — many per day is normal |
| **During day** | `thanks` (micro-pause) | Synthesis of prior two log events (recent rhythm) + optional park + one telemetry line — no maintenance stack |
| **End of day** | `dream` | Memory normalization, integrity, governance, contradiction digest |
| **Session close** | `bridge` | Seal repos (commit/push), synthesize transfer prompt for next session |

**Dream's role is maintenance, not session closure.** Dream settles continuity and writes the handoff artifact. It does not commit, push, or produce a transfer prompt. If the operator is also closing the Cursor session, `bridge` follows dream.

| Scenario | Path |
|----------|------|
| End of day + closing session | `dream` then `bridge` |
| End of day, keeping session | `dream` alone |
| Mid-day, closing session | `bridge` alone (no dream needed) |

**One-command bundle:** `python3 scripts/operator_end_of_day.py -u grace-mar` runs dream + handoff-check. If also closing the session, say `bridge` afterward.

**Morning pickup:** `operator_daily_warmup.py` reads `last-dream.json` and displays a **collapsed** “Last dream” block by default; use **`--verbose-dream`** for full paths, civ-mem snippets, and followups.

For the full decision tree including signing-off **`coffee`** (lightweight alternative to bridge), see [bridge SKILL.md](../bridge/SKILL.md).

**Deeper choreography** (ordering, data flow, synthesis depths, harvest vs clocks): [work-cadence README — Cadence choreography](../../../docs/skill-work/work-cadence/README.md#cadence-choreography).

## Cadence audit

Each successful dream run appends one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. This is automatic — no operator action required; the line includes **`cursor_model=…`** (see **Morning handoff** above for how to set it). **`operator_end_of_day.py`** forwards **`--cursor-model`** to `auto_dream.py`.

## Related files

- `docs/skill-work/work-dream/README.md` — territory doctrine and boundaries
- `docs/skill-work/work-dream/work-dream-history.md` — design history (architecture changes, not per-run telemetry)
- `docs/skill-work/work-cadence/work-cadence-events.md` — per-run cadence telemetry
- `.cursor/skills/coffee/SKILL.md` — morning-side counterpart
- `.cursor/skills/thanks/SKILL.md` — micro-pause (not a substitute for dream)
- `.cursor/skills/bridge/SKILL.md` — session-scale handoff
