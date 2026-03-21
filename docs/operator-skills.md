# Operator skills

Project-local workflow skills for Grace-Mar operator routines.

These skills package recurring "morning coffee" and territory pulse workflows into reusable commands for Cursor agents. They do not change the gated merge rule, and they do not create new memory lanes. They are read-only workflow surfaces over canonical repo state.

---

## Included skills

| Skill | Purpose | Default command |
|------|---------|-----------------|
| `daily-warmup` | Repo-wide operator warmup: gate state, work-politics status, integrity, local worktree noise, and top priorities | `python3 scripts/operator_daily_warmup.py -u grace-mar` |
| `wap-pulse` | Territory-only status sweep for `work-politics` | `python3 scripts/operator_work_politics_pulse.py -u grace-mar` (legacy: `operator_wap_pulse.py`) |
| `weekly-brief-run` | Weekly brief readiness pass plus scaffold generation for `work-politics` | `python3 scripts/operator_weekly_brief_run.py -u grace-mar` |
| `gate-review-pass` | Recommendation-oriented review pass over pending `RECURSION-GATE` candidates | `python3 scripts/operator_gate_review_pass.py -u grace-mar` |
| `handoff-check` | Stop/resume summary with recent commits, local work, runtime noise, and a re-entry prompt | `python3 scripts/operator_handoff_check.py -u grace-mar` |
| `massie-x-news-search-draft` | Real-time news search + suggested @usa_first_ky X drafts (human approves; no auto-post) | Agent: follow `.cursor/skills/massie-x-news-search-draft/SKILL.md` |
| `wap-dashboard` | Internal miniapp UI at `/wap` — work-politics job tracker (token: `WAP_DASHBOARD_TOKEN`) | [wap-dashboard.md](wap-dashboard.md) |

---

## Suggested daily pattern

1. Start with `daily-warmup` when opening a new work block or a new agent thread.
2. Run `wap-pulse` when the day includes campaign work, brief prep, or X/content operations.
3. Use `massie-x-news-search-draft` when you want breaking-news hooks and draft tweets for the Massie shadow X account.
4. Use `weekly-brief-run` for the actual work-politics brief cycle after checking source freshness. If the cycle covers **high-stakes** topics (war powers, ethics/insider, cartel-economy legal claims, border + civil liberties), complete **weekly brief §8** / `docs/skill-work/work-politics/america-first-ky/` stress-test before treating drafts as final.
5. Use `gate-review-pass` when you want a queue review recommendation without taking action yet.
6. End or resume a session with `handoff-check`.

---

## Output contract

### `daily-warmup`

Must answer:

- What needs attention first?
- Are there pending gate items?
- Is work-politics blocked or stale?
- Is repo integrity healthy?
- Is the worktree noisy enough to affect the next move?

### `wap-pulse`

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

- What was recently committed?
- What meaningful local work is still in progress?
- What looks like runtime-only noise?
- What is the best first prompt for the next session?

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
