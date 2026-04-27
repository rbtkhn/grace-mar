---
name: coffee
preferred_activation: coffee
requires: [handoff-check]
description: "Grace-Mar operator cadence and tempo. Primary trigger: coffee. Step 2 = hub A–E + Conductor MCQ (masters A–E) + after a master is picked, Conductor action MCQ (third A–E, repo-grounded). Conductor may run without full coffee. Before Step 1, Recent rhythm. Signing-off: same menu; closeout in Step 1."
---

# Coffee

**Preferred activation (operator):** say **`coffee`**. Legacy **`hey`** still works as a compatibility alias, but **`coffee`** is the canonical trigger now.

**Signing-off intent** (end of session, wrapping the day, stepping away) uses the **same** **`coffee`** trigger and the **same** **A, B, C, D, E** menu. There is **no** separate closeout branch or closeout-only menu item. **Step 1** switches to handoff-weighted output when intent is signing off; **Step 2** is unchanged.

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

<a id="conductor-only-no-coffee"></a>

## Conductor only (no `coffee` session)

The operator may invoke **D — Conductor** **without** opening **`coffee`**. This is a **valid shortcut**; it is **not** a second menu or a different protocol.

**When to use this path:** the operator clearly wants the strategy-notebook **Conductor** beat only — e.g. bare **`D`**, **`D`** + name fragment (`D tos`, `D bern`, `D kleib`), or plain language with the same intent (**"Toscanini pass"**, **"run Karajan for the notebook"**, **"conductor: kleiber"**). If intent is unclear, ask once.

**Do not** run `operator_coffee.py`, **do not** paste work-start or closeout **Step 1** output, and **do not** lead with **Recent rhythm** (no synthetic Step 0) — unless the same message also says **`coffee`** or **`hey`**.

**Do** show the **Conductor MCQ** (`build_conductor_mcq_for_user('grace-mar')` or `format_conductor_mcq_block`) when the pick is not yet disambiguated; **do** resolve the slug the **same** way as [Step 2 — D](#coffee-step-2-d) (this file): `resolve_d_conductor` + [work-cadence-events.md](../../../docs/skill-work/work-cadence/work-cadence-events.md) for continuation. On success deliver the same **short** orientation as [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-d-menu) and [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../../../docs/skill-work/work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md). **Then, always** deliver the **Conductor action MCQ** — **five** **A.–E.** **specific** next actions, **master-shaped** (not a repeat of the five-masters list) — per [CONDUCTOR-PASS — Conductor action MCQ](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-action-mcq) and [conductor skill](../conductor/SKILL.md). **Skip** the action menu **only** if the operator said **"orientation only"** / **"no action menu"** in the same turn. **Append** a **`coffee_pick`** line: `log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=D conductor=<slug>`. **Do not** append a separate **`coffee`** event unless they actually ran `coffee` Step 1.

**Conductor close (optimal loop):** Prompt the operator to **anchor the pass in disk** — at least one of: (a) add a **Conductor close** block per [CONDUCTOR-CLOSE-TEMPLATE.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md) in **`chapters/YYYY-MM/days.md`** (or a relevant **`strategy-page` · Reflection**), or (b) run `log_cadence_event.py` **`--kind coffee_conductor_outcome`** with `verdict=` (and optional `notebook_ref=` / `falsify=`). **SSOT:** [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md). **Not** required for a five-second reorientation, but **required** to claim a **closed** improvement loop in the same session.

**After the reply:** return to **normal workflow** (same as after **D** during a full `coffee` session) unless the operator says **`stay in coffee`** or **`coffee`**.

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

**Dream handoff:** If `dream` ran overnight, the daily warmup includes a last-dream block from `users/grace-mar/last-dream.json` (**"Last dream (night handoff)"** when there is something to read out, or a **one-line "quiet handoff"** when `integrity` / `governance` / digest counts are clean and there are no followups). A successful dream may add **`last_coffee_echo`**: a single warm line (from the 24h cadence rollup) that ties yesterday’s `coffee` into morning startup—**cadence / runtime only**, not Record. **Signal days** (issues, followups, or non-zero digests) still use the fuller collapsed block. Extra lines (civ-mem summary, coffee 24h rollup) are **off** by default; tune `config/context_budgets/coffee.json` or pass `--show-civ-mem` / `--show-rollup` on `operator_daily_warmup.py`, `operator_coffee.py`, or `operator_reentry_stack.py`. After that block (or alone if the Last dream section is turned off), warmup prints one line **`Dream → coffee menu:`** mapping dream’s suggested execution path to **A / B / C** (Build / Steward / Strategy · daily brief) — operational hint only; see [dream/SKILL.md](../dream/SKILL.md) § *Five-second closeout*. Approximate paste footprint: `python3 scripts/audit_context_tax.py -u grace-mar`. These files are operator scaffolding, not Record. For full paths / snippets / followups, use **`--verbose-dream`**. When pasting warmup for the operator, prefer **collapsed** unless they ask for detail.

**Step 1 deliverables (work-start):** Warmup brief (priorities, gate, work-politics snapshot where relevant, integrity), branch snapshot, daily brief + intel defer line (path pattern + **menu C — Strategy (daily brief)** when ready), optional PH/Jiang line. **No** Polymarket / poll / Massie blocks in Step 1 unless the operator explicitly asked in the same message.

**Step 1 guardrail:** Stay read-only — no merge/stage unless they switch lanes or use a pipeline phrase ("we …").

**Done when:** Script output is pasted in the reply, Recent rhythm is at the top, and the full coffee menu follows immediately.

For cadence tables and explicit phrase definitions (`coffee light`, `coffee minimal`, `coffee survey`): see [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md).

### Multiple coffees per day

The operator may say **`coffee`** **more than once per calendar day** for reorientation. This is normal. Each new `coffee` runs Step 1 again and starts a new **A, B, C, D, E** cycle. If **`coffee`** arrives mid-hub, treat it as a **reorientation restart**: run Step 1 again, then offer a fresh menu.

<a id="coffee-step-2-d"></a>

### Step 2 — Hub menu (five lines) + **Conductor MCQ** (five options)

Immediately **after** Step 1 content, output (1) the **hub** menu — **five lines** (**A, B, C, D, E**), then (2) a **blank line**, then (3) the **Conductor MCQ** block — **five** lettered options **A.–E.** that name the **five masters** (strategy-notebook) with a **one-line** attribute and a **continuity** kicker per card (last `coffee_pick`, optional `focus` / `arc`, and dream / session-load advisory). **Do not** add micro-hints, fork shorthand, or F/G/Xavier/Dev tags **under the hub list**; the Conductor MCQ is **not** micro-hints — it is the **selectable** conductor interface.

**How to build the Conductor MCQ (required text):** run in-repo (or reimplement with the same data):

`python3 -c "from scripts.cadence_conductor_resolution import build_conductor_mcq_for_user; print(build_conductor_mcq_for_user('grace-mar'))"`

That prints the five options with up-to-date continuity. Alternatively call `format_conductor_mcq_block(...)` with explicit `last_slug` / `focus_text` / `recommended_slug` from `parse_events` + `assess_load` + optional `last-dream.json` — see [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-mcq).

**Letter collision (important):** the **first** **A.–E.** row is the **hub** (Build, Steward, Strategy, Conductor, system choice). The **Conductor** row’s **A.–E.** re-use the same letters for **Toscanini, Furtwängler, Karajan, Kleiber, Bernstein** in **fixed** order. In chat, a **second** turn letter after choosing hub **D** (or a **conductor-only** message) means a **master**; **B** in the Conductor block = **Furtwängler** (not hub Steward). Single-character **`A`–`E` outside the hub** in a conductor turn resolves via `conductor_submenu_letter_to_slug` / `resolve_d_conductor` in `scripts/cadence_conductor_resolution.py`.

**D — Conductor (hub line):** Hub **D** is the “open strategy-notebook **Conductor** lane” (see Conductor MCQ for the **five** cards). The operator may also run **D** with the **same** rules **without** a prior **coffee** this turn — see [§ *Conductor only*](#conductor-only-no-coffee) above. On pick:

- **Conductor MCQ** letters **A** = Toscanini · **B** = Furtwängler · **C** = Karajan · **D** = Kleiber · **E** = Bernstein.
- **Bare `D`** in the *hub* (or on a **conductor-only** line) with **no** second token **continues the same conductor as last time** — `last_logged_conductor` / `resolve_d_conductor("", last_conductor_slug=…)` from [work-cadence-events.md](../../../docs/skill-work/work-cadence/work-cadence-events.md) and/or `last_coffee_echo` in `last-dream.json`. If there is **no** prior conductor, say so in **one** line and show the Conductor MCQ.
- **Name fragment** (after hub **D** or in **conductor-only** mode) picks a master: `D bern`, `D klei`, `tos`, `kleib`, … — `resolve_d_conductor`. If a single character is **A**–**E**, it is the **Conductor MCQ** row (e.g. **`B`** → Furtwängler), **not** hub Steward.
- **Logging:** `coffee_pick` uses **`picked=D`** with **`conductor=<single-slug>`** — no `+` in new logs. Legacy `picked=D1`..`D5` in the file remain readable.
- **Conductor close (same as [§ *Conductor only*](#conductor-only-no-coffee)):** Offer or apply the [CONDUCTOR-CLOSE-TEMPLATE.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md) in **`days.md` / a page, or `coffee_conductor_outcome` — see [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md). **Conductor action MCQ** (required after master pick unless **orientation only**): [CONDUCTOR-PASS — Conductor action MCQ](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-action-mcq) · [conductor skill](../conductor/SKILL.md).

**Hub menu (example):**

```
A. Build
B. Steward
C. Strategy (daily brief)
D. Conductor — (pick a master: use the Conductor MCQ **A.–E.** block below, a fragment, or bare **D** to continue last)
E. (system choice) — <one short line: the single best alternate lane this session>
```

Then paste the full output of `build_conductor_mcq_for_user('grace-mar')` (or equivalent).

**Filling E — (system choice):** Pick **one** concrete slice for this turn, using Step 1 context — e.g. **self-skill-write** (prompts, PRP, Lexile, bot/prompt **proposals** — not merge), **work-cici** next (ground in `coffee_lane_next_hints` / SYNC-DAILY / INDEX), **work-dev** next from [workspace.md](../../../docs/skill-work/work-dev/workspace.md) § **Next actions**, **work-strategy-rome** / ROME-PASS (Compass-style), **work-jiang / PH** (Book-style), or match **`Dream → coffee menu`** when it points at a path not already covered by **A–C / D**.

**Fixed E option (always available):** **Self-knowledge quiz (bookshelf membrane)**.

- Session is **multi-round**: 5–10 MCQs per round about bookshelf subject matter.
- After each round, ask continue/stop.
- On stop, produce:
  - `docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF-MEMBRANE-REPORT.md`
  - `docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF-MEMBRANE-CANDIDATE-DRAFTS.md`
- Output is draft-only; no direct writes to `users/grace-mar/recursion-gate.md` unless explicitly requested.

**Write-shaped** work is **not** a tenth letter — it defaults here or when the operator says **`write`** / **`skill-write`** without **`coffee`**. State it plainly in the angle-bracket line; **do not** add a separate “micro-hints” row.

**Step 1 context for E:** `operator_coffee.py` prints **`Lane context (for menu E)`** — two lines from `scripts/coffee_lane_next_hints.py` (work-cici + work-dev). Use when choosing **E** or when wording the **E** line.

**Optional load note:** Step 1 may print `Session load: … (recommended: X)` (**A** / **B** / **C**). You may mention that **one** recommended hub letter and/or **one** recommended conductor in prose before or after the menu — the **Conductor MCQ** already bakes in advisory; do **not** add a *third* duplicate block. **Not** micro-hints under the hub list.

**Quick reference (modes):**

- **A. Build** — **work-dev + skills/meta** (not git/ship or full membrane audits — those are **B**): `docs/skill-work/work-dev/` + [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md); **skills / meta** when **`skills`** / **`meta`** with **A**. **One** prescribed next action. Detail: [menu-reference § Build — detailed scope](../../../docs/skill-work/work-coffee/menu-reference.md#build-b--detailed-scope) (legacy letter **B** in that doc = current **A**).

- **B. Steward** — **Governance membrane:** **gate** \| **template/boundary** \| **integrity/exports** \| **git/ship**. **Default if the operator says `B` only:** **gate** if pending candidates; else **template/boundary**. **`B integrity`** / **`B git`** / **`B ship`** → that track; **`B both`** / **`B all`** as in [menu-reference — Steward](../../../docs/skill-work/work-coffee/menu-reference.md#ah-table). Gate merges never without companion **approve** + `process_approved_candidates.py`.

- **C. Strategy (daily brief)** — **Two-stage flow (default; do not collapse to intel-only):** **(1)** Daily brief path — generator and/or `daily-brief-YYYY-MM-DD.md`, **§1d** / **§1e** / **§1g** / **§1h** (PRC / IRI when load-bearing), optional **KY-4** (Polymarket, polls, Massie X per cadence). **(2)** In the **same turn**, offer **Tri-Frame** minds **Barnes → Mearsheimer → Mercouris**, wait for **which mind**, then [daily-brief-minds-menu.md](../../../docs/skill-work/work-strategy/daily-brief-minds-menu.md). **Do not** end **C** on polls alone unless **`intel only`** / **`no tri-frame`** / survey-only. **Companion survey** when **`coffee survey`**. See [menu-reference — Tri-Frame](../../../docs/skill-work/work-coffee/menu-reference.md#tri-frame-daily-brief).

- **D. Conductor** — **Strategy coffee cadence** (strategy-notebook) per [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../../../docs/skill-work/work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) and [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md): the **Conductor MCQ** lists five selectable **A.–E.** rows (one per master) with **continuity** kickers. The reply names **which** conductor is active (Conductor **A.–E.**, name fragment, or bare **D** / `resolve_d_conductor`). **On master resolution,** also output **Conductor action MCQ** (second **A.–E.** for **this** pass) — [CONDUCTOR-PASS#conductor-action-mcq](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-action-mcq). **Not** a merge, **not** the full 15–45m embodied ritual in chat unless the operator extends. After the turn: `log_cadence_event.py` **`coffee_pick`** with `--kv picked=D conductor=<slug>`. **Not** work-dev implementation (hub **A**), not daily-brief + Tri-Frame alone (hub **C**). **Not** `self-skill-write` (use hub **E** for write slice).

- **E. (system choice)** — As filled on the menu line; typically one of: **self-knowledge quiz (bookshelf membrane)**, **skill-write** / PRP, Cici next, Dev next (workspace), Compass/Rome, Jiang/PH — **one** step.

**Exit / re-offer:** After **A**, **B**, or **E**, re-offer the full menu by default. After **C** or **D**, **exit to normal workflow** unless **`stay in coffee`**. After **B** (Steward), see [menu-reference § Steward follow-up fork](../../../docs/skill-work/work-coffee/menu-reference.md#steward-follow-up-fork-implement-now-vs-later) (replace legacy **E** with **B** when reading that section). Synonyms **`B+ship`** / **`EXECUTE`** ≈ **Implement now** on steward track.

Legacy **A–G** detail tables in [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md) still describe **workloads**; map letters: old **Daily Brief → C**, **Build → A**, **Steward → B**, **Compass/Book/F/G** → usually **E** (system choice) unless you fold Rome/Jiang into **C**; old **write-shaped** work → **E**; the legacy table’s old **D Book (Jiang)** is **not** the same as current **D — Conductor** (see menu-reference).

**Done when:** The operator has picked a letter (or combo), the selected branch has been executed, and the re-offer or exit rule has been applied.

---

## Session trail (optional)

Sessions begin when the operator says **`coffee`** (optional modifiers). To keep a trail: use **`users/<id>/session-transcript.md`** and/or append dated bullets to **`docs/skill-work/work-*/*-history.md`**. **Not** the gated Record; **not** `self-memory`. See [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).

## Cadence audit

Each successful coffee run appends one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. This is automatic — no operator action required. The line always includes **`cursor_model=…`** (audit parity with bridge/harvest **Agent surface**): set **`CURSOR_MODEL`** in the environment, or pass **`--cursor-model "…"`** to `operator_coffee.py`, using the model name from the Cursor UI. If unset, **`unknown`**.

**After the operator states their menu letter** (and steward track if **B**), the assistant may append a **`coffee_pick`** cadence line (same file) for rollup:  
`python3 scripts/log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=B steward=gate --cursor-model "<from Cursor UI>"`  
(`steward=` only when `picked=B`; values: `gate`, `template`, `integrity`, `git`, `both`, or `all`.) For **Conductor**, `coffee_pick` uses **`picked=D`** with **`conductor=<single-slug>`** (e.g. `karajan`, `toscanini`) — **no** `+` in new logs. Legacy files may still contain `picked=D1`..`D5`. **Optional closure after a conductor run:** `python3 scripts/log_cadence_event.py --kind coffee_conductor_outcome -u grace-mar --ok --kv verdict=watch` (see [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md) § 3 for `notebook_ref` / `falsify` examples). Optional: `scripts/log_operator_choice.py --context COFFEE --picked B` for `session-transcript.md`.

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
