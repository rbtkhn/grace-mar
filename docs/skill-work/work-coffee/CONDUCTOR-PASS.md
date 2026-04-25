# Conductor pass (generic) — five movements, any territory

**Status:** WORK (operator pattern). **Not** Record. **Not** a merge or gate substitute.

**Purpose:** A **territory-agnostic** description of the **conductor** role in Grace‑Mar: the operator sets **emphasis, tempo, and depth**; tools and file trees do **not** replace judgment. The **five movement** map (Precision → … → Selectivity) is **portable**—it describes **modes of attention**, not one folder.

**Relationship to the `coffee` menu:** The trigger **`coffee` → D1–D5** (all on the **same** Step 2 list as **A–C** and **E**) still names **one** SSOT for the **strategy-notebook** instantiation — [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) (*Symphony of Civilization*, expert threads, `strategy-page` seeds). This file is the **shared spine** you can use **by analogy** in other lanes without relabeling those lanes as menu lines outside strategy-notebook coffee.

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
| **Strategy notebook** ( **`coffee` D1–D5** ) | Expert/voice **threads**, **Machine** + **Journal**, `strategy-page`, `days.md` / `meta.md` | [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) |
| **work-dev** | Specs, integration, `workspace.md` next actions | [workspace.md](../work-dev/workspace.md), [INTEGRATION-PROGRAM.md](../work-dev/INTEGRATION-PROGRAM.md) |
| **work-politics** | Daily brief, campaign queue, brief registry | [brief-source-registry.md](../work-politics/brief-source-registry.md), `daily-brief-YYYY-MM-DD.md` |
| **work-cici** | Cici/OB1 rhythm, handoff, day journal | [INDEX.md](../work-cici/INDEX.md), [SYNC-DAILY.md](../work-cici/SYNC-DAILY.md) |
| **work-jiang / PH** | Lecture pipeline, forward chains, STATUS | [research/external/work-jiang/README.md](../../../research/external/work-jiang/README.md) |
| **Steward / membrane** | Gate, template parity, integrity, ship | [menu-reference — Steward](menu-reference.md#steward-follow-up-fork-implement-now-vs-later) ( **`coffee` B** ) — **governance** work is **not** a substitute for artistic “balance” in threads; it is the **frame** that keeps other lanes safe. |

When you are **not** in **`coffee`**, you do **not** need to call this a “Conductor pass” in chat—**use the lane’s normal names**. The value of this doc is a **common vocabulary** for “how we sequence attention” in retrospectives, handoffs, and skill text.

---

<a id="conductor-d1-d5"></a>

## `coffee` menu **D1–D5** (strategy-notebook) — main menu, not a submenu

**D1–D5** are **five separate lines** on the same Step 2 list as **A, B, C, E** (see [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md)). There is **no** second turn that asks “which D?” after a single **D** — the operator picks **D1**, **D2**, **D3**, **D4**, or **D5** directly from the **first** menu paste.

| ID | Main menu line (shape) | Behavior |
|----|------------------------------|----------|
| **D1** | `D1. Conductor — Toscanini` | **Truth-to-form** pick: seam enforcement, verification, anti-indulgence, and disciplined score architecture. |
| **D2** | `D2. Conductor — Furtwängler` | **Flow** pick: organic emergence, tension without forced closure, and listening for the line beneath the line. |
| **D3** | `D3. Conductor — Bernstein` | **Vitality** pick: communicative heat, public pulse, and what must become vividly legible. |
| **D4** | `D4. Conductor — Karajan` | **Elegance** pick: integrated architecture, long arc, blend, and the total effect of the whole. |
| **D5** | `D5. Conductor — Kleiber` | **Selectivity** pick: chosen hotspots, depth by refusal, and disproportionate attention to what matters most. |

**On pick D1–D5,** give the usual **short** Conductor orientation ([COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md)) plus **concrete** next actions for the **chosen** movement.

**Continuity + recommendation helpers:** The assistant may still mention **last picked** conductor and **system recommended** conductor in prose before or after the menu. Those helpers come from [scripts/cadence_conductor_resolution.py](../../../scripts/cadence_conductor_resolution.py) and are **advisory**, not menu-letter semantics.

**Persistence (history / continuity):** Look for the **most recent** `coffee_pick` in [work-cadence/work-cadence-events.md](work-cadence/work-cadence-events.md) for this user with **`picked=D1`**, **`picked=D2`**, **`picked=D3`**, **`picked=D4`**, or **`picked=D5`** and a `conductor=` value (legacy: **`picked=D`**). **Convention:** `conductor=` is a **single** slug: `toscanini` \| `furtwangler` \| `bernstein` \| `karajan` \| `kleiber`. **Legacy** lines may contain `a+b`; normalize to the **first** slug only. **New** logs must **not** use `+`. **Optional** log after the turn: `python3 scripts/log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=D4 conductor=karajan` — [coffee SKILL — Cadence audit](../../../.cursor/skills/coffee/SKILL.md#cadence-audit).

---

## What this is not

- **Not** a second **`coffee`** step for every lane; the **Step 2** list is **A, B, C, D1, D2, D3, D4, D5, E** in [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md).
- **Not** an instruction to **merge** the Record, auto-promote, or replace **B — Steward** with “conduct the gate.”
- **Not** a replacement for **C — Strategy (daily brief)** (field + Tri-Frame when chosen).

---

## See also

- [menu-reference.md](menu-reference.md#conductor-fork-d1-d5) — **D1–D5** and full coffee menu contract.
- [work-coffee README](README.md) — territory role of `work-coffee`.
