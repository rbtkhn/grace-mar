# Conductor pass (generic) — five movements, any territory

**Status:** WORK (operator pattern). **Not** Record. **Not** a merge or gate substitute.

**Purpose:** A **territory-agnostic** description of the **conductor** role in Grace‑Mar: the operator sets **emphasis, tempo, and depth**; tools and file trees do **not** replace judgment. The **five movement** map (Precision → … → Selectivity) is **portable**—it describes **modes of attention**, not one folder.

**Relationship to the `coffee` menu:** The trigger **`coffee` → D** (one **Conductor** line on the **same** Step 2 list as **A–C** and **E**) names **one** SSOT for the **strategy-notebook** instantiation — [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) (*Symphony of Civilization*, expert threads, `strategy-page` seeds). The menu line lists **Toscanini / Furtwängler / Karajan / Kleiber / Bernstein**; bare **D** continues the last conductor; **D** plus a few letters picks by prefix. This file is the **shared spine** you can use **by analogy** in other lanes without relabeling those lanes as menu lines outside strategy-notebook coffee.

**Relationship to synthesis doctrine:** The same **figures → Grace‑Mar anchor** table lives in [SYNTHESIS-OPERATING-MODEL.md](../work-strategy/strategy-notebook/SYNTHESIS-OPERATING-MODEL.md#techniques-inspired-by-the-masters) (*Techniques inspired by the masters*). These three documents are **consistent**, not competitive: **SYNTHESIS-OM** = theory; this page = **cross-lane** pass shape; **COFFEE-CADENCE** = **notebook** timeboxed ritual and seeds.

---

## The five movements (abstraction)

| Movement | Mode | What it is (any lane) |
|----------|------|------------------------|
| **1 — Precision** | Toscanini | **Truth-to-form** — seams, verification, anti-indulgence, and where rhetoric outruns the actual score. |
| **2 — Flow** | Furtwängler | **Tension without forced closure** — let conflicting pulls show; listen for what is emerging before naming the verdict. |
| **3 — Vitality** | Bernstein | **Stakes and communicative heat** — why this matters *now* and what must be felt, not just noted. |
| **4 — Elegance** | Karajan | **Long arc and integrated balance** — how the whole sits in a week, month, or program line; what to remove so the arc reads cleanly. |
| **5 — Selectivity** | Kleiber | **Depth budget by refusal** — one or two things get disproportionate follow-up; the rest is explicitly *not* deepened this round. |

**Stop rule:** One session = **one** primary territory (table below) unless you are explicitly doing a **tour** (rare). End with a **concrete** next handoff: file path, brief line in `days.md` / inbox, or **no** action stated plainly.

---

## Instantiations by territory (pointers, not menu letters)

| Territory | “Score” to conduct | First anchor (illustrative) |
|-----------|--------------------|-----------------------------|
| **Strategy notebook** ( **`coffee` D — Conductor** ) | Expert/voice **threads**, **Machine** + **Journal**, `strategy-page`, `days.md` / `meta.md` | [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) |
| **work-dev** | Specs, integration, `workspace.md` next actions | [workspace.md](../work-dev/workspace.md), [INTEGRATION-PROGRAM.md](../work-dev/INTEGRATION-PROGRAM.md) |
| **work-politics** | Daily brief, campaign queue, brief registry | [brief-source-registry.md](../work-politics/brief-source-registry.md), `daily-brief-YYYY-MM-DD.md` |
| **work-cici** | Cici/OB1 rhythm, handoff, day journal | [INDEX.md](../work-cici/INDEX.md), [SYNC-DAILY.md](../work-cici/SYNC-DAILY.md) |
| **work-jiang / PH** | Lecture pipeline, forward chains, STATUS | [research/external/work-jiang/README.md](../../../research/external/work-jiang/README.md) |
| **Steward / membrane** | Gate, template parity, integrity, ship | [menu-reference — Steward](menu-reference.md#steward-follow-up-fork-implement-now-vs-later) ( **`coffee` B** ) — **governance** work is **not** a substitute for artistic “balance” in threads; it is the **frame** that keeps other lanes safe. |

When you are **not** in **`coffee`**, you do **not** need to call this a “Conductor pass” in chat—**use the lane’s normal names**. The value of this doc is a **common vocabulary** for “how we sequence attention” in retrospectives, handoffs, and skill text.

---

<a id="conductor-d-menu"></a>
<a id="conductor-d1-d5"></a>

## `coffee` menu **D — Conductor** (strategy-notebook)

**One line** on the same Step 2 list as **A, B, C, E** (see [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md)):

`D. Conductor` on the **hub** menu opens this lane. The **Conductor MCQ** (second **A.–E.** row) is the selectable list — see [`.cursor/skills/coffee/SKILL.md`](../../../.cursor/skills/coffee/SKILL.md) Step 2 and `scripts/cadence_conductor_resolution.py` (`build_conductor_mcq_for_user`, `format_conductor_mcq_block`).

<a id="conductor-mcq"></a>

### Conductor MCQ — letters **A.–E.** = five masters (not hub letters)

| MCQ letter | Master | Movement | What this card does |
|------------|--------|------------|----------------------|
| **A** | Toscanini | Precision | **Truth-to-form** — seams, verification, anti-indulgence, disciplined score architecture. |
| **B** | Furtwängler | Flow | **Organic emergence** — tension without forced closure; listen before the verdict. |
| **C** | Karajan | Elegance | **Long arc** — integrated balance, economy, total effect of the whole. |
| **D** | Kleiber | Selectivity | **Depth by refusal** — chosen hotspots; what is *not* deepened this round. |
| **E** | Bernstein | Vitality | **Communicative heat** — stakes and pulse; what must be felt. |

Each printed option includes a **continuity** tail: last `coffee_pick` slug, optional `focus` / `arc`, and the dream / session-load **advisory** match when relevant.

**How the operator picks:** A **Conductor MCQ** letter **A.–E.**; or **`D`** (hub) then **A.–E.** / fragment on the next line; or **`D` +** name fragment in one line; or **bare `D`** to continue the **same conductor as last time** (`last_logged_conductor` / `resolve_d_conductor("", …)`). If two prefix fragments match, ask for a longer fragment or a Conductor **A.–E.** letter. Single-character **A.–E** in a conductor turn maps to the **Conductor** row (`conductor_submenu_letter_to_slug`), not the hub.

**On pick,** give the usual **short** Conductor orientation ([COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md)) plus **concrete** next actions for the **chosen** movement.

**Outside `coffee`:** the operator may issue the **same** conductor pick (**`D`**, **`D` +** fragment, or clear natural-language equivalent) **without** running `coffee` Step 0–1. Resolution, orientation, and **`coffee_pick`** logging match **`coffee` Step 2 D**; do **not** require Recent rhythm or `operator_coffee.py` for that turn. See [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md) § *Conductor only (no `coffee` session)*.

**Continuity + recommendation helpers:** The assistant may still mention **last picked** conductor and **system recommended** conductor in prose before or after the menu. Those helpers come from [scripts/cadence_conductor_resolution.py](../../../scripts/cadence_conductor_resolution.py) and are **advisory**, not a second menu.

**Persistence (history / continuity):** **New** logs: **`picked=D`** with **`conductor=<single-slug>`**. **Legacy** logs may still show **`picked=D1`..`D5`** or **`picked=D`**; **Convention:** `conductor=` is `toscanini` \| `furtwangler` \| `karajan` \| `kleiber` \| `bernstein`. **Legacy** `a+b` stacks: normalize to the **first** slug. **New** logs must **not** use `+`. **Example:** `python3 scripts/log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=D conductor=karajan` — [coffee SKILL — Cadence audit](../../../.cursor/skills/coffee/SKILL.md#cadence-audit).

### Learning loop (optimal / recursive self-improvement)

Cadence lines alone are **insufficient** to store *what* improved in the work. **After** orientation and the prescribed notebook actions, the operator (or agent, with the operator’s OK) should **close** the pass with at least one of:

1. A **Conductor close** in **`chapters/YYYY-MM/days.md`** (or a `strategy-page` **Reflection**), using the paste block in [CONDUCTOR-CLOSE-TEMPLATE.md](../work-strategy/strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md) — *stance, object, falsify / next test, escalation*; or  
2. **`coffee_conductor_outcome`** in [work-cadence-events.md](../work-cadence/work-cadence-events.md) with `verdict=` and optional `notebook_ref=` / `falsify=`.

**SSOT (layer map, mermaid, gate boundary):** [CONDUCTOR-IMPROVEMENT-LOOP.md](../work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md). **Not** Record; **not** a substitute for full **EOD** `strategy page` when the day needs a real compose.

---

## What this is not

- **Not** a second **`coffee`** step for every lane; the **Step 2** list is **A, B, C, D, E** in [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md).
- **Not** an instruction to **merge** the Record, auto-promote, or replace **B — Steward** with “conduct the gate.”
- **Not** a replacement for **C — Strategy (daily brief)** (field + Tri-Frame when chosen).

---

## See also

- [CONDUCTOR-IMPROVEMENT-LOOP.md](../work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md) — operator **improvement loop** (conductor + notebook + promotion + gate when policy).
- [menu-reference.md](menu-reference.md#conductor-fork-d-menu) — **D — Conductor** and full coffee menu contract.
- [work-coffee README](README.md) — territory role of `work-coffee`.
