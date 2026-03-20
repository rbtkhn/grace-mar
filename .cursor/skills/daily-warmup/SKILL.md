---
name: daily-warmup
description: Generate a Grace-Mar morning coffee or daily operator warmup with gate state, WAP status, repo integrity, and top priorities. Use when the operator says good morning, when starting a new thread, planning the day, asking what to work on next, or requesting a pulse check before implementation.
---

# Daily Warmup

Use this skill at the start of a work block when the operator wants a quick planning pass grounded in repo state.

## "Good morning" = start here

When the operator begins with **"good morning"** (or clearly the same intent), treat it as a **daily session start**:

1. Run the warmup commands below (warmup + harness when instance state matters).
2. **Always** run today’s combined daily brief and write it to the repo:
   ```bash
   python3 scripts/generate_wap_daily_brief.py -u grace-mar -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md
   ```
   Include the output path in your reply and a short summary (top WAP + strategy headlines, next actions).
3. Run the `.cursor/skills/massie-x-news-search-draft/SKILL.md` flow to do a daily web scan of Massie-relevant news and **his latest X posts**, producing **draft-only** candidate posts for `@usa_first_ky`.
4. Return the warmup brief (priorities, gate, WAP, integrity) plus:
   - daily-brief summary (with output path)
   - X scan top links (short)
   - 1–2 draft post candidates for `@usa_first_ky` (still draft-only; human approval required)
5. Stay read-only otherwise: no merge/stage unless they switch lanes or use a pipeline phrase ("we …").

## Run this first

```bash
python3 scripts/operator_daily_warmup.py -u grace-mar
```

If the work touches instance state and the thread does not already contain a warmup snapshot, also run:

```bash
python3 scripts/harness_warmup.py -u grace-mar
```

Paste or quote the warmup block so the thread carries the same continuity snapshot.

## What to return

Return a short operator brief with:

- top 3 priorities
- gate state and whether anything needs review now
- WAP blockers or next actions
- integrity status
- local worktree noise only if it matters for the next move
- (Optional) X scan top links + 1–2 draft post candidates for `@usa_first_ky` (draft-only)

## Guardrails

- This is read-only planning. Do not merge or stage just because the warmup mentions candidates.
- If integrity fails, surface that before optional improvements.
- Treat `users/grace-mar/recursion-gate.md` and `self-evidence.md` as canonical, not the summary.

## Related files

- `docs/operator-skills.md`
- `docs/skill-work/work-politics/workspace.md`
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md` (high-stakes WAP messaging discipline; weekly brief §8)
