---
name: coffee
preferred_activation: coffee
requires: [handoff-check]
description: "Grace-Mar operator cadence and tempo. Primary trigger: coffee. Coffee is a repeatable sip of coherence: a lightweight reorientation ritual that restores clarity, framing, and agency. Multiple coffee sessions per day are normal. Before Step 1 scripts run, synthesize the previous four events from work-cadence-events.md into plain-language **Recent rhythm** (no internal ops jargon or timestamps in chat). Work-start coffee runs the read-only grounding stack, then the fixed A–G menu (seven modes: A–E core + **F** work-xavier next + **G** work-dev next). Compass (C) includes work-strategy-rome (ROME-PASS). Signing-off intent uses the same menu; closeout is merged into Step 1. Exit the hub by picking **Later** after a steward fork, choosing **C** or **D** (exit to normal workflow unless stay in coffee), or starting a non-coffee task without expecting the ritual menu."
---

# Coffee

**Preferred activation (operator):** say **`coffee`**. Legacy **`hey`** still works as a compatibility alias, but **`coffee`** is the canonical trigger now.

**Signing-off intent** (end of session, wrapping the day, stepping away) uses the **same** **`coffee`** trigger and the **same** **A–G** menu. There is **no** separate closeout branch or closeout-only menu item. **Step 1** switches to handoff-weighted output when intent is signing off; **Step 2** is unchanged.

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

**Dream handoff:** If `dream` ran overnight, the daily warmup automatically includes a **"Last dream (night handoff)"** block from `users/grace-mar/last-dream.json`. **Default:** that block is **collapsed** (status, digest counts, tomorrow hint). Extra lines (civ-mem summary, coffee 24h rollup) are **off** by default; tune `config/context_budgets/coffee.json` or pass `--show-civ-mem` / `--show-rollup` on `operator_daily_warmup.py`, `operator_coffee.py`, or `operator_reentry_stack.py`. Approximate paste footprint: `python3 scripts/audit_context_tax.py -u grace-mar`. These files are operator scaffolding, not Record. For full paths / snippets / followups, use **`--verbose-dream`**. When pasting warmup for the operator, prefer **collapsed** unless they ask for detail.

**Step 1 deliverables (work-start):** Warmup brief (priorities, gate, work-politics, integrity), branch snapshot, daily brief + intel defer line (path pattern + **menu A — Today** when ready), optional PH/Jiang line. **No** Polymarket / poll / Massie blocks in Step 1 unless the operator explicitly asked in the same message.

**Step 1 guardrail:** Stay read-only — no merge/stage unless they switch lanes or use a pipeline phrase ("we …").

**Done when:** Script output is pasted in the reply, Recent rhythm is at the top, and the A–G menu follows immediately.

For cadence tables and explicit phrase definitions (`coffee light`, `coffee minimal`, `coffee survey`): see [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md).

### Multiple coffees per day

The operator may say **`coffee`** **more than once per calendar day** for reorientation. This is normal. Each new `coffee` runs Step 1 again and starts a new **A–G** cycle. If **`coffee`** arrives mid-hub, treat it as a **reorientation restart**: run Step 1 again, then offer a fresh **A–G** menu.

### Step 2 — Multiple choice (required; always A–G, load-annotated)

Immediately **after** Step 1 content, output the fixed **coffee** menu: **seven** lettered options **A through G** (present **A, B, C, D, E, F, G**). **There is no separate “close” letter** — exit paths are **C** / **D** (normal workflow unless **`stay in coffee`**), or a **steward fork** (**Later**) that returns to this full menu.

**Step 1 lane hints:** After session load, `operator_coffee.py` prints **`lane next hints (F / G)`** — two lines from `scripts/coffee_lane_next_hints.py` (work-xavier + work-dev). Ground **F** and **G** in those lines plus the linked docs below; refresh hints on the next `coffee` if stale.

**Load annotation:** `operator_coffee.py` prints a session load one-liner at the end of Step 1 (e.g. `Session load: MODERATE — 3 coffees today, 5 pending candidates`). Use `scripts/assess_session_load.py` output (or the one-liner already printed) to **annotate each A–G option** with its cost tag — `(light)`, `(moderate)`, or `(heavy)` — and mark the recommended option (**A–E** only for “recommended”; **F**/**G** are always available but not auto-recommended). The letters stay fixed; the tags are advisory. Example:

```
A. Today — (light) recommended: quick reorientation matches current pace
B. Build — (moderate) dev + hygiene; 2 non-main branches
C. Compass — (heavy) sustained strategy; consider after break
D. Book — (moderate) Jiang/PH; 1 pending step
E. Steward — (light) 3 pending candidates; bounded gate pass
F. Xavier next — (moderate) work-xavier; one next task from SYNC-DAILY / WORK-LEDGER / INDEX
G. Dev next — (moderate) work-dev; first open line in workspace.md § Next actions
```

If the session load script is unavailable or errored, present the menu without annotations (unchanged behavior).

**Micro-hints (one line under the A–G list):** `Micro-hints: B+skills/meta | F=xavier next | G=dev next (workspace) | E=gate | template | integrity | E both | after actionable E: Implement now / Later`

**Quick reference (modes):**

- **A. Today** — Daily brief (generator + §1d Putin only when chosen) + work-politics intel (KY-4 Polymarket, polls, Massie X per cadence), brief registry / campaign / queue — **one** next step. **Companion survey** defaults here when the operator opened with **`coffee survey`**.
- **B. Build** — **Ship-lane mechanics + work-dev execution** ( **not** integrity/template audits — those are **E** ): [git-branch-hygiene.md](../../../docs/skill-work/work-dev/git-branch-hygiene.md), `git status`, commit/push plan; `docs/skill-work/work-dev/` + [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md); **skills / meta** pipeline ([skills-portable/skill-candidates.md](../../../skills-portable/skill-candidates.md), extract-skill, portable-skills-sync) when **`skills`** / **`meta`** with **B**. **One** prescribed next action. Detail: [menu-reference § Build (B) — detailed scope](../../../docs/skill-work/work-coffee/menu-reference.md#build-b--detailed-scope).
- **C. Compass** — **work-strategy** + **work-strategy-rome** (ROME-PASS, manifest, exemplars, notes) — **one** develop step. Vatican / Holy See / ROME-PASS work lives **here**, not under **Today** alone.
- **D. Book** — **work-jiang / Predictive History** — **one** next step.
- **E. Steward** — **Governance membrane:** **gate** \| **template/boundary** \| **integrity/exports**. **Default if the operator says `E` only:** **gate** when there is at least one pending gate candidate; otherwise **template/boundary** — **integrity/exports is not** in the default rotation. **`E integrity`** / **`E exports`** → integrity/exports only; **`E both`** → gate + template/boundary; **`E all`** → all three (explicit only). **First line:** name the track(s). **Integrity/exports:** `validate-integrity.py` (report); `refresh_derived_exports.py` **writes** — ship via **Implement now**, never silent. Template/boundary: **Reconciliation code** per [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md). **Gate merges** never run from steward alone — companion **approve** + `process_approved_candidates.py` only.
- **F. Xavier next** — **work-xavier** — **one** next task: use Step 1 **lane next hints** line + [INDEX.md](../../../docs/skill-work/work-xavier/INDEX.md), [SYNC-DAILY.md](../../../docs/skill-work/work-xavier/SYNC-DAILY.md), [WORK-LEDGER.md](../../../docs/skill-work/work-xavier/WORK-LEDGER.md), [DAILY-OPS-CARD.md](../../../docs/skill-work/work-xavier/DAILY-OPS-CARD.md); mirrors / BrewMind / runbooks only as needed for that single step — **not** a full territory sweep unless the operator asks.
- **G. Dev next** — **work-dev next task only** — **one** concrete step from the first **open** numbered item in [workspace.md](../../../docs/skill-work/work-dev/workspace.md) § **Next actions** (operator-maintained). **Narrower than B:** no default full hygiene/skills pass unless the operator folds it in.

**Re-offer rules:** After **A**, **B**, **F**, or **G**, re-offer the full **A–G** menu by default. After **C** or **D**, **exit to normal workflow** unless the operator says **`stay in coffee`**. After **E**, see [menu-reference.md § Steward follow-up fork](../../../docs/skill-work/work-coffee/menu-reference.md#steward-follow-up-fork-implement-now-vs-later): if the steward pass **surfaces actionable possibilities** (defined there), **do not** re-offer the full menu — offer **only** **1. Implement now** and **2. Later** (**Later** → then present full **A–G**). If **nothing actionable** surfaced, re-offer full **A–G** as after **A**/**B**/**F**/**G**. Synonyms: **`E+ship`** / **`E implement`** / **`EXECUTE`** + slice ≈ **Implement now** when the operator uses them instead of the numbered pick.

For full **A–G** definitions, signing-off add-ons per letter, and the companion survey track: see [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md).

**Done when:** The operator has picked a letter (or combo), the selected branch has been executed, and the re-offer or exit rule has been applied.

---

## Session trail (optional)

Sessions begin when the operator says **`coffee`** (optional modifiers). To keep a trail: use **`users/<id>/session-transcript.md`** and/or append dated bullets to **`docs/skill-work/work-*/*-history.md`**. **Not** the gated Record; **not** `self-memory`. See [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).

## Cadence audit

Each successful coffee run appends one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. This is automatic — no operator action required. The line always includes **`cursor_model=…`** (audit parity with bridge/harvest **Agent surface**): set **`CURSOR_MODEL`** in the environment, or pass **`--cursor-model "…"`** to `operator_coffee.py`, using the model name from the Cursor UI. If unset, **`unknown`**.

**After the operator states their menu letter** (and steward track if **E**), the assistant may append a **`coffee_pick`** cadence line (same file) for rollup:  
`python3 scripts/log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=E steward=gate --cursor-model "<from Cursor UI>"`  
(`steward=` only when `picked=E`; values: `gate`, `template`, `integrity`, `both`, or `all`.) Optional: `scripts/log_operator_choice.py --context COFFEE --picked E` for `session-transcript.md`.

## Related files

- `docs/skill-work/work-cadence/README.md` — **Cadence choreography** (ordering, handoffs, Step 0 recent rhythm window depths, harvest vs triad)
- `docs/skill-work/work-coffee/README.md` — territory rationale and boundaries
- `docs/skill-work/work-coffee/menu-reference.md` — full A–G definitions, cadence, survey track, signing-off add-ons
- `docs/skill-work/work-coffee/work-coffee-history.md` — lane breadcrumbs
- `docs/skill-work/work-cadence/work-cadence-events.md` — per-run cadence telemetry
- `.cursor/skills/dream/SKILL.md` — night-side counterpart
- `.cursor/skills/thanks/SKILL.md` — micro-pause cadence (`thanks`; not a substitute for coffee / dream / bridge)
- `docs/skill-work/work-politics/polling-and-markets.md` — KY-4 polling (**menu A — Today**)
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md` — messaging discipline
