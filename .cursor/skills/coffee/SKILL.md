---
name: coffee
preferred_activation: coffee
description: "Grace-Mar operator cadence and tempo. Primary trigger: coffee. Coffee is a repeatable sip of coherence: a lightweight reorientation ritual that restores clarity, framing, and agency. Multiple coffee sessions per day are normal. Work-start coffee runs the read-only grounding stack, then the fixed A–E menu (five modes). Compass (C) includes work-strategy-rome (ROME-PASS). Signing-off intent uses the same menu; closeout is merged into Step 1. Exit the hub by picking **Later** after a steward fork, choosing **C** or **D** (exit to normal workflow unless stay in coffee), or starting a non-coffee task without expecting the ritual menu."
---

# Coffee

**Preferred activation (operator):** say **`coffee`**. Legacy **`hey`** still works as a compatibility alias, but **`coffee`** is the canonical trigger now.

**Signing-off intent** (end of session, wrapping the day, stepping away) uses the **same** **`coffee`** trigger and the **same** **A–E** menu. There is **no** separate closeout branch or closeout-only menu item. **Step 1** switches to handoff-weighted output when intent is signing off; **Step 2** is unchanged.

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

For cadence tables and explicit phrase definitions (`coffee light`, `coffee minimal`, `coffee survey`): see [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md).

### Multiple coffees per day

The operator may say **`coffee`** **more than once per calendar day** for reorientation. This is normal. Each new `coffee` runs Step 1 again and starts a new **A–E** cycle. If **`coffee`** arrives mid-hub, treat it as a **reorientation restart**: run Step 1 again, then offer a fresh **A–E** menu.

### Step 2 — Multiple choice (required; always A–E)

Immediately **after** Step 1 content, output the fixed **coffee** menu: **five** lettered options **A through E** (present **A, B, C, D, E**). **There is no separate “close” letter** — exit paths are **C** / **D** (normal workflow unless **`stay in coffee`**), or a **steward fork** (**Later**) that returns to this full menu.

**Micro-hints (one line under the A–E list):** `Micro-hints: B+skills/meta | E=gate/template/boundary | after actionable E: Implement now / Later`

**Quick reference (modes):**

- **A. Today** — Daily brief (generator + §1d Putin only when chosen) + work-politics intel (KY-4 Polymarket, polls, Massie X per cadence), brief registry / campaign / queue — **one** next step. **Companion survey** defaults here when the operator opened with **`coffee survey`**.
- **B. Build** — **work-dev** + **repository hygiene**: `docs/skill-work/work-dev/`, [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md), [git-branch-hygiene.md](../../../docs/skill-work/work-dev/git-branch-hygiene.md), branch snapshot, `git status`, exports/integrity pointers — **one** prescribed next action. **Skills / meta pipeline** ([skills-portable/skill-candidates.md](../../../skills-portable/skill-candidates.md), extract-skill, portable-skills-sync): say **`skills`** or **`meta`** in the same turn as **B**, or ask for skills depth after **Build** — not a sixth menu letter.
- **C. Compass** — **work-strategy** + **work-strategy-rome** (ROME-PASS, manifest, exemplars, notes) — **one** develop step. Vatican / Holy See / ROME-PASS work lives **here**, not under **Today** alone.
- **D. Book** — **work-jiang / Predictive History** — **one** next step.
- **E. Steward** — **RECURSION-GATE** + **template / boundary audit** (companion-self parity, fork isolation, optional `validate-integrity.py`). **Mandatory single-track default:** if the operator says **E** only (no sub-track), run **exactly one** track this turn: **gate** when there is at least one pending gate candidate; otherwise **template/boundary**. **`both`** (gate and template/boundary in one turn) is allowed **only** when the operator explicitly asks for both. **First line of the reply:** name the track you are executing (**gate** or **template/boundary**). When the turn includes **template/boundary / companion-self parity**, end with the **Reconciliation code** block per [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md). **Default = audit only** (read-only) until the operator chooses **Implement now**. **Gate merges** never run from steward alone — companion **approve** + `process_approved_candidates.py` only.

**Re-offer rules:** After **A** or **B**, re-offer the full **A–E** menu by default. After **C** or **D**, **exit to normal workflow** unless the operator says **`stay in coffee`**. After **E**, see [menu-reference.md § Steward follow-up fork](../../../docs/skill-work/work-coffee/menu-reference.md#steward-follow-up-fork-implement-now-vs-later): if the steward pass **surfaces actionable possibilities** (defined there), **do not** re-offer the full menu — offer **only** **1. Implement now** and **2. Later** (**Later** → then present full **A–E**). If **nothing actionable** surfaced, re-offer full **A–E** as after **A**/**B**. Synonyms: **`E+ship`** / **`E implement`** / **`EXECUTE`** + slice ≈ **Implement now** when the operator uses them instead of the numbered pick.

For full **A–E** definitions, signing-off add-ons per letter, and the companion survey track: see [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md).

---

## Session trail (optional)

Sessions begin when the operator says **`coffee`** (optional modifiers). To keep a trail: use **`users/<id>/session-transcript.md`** and/or append dated bullets to **`docs/skill-work/work-*/*-history.md`**. **Not** the gated Record; **not** `self-memory`. See [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).

## Cadence audit

Each successful coffee run appends one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. This is automatic — no operator action required.

**After the operator states their menu letter** (and steward track if **E**), the assistant may append a **`coffee_pick`** cadence line (same file) for rollup:  
`python3 scripts/log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=E steward=gate`  
(`steward=` only when `picked=E`; values: `gate`, `template`, or `both`.) Optional: `scripts/log_operator_choice.py --context COFFEE --picked E` for `session-transcript.md`.

## Related files

- `docs/skill-work/work-coffee/README.md` — territory rationale and boundaries
- `docs/skill-work/work-coffee/menu-reference.md` — full A–E definitions, cadence, survey track, signing-off add-ons
- `docs/skill-work/work-coffee/work-coffee-history.md` — lane breadcrumbs
- `docs/skill-work/work-cadence/work-cadence-events.md` — per-run cadence telemetry
- `.cursor/skills/dream/SKILL.md` — night-side counterpart
- `docs/skill-work/work-politics/polling-and-markets.md` — KY-4 polling (**menu A — Today**)
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md` — messaging discipline
