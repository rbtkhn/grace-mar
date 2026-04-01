# work-cadence

**Purpose:** Doctrine, boundaries, and architecture for the daily cadence triad — `coffee` (morning orientation), `dream` (night consolidation), and `bridge` (session-scale handoff). Executable trigger surfaces live in `.cursor/skills/coffee/SKILL.md`, `.cursor/skills/dream/SKILL.md`, and `.cursor/skills/bridge/SKILL.md`.

**Not** Record truth. **Not** a merge path. **Not** identity-relevant unless gated.

---

## Role

| Role | Description |
|------|-------------|
| **Cadence architecture** | Defines the shape of operator rhythm: coffee (orientation, repeated), dream (consolidation, once per day), bridge (session-scale carry-forward). |
| **Night-to-morning handoff** | Documents the `last-dream.json` data contract that bridges dream output to coffee Step 1. |
| **Cadence event audit** | Append-only telemetry of each run via `work-cadence-events.md` and `scripts/log_cadence_event.py`. |
| **Boundary surface** | Explains what belongs in operational/ephemeral surfaces versus what must escalate to the gate. |

---

## Daily rhythm

| Time | Ritual | What it does |
|------|--------|-------------|
| **Morning** | `coffee` (work-start) | Read dream handoff, warmup brief, harness, branch snapshot, A-H menu |
| **During day** | `coffee` (reorientation) | Re-sip as needed — many per day is normal |
| **End of day** | `dream` | Memory normalization, integrity, governance, contradiction digest, handoff JSON |
| **Session close** | `bridge` | Seal (commit/push), synthesize transfer prompt for next Cursor session |

**Many coffees, one dream, one bridge.** `coffee` is for repetition. `dream` is for closure. `bridge` is for carry-forward.

---

## Contents

| File | Purpose |
|------|---------|
| **This README** | Scope, rhythm, boundaries for work-cadence. |
| **[work-cadence-events.md](work-cadence-events.md)** | Append-only audit of cadence runs (coffee/dream/bridge). Not Record. |

---

## Cadence event audit

Each coffee, dream, and bridge run appends one line to [work-cadence-events.md](work-cadence-events.md) via `scripts/log_cadence_event.py`. This is operator-facing telemetry — not the Record, not self-memory.

**Emitters:**
- **dream** — `auto_dream.py` appends after successful completion (gated on `apply=True`)
- **coffee** — `operator_coffee.py` appends after all steps succeed
- **bridge** — agent runs `log_cadence_event.py --kind bridge` in Step 2 after push

**Leaf-only rule:** Orchestrators (`operator_end_of_day.py`, `operator_coffee.py` when it chains) do not emit their own events. Only the leaf ritual logs.

**Split threshold:** If cadence events exceed ~200 lines/month, consider adding a JSONL sibling and keeping monthly rollup bullets in this markdown file.

---

## Script topology (grace-mar)

```
operator_coffee.py          consolidated morning runner (modes: work-start, light, minimal, closeout, reentry)
  ├─ operator_daily_warmup.py    priorities, gate, territories, integrity, dream handoff pickup
  ├─ harness_warmup.py           compact state snapshot
  └─ operator_handoff_check.py   (closeout mode only)

operator_end_of_day.py      night-side bundle
  ├─ auto_dream.py               memory normalization, integrity, governance, contradiction, last-dream.json
  └─ operator_handoff_check.py   gate, commits, worktree, re-entry prompt
```

---

## Gate threshold

`work-cadence` is **operational by default**. Stage to `recursion-gate.md` only when a cadence insight would change governed behavior (prompt, policy, identity-relevant signals).

---

## Adjacent surfaces

- [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md) — coffee trigger
- [.cursor/skills/dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md) — dream trigger
- [.cursor/skills/bridge/SKILL.md](../../../.cursor/skills/bridge/SKILL.md) — bridge trigger
- [work-coffee/](../work-coffee/) — coffee design history and menu reference
- [work-dream/](../work-dream/) — dream design history and doctrine
- [work-modules-history-principle.md](../work-modules-history-principle.md) — cross-territory history convention
