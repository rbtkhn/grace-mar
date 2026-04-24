# Conductor pass (generic) — five movements, any territory

**Status:** WORK (operator pattern). **Not** Record. **Not** a merge or gate substitute.

**Purpose:** A **territory-agnostic** description of the **conductor** role in Grace‑Mar: the operator sets **emphasis, tempo, and depth**; tools and file trees do **not** replace judgment. The **five movement** map (Precision → … → Selectivity) is **portable**—it describes **modes of attention**, not one folder.

**Relationship to the `coffee` menu:** The trigger **`coffee` → D1** or **`D2`** (both on the **same** Step 2 list as **A–C** and **E**) still names **one** SSOT for the **strategy-notebook** instantiation — [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) (*Symphony of Civilization*, expert threads, `strategy-page` seeds). This file is the **shared spine** you can use **by analogy** in other lanes without relabeling those lanes as **D1/D2** in the menu.

**Relationship to synthesis doctrine:** The same **figures → Grace‑Mar anchor** table lives in [SYNTHESIS-OPERATING-MODEL.md](../work-strategy/strategy-notebook/SYNTHESIS-OPERATING-MODEL.md#techniques-inspired-by-the-masters) (*Techniques inspired by the masters*). These three documents are **consistent**, not competitive: **SYNTHESIS-OM** = theory; this page = **cross-lane** pass shape; **COFFEE-CADENCE** = **notebook** timeboxed ritual and seeds.

---

## The five movements (abstraction)

| Movement | Mode | What it is (any lane) |
|----------|------|------------------------|
| **1 — Precision** | Toscanini | **Seams and verification** — what is unambiguous, what must not be asserted without support, what is a proper noun or date to check. |
| **2 — Flow** | Furtwängler | **Tension without resolution** — let conflicting pulls show; do not force a single story yet. |
| **3 — Vitality** | Bernstein | **Stakes and heat** — why this block of work matters *now* (still bounded by facts you actually have). |
| **4 — Elegance** | Karajan | **Long arc and balance** — how this sits in a week, month, or program line (not a polish pass on everything). |
| **5 — Selectivity** | Kleiber | **Depth budget** — one or two things get disproportionate follow-up; the rest is explicitly *not* deepened this round. |

**Stop rule:** One session = **one** primary territory (table below) unless you are explicitly doing a **tour** (rare). End with a **concrete** next handoff: file path, brief line in `days.md` / inbox, or **no** action stated plainly.

---

## Instantiations by territory (pointers, not menu letters)

| Territory | “Score” to conduct | First anchor (illustrative) |
|-----------|--------------------|-----------------------------|
| **Strategy notebook** ( **`coffee` D1 / D2** ) | Expert/voice **threads**, **Machine** + **Journal**, `strategy-page`, `days.md` / `meta.md` | [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) |
| **work-dev** | Specs, integration, `workspace.md` next actions | [workspace.md](../work-dev/workspace.md), [INTEGRATION-PROGRAM.md](../work-dev/INTEGRATION-PROGRAM.md) |
| **work-politics** | Daily brief, campaign queue, brief registry | [brief-source-registry.md](../work-politics/brief-source-registry.md), `daily-brief-YYYY-MM-DD.md` |
| **work-cici** | Cici/OB1 rhythm, handoff, day journal | [INDEX.md](../work-cici/INDEX.md), [SYNC-DAILY.md](../work-cici/SYNC-DAILY.md) |
| **work-jiang / PH** | Lecture pipeline, forward chains, STATUS | [research/external/work-jiang/README.md](../../../research/external/work-jiang/README.md) |
| **Steward / membrane** | Gate, template parity, integrity, ship | [menu-reference — Steward](menu-reference.md#steward-follow-up-fork-implement-now-vs-later) ( **`coffee` B** ) — **governance** work is **not** a substitute for artistic “balance” in threads; it is the **frame** that keeps other lanes safe. |

When you are **not** in **`coffee`**, you do **not** need to call this a “Conductor pass” in chat—**use the lane’s normal names**. The value of this doc is a **common vocabulary** for “how we sequence attention” in retrospectives, handoffs, and skill text.

---

<a id="conductor-d1-d2"></a>

## `coffee` menu **D1** and **D2** (strategy-notebook) — main menu, not a submenu

**D1** and **D2** are **two separate lines** on the same Step 2 list as **A, B, C, E** (see [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md)). There is **no** second turn that asks “D1 or D2?” after a single **D** — the operator picks **D1** or **D2** directly from the **first** menu paste.

| ID | Main menu line (abbreviated) | Behavior |
|----|------------------------------|----------|
| **D1** | Conductor — continue last emphasis | Reuse the **same movement emphasis** as the **last** completed Conductor run recorded on disk (see **Persistence**). If **none** is found, say so in one line and use **D2** logic or ask for **one** named movement. |
| **D2** | Conductor — system recommended | Recommend a **movement stack** (one or two modes) from **operational** signals in **priority order** — not Record, not policy. **Resolution order** (first match wins unless you merge hints): (1) `users/<id>/last-dream.json` — `worktreeState` / `worktreeAdvice` (e.g. risky residue → **Toscanini** then **Karajan**), `tomorrow_inherits` and steward-flavored hints → **Kleiber** + **Toscanini**; (2) collapsed **Last dream** / **Dream → coffee menu** in Step 1 warmup (e.g. lean **B—Steward** → **Kleiber** + **Toscanini**); (3) `Session load: … (recommended: … )` from `operator_coffee.py` — map **A→Build/implementation** to **Toscanini** + **Karajan**, **B→Steward** to **Kleiber** + **Toscanini**, **C→Strategy** to **Bernstein** + **Furtwängler**; (4) if still empty, default **Furtwängler** + **Kleiber**. **Heuristic, not oracular** — the operator may override. |

**On pick D1 or D2,** give the usual **short** Conductor orientation ([COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) + **concrete** next actions for the chosen movement(s)).

**Persistence (D1):** Look for the **most recent** `coffee_pick` in [work-cadence/work-cadence-events.md](work-cadence/work-cadence-events.md) for this user with **`picked=D1`** or **`picked=D2`** and a `conductor=` value (legacy: **`picked=D`**). **Convention:** one movement = slug `toscanini` \| `furtwangler` \| `bernstein` \| `karajan` \| `kleiber`; two slugs = `+` (no spaces). If **no** line exists, D1 is **empty**. **Optional** log after the turn: `python3 scripts/log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=D1 conductor=kleiber` (or `picked=D2 conductor=...`) — [coffee SKILL — Cadence audit](../../../.cursor/skills/coffee/SKILL.md#cadence-audit).

---

## What this is not

- **Not** a second **`coffee`** step for every lane; the **Step 2** list is **A–D2–E** in [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md).
- **Not** an instruction to **merge** the Record, auto-promote, or replace **B — Steward** with “conduct the gate.”
- **Not** a replacement for **C — Strategy (daily brief)** (field + Tri-Frame when chosen).

---

## See also

- [menu-reference.md](menu-reference.md#conductor-fork-d1-d2) — **D1 / D2** and full **A–D2–E** contract.
- [work-coffee README](README.md) — territory role of `work-coffee`.
