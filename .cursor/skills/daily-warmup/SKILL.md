---
name: daily-warmup
description: "Grace-Mar operator rhythm. Triggers: good morning, good night, good morning light, good morning minimal, good morning survey. Read-only planning: no merge/stage from warmup; Step 1 = scripts (daily warmup + harness when needed) + branch snapshot only—no Polymarket/poll web/Massie X until operator picks menu E→work-politics or explicitly requests in the same message; survey path skips intel unless asked. Step 2 = fixed A–F; after A–E re-offer full A–F until F. Good night Step 1 = operator_handoff_check.py + summary. Menu letter meanings and cadence live in the skill body."
---

# Daily Warmup

Use this skill at the start of a work block when the operator wants a quick planning pass grounded in repo state.

## Cadence by weekday

Default rhythm (operator can override any day):

| Day | Mode | What to run |
|-----|------|-------------|
| **Monday** | **Full** | Complete [“Good morning”](#good-morning--start-here-two-steps) flow: operator + harness + branch snapshot in Step 1. **Internet intel** (Polymarket, independent polls, Massie X): **not** Step 1 — run on **menu E → work-politics** (full Monday weight) or explicit request. **Daily brief:** **menu C** only. |
| **Tuesday–Friday** | **Lighter** | Same Step 1 as Monday (scripts + branch snapshot). **Polling + Polymarket + Massie X:** only when **E / work-politics** (compact) or explicit request. **Daily brief:** **menu C** only (Step 1 one-lines the path pattern). |
| **Sunday** | **Week ahead (~10 min)** | Not a full good morning. Focus: **FEC / compliance dates** and **voter registration** — use **last on-disk** `daily-brief-*.md` calendar slice if present, else [brief-source-registry.md](../../../docs/skill-work/work-politics/brief-source-registry.md) (`needs_refresh`, `watch`). **Generating** today’s brief remains **menu C**. Optional: skim `pol-pulse` / weekly-brief readiness. |
| **Friday** | **Lighter + post-mortem** | Same as Tue–Fri **plus** two lines at the end of the reply: **(1)** What repeated this week? **(2)** What to drop from the routine? |

If the operator says **“good morning”** on a **Sunday**, default to **week-ahead** mode unless they ask for the full Monday stack. Still run **Step 1** scaled to that mode, then **Step 2** with the full **A–F** menu (labels can be shorter; meanings unchanged).

### Explicit phrases (override default cadence when stated)

**“Good morning light”** (or clear equivalent):

- Run **`operator_daily_warmup.py`** and, when instance state matters, **`harness_warmup.py`**.
- **Internet intel** (Polymarket, polls, Massie X) is **never** Step 1 — same as full good morning; choose **E → work-politics** when you want it (or ask explicitly). **Light** keeps **branch snapshot** compact (one line unless multiple branches).
- **Daily brief:** **do not** generate in Step 1 — one-line pointer to **menu C** and path pattern `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` (e.g. `daily-brief-2026-03-29.md`).
- Deliver a **compact brief** from script outputs + thread context; then **full Step 2 A–F** (do not omit **F**). On later turns, **A–E** executes the track then **re-offers full A–F** until **F**. **Track B:** **compact** repository hygiene (branch + `git status` + one prescribed action or “clean”) — not a full sweep unless the operator asks.

**“Good morning minimal”** (or clear equivalent):

- Run **`harness_warmup.py`** only when instance state matters; **do not** run `operator_daily_warmup.py` unless the operator asks.
- Step 1 has **no** Polymarket / Massie X / poll web search unless the operator **explicitly** asks in the same message. **Daily brief** still **only** via **menu C** (never Step 1).
- Optional **one-line** gate pointer (e.g. pending count from warmup output if already pasted, or “see `users/grace-mar/recursion-gate.md`”).
- Still output **full Step 2 A–F**. On later turns, **A–E** then **re-offer full A–F** until **F** (same as full/light good morning). **Track B:** **minimal** repository hygiene — extend the Step 1 branch line with `git status -sb` + **one** next action (or “clean”); no unrelated sweeps.

**“Good morning survey”** (or **“good morning + survey”** / clear equivalent):

- Run **Step 1** using the same **[cadence by weekday](#cadence-by-weekday)** or **[explicit phrases](#explicit-phrases-override-default-cadence-when-stated)** as if they had said plain **good morning** (they may combine with **good morning light** or **minimal** — apply both: thin work-politics steps *and* survey intent).
- In the **Step 1 warmup brief**, add a short **Companion survey** block (2–4 lines): purpose (IX-B / IX-C refinement), suggested cadence hint (e.g. **monthly micro** 3–5 questions vs **quarterly** deeper pass), pointer that execution is **menu E** (work-politics sub-lane) this session unless they choose another letter first.
- **Step 2** remains the **same fixed A–F** menu (do not drop letters). When the operator chooses **E**, **default** the **work-politics** sub-lane and run **[Companion survey track](#companion-survey-track-good-morning)** for that turn (unless they explicitly steer **E** to work-dev or work-strategy in the same message, e.g. “E work-dev only”).
- **Pipeline:** survey work **stages** `recursion-gate.md` candidates only — **no merge** without companion approval; same rule as the rest of this skill.

---

## "Good morning" = start here (two steps)

When the operator begins with **"good morning"** (or clearly the same intent), treat it as opening a **good morning session**. **Scale Step 1** using **[explicit phrases](#explicit-phrases-override-default-cadence-when-stated)** when the operator used one; otherwise use **[cadence by weekday](#cadence-by-weekday)** (Sunday → week-ahead; Tue–Fri → lighter; Monday → full). **Step 2** (A–F menu) always follows Step 1.

### Multiple good mornings per day (reorientation)

The operator may say **good morning** **more than once per calendar day** whenever they need **reorientation** toward the most productive tasks — not only at literal day start. **Each** new **good morning** runs **Step 1** again (at the cadence or explicit phrase for that message) and starts a **new** A–F cycle. **F** closes only the **current** morning meeting in this thread; it does **not** imply a one-per-day limit.

**Habit (optional):** For a **second or later** pass the same day, **good morning light** / **minimal** shortens scripts and branch snapshot. Plain **good morning** again still **does not** auto-run internet intel in Step 1 — for refreshed markets / Massie X they choose **E → work-politics** (or ask explicitly in the message).

If **good morning** arrives **before** the prior morning session reached **F**, treat it as a **reorientation restart:** run Step 1 again, then offer a fresh A–F (use thread context to label **E** sub-lanes).

### Step 1 — Automated actions (run first; paste outputs)

**Work-jiang (Predictive History) — built-in momentum:** `python3 scripts/operator_daily_warmup.py` now appends **`## Predictive History — morning momentum`** (WORK container, STATUS/CHAPTER-QUEUE nudge, rotating **Spark**, dive links). **Customize sparks** in [`research/external/work-jiang/metadata/warmup-sparks.yaml`](../../../research/external/work-jiang/metadata/warmup-sparks.yaml) (operator voice; day-of-year rotation). Standalone: `python3 scripts/work_jiang/warmup_jiang_pulse.py -u grace-mar`. Context: first curated series **Geo-Strategy**; second **Civilization** — when integrating Civilization transcripts, mention raw pulls under `research/external/youtube-channels/predictive-history/` and [WORKFLOW-transcripts.md](../../../research/external/work-jiang/WORKFLOW-transcripts.md); see `users/grace-mar/work-jiang.md` § Operator schedule.

**Alpha / mastery lens (optional):** If the operator ties the day to **mastery gates**, **2-hour academic ceiling**, or **“Time Back”**, point at [alpha-mastery-adaptation.md](../../../docs/alpha-mastery-adaptation.md) and optional `python3 scripts/good-morning-brief.py` / `reflection-proposals/DAILY-INTENTION-*.md` — design vocabulary, not school product claims.

1. Run **`operator_daily_warmup.py`** and, when instance state matters, **`harness_warmup.py`** (see [Run this first](#run-this-first)).
   - **Ranked morning forks (deterministic, optional paste):** `python3 scripts/suggest_morning_forks.py -u grace-mar` prints the top 3 forks from gate + pipeline-events + self-memory + session-log signals; add `--markdown` or `-o path.md` for doc-shaped output. The same block appears when running `python3 scripts/good-morning-brief.py`. Conventions: [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).
2. **Daily brief (deferred — menu C only):** Do **not** run `generate_work_politics_daily_brief.py` in Step 1. In the reply, **one line**: path `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` (today’s date; stem `daily-brief-`, e.g. `daily-brief-2026-03-29.md`) and **menu C** to **generate** (when missing or refresh requested), complete **§1d** Putin in-file, and summarize. If today’s file **already exists**, naming the path is enough — **no** full brief regen in Step 1.
3. **Polling + Polymarket + web polls + Massie X (deferred — menu E / work-politics):** Do **not** fetch Polymarket, run web search for polls, or run the Massie X skill in Step 1 **unless** the operator’s **same message** explicitly requests that intel (e.g. “good morning + Polymarket” / “run KY-4 markets”) — then run the stack **in Step 1** for that turn. Otherwise **one line** in the warmup reply: e.g. “KY-4 markets + polls + Massie X: choose **E → work-politics**.” When the operator chooses **[E / work-politics](#good-morning--multiple-choice-af-required)** and the track is **not** **[good morning survey](#explicit-phrases-override-default-cadence-when-stated)** defaulting to **[Companion survey](#companion-survey-track-good-morning)** only, run [polling-and-markets.md](../../../docs/skill-work/work-politics/polling-and-markets.md) **and** `.cursor/skills/massie-x-news-search-draft/SKILL.md` — **Monday / full** = full pass; **Tue–Fri** = compact (top story links or one draft) unless the operator asks for more. **Good morning survey** + **E** / work-politics **survey** path: run the **survey** track **without** the Polymarket / poll / Massie web stack **unless** the operator asks for both in that message. Update **`Last checked`** in `polling-and-markets.md` when you materially refresh numbers.
4. **Branch snapshot (operator default):** Run `git status -sb` and `git branch -vv` (read-only). Deliver **one short plain-language block** in the warmup reply: if only `main` (or clean tracking), say **branch hygiene: clean**; if other branches exist, classify **merged/stale vs active** per [git-branch-hygiene.md](../../../docs/skill-work/work-dev/git-branch-hygiene.md) and give **one prescribed action** or **no action**. **Not menu A** — A is template/boundary audit; this is **local git** hygiene only. **Good morning light / minimal:** one line from `git branch -vv` unless multiple non-`main` branches or ambiguous tracking — then the short paragraph.
5. In the reply body, deliver the **warmup brief** (priorities, gate, work-politics, integrity from scripts): **branch snapshot** from step 4, **daily brief** defer line from step 2, **intel defer** line from step 3, optional Civilization transcript line from daily warmup output. **No** Polymarket / poll / Massie blocks in Step 1. **No** standalone **Putin — last 48h** web scan in Step 1 — that runs under **menu C** after the brief exists or is generated.

**Step 1 guardrail:** Stay read-only — no merge/stage unless they switch lanes or use a pipeline phrase ("we …"). **Git branch delete/merge** is not Step 1 — operator executes when ready or chooses **B**.

### Step 2 — Multiple choice (required; always A–F)

Immediately **after** Step 1 content, output the fixed **A–F** menu (see [Good morning — multiple choice (A–F required)](#good-morning--multiple-choice-af-required)). **Do not** omit **F**.

When the operator later sends **A**, **B**, **C**, **D**, or **E** (or equivalent), **execute that track** without re-running Step 1 unless they say **good morning** again. **After** that track’s content, **always output the full A–F morning menu again** (same roles as [Good morning — multiple choice](#good-morning--multiple-choice-af-required)). The good morning session stays **open** until **F** — do not skip the menu on A–E turns.

When the operator sends **F** (or “end morning meeting” / clear equivalent): **formally close** the good morning session — short acknowledgment (one or two sentences). **Do not** run Step 1 automated stack on subsequent turns until the next **good morning** (which may be **later the same day** for reorientation). **F is not good night** — no required `operator_handoff_check.py` unless they also invoke **Good night** below.

---

## Good morning — multiple choice (A–F required)

The **first** good morning reply ends **Step 2** with **exactly six options — A through F**. **Each follow-up** after the operator chooses **A**, **B**, **C**, **D**, or **E** must also end with the **same full A–F menu** (until **F** closes the session). Wording may vary; **roles must not**.

| Letter | Role | What it means when chosen |
|--------|------|---------------------------|
| **A** | **Template + boundary audit** | **Unchanged — combined when A is chosen:** (1) **Template — grace-mar vs companion-self:** `python scripts/template_diff.py` (see `--help`; default `./companion-self` if cloned beside repo) → refresh [`audit-report.md`](../../../docs/skill-work/work-companion-self/audit-report.md) or `--use-manifest` → [`audit-report-manifest.md`](../../../docs/skill-work/work-companion-self/audit-report-manifest.md). Read [audit-grace-mar-vs-companion-self-template.md](../../../docs/audit-grace-mar-vs-companion-self-template.md), [MERGING-FROM-COMPANION-SELF.md](../../../docs/merging-from-companion-self.md), [work-companion-self/README.md](../../../docs/skill-work/work-companion-self/README.md). (2) **Boundary — leakage / isolation:** spot-check that **grace-mar** Record/identity is not copied into wrong trees; [audit-boundary-grace-mar-companion-self.md](../../../docs/audit-boundary-grace-mar-companion-self.md), [fork isolation](../../../docs/fork-isolation-and-multi-tenant.md); THINK/WRITE vs WORK — [skills-modularity.md](../../../docs/skills-modularity.md). Optional: `python3 scripts/validate-integrity.py --user grace-mar` if Step 1 or thread flagged drift (report only unless operator asks to fix). (3) **Required closing — reconciliation code:** per [work-companion-self § Reconciliation code audit](../../../docs/skill-work/work-companion-self/README.md#reconciliation-code-audit-upstream-and-downstream): **Upstream** (grace-mar → companion-self) and **Downstream** (companion-self → grace-mar) bullets with **concrete paths** (scripts, validators, CI, hooks), or **`Reconciliation code: none`** with one-line rationale. |
| **B** | **Repository hygiene** | **Local repo health** when chosen (not menu **A** — A is template / companion-self / fork reconciliation). **Builds on** Step 1 branch snapshot: full pass per [git-branch-hygiene.md](../../../docs/skill-work/work-dev/git-branch-hygiene.md) (merge vs delete vs update from `main`); **`git status -sb`** and **uncommitted grouping** (real work vs runtime junk — align with [handoff-check](../handoff-check/SKILL.md)); optional **`git worktree list`** if multi-tree; **commit / push** plan (read-only unless operator ships); optional **`python3 scripts/refresh_derived_exports.py -u grace-mar`** + **`validate-integrity.py --user grace-mar`** if manifests / PRP / handoff suggest staleness (report only unless they ask to fix). Deliver: **short ordered checklist** + **one** prescribed next action (or “clean / no action”). **Pending RECURSION-GATE candidates** are **not** repository hygiene — use **menu D**. |
| **C** | **Daily brief** | **Only when chosen** — Step 1 **never** runs the generator. **(1) Generate** (when today’s `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` is missing, or the operator asks for refresh in the same message): `python3 scripts/generate_work_politics_daily_brief.py -u grace-mar -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md`. **When C runs:** **Monday / full** cadence → run generator on **C**; **Tue–Fri** → generate if missing, else summarize from disk unless refresh requested. **(2) Putin — last 48 hours:** per [daily-brief-putin-watch.md](../../../docs/skill-work/work-strategy/daily-brief-putin-watch.md) — web scan; **update §1d** (`## 1d. Putin — last 48 hours`) **in the daily brief file** (edit markdown after generation). **(3) Deliver** path + **short summary** + **one** concrete next action suggested by the brief (work-politics / strategy / Jiang hooks as the file surfaces). **Ship:** committing the brief is operator lane. |
| **D** | **RECURSION-GATE** | **`users/grace-mar/recursion-gate.md`** — the **gated pipeline** queue for the Record. Follow [gate-review-pass](../gate-review-pass/SKILL.md): pending vs processed, **top 1–3** items to review first, duplicate/stale hints, escalation signals; optional `python3 scripts/operator_gate_review_pass.py -u grace-mar` when useful. **Read-only** workflow guidance — **no merge** into SELF/EVIDENCE/prompt without companion approval; on approve, operator runs `process_approved_candidates.py` (see AGENTS). Tie in Step 1 / harness gate snapshot when already pasted. **Not** menu **B** (git/export hygiene) or **E** (work-territory recommendations). |
| **E** | **Work-dev *or* work-strategy *or* work-politics — recommendation** | When **E** is chosen, pick **exactly one** sub-lane (state it in the **first line** of the reply; if the operator names one in the same message, follow that). **(1) Work-dev** — `docs/skill-work/work-dev/`: [INTEGRATION-PROGRAM.md](../../../docs/skill-work/work-dev/INTEGRATION-PROGRAM.md), [README.md](../../../docs/skill-work/work-dev/README.md); **read** [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md); **real-time** spot-check of listed sources **only when this sub-lane is chosen** (internet as needed for those sources); deliver **delta** + **one** concrete next step (read-only unless operator ships). **Edits** to `work-dev-sources.md` only with operator approval. **(2) Work-strategy** — `docs/skill-work/work-strategy/`: [STRATEGY.md](../../../docs/skill-work/work-strategy/STRATEGY.md), daily-brief pointers, Putin watch procedure, calendar / synthesis docs as relevant; **one** actionable next step (no extra web sweep unless the operator asks). **(3) Work-politics** — **Internet intel (lazy):** when this sub-lane is chosen **and** the session is **not** executing **only** the [Companion survey](#companion-survey-track-good-morning) track (see survey default below), run **KY-4 Polymarket + independent poll search + Massie X** per [polling-and-markets.md](../../../docs/skill-work/work-politics/polling-and-markets.md) and `.cursor/skills/massie-x-news-search-draft/SKILL.md` (weight per [cadence](#cadence-by-weekday)). Then: brief registry, campaign, queue — **one** actionable next step (**gate** = **menu D**). **[Companion survey](#companion-survey-track-good-morning)** **defaults under E** / **work-politics** when the operator opened with **good morning survey** — run **survey** without the Polymarket / poll / Massie stack unless they ask for intel too. **Not** duplicating **A** / **B** / **C** / **D**. |
| **F** | **End good morning → normal workflow** | **Formally closes** the good morning session (see **Step 2** under [Good morning = start here](#good-morning--start-here-two-steps)). Transition to normal chat/work until the next **good morning**. Not handoff / not good night unless they say so separately. |

**Example shape (E shows chosen sub-lane when picked):**

```markdown
**Good morning — pick one:**
- **A.** Template + boundary audit — `template_diff` / audit reports + leakage / fork isolation / skills-modularity (combined when chosen)
- **B.** **Repository hygiene** — branches, status, commit/push plan, exports/integrity per [git-branch-hygiene.md](../../../docs/skill-work/work-dev/git-branch-hygiene.md) *(checklist + one prescribed action when chosen)*
- **C.** **Daily brief** — generate if needed, **§1d** Putin in-file, summary + one next step *(only when chosen; §1d = web when C runs)*
- **D.** **RECURSION-GATE** — pending queue, review order, gate-review-pass; **no merge** without companion approval
- **E.** **Work-dev *or* work-strategy *or* work-politics** — **one** lane + one recommendation *(work-politics = KY-4 + Polymarket + polls + Massie X **here**, not Step 1; survey-only path skips that stack; work-dev = source spot-check **here** only)*
- **F.** **End good morning** — close session; normal workflow until next “good morning”
```

When the operator chooses **A**, the reply must end the audit section with a **Reconciliation code** block, for example:

```markdown
### Reconciliation code
- **Upstream (grace-mar → companion-self):** *(specific paths + one line each, or “none — …”)*
- **Downstream (companion-self → grace-mar):** *(specific paths + adopt command if any, or “none — …”)*
```

---

## Shared A–C (morning and night)

**Good morning** and **good night** use the **same** meanings for **A**, **B**, and **C**. When the operator chooses **A**, **B**, or **C** during **good night**, execute the same track as the matching row in **[Good morning — multiple choice (A–F required)](#good-morning--multiple-choice-af-required)**.

- **Grounding for B at night:** Use **handoff** output and good night Step 1 **branch snapshot** (you do not re-run morning Step 1).
- **C at night:** Still **only** runs `generate_work_politics_daily_brief.py` + §1d when **C** is chosen — typical use is **catch up or refresh today’s** `daily-brief-YYYY-MM-DD.md` before sign-off.

---

## Shared D (morning and night)

**Good morning** and **good night** use the **same** meaning for **D** — **RECURSION-GATE**. When the operator chooses **D** during **good night**, execute the same track as **[good morning D](#good-morning--multiple-choice-af-required)** (deepen from handoff **`## RECURSION-GATE (pending)`** when helpful).

---

## Companion survey track (good morning)

**When:** Operator chose **good morning E** with **work-politics** sub-lane and the pick is survey — or they began with **[good morning survey](#explicit-phrases-override-default-cadence-when-stated)** and then chose **E** (default survey under **E** / work-politics). **Good night:** survey still available under **night E** (system pick), not under **night A–D**.

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
3. **One short paragraph** after the paste: what moved today (if known from the thread), what is parked, **gate + Jiang** carryovers, and the **suggested re-entry prompt** from the script output. If the thread produced a **repeatable procedure**, add **one optional phrase**: log a line in `skills-portable/skill-candidates.md` or use good night **E** for skill discovery / [extract-skill-from-session](../extract-skill-from-session/SKILL.md) (not Record).
4. If the handoff or thread shows **risky uncommitted noise**, one line distinguishing real work vs runtime junk (see [handoff-check](../handoff-check/SKILL.md)); still **read-only** — no merge, stage, or commit as part of good night **Step 1**.
5. **Branch snapshot (same as good morning step 6):** `git status -sb` and `git branch -vv`; **one plain sentence** if any non-`main` branch exists or tracking looks stale — else **skip** with “branch hygiene: clean.” Prescriptive rules: [git-branch-hygiene.md](../../../docs/skill-work/work-dev/git-branch-hygiene.md). **Not menu A.**

Full spec: [`.cursor/skills/handoff-check/SKILL.md`](../handoff-check/SKILL.md).

### Step 2 — Multiple choice (required; always A–F)

Immediately **after** Step 1, output the fixed **A–F** menu (see [Good night — multiple choice (A–F required)](#good-night--multiple-choice-af-required)). **Do not** omit **F**.

When the operator later sends **A**, **B**, **C**, **D**, or **E** (or equivalent), **execute that track** without re-running **Step 1** (`operator_handoff_check.py`) unless they ask for a **fresh handoff** or say **good night** again. **After** that track’s content, **always output the full A–F night menu again** (same roles as [Good night — multiple choice](#good-night--multiple-choice-af-required)). The good night session stays **open** until **F** — do not skip the menu on A–E turns.

When the operator sends **F** (or “end night session” / clear equivalent): **formally close** the good night session — short acknowledgment (one or two sentences). **Do not** re-run the full good night **Step 1** stack on subsequent turns until the next **good night**. **Next calendar start** for morning automation is **good morning** (not implied by **F**).

**Distinctions**

- **Good morning `F`:** ends the **morning meeting** only; day may continue.
- **Good night `F`:** ends the **day-closeout / night session**; normal chat can continue, but **do not** treat the thread as still “in good night” for rerunning handoff.
- **Good night** is **not** **good morning**; the operator starts the next workday with **good morning** when they want Step 1 morning automation again.

---

## Good night — multiple choice (A–F required)

Every **good night** reply ends **Step 2** with **exactly six options — A through F**. Wording may vary; **roles must not**.

**A–D** match good morning — see **[Shared A–C (morning and night)](#shared-ac-morning-and-night)**, **[Shared D (morning and night)](#shared-d-morning-and-night)**, and the **[good morning table](#good-morning--multiple-choice-af-required)**.

| Letter | Role | What it means when chosen |
|--------|------|---------------------------|
| **A** | **Template + boundary audit** | **Same as good morning A** — [row above](#good-morning--multiple-choice-af-required). |
| **B** | **Repository hygiene** | **Same as good morning B** — [row above](#good-morning--multiple-choice-af-required); ground in **handoff** + good night Step 1 branch snapshot. |
| **C** | **Daily brief** | **Same as good morning C** — [row above](#good-morning--multiple-choice-af-required); generator + §1d **only when chosen** (often today’s file before sign-off). |
| **D** | **RECURSION-GATE** | **Same as good morning D** — [row above](#good-morning--multiple-choice-af-required); use handoff **`## RECURSION-GATE (pending)`** as primary grounding. |
| **E** | **System pick — productive or hygiene** | **Night closeout and extras** — **not** duplicating A–D. **Prefer B** for full repo hygiene, **C** for daily brief, **D** for gate queue review. **Quick boundary / integrity** — fork isolation / leakage or **`validate-integrity.py --user grace-mar`** if handoff flagged drift. **Predictive History night closeout** — act on **`## Predictive History — night closeout`** in handoff (Jiang lane, Spark / `rebuild_all`, pointers to `session-log.md` / `work-jiang.md`). **Also:** work-strategy / work-jiang / work-politics next step without duplicating **D**, **companion survey** ([survey track](#companion-survey-track-good-morning)), commit/push grouping, derived-export refresh, weekly-brief carryover, work-politics / `@usa_first_ky` queue. **Skill discovery** — [skills-portable/skill-candidates.md](../../../skills-portable/skill-candidates.md) (one-line pointer), `skills-portable/_drafts/`, or [extract-skill-from-session](../extract-skill-from-session/SKILL.md) when today’s thread invented a repeatable procedure; not Record, not gate. One clear recommendation + optional “if you only have 5 minutes.” Read-only unless operator asks to implement. |
| **F** | **End night session** | **Formally closes** the good night session (see **Step 2** under [“Good night” = end session here (two steps)](#good-night--end-session-here-two-steps)). Does **not** run morning stack; next **automated** morning block awaits **good morning**. |

**Example shape (E shows one system pick when chosen):**

```markdown
**Good night — pick one:**
- **A.** Template + boundary audit — same as good morning **A** (`template_diff` / audit + reconciliation code when chosen)
- **B.** **Repository hygiene** — same as good morning **B** *(ground in handoff + branch snapshot)*
- **C.** **Daily brief** — same as good morning **C** *(generator + §1d only when chosen)*
- **D.** **RECURSION-GATE** — same as good morning **D** *(handoff gate block + gate-review-pass)*
- **E.** **System pick** — night closeout *(integrity, Jiang handoff block, survey, commit grouping, **skill discovery** / `skill-candidates.md` / extract-skill — fill from handoff; prefer **B** / **C** / **D** when one letter covers the whole job)*
- **F.** **End night session** — close good night; no rerun handoff until next “good night”
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
- **KY-4 + Polymarket + polls + Massie X:** **not** in Step 1 — deliver **only** when **menu E → work-politics** (or explicit same-message request, or Massie X / polling doc run as part of that E turn). See [polling-and-markets.md](../../../docs/skill-work/work-politics/polling-and-markets.md)
- **Daily brief + Putin §1d** (when **menu C** is executed): see [daily-brief-putin-watch.md](../../../docs/skill-work/work-strategy/daily-brief-putin-watch.md); Step 1 does **not** run the brief generator or standalone Putin web scan
- X scan + drafts for `@usa_first_ky`: **only** when Massie X skill runs (**E / work-politics** intel path or explicit request), not Step 1 by default
- **Step 2 — A–F menu** (required for “good morning”): fixed **A–F** as in [Good morning — multiple choice (A–F required)](#good-morning--multiple-choice-af-required)
- **Good night:** handoff script output + summary (**Step 1**), then **Step 2 — A–F** as in [Good night — multiple choice (A–F required)](#good-night--multiple-choice-af-required) (**A–D** same as morning; see [Shared A–C](#shared-ac-morning-and-night) and [Shared D](#shared-d-morning-and-night))

## Guardrails

- This is read-only planning. Do not merge or stage just because the warmup mentions candidates.
- If integrity fails, surface that before optional improvements.
- Treat `users/grace-mar/recursion-gate.md` and `self-evidence.md` as canonical, not the summary.
- **Contextual stewardship:** Agents have no cross-thread institutional memory; authority for the Record is **on-disk files + gated pipeline** — not model recall or chat summary.

## Related files

- `docs/operator-skills.md`
- `docs/skill-work/work-politics/polling-and-markets.md` (KY-4 polling + Polymarket — run on **menu E → work-politics** or explicit request, not Step 1)
- `docs/skill-work/work-politics/workspace.md`
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md` (high-stakes work-politics messaging discipline; weekly brief §8)
