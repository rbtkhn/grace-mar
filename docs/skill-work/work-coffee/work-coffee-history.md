# work-coffee history

Append-only operator trail for cadence design, ritual changes, and `coffee` workflow architecture.

This log is WORK-only. It is not the Record, not MEMORY, and not a substitute for `recursion-gate.md`.

---

## 2026-03-31 — `hey` to `coffee`, ritual doctrine formalized

- Reframed the daily operator ritual so `coffee` became the canonical trigger and `hey` became a legacy alias.
- Locked in the principle that concrete lane picks under `E` or `G` should exit the ritual and return to normal workflow unless the operator explicitly says `stay in coffee`.
- Added seed-phase support for a default-first cadence preference so future companions can keep `coffee` or later rename the ritual.
- Split ritual concerns into two homes:
  - executable behavior in the `coffee` skill
  - rationale, history, and boundary doctrine in `work-coffee`
- Decided to remove `operator-cadence` as the canonical skill surface and replace it fully with `coffee`.
- Named the main boundary explicitly:
  - operator rhythm and workflow tuning stay in WORK
  - durable governed behavior crosses through `RECURSION-GATE`
  - cross-surface governance changes may need change review first

## 2026-04-02 — coffee Step 2 → **A–E** five modes (**Build** = work-dev + hygiene; no **F**)

- Replaced the **A–I + F** hub with **five** lettered options: **A Today**, **B Build**, **C Compass**, **D Book**, **E Steward** (see [menu-reference.md](menu-reference.md), [coffee SKILL.md](../../../.cursor/skills/coffee/SKILL.md)).
- **Today** merges daily brief + §1d Putin + §1e JD Vance + KY-4 intel (formerly **C** + **E → work-politics**). **Build** merges work-dev + repository hygiene (formerly **B** + **E → work-dev**). **Compass** merges work-strategy + **work-strategy-rome** (formerly **E → strategy** + **I**). **Book** = Jiang / PH (formerly **G**). **Steward** merges gate + template/boundary (formerly **D** + **A**).
- **No close letter:** exit the hub by **C** / **D** (normal workflow unless `stay in coffee`), **Later** on the steward fork, or a non-coffee task. **Skills / meta:** say **skills** / **meta** with **B** or after **Build**, not a sixth menu slot.
- Cross-refs updated: operator-style, handoff-check, dream/bridge/cadence tables, polling-and-markets, pol-dashboard, operator-skills, bootstrap, etc.

## 2026-04-02 — closeout merged into unified `coffee` (no separate closeout menu)

- Removed the **Coffee — closeout** branch as a separate skill section and the **closeout-only** row for **E**.
- **Signing-off** intent still uses `operator_coffee.py --mode closeout` or `operator_handoff_check.py` for **Step 1**; **Step 2** matched work-start (**A–I** until the same-calendar-day **A–E** redesign — see newer 2026-04-02 entry above).
- Former closeout **system pick** was **old menu E** with **no** work sub-lane after signing-off Step 1 (**A–E** redesign: **E — Steward** without gate/template split → system pick).
- Docs and cross-refs updated: `menu-reference.md`, `operator-skills.md`, `handoff-check`, `bridge`, `harness-warmup.mdc`, `operator-style.mdc`, cadence README, etc.

## 2026-04-04 — **E** steward fork: **Implement now / Later**; coffee drops **no menu**

- After **E — Steward**, when **actionable** possibilities exist (pending gate candidates or non-trivial reconciliation), the assistant offers **only** **Implement now** vs **Later**; **Later** returns to full **A–E**. No full coffee menu on that turn.
- When **nothing actionable** surfaced, **E** returns straight to full **A–E** like **A** / **B**.
- Removed **no menu** as a coffee escape; **no menu** / **no options** remains for **non-coffee** WORK menus only (`operator-style.mdc`, [menu-reference.md](menu-reference.md), [coffee SKILL.md](../../../.cursor/skills/coffee/SKILL.md)).

## 2026-04-01 — letter **I** = work-strategy-rome (always on the coffee menu)

- Added **I** to the fixed **`coffee`** Step 2 menu so **work-strategy-rome** always has a dedicated pivot (ROME-PASS, manifest, exemplars, notes).
- Presentation order: **A, B, C, D, E, G, H, I, F** (**F** closes). **I** exits to normal workflow after the turn like **E** (sub-lane) and **G**, unless **`stay in coffee`**.
- **E → work-strategy** (non-Rome) no longer implied Vatican/Rome work; Rome is **menu I** only.
- **Superseded 2026-04-02:** five-mode menu; Rome lives under **C — Compass** (no dedicated **I** letter).

## 2026-04-08 — coffee **A–G**: **F — Cici next**, **G — Dev next**

- Extended Step 2 from five to **seven** letters: **F** = one **work-cici** next task (ground in Step 1 **lane next hints** + SYNC-DAILY / WORK-LEDGER / INDEX); **G** = one **work-dev** next task from [workspace.md](../work-dev/workspace.md) § **Next actions** (narrower than **B — Build**).
- Added `scripts/coffee_lane_next_hints.py`; `operator_coffee.py` prints **`lane next hints (F / G)`** after session load. `assess_session_load.py` annotates **F** and **G**; load **recommendation** stays **A–E** only.
- Cross-refs: `menu-reference.md`, `operator-skills.md`, `operator-style.mdc`, harness-warmup, dream/bridge/harvest/thanks, handoff-check, cadence README, glossary, skills-portable README.

## 2026-04-23 — **D** = **Conductor** (replaces **D — Write**)

- **Canonical menu:** **A** Build, **B** Steward, **C** Strategy (daily brief), **D** Conductor (strategy coffee cadence / [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md)), **E** (system choice — **self-skill-write** / PRP / Xavier / Dev / Rome / Jiang live here or explicit `write` without `coffee`). **D — Write** removed as a menu letter; write-shaped work is **E** or out-of-band **`skill-write`**.

## 2026-04-23 — coffee **A–D2–E** (six lines: **D1** / **D2** Conductor on main menu; no conductor submenu)

- Two Conductor lines on the main menu; **superseded 2026-04-25** by a single **D** line (entry below). A later pass expanded to **D1–D5** (five lines) before consolidation.

## 2026-04-25 — **one** **D — Conductor** (five names, prefix match, bare **D** = continue last)

- **Menu D** is one line: **Toscanini / Furtwängler / Karajan / Kleiber / Bernstein**; operator types **D** + a name prefix, or bare **D** to continue the last `coffee_pick` conductor. **`coffee_pick`** uses **`picked=D` `conductor=<slug>`**; legacy **`D1`..`D5`** still parse from old logs.
- **`assess_session_load.py`:** one **D** key in `option_weights` and `format_annotated_menu` (session-load recommendation remains **A–C** only).

## 2026-04-11 — coffee **A–E** (five options); no micro-hints line

- **Canonical menu:** **A** Build, **B** Steward, **C** Strategy (daily brief), **D** Write, **E** (system choice — one assistant-filled line per session). **Removed** the separate **micro-hints** row under the menu; **removed** dedicated **F/G** letters (Xavier / Dev next fold into **E** or Step 1 lane context).
- **Dream → coffee** mapping: `today_field` → **C**, `build` → **A**, `steward` → **B** (`dream_execution_paths.py`).
- **`assess_session_load.py`:** recommendation and `format_annotated_menu` use **A–E** labels only.
- **`operator_coffee.py`:** lane hints block renamed **Lane context (for menu E — system choice)**.
- Cross-refs: coffee SKILL, operator-style, harness-warmup, handoff-check, menu-reference (legacy A–G tables retained for workload detail), dream SKILL cadence table.

## 2026-03-31 — auto-research and swarm context sharpened the cadence boundary

- Auto-research scaffold work clarified the repo-wide rule that proposal artifacts and orchestration surfaces can evolve without bypassing the gate.
- Swarm integration reinforced the same pattern for operator-only workflow controls: operational state belongs in WORK and orchestration, not in the child Voice prompt.
- This made `work-coffee` a better fit than keeping cadence doctrine buried inside the skill file alone.

## 2026-04-08 — Steward **integrity/exports**; Build scope table

- **E — Steward** now has three sub-tracks: **gate** \| **template/boundary** \| **integrity/exports**. Default **`E` only** remains **gate** if pending, else **template/boundary** — **integrity** is explicit (`E integrity`, `E exports`, or `E all`).
- Moved **`validate-integrity.py`** and **`refresh_derived_exports.py`** (audit / ship) from **B — Build** into Steward; Build = **ship-lane git + work-dev execution** + skills/meta tooling.
- **Steward fork:** template actionable excludes **policy-only expected drift** with no adopt step; integrity failures / clear remediation trigger fork. **menu-reference** adds [Build (B) — detailed scope](menu-reference.md#build-b--detailed-scope); **git-branch-hygiene** fixes cross-ref (template/boundary is **E**, not **A**).
- Cross-refs: `coffee/SKILL.md`, `operator-style.mdc`, `operator-skills.md`.

## 2026-04-08 — **git/ship** under Steward **E** (not Build **B**)

- **Local git** (branches, `git status`, worktrees, commit/push plan) moved from **B — Build** to **E — Steward** as sub-track **git/ship** (`E git`, `E ship`, included in `E all`).
- **B — Build** is now **work-dev execution + skills/meta** only. **Signing-off** add-on: **B** = work-dev/skills carryover; **E** prefers **`E git`** when handoff shows dirty tree / branch noise.
- **Fork actionable** includes git/ship when the tree prescribes commit/push work. `git-branch-hygiene.md` cross-ref: coffee **E — git/ship** (not menu B).

## 2026-04-10 — **A** labeled **Daily Brief** (not “work-politics-first”)

- Renamed coffee Step 2 **A** from **Today** to **Daily Brief** in [menu-reference.md](menu-reference.md), [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md), `assess_session_load.py` (annotated menu label), `dream_execution_paths.py` (handoff titles + `first_move` text), operator docs, and daily-brief watch footers.
- **Framing:** the **daily brief** path (generator, §1d/§1e watch slices, registry) is the primary meaning of **A**; KY-4 / Polymarket / Massie intel remains **deferred from Step 1** and runs as an **optional slice** when the operator chooses **A** (or asks explicitly), not as the fixed identity of the letter.
