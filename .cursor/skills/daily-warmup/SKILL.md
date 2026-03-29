---
name: daily-warmup
description: Grace-Mar operator rhythm: **Good morning** = Step 1 + Step 2 **A–E** (repeat **good morning** same day OK for reorientation; **E** closes only the current meeting). Morning **A** = template + boundary audit combined; **B** work-dev + [work-dev-sources.md](docs/skill-work/work-dev/work-dev-sources.md); **C** work-strategy / work-jiang / work-politics; **D** system pick (includes optional **companion IX-B / IX-C survey wave** — stage to gate only); **E** end morning → normal workflow. After **A–D**, **re-offer full A–E** until **E**. **Good morning survey** = same Step 1 cadence + brief flags **D** survey track (see § Companion survey). **Good morning light** / **minimal** for lighter repeat passes. **Good night** = Step 1 (`operator_handoff_check.py` + summary) + Step 2 **A–E** (night **A–C** / **E** as before; night **D** = same *system pick — productive or hygiene* style as morning **D**, scoped to handoff/closeout). Good morning **E** is not good night; good night **E** is not the next day’s good morning.
---

# Daily Warmup

Use this skill at the start of a work block when the operator wants a quick planning pass grounded in repo state.

## Cadence by weekday

Default rhythm (operator can override any day):

| Day | Mode | What to run |
|-----|------|-------------|
| **Monday** | **Full** | Complete [“Good morning”](#good-morning--start-here-two-steps) flow: operator + harness, **generate** daily brief, polling + Polymarket, Massie X scan + 1–2 drafts. |
| **Tuesday–Friday** | **Lighter** | `operator_daily_warmup.py` + `harness_warmup.py` (when instance state matters). **Polling + Polymarket** stays (compact). **Daily brief:** generate only if missing for today, else one-line pointer to `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md`. **Massie X:** shorten to **top story links** (or one draft) unless the content queue / news cycle demands more. |
| **Sunday** | **Week ahead (~10 min)** | Not a full good morning. Focus: **FEC / compliance dates** and **voter registration** from the daily brief calendar + [brief-source-registry.md](../../../docs/skill-work/work-politics/brief-source-registry.md) (`needs_refresh`, `watch`). Optional: skim `pol-pulse` / weekly-brief readiness. |
| **Friday** | **Lighter + post-mortem** | Same as Tue–Fri **plus** two lines at the end of the reply: **(1)** What repeated this week? **(2)** What to drop from the routine? |

If the operator says **“good morning”** on a **Sunday**, default to **week-ahead** mode unless they ask for the full Monday stack. Still run **Step 1** scaled to that mode, then **Step 2** with the full **A–E** menu (labels can be shorter; meanings unchanged).

### Explicit phrases (override default cadence when stated)

**“Good morning light”** (or clear equivalent):

- Run **`operator_daily_warmup.py`** and, when instance state matters, **`harness_warmup.py`**.
- **Skip** full **polling + Polymarket** ([polling-and-markets.md](../../../docs/skill-work/work-politics/polling-and-markets.md)) and the **Massie X** skill (`.cursor/skills/massie-x-news-search-draft/SKILL.md`).
- **Daily brief:** same as Tue–Fri — generate only if today’s file is missing; else one-line pointer to `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md`.
- Deliver a **compact brief** from script outputs + thread context; then **full Step 2 A–E** (do not omit **E**). On later turns, **A–D** executes the track then **re-offers full A–E** until **E**. **Track B:** prefer a **lighter** real-time pass over [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md) (e.g. spot-check one or two listed sources) instead of a full sweep.

**“Good morning minimal”** (or clear equivalent):

- Run **`harness_warmup.py`** only when instance state matters; **do not** run `operator_daily_warmup.py` unless the operator asks.
- **Skip** daily brief generation, Polymarket, and Massie X unless explicitly requested.
- Optional **one-line** gate pointer (e.g. pending count from warmup output if already pasted, or “see `users/grace-mar/recursion-gate.md`”).
- Still output **full Step 2 A–E**. On later turns, **A–D** then **re-offer full A–E** until **E** (same as full/light good morning). **Track B:** **do not** run a broad web sweep; give **one** suggested work-dev next step from repo context + a **single** optional real-time check if the operator later chooses **B**.

**“Good morning survey”** (or **“good morning + survey”** / clear equivalent):

- Run **Step 1** using the same **[cadence by weekday](#cadence-by-weekday)** or **[explicit phrases](#explicit-phrases-override-default-cadence-when-stated)** as if they had said plain **good morning** (they may combine with **good morning light** or **minimal** — apply both: thin work-politics steps *and* survey intent).
- In the **Step 1 warmup brief**, add a short **Companion survey** block (2–4 lines): purpose (IX-B / IX-C refinement), suggested cadence hint (e.g. **monthly micro** 3–5 questions vs **quarterly** deeper pass), pointer that execution is **menu D** this session unless they choose another letter first.
- **Step 2** remains the **same fixed A–E** menu (do not add letters). When the operator chooses **D**, run **[Companion survey track](#companion-survey-track-good-morning)** as the **D** track for that turn (unless they explicitly steer D to something else in the same message, e.g. “D but gate review only”).
- **Pipeline:** survey work **stages** `recursion-gate.md` candidates only — **no merge** without companion approval; same rule as the rest of this skill.

---

## "Good morning" = start here (two steps)

When the operator begins with **"good morning"** (or clearly the same intent), treat it as opening a **good morning session**. **Scale Step 1** using **[explicit phrases](#explicit-phrases-override-default-cadence-when-stated)** when the operator used one; otherwise use **[cadence by weekday](#cadence-by-weekday)** (Sunday → week-ahead; Tue–Fri → lighter; Monday → full). **Step 2** (A–E menu) always follows Step 1.

### Multiple good mornings per day (reorientation)

The operator may say **good morning** **more than once per calendar day** whenever they need **reorientation** toward the most productive tasks — not only at literal day start. **Each** new **good morning** runs **Step 1** again (at the cadence or explicit phrase for that message) and starts a **new** A–E cycle. **E** closes only the **current** morning meeting in this thread; it does **not** imply a one-per-day limit.

**Habit (optional):** For a **second or later** pass the same day when heavy intel was already run, the operator can say **good morning light** or **good morning minimal** to skip or shorten Polymarket, Putin, and Massie X while still refreshing `operator_daily_warmup.py` / `harness_warmup.py` (when used) and the A–E menu. If they use plain **good morning** again, run Step 1 at full cadence for that day — they may want refreshed markets and scans.

If **good morning** arrives **before** the prior morning session reached **E**, treat it as a **reorientation restart:** run Step 1 again, then offer a fresh A–E (use thread context to label B/C/D).

### Step 1 — Automated actions (run first; paste outputs)

**Work-jiang (Predictive History) — built-in momentum:** `python3 scripts/operator_daily_warmup.py` now appends **`## Predictive History — morning momentum`** (WORK container, STATUS/CHAPTER-QUEUE nudge, rotating **Spark**, dive links). **Customize sparks** in [`research/external/work-jiang/metadata/warmup-sparks.yaml`](../../../research/external/work-jiang/metadata/warmup-sparks.yaml) (operator voice; day-of-year rotation). Standalone: `python3 scripts/work_jiang/warmup_jiang_pulse.py -u grace-mar`. Context: first curated series **Geo-Strategy**; second **Civilization** — when integrating Civilization transcripts, mention raw pulls under `research/external/youtube-channels/predictive-history/` and [WORKFLOW-transcripts.md](../../../research/external/work-jiang/WORKFLOW-transcripts.md); see `users/grace-mar/work-jiang.md` § Operator schedule.

**Alpha / mastery lens (optional):** If the operator ties the day to **mastery gates**, **2-hour academic ceiling**, or **“Time Back”**, point at [alpha-mastery-adaptation.md](../../../docs/alpha-mastery-adaptation.md) and optional `python3 scripts/good-morning-brief.py` / `reflection-proposals/DAILY-INTENTION-*.md` — design vocabulary, not school product claims.

1. Run **`operator_daily_warmup.py`** and, when instance state matters, **`harness_warmup.py`** (see [Run this first](#run-this-first)).
   - **Ranked morning forks (deterministic, optional paste):** `python3 scripts/suggest_morning_forks.py -u grace-mar` prints the top 3 forks from gate + pipeline-events + self-memory + session-log signals; add `--markdown` or `-o path.md` for doc-shaped output. The same block appears when running `python3 scripts/good-morning-brief.py`. Conventions: [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).
2. **Daily brief:** Per cadence — **Monday / full day:** generate today’s file:
   ```bash
   python3 scripts/generate_work_politics_daily_brief.py -u grace-mar -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md
   ```
   **Tue–Fri (lighter):** generate only if missing for today; else one-line pointer to `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md`. **Sunday (week-ahead):** lean on calendar + brief-source-registry; brief step optional/minimal.
3. **Polling + prediction markets:** Follow [polling-and-markets.md](../../../docs/skill-work/work-politics/polling-and-markets.md). **Fetch** the two canonical Polymarket pages (KY-04 GOP primary + GE party); **search** for independent public horserace polls (Massie vs Gallrein) in the last ~30 days. **Compact block:** implied probabilities + **volume**, named poll **or** “no independent poll found,” **one-line caveat**, URLs. Update **`Last checked`** in that doc when you materially refresh numbers.
4. **Putin — last 48 hours:** Follow [daily-brief-putin-watch.md](../../../docs/skill-work/work-strategy/daily-brief-putin-watch.md). **Web scan** Kremlin events/transcripts plus major wires; **compact block** (bullets + URLs) in the reply. Target paste: generated daily brief **§1d** (`## 1d. Putin — last 48 hours`). **Good morning light / minimal:** include only if the operator asked for full morning intel or strategy/geo lane; otherwise one line pointing at §1d procedure.
5. **Massie X:** Run `.cursor/skills/massie-x-news-search-draft/SKILL.md` (full or shortened per cadence): web scan + latest X posts; **draft-only** posts for `@usa_first_ky`.
6. In the reply body, deliver the **warmup brief** (priorities, gate, work-politics, integrity): daily-brief path + summary, polling + Polymarket block, **Putin 48h block**, X links + 1–2 drafts (if applicable), optional Civilization transcript line.

**Step 1 guardrail:** Stay read-only — no merge/stage unless they switch lanes or use a pipeline phrase ("we …").

### Step 2 — Multiple choice (required; always A–E)

Immediately **after** Step 1 content, output the fixed **A–E** menu (see [Good morning — multiple choice (A–E required)](#good-morning--multiple-choice-ae-required)). **Do not** omit **E**.

When the operator later sends **A**, **B**, **C**, or **D** (or equivalent), **execute that track** without re-running Step 1 unless they say **good morning** again. **After** that track’s content, **always output the full A–E morning menu again** (same roles as [Good morning — multiple choice](#good-morning--multiple-choice-ae-required)). The good morning session stays **open** until **E** — do not skip the menu on A–D turns.

When the operator sends **E** (or “end morning meeting” / clear equivalent): **formally close** the good morning session — short acknowledgment (one or two sentences). **Do not** run Step 1 automated stack on subsequent turns until the next **good morning** (which may be **later the same day** for reorientation). **E is not good night** — no required `operator_handoff_check.py` unless they also invoke **Good night** below.

---

## Good morning — multiple choice (A–E required)

The **first** good morning reply ends **Step 2** with **exactly five options — A through E**. **Each follow-up** after the operator chooses **A**, **B**, **C**, or **D** must also end with the **same full A–E menu** (until **E** closes the session). Wording may vary; **roles must not**.

| Letter | Role | What it means when chosen |
|--------|------|---------------------------|
| **A** | **Template + boundary audit** | **Unchanged — combined when A is chosen:** (1) **Template — grace-mar vs companion-self:** `python scripts/template_diff.py` (see `--help`; default `./companion-self` if cloned beside repo) → refresh [`audit-report.md`](../../../docs/skill-work/work-companion-self/audit-report.md) or `--use-manifest` → [`audit-report-manifest.md`](../../../docs/skill-work/work-companion-self/audit-report-manifest.md). Read [audit-grace-mar-vs-companion-self-template.md](../../../docs/audit-grace-mar-vs-companion-self-template.md), [MERGING-FROM-COMPANION-SELF.md](../../../docs/merging-from-companion-self.md), [work-companion-self/README.md](../../../docs/skill-work/work-companion-self/README.md). (2) **Boundary — leakage / isolation:** spot-check that **grace-mar** Record/identity is not copied into wrong trees; [audit-boundary-grace-mar-companion-self.md](../../../docs/audit-boundary-grace-mar-companion-self.md), [fork isolation](../../../docs/fork-isolation-and-multi-tenant.md); THINK/WRITE vs WORK — [skills-modularity.md](../../../docs/skills-modularity.md). Optional: `python3 scripts/validate-integrity.py --user grace-mar` if Step 1 or thread flagged drift (report only unless operator asks to fix). (3) **Required closing — reconciliation code:** per [work-companion-self § Reconciliation code audit](../../../docs/skill-work/work-companion-self/README.md#reconciliation-code-audit-upstream-and-downstream): **Upstream** (grace-mar → companion-self) and **Downstream** (companion-self → grace-mar) bullets with **concrete paths** (scripts, validators, CI, hooks), or **`Reconciliation code: none`** with one-line rationale. |
| **B** | **Work-dev — next step + sources refresh** | **Territory:** `docs/skill-work/work-dev/` (integration / OpenClaw / export–stage–merge rhythm — [INTEGRATION-PROGRAM.md](../../../docs/skill-work/work-dev/INTEGRATION-PROGRAM.md), [README.md](../../../docs/skill-work/work-dev/README.md)). **Always read** [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md) (authorized channel/podcast list). **Real-time search / fetch:** web-check listed sources (home pages, recent posts, “still active”) so the operator sees **current** signal, not only disk. Deliver: **(1)** short **delta** vs what the doc implies (stale URL, renamed show, one-line per notable change), **(2)** **one** concrete **suggested next step** (e.g. run export script, update a doc row, open a staging checklist — read-only unless operator switches to ship). **Edits** to `work-dev-sources.md` only when the operator approves implementation. |
| **C** | **Work-strategy / work-jiang / work-politics — next step** | Pick **exactly one** lane by leverage from Step 1 + thread + `users/grace-mar/session-log.md` / `work-*.md`: **work-strategy** (`docs/skill-work/work-strategy/` — daily brief, Putin watch, calendar), **work-jiang** (`research/external/work-jiang/`, `users/grace-mar/work-jiang.md`, Predictive History), or **work-politics** (`docs/skill-work/work-politics/` — polling, brief registry, campaign, Massie X queue). **State which lane** in the first line, then **one** actionable next step (read-only unless operator ships). |
| **D** | **System pick — productive or hygiene** | **Not** repeating A/B/C: the single best **alternative** next move from repo state — e.g. RECURSION-GATE review ([gate-review-pass](../gate-review-pass/SKILL.md)), `validate-integrity.py`, commit/push grouping, weekly-brief prep, derived-export refresh, worktree noise triage, content-queue hygiene, or **[companion IX-B / IX-C survey wave](#companion-survey-track-good-morning)** (questions + gate drafts, merge only after companion approve). If the operator opened with **good morning survey**, **default D** to the companion survey track unless a higher-urgency hygiene item (e.g. integrity failure) clearly wins. One clear recommendation + optional second line “if you only have 5 minutes.” Read-only unless operator asks to implement. |
| **E** | **End good morning → normal workflow** | **Formally closes** the good morning session (see **Step 2** under [Good morning = start here](#good-morning--start-here-two-steps)). Transition to normal chat/work until the next **good morning**. Not handoff / not good night unless they say so separately. |

**Example shape (B/C/D show inferred labels; adjust each turn):**

```markdown
**Good morning — pick one:**
- **A.** Template + boundary audit — `template_diff` / audit reports + leakage / fork isolation / skills-modularity (combined when chosen)
- **B.** Work-dev — next step + **real-time** pass on [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md) *(name the suggested step after you choose B)*
- **C.** **Work-jiang** — next step *(or work-strategy / work-politics — one lane only when chosen)*
- **D.** **System pick** — e.g. gate review, integrity, repo hygiene, or **companion survey** (IX-B / IX-C → gate drafts) *(fill from state when chosen; [survey track](#companion-survey-track-good-morning) when “good morning survey” or operator picks survey under D)*
- **E.** **End good morning** — close session; normal workflow until next “good morning”
```

When the operator chooses **A**, the reply must end the audit section with a **Reconciliation code** block, for example:

```markdown
### Reconciliation code
- **Upstream (grace-mar → companion-self):** *(specific paths + one line each, or “none — …”)*
- **Downstream (companion-self → grace-mar):** *(specific paths + adopt command if any, or “none — …”)*
```

---

## Companion survey track (good morning)

**When:** Operator chose **D** and the system pick is survey, or they began with **[good morning survey](#explicit-phrases-override-default-cadence-when-stated)** and then chose **D** (or steered **D** to survey).

**Goal:** Refresh **self-curiosity (IX-B)** and **self-personality (IX-C)** on a **cadence** (typical: **monthly micro** 3–5 questions, or **quarterly** longer refinement), without bypassing the gated pipeline.

**Operator / agent actions (read-only unless operator switches to ship):**

1. **Scope** — Pick one wave type: **micro** (few questions, one candidate per answer cluster) vs **theme** (one candidate synthesizing a short battery). Prefer **split candidates** (one mergeable gate block per theme) like the Abigail refinement pattern: `CANDIDATE-0092`–`0097`-style rows in `users/grace-mar/recursion-gate.md` (survey_log in `source_exchange`, `new_vs_record` filled, `channel_key` e.g. `operator:cursor` or `telegram:…`).
2. **Grounding** — Each staged block must carry **literal companion answers** (or transcript pointer) under `source_exchange`; no inferred facts beyond the log (see `recursion-gate.md` merge checklist + AGENTS gated pipeline).
3. **Draft** — Output **ready-to-paste YAML blocks** with `status: pending` for operator/companion review; or, if operator pastes a `survey_log`, map Q clusters → candidates with `suggested_entry` / `prompt_addition` aligned to IX-B vs IX-C.
4. **Close the loop** — Optionally suggest **one** `suggested_followup` the Voice or parent can try in real life after merges (stored in candidate YAML); optional one-line note in `session-log.md` only if operator asks to record the run.
5. **Merge** — Companion **approve** in gate → operator runs `python3 scripts/process_approved_candidates.py -u grace-mar --quick CANDIDATE-XXXX --approved-by companion` (or receipt flow). **Agent does not merge** without approval.

**Cadence hint for Step 1:** If helpful, mention “last survey wave” from recent **Processed** blocks or session memory — optional; do not block the track if unknown.

---

## "Good night" = end session here (two steps)

When the operator says **"good night"**, **"goodnight"**, or clearly the same intent (signing off for the day, closing the session), treat it as opening a **good night session** — **not** a daily start.

**Do not** run the full [Good morning](#good-morning--start-here-two-steps) **Step 1** stack (no daily brief generation, no Polymarket / Massie X pass, no `operator_daily_warmup.py` / `harness_warmup.py` as the main flow) **unless** they explicitly ask for morning-style output in the same message.

### Step 1 — Automated actions (handoff; paste output)

1. Run the **handoff check** so the next thread can resume cleanly:

   ```bash
   python3 scripts/operator_handoff_check.py -u grace-mar
   ```

2. **Include the command output** in your reply (paste verbatim or as a fenced markdown block). The script embeds **`## RECURSION-GATE (pending)`** (counts, optional item list, proposed merge steps) and **`## Predictive History — night closeout`** (lane status, tomorrow’s lever, rotating spark, optional `rebuild_all` ritual). Treat merge steps as **guidance only** — no merge without companion approval.
3. **One short paragraph** after the paste: what moved today (if known from the thread), what is parked, **gate + Jiang** carryovers, and the **suggested re-entry prompt** from the script output.
4. If the handoff or thread shows **risky uncommitted noise**, one line distinguishing real work vs runtime junk (see [handoff-check](../handoff-check/SKILL.md)); still **read-only** — no merge, stage, or commit as part of good night **Step 1**.

Full spec: [`.cursor/skills/handoff-check/SKILL.md`](../handoff-check/SKILL.md).

### Step 2 — Multiple choice (required; always A–E)

Immediately **after** Step 1, output the fixed **A–E** menu (see [Good night — multiple choice (A–E required)](#good-night--multiple-choice-ae-required)). **Do not** omit **E**.

When the operator later sends **A**, **B**, **C**, or **D** (or equivalent), **execute that track** without re-running **Step 1** (`operator_handoff_check.py`) unless they ask for a **fresh handoff** or say **good night** again. **After** that track’s content, **always output the full A–E night menu again** (same roles as [Good night — multiple choice](#good-night--multiple-choice-ae-required)). The good night session stays **open** until **E** — do not skip the menu on A–D turns.

When the operator sends **E** (or “end night session” / clear equivalent): **formally close** the good night session — short acknowledgment (one or two sentences). **Do not** re-run the full good night **Step 1** stack on subsequent turns until the next **good night**. **Next calendar start** for morning automation is **good morning** (not implied by **E**).

**Distinctions**

- **Good morning `E`:** ends the **morning meeting** only; day may continue.
- **Good night `E`:** ends the **day-closeout / night session**; normal chat can continue, but **do not** treat the thread as still “in good night” for rerunning handoff.
- **Good night** is **not** **good morning**; the operator starts the next workday with **good morning** when they want Step 1 morning automation again.

---

## Good night — multiple choice (A–E required)

Every **good night** reply ends **Step 2** with **exactly five options — A through E**. Wording may vary; **roles must not**.

| Letter | Role | What it means when chosen |
|--------|------|---------------------------|
| **A** | **Gate — tomorrow first** | Deepen **RECURSION-GATE** from handoff output: top **1–3** pending items, suggested **review order** for next session, pointer to `operator_gate_review_pass` / in-file approve → `process_approved_candidates.py` — **read-only** reminders; **no merge** without companion approval. |
| **B** | **Boundary / integrity** | Quick pass: **fork isolation** / leakage ([audit-boundary-grace-mar-companion-self.md](../../../docs/audit-boundary-grace-mar-companion-self.md)) or run **`python3 scripts/validate-integrity.py --user grace-mar`** (or `--json`) if handoff or thread flagged drift; report only unless operator asks to fix. |
| **C** | **Night closeout lane** | Act on **`## Predictive History — night closeout`** from handoff: Jiang lane rest position, **Spark** / `rebuild_all` ritual if relevant, optional pointer to `users/grace-mar/session-log.md` or `work-jiang.md` for tomorrow — still **not** Record merge unless pipeline invoked. |
| **D** | **System pick — productive or hygiene** | **Same style as good morning D**, night-scoped: the single best **alternative** closeout move from handoff + thread **that is not** already A/B/C — e.g. **commit / push hygiene** (grouping, what to commit vs ignore, push caution), **derived-export refresh** (`refresh_derived_exports.py` + integrity), **weekly-brief** carryover for tomorrow, **work-politics** inbox or `@usa_first_ky` draft queue for morning, **light gate queue skim** only if **A** was not chosen and handoff still warrants a non-deep ordering note. One clear recommendation + optional “if you only have 5 minutes.” Read-only unless operator asks to implement. |
| **E** | **End night session** | **Formally closes** the good night session (see **Step 2** under [“Good night” = end session here (two steps)](#good-night--end-session-here-two-steps)). Does **not** run morning stack; next **automated** morning block awaits **good morning**. |

**Example shape (D shows one system pick when chosen):**

```markdown
**Good night — pick one:**
- **A.** Gate — tomorrow first (top pending + review order; merge = companion approval only)
- **B.** Boundary / integrity — quick isolation check or `validate-integrity.py`
- **C.** Night closeout — work-jiang / Predictive History carryover from handoff block
- **D.** **System pick** — productive or hygiene *(e.g. commit/push grouping, derived exports, morning draft queue — fill from handoff when chosen)*
- **E.** **End night session** — close good night; no rerun handoff until next “good night”
```

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
- **Putin — last 48 hours** (required for full “good morning”; optional for **good morning light** per Step 1 §4): see [daily-brief-putin-watch.md](../../../docs/skill-work/work-strategy/daily-brief-putin-watch.md)
- X scan top links + 1–2 draft post candidates for `@usa_first_ky` (draft-only; required when running the Massie X skill step)
- **Step 2 — A–E menu** (required for “good morning”): fixed **A–E** as in [Good morning — multiple choice (A–E required)](#good-morning--multiple-choice-ae-required)
- **Good night:** handoff script output + summary (**Step 1**), then **Step 2 — A–E** as in [Good night — multiple choice (A–E required)](#good-night--multiple-choice-ae-required)

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
