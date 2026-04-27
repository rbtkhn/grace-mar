---
name: conductor
preferred_activation: conductor
description: "Conductor: work-dev–associated execution — pick → act on disk → falsify → log → compress. After any resolved conductor=<slug>, emit Conductor action MCQ (five A–E repo-grounded next moves, master-shaped). Triggers: conductor, D + prefix, coffee Step 2 after hub D."
---

# Conductor (work-dev — execution recursion)

**Territory home:** [work-dev](../../../docs/skill-work/work-dev/README.md) — the lane where **scripts**, **workspace**, **integration**, and **CI-backed** compounding sit ([workspace.md](../../../docs/skill-work/work-dev/workspace.md), [compound-loop.md](../../../docs/skill-work/work-dev/compound-loop.md), [three-compounding-loops.md](../../../docs/skill-work/work-dev/three-compounding-loops.md)). **On-disk** **durable** **Conductor** **closes** for **this** **lane** are **wired** in [dev-notebook (work notebook)](../../../docs/skill-work/work-dev/dev-notebook/README.md#conductor-work-dev) and **day** **files** under [work-dev/journal](../../../docs/skill-work/work-dev/dev-notebook/work-dev/journal/README.md#conductor-in-dev-journal) — **not** in strategy **chapters/…/days.md** when the object is **work-dev**-native. The **Conductor** skill is **not** a second OpenClaw spec; it names **one** **recursive** **shape** the operator reuses **across** work modes: **choose emphasis** (stance) → **one** or **two** **hotspots** on disk → **falsify** or **outcome** line → **cadence** (optional) → hand off to **dream** / **bridge** / **Steward** as needed.

**Named Symphony surface (vocabulary + menu):** The **Toscanini → Bernstein** **masters**, `coffee` **hub** **D**, and **Conductor** **MCQ** **row** are **SSOT** in [`.cursor/skills/coffee/SKILL.md`](../coffee/SKILL.md) and [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md) (strategy-notebook / **Symphony of Civilization**). **work-dev** does **not** own those **names**; it **uses** the same **conductor** **turn** for **clarity of next move** on **this** **repo’s** **execution** **spine**.

**Short router:** Use this file when the operator says **`conductor`**, **Conductor pass**, or **`D` + prefix** / **bare** **`D`**, and you need **concise** **routing** without pasting the full **coffee** doc.

## When to read this

- Operator says **`conductor`**, or **`D` +** fragment, with or without **`coffee`**.
- **Hub** **D** then **second** **A**–**E** = **masters** row — [CONDUCTOR-PASS — Conductor MCQ](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-mcq).
- **work-dev** **Build** (coffee **A**) often **feeds** the same session: [work-dev workspace Next actions](../../../docs/skill-work/work-dev/workspace.md) can **inform** **action** **MCQ** **options** when the **object** is **ship** / **harness** / **derived** **regeneration** — still **at least one** **explicit** **refusal** or **scope** line where **Kleiber**-style depth applies.

## Do / don’t

| Do | Don’t |
|----|--------|
| **Conductor only** (no **`coffee`**): no `operator_coffee.py`, no **Recent rhythm** — [coffee § Conductor only](../coffee/SKILL.md#conductor-only-no-coffee) | Re-spec full **COFFEE-CADENCE** **movements** — [protocol](../../../docs/skill-work/work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) is SSOT. |
| **MCQ (masters):** [cadence_conductor_resolution.py](../../../scripts/cadence_conductor_resolution.py) `build_conductor_mcq_for_user` | Conflate **hub** **A**–**E** with **Conductor** **A**–**E**. |
| **Log:** `coffee_pick` `picked=D` `conductor=<slug>`. [Cadence audit](../coffee/SKILL.md#cadence-audit) | Merge **Record** from Conductor. |
| **Close (optional):** [CONDUCTOR-IMPROVEMENT-LOOP](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md) · [CONDUCTOR-CLOSE-TEMPLATE](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md) · `coffee_conductor_outcome` | Treat log lines as full memory. |
| **Conductor action MCQ (required** unless **orientation only** / **no action menu**): for **every** resolved slug, **not** only **Kleiber** — **five** **A.–E.** **next** **moves** for **this** `conductor`; each line = **concrete** path, edit, or **explicit** **not-this-round**; ground in **current** **repo** — **strategy-notebook** (e.g. `chapters/…/days.md`, weave, `strategy-state-iran/`) and/or [workspace.md](../../../docs/skill-work/work-dev/workspace.md) + [dev-notebook](../../../docs/skill-work/work-dev/dev-notebook/README.md) when **ship**-heavy. See **§ Conductor action MCQ** below. | Generic lists; re-list **Toscanini…Bernstein** as if they were “actions.” |

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

**Done when:** Master resolved; orientation delivered; **Conductor action MCQ** (five **A.–E.**) unless operator opted out; `coffee_pick` if applicable; optional close; return to normal workflow (unless **`stay in coffee`**).

## Conductor action MCQ (second **A.–E.** for the resolved slug)

**When:** Immediately **after** short orientation, whenever `conductor=<slug>` is **known** — **coffee** path, **conductor-only** path, or **D** + letter/name **without** a prior “orientation only” opt-out. **SSOT** anchor: [CONDUCTOR-PASS — Conductor action MCQ](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-action-mcq).

**What:** A **header** (e.g. **Conductor action MCQ** — **Reply A–E** for **this** `bernstein` pass) and **exactly five** lines **A.** … **E.** Each option is a **discriminating** next move: **file path** or **editing target**, **one** main **verb**, and **enough** **constraint** that **A** vs **B** vs **C** are **not** interchangeable. Re-use letters **A–E**; this is the **third** letter row in a full **coffee+Conductor** turn (hub → masters → **actions**), so **label** the block so it is not confused with **hub** or **master** rows.

| Slug (anchor) | Shape hints (each of the 5 should reflect **this** row — mix as appropriate) |
|---------------|-----------------------------------------------------------------------------|
| **toscanini** | Verify or pin **receipt**; **split** a claim by **tier**; **one** falsify line; **seam** between thread and `days.md` / chapter; **one** “what would change the tag?” |
| **furtwangler** | Hold **tension** without forced verdict; **watch** / **worry** lines; **one** paragraph that **stops** at **conditions**; **linkage** you are **not** closing; **contrast** two institutional voices |
| **karajan** | **Month-arc** balance; **trim** or **dedupe** pointer; **across** two voices or channels; **one** long-horizon bet; **one** “what we are **not** optimizing this week” |
| **kleiber** | **Hotspot** on disk; **depth**; **explicit** **refusals** / not-this-round; **falsify**; **harness** or **script** touch when the loop is **execution**-native |
| **bernstein** | **Stakes** in **one** line; **pulse** in `days.md` or **Reflection**; **one** “live **Judgment**” or **public legibility** move; **Conductor close** with **heat**; **contrast** arc vs wire |

**Stop making the mistake** = treat **Kleiber** as **exemplar**, **not** **exclusive** — the **action** **MCQ** is **contract** for **every** slug unless the operator opts out in the same message.
