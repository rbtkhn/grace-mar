---
name: daily-warmup
description: Generate a Grace-Mar morning coffee or daily operator warmup with gate state, work-politics status, KY-4 polling and Polymarket snapshot, repo integrity, and top priorities. Use when the operator says good morning, when starting a new thread, planning the day, asking what to work on next, or requesting a pulse check before implementation.
---

# Daily Warmup

Use this skill at the start of a work block when the operator wants a quick planning pass grounded in repo state.

## "Good morning" = start here

When the operator begins with **"good morning"** (or clearly the same intent), treat it as a **daily session start**:

**Work-jiang (Jiang) standing note:** The first curated lecture series in-repo is **Geo-Strategy** (`research/external/work-jiang/lectures/`). The **second** series is **Civilization** (channel naming). When the operator is about to upload or integrate **Civilization** transcripts, mention it in the brief (next step: raw pulls under `research/external/youtube-channels/predictive-history/`, then curated files per [WORKFLOW-transcripts.md](../../../research/external/work-jiang/WORKFLOW-transcripts.md)). See also `users/grace-mar/work-jiang.md` § Operator schedule.

1. Run the warmup commands below (warmup + harness when instance state matters).
2. **Always** run today’s combined daily brief and write it to the repo:
   ```bash
   python3 scripts/generate_work_politics_daily_brief.py -u grace-mar -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md
   ```
   Include the output path in your reply and a short summary (top work-politics + strategy headlines, next actions).
3. **Polling + prediction markets (standard):** Follow [docs/skill-work/work-politics/polling-and-markets.md](../../../docs/skill-work/work-politics/polling-and-markets.md). **Fetch** the two canonical Polymarket pages (KY-04 GOP primary + GE party); **search** for any **independent** public horserace polls (Massie vs Gallrein) from the last ~30 days. Return a **compact block**: implied probabilities + **volume**, named public poll **or** “no independent poll found,” and a **one-line caveat** (markets ≠ polls; ignore Polymarket AI narrative blurbs; cite URLs). Update **`Last checked`** in that doc when you materially refresh numbers (same day is enough to set the date).
4. Run the `.cursor/skills/massie-x-news-search-draft/SKILL.md` flow to do a daily web scan of Massie-relevant news and **his latest X posts**, producing **draft-only** candidate posts for `@usa_first_ky`.
5. Return the warmup brief (priorities, gate, work-politics, integrity) plus:
   - daily-brief summary (with output path)
   - **polling + Polymarket block** (step 3)
   - X scan top links (short)
   - 1–2 draft post candidates for `@usa_first_ky` (still draft-only; human approval required)
   - If **Civilization** transcripts are pending or just landed, one line on that (upload/integrate status).
6. Stay read-only otherwise: no merge/stage unless they switch lanes or use a pipeline phrase ("we …").

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
- work-politics blockers or next actions
- integrity status
- local worktree noise only if it matters for the next move
- **KY-4 polling + Polymarket** (required for “good morning”): implied odds + volume + independent poll status + caveats — see [polling-and-markets.md](../../../docs/skill-work/work-politics/polling-and-markets.md)
- X scan top links + 1–2 draft post candidates for `@usa_first_ky` (draft-only; required when running the Massie X skill step)

## Guardrails

- This is read-only planning. Do not merge or stage just because the warmup mentions candidates.
- If integrity fails, surface that before optional improvements.
- Treat `users/grace-mar/recursion-gate.md` and `self-evidence.md` as canonical, not the summary.
- **Contextual stewardship:** Agents have no cross-thread institutional memory; authority for the Record is **on-disk files + gated pipeline** — not model recall or chat summary.

## Related files

- `docs/operator-skills.md`
- `docs/skill-work/work-politics/polling-and-markets.md` (KY-4 polling + Polymarket — good morning standard)
- `docs/skill-work/work-politics/workspace.md`
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md` (high-stakes work-politics messaging discipline; weekly brief §8)
