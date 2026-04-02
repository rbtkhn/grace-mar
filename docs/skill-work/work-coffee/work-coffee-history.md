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

## 2026-04-02 — closeout merged into unified `coffee` (no separate closeout menu)

- Removed the **Coffee — closeout** branch as a separate skill section and the **closeout-only** row for **E**.
- **Signing-off** intent still uses `operator_coffee.py --mode closeout` or `operator_handoff_check.py` for **Step 1**; **Step 2** matches work-start (now **A–I** after letter **I** was added — see next entry).
- Former closeout **E** (**system pick**) is now **E** with **no** work-dev/strategy/politics sub-lane after signing-off Step 1.
- Docs and cross-refs updated: `menu-reference.md`, `operator-skills.md`, `handoff-check`, `bridge`, `harness-warmup.mdc`, `operator-style.mdc`, cadence README, etc.

## 2026-04-01 — letter **I** = work-strategy-rome (always on the coffee menu)

- Added **I** to the fixed **`coffee`** Step 2 menu so **work-strategy-rome** always has a dedicated pivot (ROME-PASS, manifest, exemplars, notes).
- Presentation order: **A, B, C, D, E, G, H, I, F** (**F** closes). **I** exits to normal workflow after the turn like **E** (sub-lane) and **G**, unless **`stay in coffee`**.
- **E → work-strategy** (non-Rome) no longer implied Vatican/Rome work; Rome is **menu I** only.

## 2026-03-31 — auto-research and swarm context sharpened the cadence boundary

- Auto-research scaffold work clarified the repo-wide rule that proposal artifacts and orchestration surfaces can evolve without bypassing the gate.
- Swarm integration reinforced the same pattern for operator-only workflow controls: operational state belongs in WORK and orchestration, not in the child Voice prompt.
- This made `work-coffee` a better fit than keeping cadence doctrine buried inside the skill file alone.
