# Operator skills

Project-local workflow skills for Grace-Mar operator routines.

These skills package recurring "morning coffee" and territory pulse workflows into reusable commands for Cursor agents. They do not change the gated merge rule, and they do not create new memory lanes. They are read-only workflow surfaces over canonical repo state.

## Contextual stewardship

- **Agents have no cross-thread institutional memory.** Authority for the Record stays **on-disk files** + **gated pipeline** (`AGENTS.md`, RECURSION-GATE, companion-approved merges) — not chat summaries or model recall.
- **Skills are weather reports, not policy.** They surface state; they do not replace reading `recursion-gate.md` / `self-evidence.md` when decisions are on the line.
- **Encoded judgment** = gate workflow + receipts + CI/tests you run before ship — not prompt length alone.

---

## Preferred activation (operator chat)

Each `.cursor/skills/*/SKILL.md` declares YAML **`preferred_activation`** (one or two words). Say that phrase in chat—or **`use <skill-name>`**—to steer the agent. Aliases in the skill body still work.

| Skill | Say this | Note |
|------|----------|------|
| `coffee` | **coffee** | Canonical cadence skill; **signing-off** intent = handoff-weighted Step 1, **same** **A–G** menu (**E — Steward** without gate/template split = system pick; **C — Compass** includes work-strategy-rome; **F** / **G** = xavier next / dev next). Legacy **hey** still works. |
| `thanks` | **thanks** | Micro-pause: optional **park** line + `log_cadence_event.py --kind thanks`. Not **`dream`** / **`bridge`**. See `.cursor/skills/thanks/SKILL.md`. |
| `handoff-check` | **handoff check** | |
| `gate-review-pass` | **gate review** | |
| `weekly-brief-run` | **weekly brief** | |
| `skill-strategy` | **strategy** | Alt: **strategy pass**, **work-strategy**. Notebook-primary work-strategy pass. See `.cursor/skills/skill-strategy/SKILL.md`. |
| `politics-massie` | **massie x** | Portable core: `skills-portable/politics-massie/` → run `sync_portable_skills.py` after edits. |
| `work-jiang-feature-checklist` | **jiang check** | |
| `portable-skills-sync` | **sync skills** | Portable core: `skills-portable/portable-skills-sync/`. |
| `extract-skill-from-session` | **save skill** | Alt: **skill from session**. |
| `pros-and-cons` | **unpack** | Alt: **pros cons**. |
| `fact-check` | **fact check** | Alt: **verify this**, **check this claim**. |
| `pol-dashboard` (doc/runbook) | **pol dash** | No `SKILL.md`; miniapp + [pol-dashboard.md](pol-dashboard.md). |

---

## Included skills

| Skill | Purpose | Default command |
|------|---------|-----------------|
| `coffee` | **Step 1** (work-start: warmup + harness + branch snapshot + **lane next hints** for **F**/**G** — **no** internet intel; **no** daily brief generator; **signing-off:** `operator_coffee.py --mode closeout` or `operator_handoff_check.py` + summary) + **Step 2** **same** menu always (order **A,B,C,D,E,F,G** — seven modes; **no** close letter). **A — Today:** brief + §1d Putin + KY-4 intel (survey defaults here with **`coffee survey`**). **B — Build:** work-dev + skills/meta — **not** git/ship ( **E git** ) or membrane-only audits. **C — Compass:** work-strategy + work-strategy-rome. **D — Book:** Jiang / PH. **E — Steward:** gate \| template \| integrity \| **git/ship** (`E integrity`, `E git`, `E both`, `E all` when explicit; default **E** = gate else template). Reconciliation code when template/boundary is in scope. **F — Xavier next:** one work-xavier step from hints + SYNC-DAILY / WORK-LEDGER / INDEX. **G — Dev next:** first open item in `workspace.md` § Next actions (narrower than **B**). **C** and **D** → exit to normal workflow unless **`stay in coffee`**; **A**, **B**, **F**, **G** re-offer full menu by default; **E** uses steward fork when actionable. **Signing-off:** **E** without steward sub-track → **system pick**. See [polling-and-markets.md](skill-work/work-politics/polling-and-markets.md), `.cursor/skills/coffee/SKILL.md`, [menu-reference — signing-off](skill-work/work-coffee/menu-reference.md#signing-off-intent). | **`operator_coffee.py`** (modes) + agent steps |
| `thanks` | **Micro-pause** cadence beat: optional one-line **park** text + append **`thanks`** line to [work-cadence-events.md](skill-work/work-cadence/work-cadence-events.md) — no dream, no handoff script, no coffee menu | `python3 scripts/log_cadence_event.py --kind thanks -u grace-mar --ok --kv park=…` (agent: `.cursor/skills/thanks/SKILL.md`) |
| `weekly-brief-run` | Weekly brief readiness pass plus scaffold generation for `work-politics` | `python3 scripts/operator_weekly_brief_run.py -u grace-mar` |
| `gate-review-pass` | Recommendation-oriented review pass over pending `RECURSION-GATE` candidates | `python3 scripts/operator_gate_review_pass.py -u grace-mar` |
| `handoff-check` | Stop/resume summary with **RECURSION-GATE pending detail**, **Predictive History night closeout** (work-jiang), recent commits, local work, runtime noise, and a re-entry prompt | `python3 scripts/operator_handoff_check.py -u grace-mar`; cold paste stack: `python3 scripts/operator_reentry_stack.py -u grace-mar` (`--compact` optional); one-liner: `python3 scripts/harness_warmup.py -u grace-mar --receipt` |
| `pros-and-cons` | When a proposal is **unclear** or the operator wants **pros/cons / unpack / tradeoffs**: plain-language **restate**, then **pros**, **cons**, **disproportion**, **recommendation** (Think lane; no ship unless asked) | Agent: follow `.cursor/skills/pros-and-cons/SKILL.md` |
| `fact-check` | **Triage-first** check on pasted/named claims: **lean** verdict table, **one cite** per claim when enough, **high abstention** + **Escalate** when stakes need deeper audit; **not** Record merge unless gated pipeline | Agent: follow `.cursor/skills/fact-check/SKILL.md` |
| `skill-strategy` | **Strategy pass** — [strategy-notebook](skill-work/work-strategy/strategy-notebook/README.md) first, [STRATEGY.md](skill-work/work-strategy/STRATEGY.md) when promoting; Islamabad/Rome, weak-signal, analogy-audit; **not** work-politics pulse | Agent: `.cursor/skills/skill-strategy/SKILL.md` |
| `work-jiang-feature-checklist` | Branch hygiene, scope, canonical verify block, and commit granularity for `research/external/work-jiang` + `scripts/work_jiang/` | Agent: follow `.cursor/skills/work-jiang-feature-checklist/SKILL.md` |
| `politics-massie` | Real-time news search + suggested @usa_first_ky X drafts (human approves; no auto-post) | Agent: follow `.cursor/skills/politics-massie/SKILL.md` |
| `portable-skills-sync` | Regenerate Cursor `SKILL.md` from `skills-portable/` + `manifest.yaml` + `CURSOR_APPENDIX.md`; run `--verify` before commit | `python3 scripts/sync_portable_skills.py --verify` then sync; agent: `.cursor/skills/portable-skills-sync/SKILL.md` |
| `extract-skill-from-session` | Codify a finished multi-step workflow as a new `SKILL.md` | Agent: `.cursor/skills/extract-skill-from-session/SKILL.md` |
| `pol-dashboard` | Internal miniapp UI at `/pol` (legacy `/wap`) — work-politics job tracker (token: `POL_DASHBOARD_TOKEN` or legacy `WAP_DASHBOARD_TOKEN`) | [pol-dashboard.md](pol-dashboard.md) |

**Stale derived exports** (manifest, PRP, fork-manifest, runtime bundle): audit under **coffee E — integrity/exports** (`validate-integrity.py`); **`refresh_derived_exports.py` writes** — ship per operator lane after proposal. Quick commands: [development-handoff.md § Quick Resume](development-handoff.md#quick-resume-commands).

**Skill discovery:** Pointer backlog [skills-portable/skill-candidates.md](../skills-portable/skill-candidates.md), draft lane `skills-portable/_drafts/`, ladder in [skills-portable/README.md](../skills-portable/README.md). After substantive **EXECUTE** / **DOCSYNC** ships, optional one-line prompt per [.cursor/rules/operator-style.mdc](../.cursor/rules/operator-style.mdc) (Skill discovery). **Skills / meta:** **coffee B — Build** + say **skills** or **meta**; **handoff-check** summary may mention the same.

### Gate review — pattern notes (doc-only)

When **`gate review`** recommendations repeatedly mis-rank or duplicate-hint wrong, capture **one line** here or in [.cursor/skills/gate-review-pass/SKILL.md](../.cursor/skills/gate-review-pass/SKILL.md) § *After a batch review*. No automation — this is institutional memory for the operator and agents.

---

## Suggested daily pattern

1. Start with `coffee` when opening a new work block or a new agent thread. **Mid-day pause** (stepping away without day-close or session seal): optional **`thanks`** + park line per `.cursor/skills/thanks/SKILL.md`. The operator may say **`coffee` more than once per day** for reorientation; each invocation runs **Step 1** again (see `.cursor/skills/coffee/SKILL.md` § *Multiple coffees per day*). Legacy **`hey`** still works. Use **coffee light** / **minimal** for lighter repeat passes. On **work-start `coffee`**, the agent runs **Step 1** (scripts + branch snapshot + **lane next hints** — **no** Polymarket / poll web / Massie X in Step 1), then **Step 2**: fixed **A–G** — **A — Today** runs brief + §1d + KY-4 intel per [polling-and-markets.md](skill-work/work-politics/polling-and-markets.md) when not survey-only; **B — Build** = work-dev + skills (+ **skills** / **meta** when asked); **C — Compass** = strategy + Rome; **D — Book** = Jiang / PH; **E — Steward** = gate / template / integrity / **git/ship** (see [menu-reference](skill-work/work-coffee/menu-reference.md)); **F — Xavier next**; **G — Dev next** (`workspace.md`). **C** and **D** exit to normal workflow unless **`stay in coffee`**; **A**, **B**, **F**, **G** re-offer the full menu by default; **E** uses the steward fork (**Implement now** / **Later**) when actionable, else full menu — see [menu-reference.md](skill-work/work-coffee/menu-reference.md#steward-follow-up-fork-implement-now-vs-later). **No close letter** — exit per [menu-reference — Exit](skill-work/work-coffee/menu-reference.md) (no **no menu** in coffee). **Cadence:** Monday = full routine; Tue–Fri = lighter; Sunday ≈ 10 min week-ahead (FEC, registration, brief registry); Friday adds a two-line post-mortem — see [menu-reference.md](skill-work/work-coffee/menu-reference.md) § Cadence by weekday. **Signing-off `coffee`** (session end / wrapping — **same** trigger): **Step 1** = `operator_handoff_check.py` (or `operator_coffee.py --mode closeout`) + summary, then the **same** menu as work-start; **E — Steward** without gate/template split → **system pick** — see [menu-reference — signing-off intent](skill-work/work-coffee/menu-reference.md#signing-off-intent).
2. When the day includes campaign work, brief prep, or X/content operations, run `python3 scripts/operator_work_politics_pulse.py -u grace-mar` (territory pulse — no dedicated skill).
3. Use `politics-massie` when you want breaking-news hooks and draft tweets for the Massie shadow X account.
4. Use `weekly-brief-run` for the actual work-politics brief cycle after checking source freshness. If the cycle covers **high-stakes** topics (war powers, ethics/insider, cartel-economy legal claims, border + civil liberties), complete **weekly brief §8** / `docs/skill-work/work-politics/america-first-ky/` stress-test before treating drafts as final.
5. Use `gate-review-pass` when you want a queue review recommendation without taking action yet.
6. End the day with **`coffee`** + **signing-off** intent: **`handoff-check`** (or `operator_coffee.py --mode closeout`) is **Step 1**; agent then shows the **same** **A–G** menu as work-start (**E — Steward** alone = system pick). To resume mid-thread without the full `coffee` flow, use `handoff-check` alone per `.cursor/skills/handoff-check/SKILL.md`.

---

## Output contract

### `coffee`

**Legacy:** Cursor skill folder/id was `daily-warmup`, then `operator-cadence`. Update bookmarks to `.cursor/skills/coffee/`.

Must answer:

- What needs attention first?
- Are there pending gate items?
- Is work-politics blocked or stale?
- Is repo integrity healthy?
- Is the worktree noisy enough to affect the next move?
- **Coffee:** **Polymarket** + **volume** + **independent** horserace poll (or none) — **only** after **menu A — Today** (intel path) or explicit same-message request; same caveats and procedure as [polling-and-markets.md](skill-work/work-politics/polling-and-markets.md). Step 1 does **not** include this block.
- **Coffee:** After **Step 1**, fixed **A–G** menu (present **A,B,C,D,E,F,G**) — **A — Today** (brief + §1d + KY-4 intel; survey defaults here with **`coffee survey`**), **B — Build** (work-dev + skills; **skills** / **meta** when asked), **C — Compass** (work-strategy + work-strategy-rome), **D — Book** (Jiang / PH), **E — Steward** (gate / template / integrity / git/ship; **reconciliation code** when template/boundary is in scope per [work-companion-self/README — Reconciliation code audit](skill-work/work-companion-self/README.md#reconciliation-code-audit-upstream-and-downstream)), **F — Xavier next**, **G — Dev next**. **Signing-off:** **E** without steward sub-track → **system pick**. **C** and **D** exit to normal workflow unless **`stay in coffee`**; **A**, **B**, **F**, **G** re-offer the menu by default; **E** per steward fork. **No close letter.** See `.cursor/skills/coffee/SKILL.md` and [menu-reference.md](skill-work/work-coffee/menu-reference.md).
- **Signing-off `coffee`:** After **Step 1** (`operator_handoff_check.py` + paragraph), **same** fixed menu as work-start; **E — Steward** without gate/template split → **system pick**. See [menu-reference — signing-off intent](skill-work/work-coffee/menu-reference.md#signing-off-intent).

### `weekly-brief-run`

Must answer:

- Are the weekly brief sources fresh enough?
- What must be refreshed first?
- Was a scaffold emitted or intentionally withheld?
- What human review is still required before use?
- If the brief touches high-stakes areas (see `weekly-brief-template.md` §8), has the operator been pointed at the factorial stress-test template and framework under `docs/skill-work/work-politics/america-first-ky/`?

### `gate-review-pass`

Must answer:

- What can likely be approved now?
- What looks stale?
- What likely duplicates existing Record content?
- What needs manual escalation instead of quick review?

### `pros-and-cons`

Must answer:

- What is the proposal **in one plain sentence** (and rough in/out scope)?
- What are the **pros** and **cons** as concrete bullets?
- **Which side is heavier** (disproportion) and why?
- What is the **recommendation** (do / defer / revise), without assuming approval to implement?

### `handoff-check`

Must answer:

- What is **pending in RECURSION-GATE** (work-politics vs companion), and what **proposed steps** does the script give to clear the queue (without merging in the skill)?
- What was recently committed?
- What meaningful local work is still in progress?
- What looks like runtime-only noise?
- What is the best first prompt for the next session?

### `work-jiang-feature-checklist`

Must answer:

- Is the working tree clean enough to review (unrelated untracks isolated)?
- Does scope stay in the Geo-Strategy lane unless the task says otherwise?
- Was the full verify block (or an explicitly justified subset) run before ship?
- Are commits or phases aligned to the plan (quotes / counter-readings / chronology / CI)?

---

## Parallel operator pass

When you want the same leverage pattern as the video workflow, run these in parallel:

```bash
python3 scripts/operator_daily_warmup.py -u grace-mar
python3 scripts/operator_work_politics_pulse.py -u grace-mar
```

Use the first output to choose the work block. Use the second to choose the work-politics action inside that block. There is **no** Cursor skill for the pulse script — invoke the script directly (or ask the agent to run it).

For a fuller operator pass:

```bash
python3 scripts/operator_daily_warmup.py -u grace-mar
python3 scripts/operator_work_politics_pulse.py -u grace-mar
python3 scripts/operator_gate_review_pass.py -u grace-mar
```

Use `weekly-brief-run` when the first two workflows say the territory is ready to produce a weekly scaffold.

---

## Guardrails

- These skills are read-only summaries over canonical files.
- `users/grace-mar/recursion-gate.md`, `self.md`, `self-evidence.md`, and work-politics docs remain the source of truth.
- work-politics remains a `WORK` surface; Record changes still require staged approval and merge flow.
- `weekly-brief-run` produces a first-pass scaffold, not final-use campaign output.
- `handoff-check` should treat runtime audit noise separately from meaningful worktree changes.
