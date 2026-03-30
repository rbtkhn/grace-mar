# Operator skills

Project-local workflow skills for Grace-Mar operator routines.

These skills package recurring "morning coffee" and territory pulse workflows into reusable commands for Cursor agents. They do not change the gated merge rule, and they do not create new memory lanes. They are read-only workflow surfaces over canonical repo state.

## Contextual stewardship

- **Agents have no cross-thread institutional memory.** Authority for the Record stays **on-disk files** + **gated pipeline** (`AGENTS.md`, RECURSION-GATE, companion-approved merges) — not chat summaries or model recall.
- **Skills are weather reports, not policy.** They surface state; they do not replace reading `recursion-gate.md` / `self-evidence.md` when decisions are on the line.
- **Encoded judgment** = gate workflow + receipts + CI/tests you run before ship — not prompt length alone.

---

## Included skills

| Skill | Purpose | Default command |
|------|---------|-----------------|
| `daily-warmup` | **Good morning:** **Step 1** (warmup + harness + branch snapshot — **no** internet intel; **no** daily brief generator; **menu C** for brief + §1d Putin web) + **Step 2** **A–H** (order **A,B,C,D,E,G,H,F**; **F** ends session). **KY-4 + Polymarket + polls + Massie X:** **menu E → work-politics** (or explicit same-message request); **Companion survey** path skips that stack unless asked. **G** = work-jiang / Predictive History; **H** = skills / meta pipeline. **Good night:** **Step 1** `operator_handoff_check.py` + summary + **Step 2** **A–H** — **A–D** same as good morning (**D** = gate); **E** night system pick; **G** / **H** same as morning; **F** end night session. See [polling-and-markets.md](skill-work/work-politics/polling-and-markets.md) and `.cursor/skills/daily-warmup/SKILL.md` § *Shared A–C* / § *Shared D* / § *Shared G-H* | Morning: `operator_daily_warmup.py` + agent steps; night: `operator_handoff_check.py` + agent steps |
| `pol-pulse` | Territory-only status sweep for `work-politics` | `python3 scripts/operator_work_politics_pulse.py -u grace-mar` (legacy script name: `operator_wap_pulse.py`) |
| `weekly-brief-run` | Weekly brief readiness pass plus scaffold generation for `work-politics` | `python3 scripts/operator_weekly_brief_run.py -u grace-mar` |
| `gate-review-pass` | Recommendation-oriented review pass over pending `RECURSION-GATE` candidates | `python3 scripts/operator_gate_review_pass.py -u grace-mar` |
| `handoff-check` | Stop/resume summary with **RECURSION-GATE pending detail**, **Predictive History night closeout** (work-jiang), recent commits, local work, runtime noise, and a re-entry prompt | `python3 scripts/operator_handoff_check.py -u grace-mar`; cold paste stack: `python3 scripts/operator_reentry_stack.py -u grace-mar` (`--compact` optional); one-liner: `python3 scripts/harness_warmup.py -u grace-mar --receipt` |
| `work-jiang-feature-checklist` | Branch hygiene, scope, canonical verify block, and commit granularity for `research/external/work-jiang` + `scripts/work_jiang/` | Agent: follow `.cursor/skills/work-jiang-feature-checklist/SKILL.md` |
| `politics-massie` | Real-time news search + suggested @usa_first_ky X drafts (human approves; no auto-post) | Agent: follow `.cursor/skills/politics-massie/SKILL.md` |
| `portable-skills-sync` | Regenerate Cursor `SKILL.md` from `skills-portable/` + `manifest.yaml` + `CURSOR_APPENDIX.md`; run `--verify` before commit | `python3 scripts/sync_portable_skills.py --verify` then sync; agent: `.cursor/skills/portable-skills-sync/SKILL.md` |
| `pol-dashboard` | Internal miniapp UI at `/pol` (legacy `/wap`) — work-politics job tracker (token: `POL_DASHBOARD_TOKEN` or legacy `WAP_DASHBOARD_TOKEN`) | [pol-dashboard.md](pol-dashboard.md) |

**Stale derived exports** (manifest, PRP, fork-manifest, runtime bundle): `python3 scripts/refresh_derived_exports.py -u grace-mar` then `python3 scripts/validate-integrity.py --user grace-mar --json`. See [development-handoff.md § Quick Resume](development-handoff.md#quick-resume-commands).

**Skill discovery:** Pointer backlog [skills-portable/skill-candidates.md](../skills-portable/skill-candidates.md), draft lane `skills-portable/_drafts/`, ladder in [skills-portable/README.md](../skills-portable/README.md). After substantive **EXECUTE** / **DOCSYNC** ships, optional one-line prompt per [.cursor/rules/operator-style.mdc](../.cursor/rules/operator-style.mdc) (Skill discovery). Good morning / good night menu **H** is the dedicated skills slot; **handoff-check** summary may mention the same.

---

## Suggested daily pattern

1. Start with `daily-warmup` when opening a new work block or a new agent thread. The operator may say **“good morning” more than once per day** for reorientation; each invocation runs **Step 1** again (see `.cursor/skills/daily-warmup/SKILL.md` § *Multiple good mornings per day*). Use **good morning light** / **minimal** for lighter repeat passes. On **“good morning”**, the agent runs **Step 1** (scripts + branch snapshot — **no** Polymarket / poll web / Massie X in Step 1), then **Step 2**: fixed **A–H** — **E → work-politics** runs KY-4 + Polymarket + polls + Massie X per [polling-and-markets.md](skill-work/work-politics/polling-and-markets.md) when not survey-only; **C** runs brief generator + §1d Putin web **only when chosen**; **G** / **H** per skill table — see `.cursor/skills/daily-warmup/SKILL.md` § *Good morning — multiple choice (A–H required)*. **Cadence:** Monday = full routine; Tue–Fri = lighter; Sunday ≈ 10 min week-ahead (FEC, registration, brief registry); Friday adds a two-line post-mortem — see `.cursor/skills/daily-warmup/SKILL.md` § Cadence by weekday. On **“good night”** (day / session end), **Step 1** = `operator_handoff_check.py` + summary, then **Step 2** = **good night A–H** — **A–D** match good morning (**D** = RECURSION-GATE); **E** = night system pick; **G** / **H** shared with morning — see `.cursor/skills/daily-warmup/SKILL.md` § *Good night*, § *Shared A–C*, § *Shared D*, § *Shared G-H*. **Good morning F** closes only the morning meeting, not the day.
2. Run `pol-pulse` when the day includes campaign work, brief prep, or X/content operations.
3. Use `politics-massie` when you want breaking-news hooks and draft tweets for the Massie shadow X account.
4. Use `weekly-brief-run` for the actual work-politics brief cycle after checking source freshness. If the cycle covers **high-stakes** topics (war powers, ethics/insider, cartel-economy legal claims, border + civil liberties), complete **weekly brief §8** / `docs/skill-work/work-politics/america-first-ky/` stress-test before treating drafts as final.
5. Use `gate-review-pass` when you want a queue review recommendation without taking action yet.
6. End the day with **good night**: **`handoff-check`** output is **Step 1**; agent then shows **good night A–H** (**F** = formally end night session). To resume mid-thread without full night flow, use `handoff-check` alone per `.cursor/skills/handoff-check/SKILL.md`.

---

## Output contract

### `daily-warmup`

Must answer:

- What needs attention first?
- Are there pending gate items?
- Is work-politics blocked or stale?
- Is repo integrity healthy?
- Is the worktree noisy enough to affect the next move?
- **Good morning:** **Polymarket** + **volume** + **independent** horserace poll (or none) — **only** after **menu E → work-politics** (intel path) or explicit same-message request; same caveats and procedure as [polling-and-markets.md](skill-work/work-politics/polling-and-markets.md). Step 1 does **not** include this block.
- **Good morning:** After **Step 1**, fixed **A–H** menu (present **A,B,C,D,E,G,H,F**) — **A** template + boundary audit combined (`template_diff.py` / audit reports + boundary / fork isolation / [skills-modularity.md](skills-modularity.md); optional `validate-integrity.py`; **required closing:** upstream/downstream **reconciliation code** recommendations per [work-companion-self/README — Reconciliation code audit](skill-work/work-companion-self/README.md#reconciliation-code-audit-upstream-and-downstream)), **B** repository hygiene (git branches, status, commit/push plan, exports/integrity per daily-warmup table), **C** Daily brief (`generate_work_politics_daily_brief.py` + §1d Putin in-file — **only when C is chosen**; Step 1 does not generate), **D** RECURSION-GATE (`recursion-gate.md`, gate-review-pass; **no merge** without companion approval), **E** work-dev *or* work-strategy *or* work-politics — **E / work-politics** = KY-4 intel stack when not survey-only; survey defaults under **E** / work-politics when “good morning survey” **without** forced Polymarket/Massie unless asked; **G** work-jiang / Predictive History; **H** skills / meta pipeline; **F** end good morning session → normal workflow. See `.cursor/skills/daily-warmup/SKILL.md` § *Good morning — multiple choice (A–H required)*.
- **Good night:** After **Step 1** (`operator_handoff_check.py` + paragraph), fixed **A–H** — **A–D** same as good morning (template + boundary, repository hygiene, Daily brief when chosen, **D** RECURSION-GATE), **E** night system pick (integrity, survey, commit grouping, etc.; prefer **G** for Jiang/PH, **H** for skills), **G** / **H** same as morning, **F** formally end night session. See `.cursor/skills/daily-warmup/SKILL.md` § *Shared A–C*, § *Shared D*, § *Shared G-H*, and § *Good night — multiple choice (A–H required)*.

### `pol-pulse`

Must answer:

- What is the current campaign timeline?
- What is stale or blocking?
- Is the weekly brief ready to generate?
- What content is moving?
- Are there live work-politics gate items?

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

Use the first output to choose the work block. Use the second to choose the work-politics action inside that block.

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
