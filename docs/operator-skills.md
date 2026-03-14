# Operator skills

Project-local workflow skills for Grace-Mar operator routines.

These skills package recurring "morning coffee" and territory pulse workflows into reusable commands for Cursor agents. They do not change the gated merge rule, and they do not create new memory lanes. They are read-only workflow surfaces over canonical repo state.

---

## Included skills

| Skill | Purpose | Default command |
|------|---------|-----------------|
| `daily-warmup` | Repo-wide operator warmup: gate state, WAP status, integrity, local worktree noise, and top priorities | `python3 scripts/operator_daily_warmup.py -u grace-mar` |
| `wap-pulse` | Territory-only status sweep for `work-american-politics` | `python3 scripts/operator_wap_pulse.py -u grace-mar` |

---

## Suggested daily pattern

1. Start with `daily-warmup` when opening a new work block or a new agent thread.
2. Run `wap-pulse` when the day includes campaign work, brief prep, or X/content operations.
3. If needed, run both in parallel and use the outputs to decide the next 1-3 actions.
4. Generate a weekly scaffold with `python3 scripts/generate_wap_weekly_brief.py -u grace-mar` after refreshing `brief-source-registry.md`.

---

## Output contract

### `daily-warmup`

Must answer:

- What needs attention first?
- Are there pending gate items?
- Is WAP blocked or stale?
- Is repo integrity healthy?
- Is the worktree noisy enough to affect the next move?

### `wap-pulse`

Must answer:

- What is the current campaign timeline?
- What is stale or blocking?
- Is the weekly brief ready to generate?
- What content is moving?
- Are there live WAP gate items?

---

## Parallel operator pass

When you want the same leverage pattern as the video workflow, run these in parallel:

```bash
python3 scripts/operator_daily_warmup.py -u grace-mar
python3 scripts/operator_wap_pulse.py -u grace-mar
```

Use the first output to choose the work block. Use the second to choose the WAP action inside that block.

---

## Guardrails

- These skills are read-only summaries over canonical files.
- `users/grace-mar/recursion-gate.md`, `self.md`, `self-evidence.md`, and WAP docs remain the source of truth.
- WAP remains a `WORK` surface; Record changes still require staged approval and merge flow.
