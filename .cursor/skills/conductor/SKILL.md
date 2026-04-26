---
name: conductor
preferred_activation: conductor
description: "Conductor: work-dev–associated execution pattern — pick → act on disk → falsify → log → compress. Triggers: conductor, D + prefix (klei, tos, …), coffee Step 2 after hub D. Five masters + cadence live in strategy-notebook + coffee; this skill is the short router. Optional Kleiber action MCQ."
---

# Conductor (work-dev — execution recursion)

**Territory home:** [work-dev](../../../docs/skill-work/work-dev/README.md) — the lane where **scripts**, **workspace**, **integration**, and **CI-backed** compounding sit ([workspace.md](../../../docs/skill-work/work-dev/workspace.md), [compound-loop.md](../../../docs/skill-work/work-dev/compound-loop.md), [three-compounding-loops.md](../../../docs/skill-work/work-dev/three-compounding-loops.md)). **On-disk** **durable** **Conductor** **closes** for **this** **lane** are **wired** in [dev-notebook (work notebook)](../../../docs/skill-work/work-dev/dev-notebook/README.md#conductor-work-dev) and **day** **files** under [work-dev/journal](../../../docs/skill-work/work-dev/dev-notebook/work-dev/journal/README.md#conductor-in-dev-journal) — **not** in strategy **chapters/…/days.md** when the object is **work-dev**-native. The **Conductor** skill is **not** a second OpenClaw spec; it names **one** **recursive** **shape** the operator reuses **across** work modes: **choose emphasis** (stance) → **one** or **two** **hotspots** on disk → **falsify** or **outcome** line → **cadence** (optional) → hand off to **dream** / **bridge** / **Steward** as needed.

**Named Symphony surface (vocabulary + menu):** The **Toscanini → Bernstein** **masters**, `coffee` **hub** **D**, and **Conductor** **MCQ** **row** are **SSOT** in [`.cursor/skills/coffee/SKILL.md`](../coffee/SKILL.md) and [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md) (strategy-notebook / **Symphony of Civilization**). **work-dev** does **not** own those **names**; it **uses** the same **conductor** **turn** for **clarity of next move** on **this** **repo’s** **execution** **spine**.

**Short router:** Use this file when the operator says **`conductor`**, **Conductor pass**, or **`D` + prefix** / **bare** **`D`**, and you need **concise** **routing** without pasting the full **coffee** doc.

## When to read this

- Operator says **`conductor`**, or **`D` +** fragment, with or without **`coffee`**.
- **Hub** **D** then **second** **A**–**E** = **masters** row — [CONDUCTOR-PASS — Conductor MCQ](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-mcq).
- **work-dev** **Build** (coffee **A**) often **feeds** the same session: [work-dev workspace Next actions](../../../docs/skill-work/work-dev/workspace.md) can **inform** **Kleiber** (or other) **action** **MCQ** **options** when the **object** is **ship** / **harness** / **derived** **regeneration** — still **one** **refusal** **wall** per pass.

## Do / don’t

| Do | Don’t |
|----|--------|
| **Conductor only** (no **`coffee`**): no `operator_coffee.py`, no **Recent rhythm** — [coffee § Conductor only](../coffee/SKILL.md#conductor-only-no-coffee) | Re-spec full **COFFEE-CADENCE** **movements** — [protocol](../../../docs/skill-work/work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) is SSOT. |
| **MCQ (masters):** [cadence_conductor_resolution.py](../../../scripts/cadence_conductor_resolution.py) `build_conductor_mcq_for_user` | Conflate **hub** **A**–**E** with **Conductor** **A**–**E**. |
| **Log:** `coffee_pick` `picked=D` `conductor=<slug>`. [Cadence audit](../coffee/SKILL.md#cadence-audit) | Merge **Record** from Conductor. |
| **Close (optional):** [CONDUCTOR-IMPROVEMENT-LOOP](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md) · [CONDUCTOR-CLOSE-TEMPLATE](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md) · `coffee_conductor_outcome` | Treat log lines as full memory. |
| **Kleiber** **action** **MCQ:** **five** **discriminating** **actions**; ground in **current** **repo** — **strategy-notebook** / **strategy-state-iran** **or** [workspace.md](../../../docs/skill-work/work-dev/workspace.md) + **work-dev** **paths** when the pass is **execution-heavy**; **one** **refusal** per option. | Generic lists; copy **master** row as “actions.” |
| **Other masters:** orientation per [CONDUCTOR-PASS](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-d-menu) + [COFFEE-CADENCE](../../../docs/skill-work/work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md); sub-MCQ **default** **Kleiber** | Replace **B** / **C** with Conductor. |

## One-liner commands

```bash
python3 -c "from scripts.cadence_conductor_resolution import build_conductor_mcq_for_user; print(build_conductor_mcq_for_user('grace-mar'))"
python3 scripts/log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=D conductor=<slug> --cursor-model "<from Cursor UI>"
python3 scripts/log_cadence_event.py --kind coffee_conductor_outcome -u grace-mar --ok --kv verdict=watch --kv notebook_ref=<path-or-fragment>
```

## Related

- [dev-notebook — Conductor (work-dev)](../../../docs/skill-work/work-dev/dev-notebook/README.md#conductor-work-dev) (where **work-dev** Conductor **output** **lands**)
- [work-dev — workspace (entrypoint)](../../../docs/skill-work/work-dev/workspace.md)
- [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md) (generic + cross-territory table)
- [work-cadence-events.md](../../../docs/skill-work/work-cadence/work-cadence-events.md) (`conductor=`)
- [STRATEGY-NOTEBOOK-ARCHITECTURE](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) (when the object is `days.md` / weave)

**Done when:** Master resolved; orientation delivered; `coffee_pick` if applicable; **Kleiber action MCQ** when **`conductor=kleiber`**; optional close; return to normal workflow (unless **`stay in coffee`**).
