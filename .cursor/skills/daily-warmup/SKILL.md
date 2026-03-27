---
name: daily-warmup
description: Generate a Grace-Mar morning coffee or daily operator warmup with gate state, work-politics status, KY-4 polling and Polymarket snapshot, repo integrity, and top priorities. Use when the operator says good morning, when starting a new thread, planning the day, asking what to work on next, or requesting a pulse check before implementation. For good night / end of session, use the Good night section (handoff check — not the morning stack).
---

# Daily Warmup

Use this skill at the start of a work block when the operator wants a quick planning pass grounded in repo state.

## Cadence by weekday

Default rhythm (operator can override any day):

| Day | Mode | What to run |
|-----|------|-------------|
| **Monday** | **Full** | Complete [“Good morning”](#good-morning--start-here) flow: operator + harness, **generate** daily brief, polling + Polymarket, Massie X scan + 1–2 drafts. |
| **Tuesday–Friday** | **Lighter** | `operator_daily_warmup.py` + `harness_warmup.py` (when instance state matters). **Polling + Polymarket** stays (compact). **Daily brief:** generate only if missing for today, else one-line pointer to `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md`. **Massie X:** shorten to **top story links** (or one draft) unless the content queue / news cycle demands more. |
| **Sunday** | **Week ahead (~10 min)** | Not a full good morning. Focus: **FEC / compliance dates** and **voter registration** from the daily brief calendar + [brief-source-registry.md](../../../docs/skill-work/work-politics/brief-source-registry.md) (`needs_refresh`, `watch`). Optional: skim `wap-pulse` / weekly-brief readiness. |
| **Friday** | **Lighter + post-mortem** | Same as Tue–Fri **plus** two lines at the end of the reply: **(1)** What repeated this week? **(2)** What to drop from the routine? |

If the operator says **“good morning”** on a **Sunday**, default to **week-ahead** mode unless they ask for the full Monday stack.

---

## "Good morning" = start here

When the operator begins with **"good morning"** (or clearly the same intent), treat it as a **daily session start** — **unless** [cadence](#cadence-by-weekday) says week-ahead (Sunday) or a lighter tier (Tue–Fri); then scale steps below accordingly.

**Work-jiang (Jiang) standing note:** The first curated lecture series in-repo is **Geo-Strategy** (`research/external/work-jiang/lectures/`). The **second** series is **Civilization** (channel naming). When the operator is about to upload or integrate **Civilization** transcripts, mention it in the brief (next step: raw pulls under `research/external/youtube-channels/predictive-history/`, then curated files per [WORKFLOW-transcripts.md](../../../research/external/work-jiang/WORKFLOW-transcripts.md)). See also `users/grace-mar/work-jiang.md` § Operator schedule.

**Alpha / mastery lens (optional):** If the operator ties the day to **mastery gates**, **2-hour academic ceiling**, or **“Time Back”**, point at [alpha-mastery-adaptation.md](../../../docs/alpha-mastery-adaptation.md) and optional `python3 scripts/good-morning-brief.py` / `reflection-proposals/DAILY-INTENTION-*.md` — design vocabulary, not school product claims.

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

---

## "Good night" = end session here

When the operator says **"good night"**, **"goodnight"**, or clearly the same intent (signing off for the day, closing the session), treat it as a **session end**, not a daily start.

**Do not** run the full [Good morning](#good-morning--start-here) stack (no daily brief generation, no Polymarket / Massie X pass, no `operator_daily_warmup.py` / `harness_warmup.py` as the main flow) **unless** they explicitly ask for morning-style output in the same message.

**Do** run the **handoff check** so the next thread can resume cleanly:

```bash
python3 scripts/operator_handoff_check.py -u grace-mar
```

1. **Include the command output** in your reply (paste verbatim or as a fenced markdown block).
2. Summarize in one short paragraph: what moved today (if known from the thread), what is parked, and the **suggested re-entry prompt** from the script output.
3. Stay read-only: no merge, stage, or commit as part of good night.

Full spec: [`.cursor/skills/handoff-check/SKILL.md`](../handoff-check/SKILL.md).

---

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
