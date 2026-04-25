---
name: coffee
preferred_activation: coffee
requires: [handoff-check]
description: "Grace-Mar operator cadence and tempo. Primary trigger: coffee. Coffee is a repeatable sip of coherence: a lightweight reorientation ritual that restores clarity, framing, and agency. Multiple coffee sessions per day are normal. Before Step 1 scripts run, synthesize the previous four events from work-cadence-events.md into plain-language **Recent rhythm** (no internal ops jargon or timestamps in chat). Work-start coffee runs the read-only grounding stack, then the **nine-line** menu **A, B, C, D1, D2, D3, D4, D5, E** (Build, Steward, Strategy (daily brief), five named Conductors, system choice). No micro-hints line under the menu. Signing-off intent uses the same menu; closeout is merged into Step 1."
---

# Coffee

**Preferred activation (operator):** say **`coffee`**. Legacy **`hey`** still works as a compatibility alias, but **`coffee`** is the canonical trigger now.

**Signing-off intent** (end of session, wrapping the day, stepping away) uses the **same** **`coffee`** trigger and the **same** **A, B, C, D1, D2, D3, D4, D5, E** menu. There is **no** separate closeout branch or closeout-only menu item. **Step 1** switches to handoff-weighted output when intent is signing off; **Step 2** is unchanged.

`coffee` is not a startup ceremony. `coffee` is a **repeatable sip of coherence**.

Its purpose is to help the operator become more awake to the actual situation, more coherent about priorities, and more directed about the next move. A coffee session does not need to complete the day's thinking. It only needs to improve orientation enough that action becomes easier.

Multiple `coffee` sessions per day are normal. That is not redundancy; it is the point. Each `coffee` is another sip.

## Guardrails

- Do not turn `coffee` into a heavy maintenance ritual by default.
- Do not overload each run with every possible obligation or stale thread.
- Prefer a small number of salient next paths over exhaustive review.
- Keep the operator in the position of renewed agency, not procedural burden.
- `coffee` is for orientation; heavier consolidation belongs to `dream`.
- This is read-only planning. Do not merge or stage just because the warmup mentions candidates.
- If integrity fails, surface that before optional improvements.
- **Contextual stewardship:** Agents have no cross-thread institutional memory; authority for the Record is **on-disk files + gated pipeline** — not model recall or chat summary.

## Relation to dream

`coffee` and `dream` form a biological-cognitive pair:
- **`coffee`** = repeated framing dose (many per day)
- **`dream`** = end-of-day consolidation pass (usually once)

`coffee` should feel like a sip. `dream` should feel like sleep. See `.cursor/skills/dream/SKILL.md` § *Cadence choreography* for the day's sequence and data handoff.

---

## "Coffee" = start here (two steps)

When the operator begins with **`coffee`** (or clearly the same intent; legacy **`hey`** still counts), treat it as opening a **coffee session**.

### Step 0 — Recent rhythm (before Step 1 scripts)

**Read first** — `operator_coffee.py` appends a new **`coffee`** line at the **end** of a successful run, so the log must be read **before** those commands if the rhythm read is to exclude this session.

1. Open **`docs/skill-work/work-cadence/work-cadence-events.md`**. Below `_(Append below this line.)_`, collect lines matching `- **YYYY-MM-DD HH:MM UTC** — kind (user) …`.
2. Take the **last 4** such lines already in the file. If there are fewer than four, use what exists; if none, **Recent rhythm:** _(no prior events)_ in the reply.
3. **Synthesize in plain prose** — **2–4 short sentences** for a human, **not** a telemetry dump: **do not** lead with a wall of `key=value` pairs. **Companion-facing UX:** label this block **Recent rhythm** (or prose only); **do not** put **dates, UTC, or clock times** in this prose (use order and light anchors like “after dream,” “then bridge,” “earlier today” without timestamps). **Must anchor in specifics** from those four lines — name what actually happened (e.g. **bridge** with **commit refs** if present, **coffee** **work-start** vs **standard**, **thanks** **park** text when non-empty, **dream** pass/fail or integrity/governance in ordinary words, **harvest** packet vs not). **Avoid** generic process filler that could apply without reading the file. Do **not** paste raw log lines unless they are already very short.

   **Cadence voice:** Follow the **cadence voice principle** ([work-cadence README](../../../docs/skill-work/work-cadence/README.md#cadence-voice-principle-all-rituals)). Lead with *felt* acknowledgment of what was settled or decided, end with the **optimal next direction**. Use **"we"** framing. The operator should feel **seen, grounded, and ready** — not debriefed. Name what was learned or decided, not what was executed. No commit hashes, no process names — warm, direct, future-facing.
4. In the reply, place **Recent rhythm:** at the **top** of Step 1 content (immediately before script output / warmup paste). Same rule for **signing-off** Step 1 (before `operator_coffee.py --mode closeout` or handoff-only flow).

If the file is missing or empty below the anchor, state that under **Recent rhythm** and continue Step 1.

### Step 1 — Automated actions (one flow, two weights)

**Detect intent**

- **Signing off / closeout / end of session / wrapping the day** → use **closeout-weighted Step 1** below.
- Otherwise → **work-start Step 1** (scale with explicit phrases or weekday cadence).

**Work-start Step 1** — run the consolidated coffee script (preferred):

```bash
python3 scripts/operator_coffee.py -u grace-mar                   # work-start (default)
python3 scripts/operator_coffee.py -u grace-mar --mode light      # lighter pass
python3 scripts/operator_coffee.py -u grace-mar --mode minimal    # compact harness only
python3 scripts/operator_coffee.py -u grace-mar --mode reentry    # cold-thread full stack
```

**Signing-off Step 1** — handoff-weighted (same trigger **`coffee`**, not a second ritual name):

```bash
python3 scripts/operator_coffee.py -u grace-mar --mode closeout
```

Or directly: `python3 scripts/operator_handoff_check.py -u grace-mar`. Include the output in your reply. Add a **short paragraph**: what moved today, what is parked, gate + Jiang carryovers, suggested re-entry prompt. Full spec: [`.cursor/skills/handoff-check/SKILL.md`](../handoff-check/SKILL.md).

If the operator **explicitly** wants **both** full warmup **and** signing-off in one message, run work-start then append handoff (rare).

Add `--compact` for shorter harness output. Individual scripts (`operator_daily_warmup.py`, `harness_warmup.py`, `operator_handoff_check.py`, `operator_reentry_stack.py`) are still available.

**Dream handoff:** If `dream` ran overnight, the daily warmup automatically includes a **"Last dream (night handoff)"** block from `users/grace-mar/last-dream.json`. **Default:** that block is **collapsed** (status, digest counts, tomorrow hint). After that block (or alone if the Last dream section is turned off), warmup prints one line **`Dream → coffee menu:`** mapping dream’s suggested execution path to **A / B / C** (Build / Steward / Strategy · daily brief) — operational hint only; see [dream/SKILL.md](../dream/SKILL.md) § *Five-second closeout*. Extra lines (civ-mem summary, coffee 24h rollup) are **off** by default; tune `config/context_budgets/coffee.json` or pass `--show-civ-mem` / `--show-rollup` on `operator_daily_warmup.py`, `operator_coffee.py`, or `operator_reentry_stack.py`. Approximate paste footprint: `python3 scripts/audit_context_tax.py -u grace-mar`. These files are operator scaffolding, not Record. For full paths / snippets / followups, use **`--verbose-dream`**. When pasting warmup for the operator, prefer **collapsed** unless they ask for detail.

**Step 1 deliverables (work-start):** Warmup brief (priorities, gate, work-politics snapshot where relevant, integrity), branch snapshot, daily brief + intel defer line (path pattern + **menu C — Strategy (daily brief)** when ready), optional PH/Jiang line. **No** Polymarket / poll / Massie blocks in Step 1 unless the operator explicitly asked in the same message.

**Step 1 guardrail:** Stay read-only — no merge/stage unless they switch lanes or use a pipeline phrase ("we …").

**Done when:** Script output is pasted in the reply, Recent rhythm is at the top, and the full coffee menu follows immediately.

For cadence tables and explicit phrase definitions (`coffee light`, `coffee minimal`, `coffee survey`): see [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md).

### Multiple coffees per day

The operator may say **`coffee`** **more than once per calendar day** for reorientation. This is normal. Each new `coffee` runs Step 1 again and starts a new **A, B, C, D1, D2, D3, D4, D5, E** cycle. If **`coffee`** arrives mid-hub, treat it as a **reorientation restart**: run Step 1 again, then offer a fresh menu.

### Step 2 — Multiple choice (required; **nine** lines)

Immediately **after** Step 1 content, output **only** this menu — **nine lines** (**A, B, C, D1, D2, D3, D4, D5, E**). **Do not** add a second row of micro-hints, fork shorthand, or F/G/Xavier/Dev tags under the list. **D1–D5** are **on the main menu** (not a follow-up submenu after a single “D”).

**D1–D5 are fixed conductor picks:** each line names **one** conductor in **Title Case**. Slugs for `coffee_pick` remain: `toscanini` → **Toscanini**; `furtwangler` → **Furtwängler**; `bernstein` → **Bernstein**; `karajan` → **Karajan**; `kleiber` → **Kleiber**.

- **D1:** `D1. Conductor — Toscanini`
- **D2:** `D2. Conductor — Furtwängler`
- **D3:** `D3. Conductor — Bernstein`
- **D4:** `D4. Conductor — Karajan`
- **D5:** `D5. Conductor — Kleiber`

**Continuity and recommendation helpers:** You may mention **last picked** conductor and **system recommended** conductor in **one short sentence** before or after the menu, grounded in [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-d1-d5) and `scripts/cadence_conductor_resolution.py`. These are **helper cues**, not menu-letter semantics.

**A, B, C, E** lines stay as below; **D1–D5** are fixed (example):

```
A. Build
B. Steward
C. Strategy (daily brief)
D1. Conductor — Toscanini
D2. Conductor — Furtwängler
D3. Conductor — Bernstein
D4. Conductor — Karajan
D5. Conductor — Kleiber
E. (system choice) — <one short line: the single best alternate lane this session>
```

**Filling E — (system choice):** Pick **one** concrete slice for this turn, using Step 1 context — e.g. **self-skill-write** (prompts, PRP, Lexile, bot/prompt **proposals** — not merge), **work-cici** next (ground in `coffee_lane_next_hints` / SYNC-DAILY / INDEX), **work-dev** next from [workspace.md](../../../docs/skill-work/work-dev/workspace.md) § **Next actions**, **work-strategy-rome** / ROME-PASS (Compass-style), **work-jiang / PH** (Book-style), or match **`Dream → coffee menu`** when it points at a path not already covered by **A–C / D1–D5**. **Write-shaped** work is **not** a tenth letter — it defaults here or when the operator says **`write`** / **`skill-write`** without **`coffee`**. State it plainly in the angle-bracket line; **do not** add a separate “micro-hints” row.

**Step 1 context for E:** `operator_coffee.py` prints **`Lane context (for menu E)`** — two lines from `scripts/coffee_lane_next_hints.py` (work-cici + work-dev). Use when choosing **E** or when wording the **E** line.

**Optional load note:** Step 1 may print `Session load: … (recommended: X)` (**A** / **B** / **C**). You may mention that **one** recommended letter and/or **one** recommended conductor in prose before or after the menu — **not** as a second labeled menu block and **not** as micro-hints under the list.

**Quick reference (modes):**

- **A. Build** — **work-dev + skills/meta** (not git/ship or full membrane audits — those are **B**): `docs/skill-work/work-dev/` + [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md); **skills / meta** when **`skills`** / **`meta`** with **A**. **One** prescribed next action. Detail: [menu-reference § Build — detailed scope](../../../docs/skill-work/work-coffee/menu-reference.md#build-b--detailed-scope) (legacy letter **B** in that doc = current **A**).

- **B. Steward** — **Governance membrane:** **gate** \| **template/boundary** \| **integrity/exports** \| **git/ship**. **Default if the operator says `B` only:** **gate** if pending candidates; else **template/boundary**. **`B integrity`** / **`B git`** / **`B ship`** → that track; **`B both`** / **`B all`** as in [menu-reference — Steward](../../../docs/skill-work/work-coffee/menu-reference.md#ah-table). Gate merges never without companion **approve** + `process_approved_candidates.py`.

- **C. Strategy (daily brief)** — **Two-stage flow (default; do not collapse to intel-only):** **(1)** Daily brief path — generator and/or `daily-brief-YYYY-MM-DD.md`, **§1d** / **§1e** / **§1g** / **§1h** (PRC / IRI when load-bearing), optional **KY-4** (Polymarket, polls, Massie X per cadence). **(2)** In the **same turn**, offer **Tri-Frame** minds **Barnes → Mearsheimer → Mercouris**, wait for **which mind**, then [daily-brief-minds-menu.md](../../../docs/skill-work/work-strategy/daily-brief-minds-menu.md). **Do not** end **C** on polls alone unless **`intel only`** / **`no tri-frame`** / survey-only. **Companion survey** when **`coffee survey`**. See [menu-reference — Tri-Frame](../../../docs/skill-work/work-coffee/menu-reference.md#tri-frame-daily-brief).

- **D1. Conductor — Toscanini** — **Strategy coffee cadence** (strategy-notebook) per [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../../../docs/skill-work/work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md): truth-to-form, seam enforcement, anti-indulgence, and disciplined score architecture.

- **D2. Conductor — Furtwängler** — Organic emergence, tension without forced closure, and listening for the line before the verdict.

- **D3. Conductor — Bernstein** — Communicative heat, pulse, and vivid operator-facing stakes without losing the score.

- **D4. Conductor — Karajan** — Long arc, integrated balance, economy, and the total effect of the whole.

- **D5. Conductor — Kleiber** — Ruthless narrowing, chosen hotspots, and disproportionate depth on what truly matters.

Each **D1–D5** choice gets a **short** orienting reply plus concrete next actions. **Not** a merge, **not** the full 15–45m embodied ritual in chat unless the operator extends. **Optional** after the turn: `log_cadence_event.py` **`coffee_pick`** with `--kv picked=D4 conductor=karajan` (or whichever explicit conductor was chosen). **Not** work-dev implementation (**A**), not daily-brief + Tri-Frame alone (**C**; use **C** for brief). **Not** `self-skill-write` (use **E** for write slice).

- **E. (system choice)** — As filled on the menu line; typically one of: **skill-write** / PRP, Cici next, Dev next (workspace), Compass/Rome, Jiang/PH — **one** step.

**Exit / re-offer:** After **A**, **B**, or **E**, re-offer the full menu by default. After **C** or **any of D1–D5**, **exit to normal workflow** unless **`stay in coffee`**. After **B** (Steward), see [menu-reference § Steward follow-up fork](../../../docs/skill-work/work-coffee/menu-reference.md#steward-follow-up-fork-implement-now-vs-later) (replace legacy **E** with **B** when reading that section). Synonyms **`B+ship`** / **`EXECUTE`** ≈ **Implement now** on steward track.

Legacy **A–G** detail tables in [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md) still describe **workloads**; map letters: old **Daily Brief → C**, **Build → A**, **Steward → B**, **Compass/Book/F/G** → usually **E** (system choice) unless you fold Rome/Jiang into **C**; old **write-shaped** work → **E**; **D** in the legacy table was **not** the same as current **D1–D5 — Conductor** (see menu-reference).

**Done when:** The operator has picked a letter (or combo), the selected branch has been executed, and the re-offer or exit rule has been applied.

---

## Session trail (optional)

Sessions begin when the operator says **`coffee`** (optional modifiers). To keep a trail: use **`users/<id>/session-transcript.md`** and/or append dated bullets to **`docs/skill-work/work-*/*-history.md`**. **Not** the gated Record; **not** `self-memory`. See [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).

## Cadence audit

Each successful coffee run appends one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. This is automatic — no operator action required. The line always includes **`cursor_model=…`** (audit parity with bridge/harvest **Agent surface**): set **`CURSOR_MODEL`** in the environment, or pass **`--cursor-model "…"`** to `operator_coffee.py`, using the model name from the Cursor UI. If unset, **`unknown`**.

**After the operator states their menu letter** (and steward track if **B**), the assistant may append a **`coffee_pick`** cadence line (same file) for rollup:  
`python3 scripts/log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=B steward=gate --cursor-model "<from Cursor UI>"`  
(`steward=` only when `picked=B`; values: `gate`, `template`, `integrity`, `git`, `both`, or `all`.) For **Conductor**, `coffee_pick` uses **`picked=D1`**, **`D2`**, **`D3`**, **`D4`**, or **`D5`** with **`conductor=<single-slug>`** (e.g. `karajan`, `toscanini`) — **no** `+` in new logs. Optional: `scripts/log_operator_choice.py --context COFFEE --picked B` for `session-transcript.md`.

## Related files

- `docs/skill-work/work-cadence/README.md` — **Cadence choreography** (ordering, handoffs, Step 0 recent rhythm window depths, harvest vs triad)
- `docs/skill-work/work-coffee/README.md` — territory rationale and boundaries
- `docs/skill-work/work-coffee/menu-reference.md` — cadence, survey track, signing-off add-ons; legacy **A–G** workload tables (map to the current coffee Step 2 above)
- `docs/skill-work/work-coffee/work-coffee-history.md` — lane breadcrumbs
- `docs/skill-work/work-cadence/work-cadence-events.md` — per-run cadence telemetry
- `.cursor/skills/dream/SKILL.md` — night-side counterpart
- `.cursor/skills/thanks/SKILL.md` — micro-pause cadence (`thanks`; not a substitute for coffee / dream / bridge)
- `docs/skill-work/work-politics/polling-and-markets.md` — KY-4 polling (**menu C — Strategy (daily brief)**)
- `docs/skill-work/work-strategy/daily-brief-minds-menu.md` — Tri-Frame **three minds** (Barnes / Mearsheimer / Mercouris) for **C — Strategy (daily brief)** second stage
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md` — messaging discipline
