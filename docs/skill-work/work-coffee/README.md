# work-coffee

**Purpose:** Operator cadence, activation, re-entry, signing-off (merged into **`coffee`** Step 1 + **A–E** hub), and workflow-state design for Grace-Mar's `coffee` ritual. **Standalone Conductor** (master name, **`conductor`**, [conductor skill](../../../.cursor/skills/conductor/SKILL.md)) remains available without `coffee`; **hub E — Conductor** continues a pass after **`coffee`** Step 1. This territory is where the system explains and evolves the ritual architecture. The executable trigger surface lives in [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md).

**Not** Record truth. **Not** MEMORY. **Not** a second merge path. **Not** generic repo hygiene, and **not** a broad health/caffeine territory. `work-coffee` is a WORK lane for ritual architecture and operator ergonomics.

---

## Role

| Role | Description |
|------|-------------|
| **Cadence architecture** | Defines work-start vs signing-off **Step 1** weight, **one** fixed **`coffee` hub** (**A–E**: Steward, Engineer, Historian, Capitalist, Conductor), **standalone Conductor** sessions, re-entry behavior, and cadence modifiers. |
| **Operator activation** | Holds the rationale for why the `coffee` ritual exists: activation, rhythm, state shift, and workflow dopamine replacement. |
| **Boundary surface** | Explains what belongs in WORK-only docs/history versus what must escalate to `RECURSION-GATE` or change review. |
| **Session trail guidance** | Clarifies how `session-transcript`, `work-*-history.md`, and `self-memory` relate without collapsing into one another. |

---

## Relationship to `coffee`

- **`coffee` skill** = executable ritual contract, trigger behavior, and exact coffee-menu semantics.
- **`work-coffee` territory** = prose home for rationale, boundaries, history, and evolution of the ritual.

This split is intentional:

- the skill should stay optimized for invocation and agent behavior
- the territory should hold the longer-form doctrine and lane-specific history

**`coffee` C — Historian** opens exactly three actionable options and nothing else: **A. Intel** (daily brief / current-events watch, including Putin/Vance watches and optional KY-4), **B. Bookshelf quiz** (self-knowledge MCQs toward IX-A candidates), and **C. Notebook synthesis** (History Notebook / Predictive History synthesis with Tri-Frame lenses). Agents should **not** auto-run the brief or auto-offer Tri-Frame before this submenu — see [menu-reference.md](menu-reference.md#tri-frame-daily-brief).

**Symphony / Conductor:** **Hub E** after **`coffee`** continues Conductor; **standalone** strategy-notebook cadence: [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) + [CONDUCTOR-PASS.md](CONDUCTOR-PASS.md); invoke by **master name**, **`conductor`**, or [conductor skill](../../../.cursor/skills/conductor/SKILL.md) without opening **`coffee`** when preferred.

---

## Gate Threshold

`work-coffee` is **WORK-only by default**.

Keep changes in docs/history only when they are about:

- menu wording or ergonomics
- pacing and rhythm
- re-entry patterns
- `stay in coffee` behavior
- warmup or signing-off Step 1 phrasing
- operator workflow preferences

Stage to **`users/grace-mar/recursion-gate.md`** only when a `work-coffee` insight would change governed behavior, such as:

- companion-facing IX-B / IX-C intake
- durable prompt or policy behavior
- approved survey/cadence structures that alter Record intake
- enduring governance changes that should not live as docs only

Use **change review first** when the change is architectural or cross-surface, for example:

- it revises how multiple governed systems relate to each other
- it changes the boundary between WORK, MEMORY, and the Record
- it changes more than one durable governance surface at once

This territory never creates a second merge path. `RECURSION-GATE` remains the membrane, and companion approval remains required before any governed merge. See [AGENTS.md](../../../AGENTS.md).

---

## Candidate shape when escalation is warranted

When a `work-coffee` insight should stage a gate candidate, prefer:

- `source: operator — work-coffee`
- `signal_type: operator_cadence_refinement`
- literal `source_exchange` from the operator session that motivated the change

Default rule: if the insight is still primarily about operator preference or ritual tuning, keep it here in WORK. Escalate only when the ritual implication becomes durable governed behavior.

---

## Continuity and trail

`work-coffee` does **not** replace any existing continuity surface.

- **Raw continuity:** `users/<id>/session-transcript.md`
- **Lane breadcrumbs:** `docs/skill-work/work-coffee/work-coffee-history.md`
- **Optional continuity memory:** `users/grace-mar/self-memory.md`
- **Governed durable changes:** `users/grace-mar/recursion-gate.md`

Per [work-menu-conventions.md](../work-menu-conventions.md) and [work-modules-history-principle.md](../work-modules-history-principle.md), `coffee` sessions may leave WORK-choice trails and per-lane breadcrumbs, but those are not Record truth.

---

## Adjacent surfaces

- [operator-session-review-checklist.md](operator-session-review-checklist.md) — session UX / procedure verification (manual + pytest pointers).
- [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md)
- [work-menu-conventions.md](../work-menu-conventions.md)
- [work-dev/git-branch-hygiene.md](../work-dev/git-branch-hygiene.md)
- [work-strategy/README.md](../work-strategy/README.md)
- [work-politics/polling-and-markets.md](../work-politics/polling-and-markets.md)
- [work-companion-self/README.md](../work-companion-self/README.md)

---

## Conductor semantics (machine)

Mechanical helpers (continuity from recent picks plus recommendation from dream + session load) live in
[`scripts/cadence_conductor_resolution.py`](../../../scripts/cadence_conductor_resolution.py).
Human contract and menu order: [CONDUCTOR-PASS.md](CONDUCTOR-PASS.md).

Run the illustration tests:

`python3 -m pytest tests/test_conductor_coffee_illustration.py -k illustration -v`

---

## Scope boundaries

In scope:

- operator cadence design
- activation rituals
- work-start / signing-off (merged into one fixed coffee flow; Rome / Jiang / notebook synthesis and self-knowledge bookshelf quiz land under **C — Historian**; skill-write / commercial slices land under **D — Capitalist**; **E — Conductor** continues Conductor; fold strategy-only into **C** per [coffee SKILL](../../../.cursor/skills/coffee/SKILL.md))
- reorientation and multi-`coffee` behavior
- survey/cadence workflow design
- relationship between hub flow and territory execution

Out of scope:

- broad health or caffeine optimization
- generic git/repo hygiene as a standalone territory
- work-politics content itself
- work-dev integration doctrine itself
- Record merges or prompt edits without the gate
