---
name: coffee
preferred_activation: coffee
description: "Grace-Mar operator cadence and tempo. Primary trigger: coffee (modifiers: coffee light, minimal, survey; legacy hey still works). Work-start coffee: Step 1 = operator_daily_warmup + harness + branch snapshot. Closeout coffee (signing off in same message): Step 1 = operator_handoff_check + summary + branch snapshot. Read-only planning; Step 2 = fixed A–H menu. Concrete work-lane picks exit to normal workflow by default. G = work-jiang/PH; H = skills/meta."
---

# Coffee

**Preferred activation (operator):** say **`coffee`**. Legacy **`hey`** still works as a compatibility alias, but **`coffee`** is the canonical trigger now. **Work-start** vs **closeout** is **intent in the same message** (e.g. reorientation vs signing off), not a second trigger phrase, one skill and two Step 1 shapes.

Use this skill when the operator wants a **paced** work block: repo-grounded snapshot, fixed **A–H** menu, and weekday-aware **cadence** (tempo), not ad-hoc drift.

### Session trail (optional — **`coffee`** is the trigger)

Sessions begin when the operator says **`coffee`** (optional modifiers: **`coffee light`**, **`coffee minimal`**, **`coffee survey`**). Legacy **`hey`**, **`hey light`**, **`hey minimal`**, and **`hey survey`** still invoke the same skill. To keep a trail: use **`users/<id>/session-transcript.md`** (raw continuity; **`log_operator_choice.py`** for **`[WORK-choice]`** menu picks) and/or append dated bullets to the relevant **`docs/skill-work/work-*/*-history.md`** files per [work-modules-history-principle.md](../../../docs/skill-work/work-modules-history-principle.md). **Not** the gated Record; **not** [`self-memory`](../../../users/grace-mar/self-memory.md). See [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).

## Cadence by weekday

Default rhythm (operator can override any day):

| Day | Mode | What to run |
|-----|------|-------------|
| **Monday** | **Full** | Complete [“Coffee”](#coffee--start-here-two-steps) flow: operator + harness + branch snapshot in Step 1. **Internet intel** (Polymarket, independent polls, Massie X): **not** Step 1 — run on **menu E → work-politics** (full Monday weight) or explicit request. **Daily brief:** **menu C** only. |
| **Tuesday–Friday** | **Lighter** | Same Step 1 as Monday (scripts + branch snapshot). **Polling + Polymarket + Massie X:** only when **E / work-politics** (compact) or explicit request. **Daily brief:** **menu C** only (Step 1 one-lines the path pattern). |
| **Sunday** | **Week ahead (~10 min)** | Lighter coffee (week-ahead focus, not Monday-full). Focus: **FEC / compliance dates** and **voter registration** — use **last on-disk** `daily-brief-*.md` calendar slice if present, else [brief-source-registry.md](../../../docs/skill-work/work-politics/brief-source-registry.md) (`needs_refresh`, `watch`). **Generating** today’s brief remains **menu C**. Optional: skim `pol-pulse` / weekly-brief readiness. |
| **Friday** | **Lighter + post-mortem** | Same as Tue–Fri **plus** two lines at the end of the reply: **(1)** What repeated this week? **(2)** What to drop from the routine? |

If the operator says **`coffee`** on a **Sunday** (or legacy **`hey`**), default to **week-ahead** mode unless they ask for the full Monday stack. Still run **Step 1** scaled to that mode, then **Step 2** with the full **A–H** menu (labels can be shorter; meanings unchanged).

### Explicit phrases (override default cadence when stated)

**`coffee light`** (or clear equivalent; legacy **`hey light`** still works):

- Run **`operator_daily_warmup.py`** and, when instance state matters, **`harness_warmup.py`**.
- **Internet intel** (Polymarket, polls, Massie X) is **never** Step 1 — same as full coffee; choose **E → work-politics** when you want it (or ask explicitly). **Light** keeps **branch snapshot** compact (one line unless multiple branches).
- **Daily brief:** **do not** generate in Step 1 — one-line pointer to **menu C** and path pattern `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` (e.g. `daily-brief-2026-03-29.md`).
- Deliver a **compact brief** from script outputs + thread context; then **full Step 2 A–H** (do not omit **F**). On later turns, **A, B, C, D, or H** re-offer the full menu unless the operator says otherwise; **E** (with a concrete sub-lane) and **G** exit to normal workflow by default after the reply. **Track B:** **compact** repository hygiene (branch + `git status` + one prescribed action or “clean”) — not a full sweep unless the operator asks.

**`coffee minimal`** (or clear equivalent; legacy **`hey minimal`** still works):

- Run **`harness_warmup.py`** only when instance state matters; **do not** run `operator_daily_warmup.py` unless the operator asks.
- Step 1 has **no** Polymarket / Massie X / poll web search unless the operator **explicitly** asks in the same message. **Daily brief** still **only** via **menu C** (never Step 1).
- Optional **one-line** gate pointer (e.g. pending count from warmup output if already pasted, or “see `users/grace-mar/recursion-gate.md`”).
- Still output **full Step 2 A–H**. On later turns, **A, B, C, D, or H** re-offer the full menu unless the operator says otherwise; **E** (with a concrete sub-lane) and **G** exit to normal workflow by default after the reply. **Track B:** **minimal** repository hygiene — extend the Step 1 branch line with `git status -sb` + **one** next action (or “clean”); no unrelated sweeps.

**`coffee survey`** (or **`coffee + survey`** / clear equivalent; legacy **`hey survey`** still works):

- Run **Step 1** using the same **[cadence by weekday](#cadence-by-weekday)** or **[explicit phrases](#explicit-phrases-override-default-cadence-when-stated)** as if they had said plain **coffee** (they may combine with **coffee light** or **minimal** — apply both: thin work-politics steps *and* survey intent).
- In the **Step 1 warmup brief**, add a short **Companion survey** block (2–4 lines): purpose (IX-B / IX-C refinement), suggested cadence hint (e.g. **monthly micro** 3–5 questions vs **quarterly** deeper pass), pointer that execution is **menu E** (work-politics sub-lane) this session unless they choose another letter first.
- **Step 2** remains the **same fixed A–H** menu (do not drop letters). When the operator chooses **E**, **default** the **work-politics** sub-lane and run **[Companion survey track](#companion-survey-track-coffee)** for that turn (unless they explicitly steer **E** to work-dev or work-strategy in the same message, e.g. “E work-dev only”). After the survey turn, exit to normal workflow by default unless the operator says **`stay in coffee`**.
- **Pipeline:** survey work **stages** `recursion-gate.md` candidates only — **no merge** without companion approval; same rule as the rest of this skill.

---

<a id="coffee--start-here-two-steps"></a>

## "Coffee" = start here (two steps)

When the operator begins with **`coffee`** (or clearly the same intent; legacy **`hey`** still counts), treat it as opening a **coffee session**. If the message **clearly means closeout** (signing off, end of session, wrapping the day, etc.), skip ahead to **[Coffee — closeout](#coffee-closeout-session-end)** — **Step 1** there is handoff-first. Otherwise **scale work-start Step 1** using **[explicit phrases](#explicit-phrases-override-default-cadence-when-stated)** when the operator used one, or **[cadence by weekday](#cadence-by-weekday)** (Sunday → week-ahead; Tue–Fri → lighter; Monday → full). **Step 2** (A–H menu) always follows Step 1.

### Multiple coffees per day (reorientation)

The operator may say **`coffee`** **more than once per calendar day** whenever they need **reorientation** toward the most productive tasks — not only at literal day start. **Each** new **coffee** runs **Step 1** again (at the cadence or explicit phrase for that message) and starts a **new** A–H cycle. **F** closes only the **current** coffee session in this thread; it does **not** imply a one-per-day limit.

**Habit (optional):** For a **second or later** pass the same day, **`coffee light`** / **minimal** shortens scripts and branch snapshot. Plain **`coffee`** again still **does not** auto-run internet intel in Step 1 — for refreshed markets / Massie X they choose **E → work-politics** (or ask explicitly in the message).

If **`coffee`** (or legacy **`hey`**) arrives **before** the prior coffee session reached **F**, treat it as a **reorientation restart:** run Step 1 again, then offer a fresh A–H menu (use thread context to label **E** sub-lanes).

### Step 1 — Automated actions (run first; paste outputs)

**Work-jiang (Predictive History) — built-in momentum:** `python3 scripts/operator_daily_warmup.py` now appends **`## Predictive History — morning momentum`** (WORK container, STATUS/CHAPTER-QUEUE nudge, rotating **Spark**, dive links). **Customize sparks** in [`research/external/work-jiang/metadata/warmup-sparks.yaml`](../../../research/external/work-jiang/metadata/warmup-sparks.yaml) (operator voice; day-of-year rotation). Standalone: `python3 scripts/work_jiang/warmup_jiang_pulse.py -u grace-mar`. Context: first curated series **Geo-Strategy**; second **Civilization** — when integrating Civilization transcripts, mention raw pulls under `research/external/youtube-channels/predictive-history/` and [WORKFLOW-transcripts.md](../../../research/external/work-jiang/WORKFLOW-transcripts.md); see `users/grace-mar/work-jiang.md` § Operator schedule.

**Alpha / mastery lens (optional):** If the operator ties the day to **mastery gates**, **2-hour academic ceiling**, or **“Time Back”**, point at [alpha-mastery-adaptation.md](../../../docs/alpha-mastery-adaptation.md) and optional `python3 scripts/good-morning-brief.py` / `reflection-proposals/DAILY-INTENTION-*.md` — design vocabulary, not school product claims.

1. Run **`operator_daily_warmup.py`** and, when instance state matters, **`harness_warmup.py`** (see [Run this first](#run-this-first)).
   - **Ranked morning forks (deterministic, optional paste):** `python3 scripts/suggest_morning_forks.py -u grace-mar` prints the top 3 forks from gate + pipeline-events + self-memory + session-log signals; add `--markdown` or `-o path.md` for doc-shaped output. The same block appears when running `python3 scripts/good-morning-brief.py`. Conventions: [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).
2. **Daily brief (deferred — menu C only):** Do **not** run `generate_work_politics_daily_brief.py` in Step 1. In the reply, **one line**: path `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` (today’s date; stem `daily-brief-`, e.g. `daily-brief-2026-03-29.md`) and **menu C** to **generate** (when missing or refresh requested), complete **§1d** Putin in-file, and summarize. If today’s file **already exists**, naming the path is enough — **no** full brief regen in Step 1.
3. **Polling + Polymarket + web polls + Massie X (deferred — menu E / work-politics):** Do **not** fetch Polymarket, run web search for polls, or run the Massie X skill in Step 1 **unless** the operator’s **same message** explicitly requests that intel (e.g. “coffee + Polymarket” / “run KY-4 markets”) — then run the stack **in Step 1** for that turn. Otherwise **one line** in the warmup reply: e.g. “KY-4 markets + polls + Massie X: choose **E → work-politics**.” When the operator chooses **[E / work-politics](#coffee--multiple-choice-ah-required)** and the track is **not** **[coffee survey](#explicit-phrases-override-default-cadence-when-stated)** defaulting to **[Companion survey](#companion-survey-track-coffee)** only, run [polling-and-markets.md](../../../docs/skill-work/work-politics/polling-and-markets.md) **and** `.cursor/skills/politics-massie/SKILL.md` — **Monday / full** = full pass; **Tue–Fri** = compact (top story links or one draft) unless the operator asks for more. **Coffee survey** + **E** / work-politics **survey** path: run the **survey** track **without** the Polymarket / poll / Massie web stack **unless** the operator asks for both in that message. Update **`Last checked`** in `polling-and-markets.md` when you materially refresh numbers.
4. **Branch snapshot (operator default):** Run `git status -sb` and `git branch -vv` (read-only). Deliver **one short plain-language block** in the warmup reply: if only `main` (or clean tracking), say **branch hygiene: clean**; if other branches exist, classify **merged/stale vs active** per [git-branch-hygiene.md](../../../docs/skill-work/work-dev/git-branch-hygiene.md) and give **one prescribed action** or **no action**. **Not menu A** — A is template/boundary audit; this is **local git** hygiene only. **Coffee light / minimal:** one line from `git branch -vv` unless multiple non-`main` branches or ambiguous tracking — then the short paragraph.
5. In the reply body, deliver the **warmup brief** (priorities, gate, work-politics, integrity from scripts): **branch snapshot** from step 4, **daily brief** defer line from step 2, **intel defer** line from step 3, optional Civilization transcript line from `operator_daily_warmup` output. **No** Polymarket / poll / Massie blocks in Step 1. **No** standalone **Putin — last 48h** web scan in Step 1 — that runs under **menu C** after the brief exists or is generated.

**Step 1 guardrail:** Stay read-only — no merge/stage unless they switch lanes or use a pipeline phrase ("we …"). **Git branch delete/merge** is not Step 1 — operator executes when ready or chooses **B**.

### Step 2 — Multiple choice (required; always A–H)

Immediately **after** Step 1 content, output the fixed **A–H** menu (see [Coffee — multiple choice (A–H required)](#coffee--multiple-choice-ah-required)). **List order:** **A, B, C, D, E, G, H, F** so **F** (end session) is last. **Do not** omit **F**.

When the operator later sends **A**, **B**, **C**, **D**, **E**, **G**, or **H** (or equivalent), **execute that track** without re-running Step 1 unless they say **`coffee`** again. **After** **A, B, C, D, or H**, re-offer the full A–H menu by default (same roles as [Coffee — multiple choice](#coffee--multiple-choice-ah-required)). **After** **E** with a concrete work sub-lane, or **G**, **exit to normal workflow by default** after the reply; do **not** automatically re-offer the menu unless the operator says **`stay in coffee`** or opens a fresh **`coffee`** turn. The coffee session stays **open** until **F** only when the operator stays in the menu/hub flow.

When the operator sends **F** (or **`end coffee session`** / clear equivalent): **formally close** the coffee session — short acknowledgment (one or two sentences). **Do not** run Step 1 automated stack on subsequent turns until the next **`coffee`** (which may be **later the same day** for reorientation). **Work-start `F`** does not require handoff — only a **closeout** **coffee** runs `operator_handoff_check.py` in Step 1 (see [Coffee — closeout](#coffee-closeout-session-end)).

---

## Coffee — multiple choice (A–H required)

The **first** coffee reply ends **Step 2** with **exactly eight options — A through H**, presented **A, B, C, D, E, G, H, F** (**F** closes). **Follow-up behavior:** **A, B, C, D, and H** re-offer the same full A–H menu by default; **E** with a concrete work sub-lane and **G** exit to normal workflow by default after the reply. Wording may vary; **roles must not**.

| Letter | Role | What it means when chosen |
|--------|------|---------------------------|
| **A** | **Template + boundary audit** | **Unchanged — combined when A is chosen:** (1) **Template — grace-mar vs companion-self:** `python scripts/template_diff.py` (see `--help`; default `./companion-self` if cloned beside repo) → refresh [`audit-report.md`](../../../docs/skill-work/work-companion-self/audit-report.md) or `--use-manifest` → [`audit-report-manifest.md`](../../../docs/skill-work/work-companion-self/audit-report-manifest.md). Read [audit-grace-mar-vs-companion-self-template.md](../../../docs/audit-grace-mar-vs-companion-self-template.md), [MERGING-FROM-COMPANION-SELF.md](../../../docs/merging-from-companion-self.md), [work-companion-self/README.md](../../../docs/skill-work/work-companion-self/README.md). (2) **Boundary — leakage / isolation:** spot-check that **grace-mar** Record/identity is not copied into wrong trees; [audit-boundary-grace-mar-companion-self.md](../../../docs/audit-boundary-grace-mar-companion-self.md), [fork isolation](../../../docs/fork-isolation-and-multi-tenant.md); THINK/WRITE vs WORK — [skills-modularity.md](../../../docs/skills-modularity.md). Optional: `python3 scripts/validate-integrity.py --user grace-mar` if Step 1 or thread flagged drift (report only unless operator asks to fix). (3) **Required closing — reconciliation code:** per [work-companion-self § Reconciliation code audit](../../../docs/skill-work/work-companion-self/README.md#reconciliation-code-audit-upstream-and-downstream): **Upstream** (grace-mar → companion-self) and **Downstream** (companion-self → grace-mar) bullets with **concrete paths** (scripts, validators, CI, hooks), or **`Reconciliation code: none`** with one-line rationale. |
| **B** | **Repository hygiene** | **Local repo health** when chosen (not menu **A** — A is template / companion-self / fork reconciliation). **Builds on** Step 1 branch snapshot: full pass per [git-branch-hygiene.md](../../../docs/skill-work/work-dev/git-branch-hygiene.md) (merge vs delete vs update from `main`); **`git status -sb`** and **uncommitted grouping** (real work vs runtime junk — align with [handoff-check](../handoff-check/SKILL.md)); optional **`git worktree list`** if multi-tree; **commit / push** plan (read-only unless operator ships); optional **`python3 scripts/refresh_derived_exports.py -u grace-mar`** + **`validate-integrity.py --user grace-mar`** if manifests / PRP / handoff suggest staleness (report only unless they ask to fix). Deliver: **short ordered checklist** + **one** prescribed next action (or “clean / no action”). **Pending RECURSION-GATE candidates** are **not** repository hygiene — use **menu D**. |
| **C** | **Daily brief** | **Only when chosen** — Step 1 **never** runs the generator. **(1) Generate** (when today’s `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` is missing, or the operator asks for refresh in the same message): `python3 scripts/generate_work_politics_daily_brief.py -u grace-mar -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md`. **When C runs:** **Monday / full** cadence → run generator on **C**; **Tue–Fri** → generate if missing, else summarize from disk unless refresh requested. **(2) Putin — last 48 hours:** per [daily-brief-putin-watch.md](../../../docs/skill-work/work-strategy/daily-brief-putin-watch.md) — web scan; **update §1d** (`## 1d. Putin — last 48 hours`) **in the daily brief file** (edit markdown after generation). **(3) Deliver** path + **short summary** + **one** concrete next action suggested by the brief (work-politics / strategy / Jiang hooks as the file surfaces). **Ship:** committing the brief is operator lane. |
| **D** | **RECURSION-GATE** | **`users/grace-mar/recursion-gate.md`** — the **gated pipeline** queue for the Record. Follow [gate-review-pass](../gate-review-pass/SKILL.md): pending vs processed, **top 1–3** items to review first, duplicate/stale hints, escalation signals; optional `python3 scripts/operator_gate_review_pass.py -u grace-mar` when useful. **Read-only** workflow guidance — **no merge** into SELF/EVIDENCE/prompt without companion approval; on approve, operator runs `process_approved_candidates.py` (see AGENTS). Tie in Step 1 / harness gate snapshot when already pasted. **Not** menu **B** (git/export hygiene) or **E** (work-territory recommendations). |
| **E** | **Work-dev *or* work-strategy *or* work-politics — recommendation** | When **E** is chosen, pick **exactly one** sub-lane (state it in the **first line** of the reply; if the operator names one in the same message, follow that). **After the reply, exit to normal workflow by default**; do **not** automatically re-offer the A–H menu unless the operator says **`stay in coffee`**. **(1) Work-dev** — `docs/skill-work/work-dev/`: [INTEGRATION-PROGRAM.md](../../../docs/skill-work/work-dev/INTEGRATION-PROGRAM.md), [README.md](../../../docs/skill-work/work-dev/README.md); **read** [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md); **real-time** spot-check of listed sources **only when this sub-lane is chosen** (internet as needed for those sources); deliver **delta** + **one** concrete next step (read-only unless operator ships). **Edits** to `work-dev-sources.md` only with operator approval. **(2) Work-strategy** — `docs/skill-work/work-strategy/`: [STRATEGY.md](../../../docs/skill-work/work-strategy/STRATEGY.md), daily-brief pointers, Putin watch procedure, calendar / synthesis docs as relevant; **one** actionable next step (no extra web sweep unless the operator asks). **(3) Work-politics** — **Internet intel (lazy):** when this sub-lane is chosen **and** the session is **not** executing **only** the [Companion survey](#companion-survey-track-coffee) track (see survey default below), run **KY-4 Polymarket + independent poll search + Massie X** per [polling-and-markets.md](../../../docs/skill-work/work-politics/polling-and-markets.md) and `.cursor/skills/politics-massie/SKILL.md` (weight per [cadence](#cadence-by-weekday)). Then: brief registry, campaign, queue — **one** actionable next step (**gate** = **menu D**). **[Companion survey](#companion-survey-track-coffee)** **defaults under E** / **work-politics** when the operator opened with **coffee survey** — run **survey** without the Polymarket / poll / Massie stack unless they ask for intel too. **Not** duplicating **A** / **B** / **C** / **D**. **Dedicated Jiang / PH lane** = **menu G**; **skills / portable pipeline** = **menu H**. |
| **G** | **work-jiang / Predictive History** | When chosen: ground in Step 1 **`## Predictive History — morning momentum`** from `operator_daily_warmup.py` (if Step 1 ran — else run that script or paste last block). [`users/grace-mar/work-jiang.md`](../../../users/grace-mar/work-jiang.md); [`warmup-sparks.yaml`](../../../research/external/work-jiang/metadata/warmup-sparks.yaml); optional `python3 scripts/work_jiang/warmup_jiang_pulse.py -u grace-mar`; [WORKFLOW-transcripts.md](../../../research/external/work-jiang/WORKFLOW-transcripts.md) when transcript integration applies; Civilization / Geo-Strategy context per Step 1 PH line. **One** concrete next step (read-only unless operator ships). **After the reply, exit to normal workflow by default** unless the operator says **`stay in coffee`**. **Not** a substitute for **E** work-politics intel (Polymarket / Massie) — use **E** for that. |
| **H** | **Skills / meta pipeline** | When chosen: [skills-portable/skill-candidates.md](../../../skills-portable/skill-candidates.md), [skills-portable/README.md](../../../skills-portable/README.md) discovery ladder, [extract-skill-from-session](../extract-skill-from-session/SKILL.md), [portable-skills-sync](../portable-skills-sync/SKILL.md). Optional **one line**: `python3 scripts/harness_warmup.py -u grace-mar --receipt` or `python3 scripts/operator_reentry_stack.py -u grace-mar` as cold-thread rails — **not** a mandatory second ritual (see harness-warmup rule). **Not** Record merge. |
| **F** | **End coffee → normal workflow** | **Formally closes** the coffee session (see **Step 2** under [Coffee = start here](#coffee--start-here-two-steps)). Transition to normal chat/work until the next **coffee**. Does **not** by itself imply closeout handoff — that comes from a **closeout** **coffee**. |

**Example shape (E shows chosen sub-lane when picked):**

```markdown
**Coffee — pick one:** *(order: A–E, then G, H, then F)*
- **A.** Template + boundary audit — `template_diff` / audit reports + leakage / fork isolation / skills-modularity (combined when chosen)
- **B.** **Repository hygiene** — branches, status, commit/push plan, exports/integrity per [git-branch-hygiene.md](../../../docs/skill-work/work-dev/git-branch-hygiene.md) *(checklist + one prescribed action when chosen)*
- **C.** **Daily brief** — generate if needed, **§1d** Putin in-file, summary + one next step *(only when chosen; §1d = web when C runs)*
- **D.** **RECURSION-GATE** — pending queue, review order, gate-review-pass; **no merge** without companion approval
- **E.** **Work-dev *or* work-strategy *or* work-politics** — **one** lane + one recommendation *(work-politics = KY-4 + Polymarket + polls + Massie X **here**, not Step 1; survey-only path skips that stack; work-dev = source spot-check **here** only; exits to normal workflow unless you say `stay in coffee`; Jiang = **G**; skills = **H**)*
- **G.** **work-jiang / Predictive History** — PH momentum block, `work-jiang.md`, sparks, optional `warmup_jiang_pulse.py` *(one next step; exits to normal workflow unless you say `stay in coffee`)*
- **H.** **Skills / meta pipeline** — skill-candidates, portable ladder, extract-skill, portable-skills-sync; optional receipt / re-entry stack line
- **F.** **End coffee** — close session; normal workflow until next `coffee`
```

When the operator chooses **A**, the reply must end the audit section with a **Reconciliation code** block, for example:

```markdown
### Reconciliation code
- **Upstream (grace-mar → companion-self):** *(specific paths + one line each, or “none — …”)*
- **Downstream (companion-self → grace-mar):** *(specific paths + adopt command if any, or “none — …”)*
```

---

<a id="shared-ac-morning-and-night"></a>

## Shared A–C (work-start and closeout under coffee)

**Work-start** and **closeout** use the **same** meanings for **A**, **B**, and **C**. When the operator chooses **A**, **B**, or **C** during a **closeout** pass, execute the same track as the matching row in **[Coffee — multiple choice (A–H required)](#coffee--multiple-choice-ah-required)**.

- **Grounding for B during closeout:** Use **handoff** output and closeout Step 1 **branch snapshot** (you do not re-run work-start Step 1).
- **C during closeout:** Still **only** runs `generate_work_politics_daily_brief.py` + §1d when **C** is chosen — typical use is **catch up or refresh today’s** `daily-brief-YYYY-MM-DD.md` before sign-off.

---

<a id="shared-d-morning-and-night"></a>

## Shared D (work-start and closeout under coffee)

**Work-start** and **closeout** use the **same** meaning for **D** — **RECURSION-GATE**. When the operator chooses **D** during **closeout**, execute the same track as **[coffee D](#coffee--multiple-choice-ah-required)** (deepen from handoff **`## RECURSION-GATE (pending)`** when helpful).

---

<a id="shared-g-h-morning-and-night"></a>

## Shared G-H (work-start and closeout under coffee)

**Work-start** and **closeout** use the **same** meanings for **G** and **H**. When the operator chooses **G** or **H** during **closeout**, execute the same track as the matching row in **[Coffee — multiple choice (A–H required)](#coffee--multiple-choice-ah-required)**.

- **G during closeout:** Ground primarily in handoff **`## Predictive History — night closeout`** (already in Step 1 paste) and deepen Jiang / PH closeout per the coffee **G** row — do not duplicate **closeout E**’s one-line “fill from handoff” unless **E** is the chosen letter.
- **H during closeout:** Same as work-start **H**; skill discovery backlog is **not** Record and **not** gate merge.

---

## Companion survey track (coffee)

**When:** Operator chose **coffee E** with **work-politics** sub-lane and the pick is survey — or they began with **[coffee survey](#explicit-phrases-override-default-cadence-when-stated)** and then chose **E** (default survey under **E** / work-politics). **During closeout:** survey still available under **E** (system pick), not under **A–D**.

**Goal:** Refresh **self-curiosity (IX-B)** and **self-personality (IX-C)** on a **cadence** (typical: **monthly micro** 3–5 questions, or **quarterly** longer refinement), without bypassing the gated pipeline.

**Operator / agent actions (read-only unless operator switches to ship):**

1. **Scope** — Pick one wave type: **micro** (few questions, one candidate per answer cluster) vs **theme** (one candidate synthesizing a short battery). Prefer **split candidates** (one mergeable gate block per theme) like the Abigail refinement pattern: `CANDIDATE-0092`–`0097`-style rows in `users/grace-mar/recursion-gate.md` (survey_log in `source_exchange`, `new_vs_record` filled, `channel_key` e.g. `operator:cursor` or `telegram:…`).
2. **Grounding** — Each staged block must carry **literal companion answers** (or transcript pointer) under `source_exchange`; no inferred facts beyond the log (see `recursion-gate.md` merge checklist + AGENTS gated pipeline).
3. **Draft** — Output **ready-to-paste YAML blocks** with `status: pending` for operator/companion review; or, if operator pastes a `survey_log`, map Q clusters → candidates with `suggested_entry` / `prompt_addition` aligned to IX-B vs IX-C.
4. **Close the loop** — Optionally suggest **one** `suggested_followup` the Voice or parent can try in real life after merges (stored in candidate YAML); optional one-line note in `session-log.md` only if operator asks to record the run.
5. **Merge** — Companion **approve** in gate → operator runs `python3 scripts/process_approved_candidates.py -u grace-mar --quick CANDIDATE-XXXX --approved-by companion` (or receipt flow). **Agent does not merge** without approval.

**Cadence hint for Step 1:** If helpful, mention “last survey wave” from recent **Processed** blocks or session memory — optional; do not block the track if unknown.

---

<a id="coffee-closeout-session-end"></a>

## Coffee — closeout (session end, same skill)

When the operator says **`coffee`** and **clearly means closeout** (signing off, end of session, wrapping the day, done for now, etc.) — **same trigger, same skill** — treat it as the **closeout** path. Legacy **`hey`** still works here too. **Do not** run the full [work-start Step 1](#coffee--start-here-two-steps) stack (no daily brief generation, no Polymarket / Massie X pass, no `operator_daily_warmup.py` / `harness_warmup.py` as the main flow) **unless** they explicitly ask for that full stack in the **same** message.

### Step 1 — Automated actions (handoff; paste output)

1. Run the **handoff check** so the next thread can resume cleanly:

   ```bash
   python3 scripts/operator_handoff_check.py -u grace-mar
   ```

2. **Include the command output** in your reply (paste verbatim or as a fenced markdown block). The script embeds **`## RECURSION-GATE (pending)`** (counts, optional item list, proposed merge steps) and **`## Predictive History — night closeout`** (lane status, tomorrow’s lever, rotating spark, optional `rebuild_all` ritual). Treat merge steps as **guidance only** — no merge without companion approval.
3. **One short paragraph** after the paste: what moved today (if known from the thread), what is parked, **gate + Jiang** carryovers, and the **suggested re-entry prompt** from the script output. If the thread produced a **repeatable procedure**, add **one optional phrase**: log a line in `skills-portable/skill-candidates.md` or choose **H** (skills / meta pipeline) / [extract-skill-from-session](../extract-skill-from-session/SKILL.md) (not Record).
4. If the handoff or thread shows **risky uncommitted noise**, one line distinguishing real work vs runtime junk (see [handoff-check](../handoff-check/SKILL.md)); still **read-only** — no merge, stage, or commit as part of closeout **Step 1**.
5. **Branch snapshot (same as coffee step 4):** `git status -sb` and `git branch -vv`; **one plain sentence** if any non-`main` branch exists or tracking looks stale — else **skip** with “branch hygiene: clean.” Prescriptive rules: [git-branch-hygiene.md](../../../docs/skill-work/work-dev/git-branch-hygiene.md). **Not menu A.**

Full spec: [`.cursor/skills/handoff-check/SKILL.md`](../handoff-check/SKILL.md).

### Step 2 — Multiple choice (required; always A–H)

Immediately **after** Step 1, output the fixed **A–H** menu (see [Coffee — closeout — multiple choice](#coffee-closeout-menu)). **List order:** **A, B, C, D, E, G, H, F**. **Do not** omit **F**.

When the operator later sends **A**, **B**, **C**, **D**, **E**, **G**, or **H** (or equivalent), **execute that track** without re-running **Step 1** (`operator_handoff_check.py`) unless they ask for a **fresh handoff** or open a new **closeout** **coffee**. **After** that track’s content, **always output the full A–H menu again** (same roles as [Coffee — closeout — multiple choice](#coffee-closeout-menu)). The closeout pass stays **open** until **F** — do not skip the menu on non-**F** turns.

When the operator sends **F** (or “end closeout” / “end session” / clear equivalent): **formally close** the closeout pass — short acknowledgment (one or two sentences). **Do not** re-run the full closeout **Step 1** stack on subsequent turns until the next **coffee** that opens closeout again. **Next** **coffee** uses operator intent again (work-start vs closeout).

**Distinctions**

- **Work-start `F`:** ends the **work-start coffee session** only; day may continue.
- **Closeout `F`:** ends the **closeout** pass; normal chat can continue, but **do not** treat the thread as still in closeout for rerunning handoff until the next **closeout** **coffee**.

---

<a id="coffee-closeout-menu"></a>

## Coffee — closeout — multiple choice (A–H required)

Every **closeout** reply ends **Step 2** with **exactly eight options — A through H**, presented **A, B, C, D, E, G, H, F**. Wording may vary; **roles must not**.

**A–D** match work-start coffee — see **[Shared A–C (work-start and closeout under coffee)](#shared-ac-morning-and-night)**, **[Shared D (work-start and closeout under coffee)](#shared-d-morning-and-night)**, and the **[coffee table](#coffee--multiple-choice-ah-required)**. **G** and **H** — see **[Shared G-H (work-start and closeout under coffee)](#shared-g-h-morning-and-night)**.

| Letter | Role | What it means when chosen |
|--------|------|---------------------------|
| **A** | **Template + boundary audit** | **Same as coffee A** — [row above](#coffee--multiple-choice-ah-required). |
| **B** | **Repository hygiene** | **Same as work-start B** — [row above](#coffee--multiple-choice-ah-required); ground in **handoff** + closeout Step 1 branch snapshot. |
| **C** | **Daily brief** | **Same as work-start C** — [row above](#coffee--multiple-choice-ah-required); generator + §1d **only when chosen** (often today’s file before sign-off). |
| **D** | **RECURSION-GATE** | **Same as work-start D** — [row above](#coffee--multiple-choice-ah-required); use handoff **`## RECURSION-GATE (pending)`** as primary grounding. |
| **E** | **System pick — productive or hygiene** | **Closeout extras** — **not** duplicating **A–D**, **G**, or **H**. **Prefer B** for full repo hygiene, **C** for daily brief, **D** for gate queue review, **G** for Predictive History / Jiang deep-dive from handoff, **H** for skill backlog / portable sync / extract-skill. **Quick boundary / integrity** — fork isolation / leakage or **`validate-integrity.py --user grace-mar`** if handoff flagged drift. **Also:** work-strategy / work-politics next step without duplicating **D**, **companion survey** ([survey track](#companion-survey-track-coffee)), commit/push grouping, derived-export refresh, weekly-brief carryover, work-politics / `@usa_first_ky` queue. One clear recommendation + optional “if you only have 5 minutes.” Read-only unless operator asks to implement. |
| **G** | **work-jiang / Predictive History** | **Same as work-start G** — [row above](#coffee--multiple-choice-ah-required); ground in handoff **`## Predictive History — night closeout`** (Jiang lane, Spark / `rebuild_all`, `session-log.md` / `work-jiang.md`). |
| **H** | **Skills / meta pipeline** | **Same as work-start H** — [row above](#coffee--multiple-choice-ah-required). |
| **F** | **End closeout** | **Formally closes** the closeout pass (see **Step 2** under [Coffee — closeout](#coffee-closeout-session-end)). Does **not** run work-start Step 1; next **coffee** uses operator intent again. |

**Example shape (E shows one system pick when chosen):**

```markdown
**Coffee — closeout — pick one:** *(order: A–E, then G, H, then F)*
- **A.** Template + boundary audit — same as work-start **A** (`template_diff` / audit + reconciliation code when chosen)
- **B.** **Repository hygiene** — same as work-start **B** *(ground in handoff + branch snapshot)*
- **C.** **Daily brief** — same as work-start **C** *(generator + §1d only when chosen)*
- **D.** **RECURSION-GATE** — same as work-start **D** *(handoff gate block + gate-review-pass)*
- **E.** **System pick** — closeout *(integrity, survey, commit grouping, exports — fill from handoff; prefer **B** / **C** / **D** / **G** / **H** when one letter covers the job)*
- **G.** **work-jiang / PH** — handoff PH night closeout block + one next step
- **H.** **Skills / meta pipeline** — skill-candidates, extract-skill, portable-skills-sync
- **F.** **End closeout** — close the closeout pass; no rerun handoff until next **closeout** **coffee**
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
- **Step 2 — A–H menu** (required for `coffee` / legacy `hey`): fixed **A–H** as in [Coffee — multiple choice (A–H required)](#coffee--multiple-choice-ah-required)
- **Closeout coffee:** handoff script output + summary (**Step 1**), then **Step 2 — A–H** as in [Coffee — closeout — multiple choice](#coffee-closeout-menu) (**A–D** same as work-start; **G–H** shared; see [Shared A–C](#shared-ac-morning-and-night), [Shared D](#shared-d-morning-and-night), [Shared G-H](#shared-g-h-morning-and-night))

## Guardrails

- This is read-only planning. Do not merge or stage just because the warmup mentions candidates.
- If integrity fails, surface that before optional improvements.
- Treat `users/grace-mar/recursion-gate.md` and `self-evidence.md` as canonical, not the summary.
- **Contextual stewardship:** Agents have no cross-thread institutional memory; authority for the Record is **on-disk files + gated pipeline** — not model recall or chat summary.

## Related files

- `docs/operator-skills.md`
- `docs/skill-work/work-coffee/README.md`
- `docs/skill-work/work-politics/polling-and-markets.md` (KY-4 polling + Polymarket — run on **menu E → work-politics** or explicit request, not Step 1)
- `docs/skill-work/work-politics/workspace.md`
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md` (high-stakes work-politics messaging discipline; weekly brief §8)
