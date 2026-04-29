# Conductor pass (generic) — five movements, any territory

**Status:** WORK (operator pattern). **Not** Record. **Not** a merge or gate substitute.

**Purpose:** A **territory-agnostic** description of the **conductor** role in Grace‑Mar: the operator sets **emphasis, tempo, and depth**; tools and file trees do **not** replace judgment. The **five movement** map (Precision → … → Selectivity) is **portable**—it describes **modes of attention**, not one folder.

**Relationship to the `coffee` menu:** The **Symphony masters** are **not** listed as five separate hub lines. **`coffee` Step 2** includes **E — Conductor** as the **single** in-`coffee` slot for **Conductor continuation** (after Step 1). You may still open **Conductor** **without** `coffee`: invoke a master **directly** (**`toscanini`**, **`karajan`**, **`bernstein`**, …), say **`conductor`** + optional fragment, or use [`.cursor/skills/conductor/SKILL.md`](../../../.cursor/skills/conductor/SKILL.md) — same resolution as [coffee SKILL — Conductor session (outside `coffee` hub menu)](../../../.cursor/skills/coffee/SKILL.md#conductor-only-no-coffee). Strategy-notebook SSOT for the embodied ritual: [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md). This file remains the **shared spine** for cross-lane analogy.

**Relationship to synthesis doctrine:** The same **figures → Grace‑Mar anchor** table lives in [SYNTHESIS-OPERATING-MODEL.md](../work-strategy/strategy-notebook/SYNTHESIS-OPERATING-MODEL.md#techniques-inspired-by-the-masters) (*Techniques inspired by the masters*). These three documents are **consistent**, not competitive: **SYNTHESIS-OM** = theory; this page = **cross-lane** pass shape; **COFFEE-CADENCE** = **notebook** timeboxed ritual and seeds.

**Layer map:** [CONDUCTOR-LAYER-MAP.md](CONDUCTOR-LAYER-MAP.md) — distinguishes synthesis theory, strategy-notebook ritual, **this** generic cross-lane pass, Cursor skills, compiled-view recipes, and coding-agent proposal lenses. **This file** defines the **generic cross-lane conductor pass** shape.

**Menus vs slugs:** Use standard labels when two **A–E** menus could appear in one thread — **Coffee Hub Menu** (`coffee` Step 2 hub); **Master Selection Menu** (stance row — [§ Conductor MCQ](#conductor-mcq)); **Conductor Action Menu** ([§ Conductor action MCQ](#conductor-action-mcq)). **Letters are UI conveniences**; **durable logs** should record **conductor slugs** (`toscanini`, `furtwangler`, `bernstein`, `karajan`, `kleiber`), not hub/action letters.

**Coding-agent proposals:** Conductor stance should change **scope, validation posture, non-goals, and acceptance criteria** — not merely wording — per [conductor proposal lenses](../work-dev/conductor-proposal-lenses.md). For coding-agent proposal work, use the **Beethoven test** appendix in that file when the five modes risk collapsing into the same PR shape under **crisis, propulsion, or formal drama**; use the **Brahms test** appendix there when the issue is **density, overlap, continuity, or anti-heaviness** rather than dramatic conflict.

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
| **Strategy notebook** ( **Conductor session** — master name / `conductor` skill ) | Expert/voice **threads**, **Machine** + **Journal**, `strategy-page`, `days.md` / `meta.md` | [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) |
| **work-dev** | Specs, integration, `workspace.md` next actions | [workspace.md](../work-dev/workspace.md), [INTEGRATION-PROGRAM.md](../work-dev/INTEGRATION-PROGRAM.md) |
| **work-politics** | Daily brief, campaign queue, brief registry | [brief-source-registry.md](../work-politics/brief-source-registry.md), `daily-brief-YYYY-MM-DD.md` |
| **work-cici** | Cici/OB1 rhythm, handoff, day journal | [INDEX.md](../work-cici/INDEX.md), [SYNC-DAILY.md](../work-cici/SYNC-DAILY.md) |
| **work-jiang / PH** | Lecture pipeline, forward chains, STATUS | [research/external/work-jiang/README.md](../../../research/external/work-jiang/README.md) |
| **Steward / membrane** | Gate, template parity, integrity, ship | [menu-reference — Steward](menu-reference.md#steward-follow-up-fork-implement-now-vs-later) ( **`coffee` A** ) — **governance** work is **not** a substitute for artistic “balance” in threads; it is the **frame** that keeps other lanes safe. |

When you are **not** in **`coffee`**, you do **not** need to call this a “Conductor pass” in chat—**use the lane’s normal names**. The value of this doc is a **common vocabulary** for “how we sequence attention” in retrospectives, handoffs, and skill text.

---

<a id="conductor-d-menu"></a>
<a id="conductor-d1-d5"></a>

## Conductor session (strategy-notebook) — hub **E** vs standalone

**`coffee` Step 2** is **A–E**. **E — Conductor** continues Conductor after **`coffee`** Step 1. **`last_logged_conductor`** from cadence is the **default master**: **auto-continue** — orientation + **Conductor action MCQ** **without** pasting the **Masters MCQ** (`build_conductor_mcq_for_user`) when a qualifying **`coffee_pick`** with **`conductor=`** exists. Paste the **Masters MCQ** only when **no** prior conductor is logged **or** the operator asks to switch masters in that turn.

Open **standalone** Conductor (no `coffee`) by **master name**, **`conductor`**, or [`.cursor/skills/conductor/SKILL.md`](../../../.cursor/skills/conductor/SKILL.md) — see [coffee SKILL — Conductor session (outside `coffee` hub menu)](../../../.cursor/skills/coffee/SKILL.md#conductor-only-no-coffee). **`build_conductor_mcq_for_user`** / `format_conductor_mcq_block` supply the Masters row when disambiguation is needed.

**Hub pick logging:** `picked=E conductor=<slug>` when the operator chose **E** from the **`coffee`** hub — **`<slug>`** is the **resolved** conductor (**auto-continued** **or** chosen after Masters MCQ). **Legacy:** `picked=conductor`, `picked=D` + `conductor=`, etc.

<a id="conductor-mcq"></a>

### Conductor MCQ — letters **A.–E.** = five masters (not hub letters)

Use this row when the operator needs to **choose or switch** masters (**standalone** Conductor, **`coffee` hub E** with **no** prior `coffee_pick` `conductor=`, **or** explicit request to see the five-master row). **`coffee` hub E** with **`last_logged_conductor`**: **skip** this row — **auto-continue** that master ([coffee SKILL — Hub E](../../../.cursor/skills/coffee/SKILL.md#hub-e-auto-continue)).

| MCQ letter | Master | Movement | What this card does |
|------------|--------|------------|----------------------|
| **A** | Toscanini | Precision | **Truth-to-form** — seams, verification, anti-indulgence, disciplined score architecture. |
| **B** | Furtwängler | Flow | **Organic emergence** — tension without forced closure; listen before the verdict. |
| **C** | Karajan | Elegance | **Long arc** — integrated balance, economy, total effect of the whole. |
| **D** | Kleiber | Selectivity | **Depth by refusal** — chosen hotspots; what is *not* deepened this round. |
| **E** | Bernstein | Vitality | **Communicative heat** — stakes and pulse; what must be felt. |

Each printed option includes a **continuity** tail: last `coffee_pick` slug, optional `focus` / `arc`, and the dream / session-load **advisory** match when relevant.

**How the operator picks:** A **Conductor MCQ** letter **A.–E.**; or **master name / prefix** in the message; or **`conductor`** + fragment; or **bare `conductor`** to continue the **same conductor as last time** when resolvable (`last_logged_conductor` / `resolve_d_conductor("", …)`). If two prefix fragments match, ask for a longer fragment or a Conductor **A.–E.** letter. Single-character **A.–E** in a **standalone conductor** turn maps to the **masters** row (`conductor_submenu_letter_to_slug`), **not** the **`coffee` hub** letters — the hub has its **own** **A–E** (including **E — Conductor**). When **both** a **coffee hub** menu and a **Conductor action MCQ** appear, **label** them ([coffee SKILL Step 2](../../../.cursor/skills/coffee/SKILL.md#coffee-step-2-hub)).

**On pick,** give the usual **short** Conductor orientation ([COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md)).

<a id="conductor-action-mcq"></a>

#### Conductor action MCQ (second **A.–E.** — **required**)

**Not** another **A.–E.** that names **Toscanini…Bernstein** — it is a **new** **five-line** list **after** the master is resolved, with **this** pass’s **repo** next moves. Label it **`Conductor action MCQ`** and instruct **Reply A–E** for **this** pass. Each line is a **concrete, repo-grounded** next move (path or explicit refusal for this round), with **verbs and constraints** that match the **active** `conductor` slug (see [`.cursor/skills/conductor/SKILL.md`](../../../.cursor/skills/conductor/SKILL.md) **Conductor action MCQ**). **Omit** only if the operator says **"orientation only"** or **"no action menu"** in the same turn. **Kleiber** is not the only mode that gets a menu; **Bernstein, Toscanini,** etc. all get **their own** five options — same **A.–E.** letters; letter-set reuse order is **coffee** hub **A–E**, optional **Masters MCQ** row **if** shown, then **Conductor action MCQ**.

**Outside `coffee`:** the operator issues the conductor pick **without** running `coffee` Step 0–1. Resolution, orientation, and **`coffee_pick`** logging match [coffee § Conductor session](../../../.cursor/skills/coffee/SKILL.md#conductor-only-no-coffee); do **not** require Recent rhythm or `operator_coffee.py` for that turn.

**Continuity + recommendation helpers:** The assistant may still mention **last picked** conductor and **system recommended** conductor in prose before or after the menu. Those helpers come from [scripts/cadence_conductor_resolution.py](../../../scripts/cadence_conductor_resolution.py) and are **advisory**, not a second menu.

**Persistence (history / continuity):** **New** logs: **`picked=conductor`** with **`conductor=<single-slug>`** (preferred). **Legacy** logs may still show **`picked=D`** + `conductor=` or **`picked=D1`..`D5`**. **Convention:** `conductor=` is `toscanini` \| `furtwangler` \| `karajan` \| `kleiber` \| `bernstein`. **Legacy** `a+b` stacks: normalize to the **first** slug. **New** logs must **not** use `+`. **Example:** `python3 scripts/log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=conductor conductor=karajan` — [coffee SKILL — Cadence audit](../../../.cursor/skills/coffee/SKILL.md#cadence-audit).

### Learning loop (optimal / recursive self-improvement)

Cadence lines alone are **insufficient** to store *what* improved in the work. **After** orientation and the prescribed notebook actions, the operator (or agent, with the operator’s OK) should **close** the pass with at least one of:

1. A **Conductor close** in **`chapters/YYYY-MM/days.md`** (or a `strategy-page` **Reflection**), using the paste block in [CONDUCTOR-CLOSE-TEMPLATE.md](../work-strategy/strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md) — *stance, object, falsify / next test, escalation*; or  
2. **`coffee_conductor_outcome`** in [work-cadence-events.md](../work-cadence/work-cadence-events.md) with `verdict=` and optional `notebook_ref=` / `falsify=`.

**SSOT (layer map, mermaid, gate boundary):** [CONDUCTOR-IMPROVEMENT-LOOP.md](../work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md). **Not** Record; **not** a substitute for full **EOD** `strategy page` when the day needs a real compose.

---

## What this is not

- **Not** a second **`coffee`** step for every lane; the **`coffee` Step 2** hub is **A–E** in [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md).
- **Not** an instruction to **merge** the Record, auto-promote, or replace **A — Steward** with “conduct the gate.”
- **Not** a replacement for **C — Historian** (daily brief + Tri-Frame when chosen).

---

## See also

- [CONDUCTOR-IMPROVEMENT-LOOP.md](../work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md) — operator **improvement loop** (conductor + notebook + promotion + gate when policy).
- [menu-reference.md](menu-reference.md) — **`coffee` A–E** hub + **standalone Conductor** (`#conductor-fork-d-menu` anchors legacy disambiguation notes).
- [work-coffee README](README.md) — territory role of `work-coffee`.
