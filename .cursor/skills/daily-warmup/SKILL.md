---
name: daily-warmup
description: Generate a Grace-Mar morning coffee or daily operator warmup with gate state, work-politics status, KY-4 polling and Polymarket snapshot, repo integrity, top priorities, then a fixed **A–E** multiple-choice block (template audit, boundary audit, continue latest work module, context slot D, **E = formally end good morning session**). Use when the operator says good morning, when starting a new thread, planning the day, asking what to work on next, or requesting a pulse check before implementation. For good night / end of day, use the Good night section (handoff check — not the morning stack). **E** closes only the morning meeting, not the full day.
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

If the operator says **“good morning”** on a **Sunday**, default to **week-ahead** mode unless they ask for the full Monday stack. Still run **Step 1** scaled to that mode, then **Step 2** with the full **A–E** menu (labels can be shorter; meanings unchanged).

---

## "Good morning" = start here (two steps)

When the operator begins with **"good morning"** (or clearly the same intent), treat it as opening a **good morning session** — **unless** [cadence](#cadence-by-weekday) says week-ahead (Sunday) or a lighter tier (Tue–Fri); then **scale Step 1** accordingly. **Step 2** (A–E menu) always follows Step 1.

### Step 1 — Automated actions (run first; paste outputs)

**Work-jiang (Predictive History) — built-in momentum:** `python3 scripts/operator_daily_warmup.py` now appends **`## Predictive History — morning momentum`** (WORK container, STATUS/CHAPTER-QUEUE nudge, rotating **Spark**, dive links). **Customize sparks** in [`research/external/work-jiang/metadata/warmup-sparks.yaml`](../../../research/external/work-jiang/metadata/warmup-sparks.yaml) (operator voice; day-of-year rotation). Standalone: `python3 scripts/work_jiang/warmup_jiang_pulse.py -u grace-mar`. Context: first curated series **Geo-Strategy**; second **Civilization** — when integrating Civilization transcripts, mention raw pulls under `research/external/youtube-channels/predictive-history/` and [WORKFLOW-transcripts.md](../../../research/external/work-jiang/WORKFLOW-transcripts.md); see `users/grace-mar/work-jiang.md` § Operator schedule.

**Alpha / mastery lens (optional):** If the operator ties the day to **mastery gates**, **2-hour academic ceiling**, or **“Time Back”**, point at [alpha-mastery-adaptation.md](../../../docs/alpha-mastery-adaptation.md) and optional `python3 scripts/good-morning-brief.py` / `reflection-proposals/DAILY-INTENTION-*.md` — design vocabulary, not school product claims.

1. Run **`operator_daily_warmup.py`** and, when instance state matters, **`harness_warmup.py`** (see [Run this first](#run-this-first)).
2. **Daily brief:** Per cadence — **Monday / full day:** generate today’s file:
   ```bash
   python3 scripts/generate_work_politics_daily_brief.py -u grace-mar -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md
   ```
   **Tue–Fri (lighter):** generate only if missing for today; else one-line pointer to `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md`. **Sunday (week-ahead):** lean on calendar + brief-source-registry; brief step optional/minimal.
3. **Polling + prediction markets:** Follow [polling-and-markets.md](../../../docs/skill-work/work-politics/polling-and-markets.md). **Fetch** the two canonical Polymarket pages (KY-04 GOP primary + GE party); **search** for independent public horserace polls (Massie vs Gallrein) in the last ~30 days. **Compact block:** implied probabilities + **volume**, named poll **or** “no independent poll found,” **one-line caveat**, URLs. Update **`Last checked`** in that doc when you materially refresh numbers.
4. **Massie X:** Run `.cursor/skills/massie-x-news-search-draft/SKILL.md` (full or shortened per cadence): web scan + latest X posts; **draft-only** posts for `@usa_first_ky`.
5. In the reply body, deliver the **warmup brief** (priorities, gate, work-politics, integrity): daily-brief path + summary, polling + Polymarket block, X links + 1–2 drafts (if applicable), optional Civilization transcript line.

**Step 1 guardrail:** Stay read-only — no merge/stage unless they switch lanes or use a pipeline phrase ("we …").

### Step 2 — Multiple choice (required; always A–E)

Immediately **after** Step 1 content, output the fixed **A–E** menu (see [Good morning — multiple choice (A–E required)](#good-morning--multiple-choice-ae-required)). **Do not** omit **E**.

When the operator later sends **A**, **B**, **C**, or **D** (or equivalent), **execute that track** without re-running Step 1 unless they say **good morning** again.

When the operator sends **E** (or “end morning meeting” / clear equivalent): **formally close** the good morning session — short acknowledgment (one or two sentences). **Do not** run Step 1 automated stack on subsequent turns until the next **good morning**. **E is not good night** — no required `operator_handoff_check.py` unless they also invoke **Good night** below.

---

## Good morning — multiple choice (A–E required)

Every **good morning** reply ends **Step 2** with **exactly five options — A through E**. Wording may vary; **roles must not**.

| Letter | Role | What it means when chosen |
|--------|------|---------------------------|
| **A** | **Template audit** | **Grace-mar vs companion-self:** `python scripts/template_diff.py` (see `--help`; default `./companion-self` if cloned beside repo) → refresh [`audit-report.md`](../../../docs/skill-work/work-companion-self/audit-report.md) or `--use-manifest` → [`audit-report-manifest.md`](../../../docs/skill-work/work-companion-self/audit-report-manifest.md). Read [audit-grace-mar-vs-companion-self-template.md](../../../docs/audit-grace-mar-vs-companion-self-template.md), [MERGING-FROM-COMPANION-SELF.md](../../../docs/merging-from-companion-self.md), [work-companion-self/README.md](../../../docs/skill-work/work-companion-self/README.md). |
| **B** | **Boundary audit** | **Leakage / isolation in this repo:** spot-check that **grace-mar** Record/identity is not copied into wrong trees; [audit-boundary-grace-mar-companion-self.md](../../../docs/audit-boundary-grace-mar-companion-self.md), [fork isolation](../../../docs/fork-isolation-and-multi-tenant.md); THINK/WRITE vs WORK — [skills-modularity.md](../../../docs/skills-modularity.md). |
| **C** | **Continue most recent work module** | Resume the **most plausible active WORK lane** — infer from this thread (if obvious), else `users/grace-mar/session-log.md` tail, warmup/Jiang hints, or recent activity in `docs/skill-work/work-*` / `users/grace-mar/work-*.md`. **Label C** with a **concrete guess** (e.g. “continue **work-jiang** transcript queue”); operator may correct. |
| **D** | **System choice (context)** | **One** option chosen from today’s surface: e.g. RECURSION-GATE review, integrity fix, work-dev gap, weekly brief prep, content-queue for `@usa_first_ky` — whatever Step 1 surfaced as highest leverage **that is not** already A/B/C. |
| **E** | **End morning meeting** | **Formally closes** the good morning session (see **Step 2** under [Good morning = start here](#good-morning--start-here-two-steps)). Not handoff / not good night unless they say so separately. |

**Example shape (D filled from context; C shows a guessed lane):**

```markdown
**Good morning — pick one:**
- **A.** Template audit — grace-mar vs companion-self (`template_diff`, audit reports)
- **B.** Boundary audit — leakage / fork isolation / skills-modularity
- **C.** Continue **work-jiang** — chapter queue + Predictive History momentum *(adjust label to match inference)*
- **D.** **Gate review** — clear top pending RECURSION-GATE items *(example only)*
- **E.** **End morning meeting** — close good morning session; normal work until next “good morning”
```

---

## "Good night" = end session here

When the operator says **"good night"**, **"goodnight"**, or clearly the same intent (signing off for the day, closing the session), treat it as a **session end**, not a daily start.

**Do not** run the full [Good morning](#good-morning--start-here-two-steps) stack (no daily brief generation, no Polymarket / Massie X pass, no `operator_daily_warmup.py` / `harness_warmup.py` as the main flow) **unless** they explicitly ask for morning-style output in the same message.

**Do** run the **handoff check** so the next thread can resume cleanly:

```bash
python3 scripts/operator_handoff_check.py -u grace-mar
```

1. **Include the command output** in your reply (paste verbatim or as a fenced markdown block). The script embeds **`## RECURSION-GATE (pending)`** (counts, optional item list, proposed merge steps) and **`## Predictive History — night closeout`** (lane status, tomorrow’s lever, rotating spark, optional `rebuild_all` ritual). Treat merge steps as **guidance only** — no merge without companion approval.
2. Summarize in one short paragraph: what moved today (if known from the thread), what is parked, **gate + Jiang lane** carryovers, and the **suggested re-entry prompt** from the script output.
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
- **Step 2 — A–E menu** (required for “good morning”): fixed **A–E** as in [Good morning — multiple choice (A–E required)](#good-morning--multiple-choice-ae-required)

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
