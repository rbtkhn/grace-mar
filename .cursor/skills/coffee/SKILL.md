---
name: coffee
preferred_activation: coffee
description: "Grace-Mar operator cadence and tempo. Primary trigger: coffee. Coffee is a repeatable sip of coherence: a lightweight reorientation ritual that restores clarity, framing, and agency. Multiple coffee sessions per day are normal. Work-start coffee runs the read-only grounding stack, then the fixed A-H menu. Concrete work-lane picks exit to normal workflow by default."
---

# Coffee

**Preferred activation (operator):** say **`coffee`**. Legacy **`hey`** still works as a compatibility alias, but **`coffee`** is the canonical trigger now. **Work-start** vs **closeout** is **intent in the same message** (e.g. reorientation vs signing off), not a second trigger phrase — one skill and two Step 1 shapes.

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

When the operator begins with **`coffee`** (or clearly the same intent; legacy **`hey`** still counts), treat it as opening a **coffee session**. If the message **clearly means closeout** (signing off, end of session, wrapping the day, etc.), skip ahead to **[Coffee — closeout](#coffee-closeout)**. Otherwise **scale work-start Step 1** using **explicit phrases** when the operator used one, or **cadence by weekday** (Sunday → week-ahead; Tue–Fri → lighter; Monday → full). **Step 2** (A–H menu) always follows Step 1.

For cadence tables and explicit phrase definitions (`coffee light`, `coffee minimal`, `coffee survey`): see [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md).

### Multiple coffees per day

The operator may say **`coffee`** **more than once per calendar day** for reorientation. This is normal. Each new `coffee` runs Step 1 again and starts a new A–H cycle. If **`coffee`** arrives before the prior session reached **F**, treat it as a **reorientation restart**: run Step 1 again, then offer a fresh A–H menu.

### Step 1 — Automated actions

Run the consolidated coffee script (preferred):

```bash
python3 scripts/operator_coffee.py -u grace-mar                   # work-start (default)
python3 scripts/operator_coffee.py -u grace-mar --mode light      # lighter pass
python3 scripts/operator_coffee.py -u grace-mar --mode minimal    # compact harness only
python3 scripts/operator_coffee.py -u grace-mar --mode closeout   # handoff check
python3 scripts/operator_coffee.py -u grace-mar --mode reentry    # cold-thread full stack
```

Add `--compact` for shorter harness output. Individual scripts (`operator_daily_warmup.py`, `harness_warmup.py`, `operator_handoff_check.py`, `operator_reentry_stack.py`) are still available.

**Dream handoff:** If `dream` ran overnight, the daily warmup automatically includes a **"Last dream (night handoff)"** block from `users/grace-mar/last-dream.json`.

**Step 1 deliverables:** Warmup brief (priorities, gate, work-politics, integrity), branch snapshot, daily brief defer line (path + "menu C"), intel defer line ("E → work-politics"), optional PH/Jiang line. **No** Polymarket / poll / Massie blocks in Step 1 unless the operator explicitly asked in the same message.

**Step 1 guardrail:** Stay read-only — no merge/stage unless they switch lanes or use a pipeline phrase ("we …").

### Step 2 — Multiple choice (required; always A–H)

Immediately **after** Step 1 content, output the fixed **A–H** menu. **List order:** **A, B, C, D, E, G, H, F** (F closes). **Do not** omit **F**.

**Quick reference:**
- **A.** Template + boundary audit
- **B.** Repository hygiene
- **C.** Daily brief (generate + §1d Putin only when C is chosen)
- **D.** RECURSION-GATE (no merge without companion approval)
- **E.** Work-dev *or* work-strategy *or* work-politics — one lane + one recommendation (exits to normal workflow; Jiang = G; skills = H)
- **G.** work-jiang / Predictive History (exits to normal workflow)
- **H.** Skills / meta pipeline
- **F.** End coffee — close session

**Re-offer rules:** After **A, B, C, D, or H**, re-offer the full A–H menu. After **E** with a concrete sub-lane or **G**, **exit to normal workflow** unless the operator says **`stay in coffee`**. **F** formally closes the session.

For full A–H definitions, shared sections (work-start ↔ closeout), and the companion survey track: see [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md).

---

<a id="coffee-closeout"></a>

## Coffee — closeout (session end)

When the operator says **`coffee`** and **clearly means closeout** — same trigger, same skill — treat as the **closeout** path. **Do not** run the full work-start Step 1 stack unless explicitly asked.

### Step 1 — Handoff

```bash
python3 scripts/operator_coffee.py -u grace-mar --mode closeout
```

Or directly: `python3 scripts/operator_handoff_check.py -u grace-mar`. Include the output in your reply. Follow with a short paragraph: what moved today, what is parked, gate + Jiang carryovers, and the suggested re-entry prompt.

Full spec: [`.cursor/skills/handoff-check/SKILL.md`](../handoff-check/SKILL.md).

### Step 2 — Multiple choice (A–H, same letters)

Same eight options. **A–D, G, H** match work-start. Only **E** differs (system pick for closeout extras). See [menu-reference.md § Closeout menu](../../../docs/skill-work/work-coffee/menu-reference.md#closeout-menu-ah).

After **any letter except F**, re-offer the full A–H menu. **F** formally closes the closeout pass.

---

## Session trail (optional)

Sessions begin when the operator says **`coffee`** (optional modifiers). To keep a trail: use **`users/<id>/session-transcript.md`** and/or append dated bullets to **`docs/skill-work/work-*/*-history.md`**. **Not** the gated Record; **not** `self-memory`. See [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).

## Related files

- `docs/skill-work/work-coffee/README.md` — territory rationale and boundaries
- `docs/skill-work/work-coffee/menu-reference.md` — full A–H definitions, cadence, survey track
- `docs/skill-work/work-coffee/work-coffee-history.md` — lane breadcrumbs
- `.cursor/skills/dream/SKILL.md` — night-side counterpart
- `docs/skill-work/work-politics/polling-and-markets.md` — KY-4 polling (menu E → work-politics)
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md` — messaging discipline
