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
| `daily-warmup` | **Good morning:** **Step 1** (warmup + harness, daily brief per cadence, **KY-4 polling + Polymarket**, Massie X, brief body) + **Step 2** **A–E** (template + boundary audit combined, continue work module, context C, compliance/sources pulse D, **E** end morning meeting). **Good night:** **Step 1** `operator_handoff_check.py` + summary + **Step 2** **A–E** (gate tomorrow, boundary/integrity, night closeout lane, context D, **E** end night session). See [polling-and-markets.md](skill-work/work-politics/polling-and-markets.md) and `.cursor/skills/daily-warmup/SKILL.md` | Morning: `operator_daily_warmup.py` + agent steps; night: `operator_handoff_check.py` + agent steps |
| `pol-pulse` | Territory-only status sweep for `work-politics` | `python3 scripts/operator_work_politics_pulse.py -u grace-mar` (legacy script name: `operator_wap_pulse.py`) |
| `weekly-brief-run` | Weekly brief readiness pass plus scaffold generation for `work-politics` | `python3 scripts/operator_weekly_brief_run.py -u grace-mar` |
| `gate-review-pass` | Recommendation-oriented review pass over pending `RECURSION-GATE` candidates | `python3 scripts/operator_gate_review_pass.py -u grace-mar` |
| `handoff-check` | Stop/resume summary with **RECURSION-GATE pending detail**, **Predictive History night closeout** (work-jiang), recent commits, local work, runtime noise, and a re-entry prompt | `python3 scripts/operator_handoff_check.py -u grace-mar` |
| `work-jiang-feature-checklist` | Branch hygiene, scope, canonical verify block, and commit granularity for `research/external/work-jiang` + `scripts/work_jiang/` | Agent: follow `.cursor/skills/work-jiang-feature-checklist/SKILL.md` |
| `massie-x-news-search-draft` | Real-time news search + suggested @usa_first_ky X drafts (human approves; no auto-post) | Agent: follow `.cursor/skills/massie-x-news-search-draft/SKILL.md` |
| `pol-dashboard` | Internal miniapp UI at `/pol` (legacy `/wap`) — work-politics job tracker (token: `POL_DASHBOARD_TOKEN` or legacy `WAP_DASHBOARD_TOKEN`) | [pol-dashboard.md](pol-dashboard.md) |

**Stale derived exports** (manifest, PRP, fork-manifest, runtime bundle): `python3 scripts/refresh_derived_exports.py -u grace-mar` then `python3 scripts/validate-integrity.py --user grace-mar --json`. See [development-handoff.md § Quick Resume](development-handoff.md#quick-resume-commands).

---

## Suggested daily pattern

1. Start with `daily-warmup` when opening a new work block or a new agent thread. On **“good morning”**, the agent runs **Step 1** (including **Polymarket** KY-04 primary + GE party and **independent** polls per [polling-and-markets.md](skill-work/work-politics/polling-and-markets.md)), then **Step 2**: fixed **A–E** menu (**A** template + boundary audit combined, **B** continue latest work module, **C** context, **D** compliance/sources pulse, **E** end morning meeting) — see `.cursor/skills/daily-warmup/SKILL.md` § *Good morning — multiple choice (A–E required)*. **Cadence:** Monday = full routine; Tue–Fri = lighter; Sunday ≈ 10 min week-ahead (FEC, registration, brief registry); Friday adds a two-line post-mortem — see `.cursor/skills/daily-warmup/SKILL.md` § Cadence by weekday. On **“good night”** (day / session end), **Step 1** = `operator_handoff_check.py` + summary, then **Step 2** = **good night A–E** — see `.cursor/skills/daily-warmup/SKILL.md` § Good night (not the morning stack). **Good morning E** closes only the morning meeting, not the day.
2. Run `pol-pulse` when the day includes campaign work, brief prep, or X/content operations.
3. Use `massie-x-news-search-draft` when you want breaking-news hooks and draft tweets for the Massie shadow X account.
4. Use `weekly-brief-run` for the actual work-politics brief cycle after checking source freshness. If the cycle covers **high-stakes** topics (war powers, ethics/insider, cartel-economy legal claims, border + civil liberties), complete **weekly brief §8** / `docs/skill-work/work-politics/america-first-ky/` stress-test before treating drafts as final.
5. Use `gate-review-pass` when you want a queue review recommendation without taking action yet.
6. End the day with **good night**: **`handoff-check`** output is **Step 1**; agent then shows **good night A–E** (**E** = formally end night session). To resume mid-thread without full night flow, use `handoff-check` alone per `.cursor/skills/handoff-check/SKILL.md`.

---

## Output contract

### `daily-warmup`

Must answer:

- What needs attention first?
- Are there pending gate items?
- Is work-politics blocked or stale?
- Is repo integrity healthy?
- Is the worktree noisy enough to affect the next move?
- **Good morning:** What are **Polymarket** implied odds + **volume** (KY-04 GOP primary and GE party markets), and is there a **named independent** horserace poll — or explicitly none? (Caveats: markets ≠ polls; cite URLs; ignore Polymarket AI blurbs — [polling-and-markets.md](skill-work/work-politics/polling-and-markets.md).)
- **Good morning:** After **Step 1**, fixed **A–E** menu — **A** template + boundary audit combined (`template_diff.py` / audit reports + boundary / fork isolation / [skills-modularity.md](skills-modularity.md); optional `validate-integrity.py`; **required closing:** upstream/downstream **reconciliation code** recommendations per [work-companion-self/README — Reconciliation code audit](skill-work/work-companion-self/README.md#reconciliation-code-audit-upstream-and-downstream)), **B** continue most recent work module, **C** context pick, **D** compliance/sources pulse (polling doc + brief-source-registry), **E** formally end morning meeting. See `.cursor/skills/daily-warmup/SKILL.md` § *Good morning — multiple choice (A–E required)*.
- **Good night:** After **Step 1** (`operator_handoff_check.py` + paragraph), fixed **A–E** — **A** gate tomorrow-first, **B** boundary/integrity, **C** night closeout lane (Jiang / handoff block), **D** context pick, **E** formally end night session. See `.cursor/skills/daily-warmup/SKILL.md` § *Good night — multiple choice (A–E required)*.

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
