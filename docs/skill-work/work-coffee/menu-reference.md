# Coffee — menu and protocol reference

Detailed **A–I** (+ **F** closes) definitions, **signing-off** (merged closeout) add-ons, cadence tables, explicit phrase modifiers, and companion survey track. The executable trigger contract lives in [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md); this file holds the full protocol specification.

---

## Cadence by weekday

Default rhythm (operator can override any day):

| Day | Mode | What to run |
|-----|------|-------------|
| **Monday** | **Full** | Complete coffee flow: operator + harness + branch snapshot in Step 1. **Internet intel** (Polymarket, independent polls, Massie X): **not** Step 1 — run on **menu E → work-politics** (full Monday weight) or explicit request. **Daily brief:** **menu C** only. |
| **Tuesday–Friday** | **Lighter** | Same Step 1 as Monday (scripts + branch snapshot). **Polling + Polymarket + Massie X:** only when **E / work-politics** (compact) or explicit request. **Daily brief:** **menu C** only (Step 1 one-lines the path pattern). |
| **Sunday** | **Week ahead (~10 min)** | Lighter coffee (week-ahead focus, not Monday-full). Focus: **FEC / compliance dates** and **voter registration** — use **last on-disk** `daily-brief-*.md` calendar slice if present, else [brief-source-registry.md](../work-politics/brief-source-registry.md) (`needs_refresh`, `watch`). **Generating** today's brief remains **menu C**. Optional: skim `pol-pulse` / weekly-brief readiness. |
| **Friday** | **Lighter + post-mortem** | Same as Tue–Fri **plus** two lines at the end of the reply: **(1)** What repeated this week? **(2)** What to drop from the routine? |

If the operator says **`coffee`** on a **Sunday** (or legacy **`hey`**), default to **week-ahead** mode unless they ask for the full Monday stack. Still run **Step 1** scaled to that mode, then **Step 2** with the full **A–I** menu (labels can be shorter; meanings unchanged).

---

## Explicit phrases (override default cadence when stated)

**`coffee light`** (or clear equivalent; legacy **`hey light`** still works):

- Run **`operator_daily_warmup.py`** and, when instance state matters, **`harness_warmup.py`**.
- **Internet intel** (Polymarket, polls, Massie X) is **never** Step 1 — same as full coffee; choose **E → work-politics** when you want it (or ask explicitly). **Light** keeps **branch snapshot** compact (one line unless multiple branches).
- **Daily brief:** **do not** generate in Step 1 — one-line pointer to **menu C** and path pattern `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` (e.g. `daily-brief-2026-03-29.md`).
- Deliver a **compact brief** from script outputs + thread context; then **full Step 2** menu **A, B, C, D, E, G, H, I, F** (do not omit **F**). On later turns, **A, B, C, D, or H** re-offer the full menu unless the operator says otherwise; **E** (with a concrete sub-lane), **G**, and **I** exit to normal workflow by default after the reply. **Track B:** **compact** repository hygiene (branch + `git status` + one prescribed action or "clean") — not a full sweep unless the operator asks.

**`coffee minimal`** (or clear equivalent; legacy **`hey minimal`** still works):

- Run **`harness_warmup.py`** only when instance state matters; **do not** run `operator_daily_warmup.py` unless the operator asks.
- Step 1 has **no** Polymarket / Massie X / poll web search unless the operator **explicitly** asks in the same message. **Daily brief** still **only** via **menu C** (never Step 1).
- Optional **one-line** gate pointer (e.g. pending count from warmup output if already pasted, or "see `users/grace-mar/recursion-gate.md`").
- Still output **full Step 2** menu **A, B, C, D, E, G, H, I, F**. On later turns, **A, B, C, D, or H** re-offer the full menu unless the operator says otherwise; **E** (with a concrete sub-lane), **G**, and **I** exit to normal workflow by default after the reply. **Track B:** **minimal** repository hygiene — extend the Step 1 branch line with `git status -sb` + **one** next action (or "clean"); no unrelated sweeps.

**`coffee survey`** (or **`coffee + survey`** / clear equivalent; legacy **`hey survey`** still works):

- Run **Step 1** using the same cadence or explicit phrases as if they had said plain **coffee** (they may combine with **coffee light** or **minimal** — apply both: thin work-politics steps *and* survey intent).
- In the **Step 1 warmup brief**, add a short **Companion survey** block (2–4 lines): purpose (IX-B / IX-C refinement), suggested cadence hint (e.g. **monthly micro** 3–5 questions vs **quarterly** deeper pass), pointer that execution is **menu E** (work-politics sub-lane) this session unless they choose another letter first.
- **Step 2** remains the **same fixed menu** **A, B, C, D, E, G, H, I, F** (do not drop letters). When the operator chooses **E**, **default** the **work-politics** sub-lane and run the [Companion survey track](#companion-survey-track) for that turn (unless they explicitly steer **E** to work-dev or work-strategy in the same message, e.g. "E work-dev only"). After the survey turn, exit to normal workflow by default unless the operator says **`stay in coffee`**.
- **Pipeline:** survey work **stages** `recursion-gate.md` candidates only — **no merge** without companion approval; same rule as the rest of this skill.

---

<a id="ah-table"></a>

## A–I menu — work-start (full definitions)

The **first** coffee reply ends **Step 2** with **exactly nine lettered options — A through I**, presented **A, B, C, D, E, G, H, I, F** (**F** closes). **Follow-up behavior:** **A, B, C, D, and H** re-offer the same full menu by default; **E** with a concrete work sub-lane, **G**, and **I** exit to normal workflow by default after the reply. Wording may vary; **roles must not**.

| Letter | Role | What it means when chosen |
|--------|------|---------------------------|
| **A** | **Template + boundary audit** | **Combined when A is chosen:** (1) **Template — grace-mar vs companion-self:** `python scripts/template_diff.py` (see `--help`; default `./companion-self` if cloned beside repo) → refresh [`audit-report.md`](../work-companion-self/audit-report.md) or `--use-manifest` → [`audit-report-manifest.md`](../work-companion-self/audit-report-manifest.md). Read [audit-grace-mar-vs-companion-self-template.md](../../audit-grace-mar-vs-companion-self-template.md), [MERGING-FROM-COMPANION-SELF.md](../../merging-from-companion-self.md), [work-companion-self/README.md](../work-companion-self/README.md). (2) **Boundary — leakage / isolation:** spot-check that **grace-mar** Record/identity is not copied into wrong trees; [audit-boundary-grace-mar-companion-self.md](../../audit-boundary-grace-mar-companion-self.md), [fork isolation](../../fork-isolation-and-multi-tenant.md); THINK/WRITE vs WORK — [skills-modularity.md](../../skills-modularity.md). Optional: `python3 scripts/validate-integrity.py --user grace-mar` if Step 1 or thread flagged drift (report only unless operator asks to fix). (3) **Required closing — reconciliation code:** per [work-companion-self § Reconciliation code audit](../work-companion-self/README.md#reconciliation-code-audit-upstream-and-downstream): **Upstream** (grace-mar → companion-self) and **Downstream** (companion-self → grace-mar) bullets with **concrete paths** (scripts, validators, CI, hooks), or **`Reconciliation code: none`** with one-line rationale. |
| **B** | **Repository hygiene** | **Local repo health** when chosen (not menu **A** — A is template / companion-self / fork reconciliation). **Builds on** Step 1 branch snapshot: full pass per [git-branch-hygiene.md](../work-dev/git-branch-hygiene.md) (merge vs delete vs update from `main`); **`git status -sb`** and **uncommitted grouping** (real work vs runtime junk — align with [handoff-check](../../../.cursor/skills/handoff-check/SKILL.md)); optional **`git worktree list`** if multi-tree; **commit / push** plan (read-only unless operator ships); optional **`python3 scripts/refresh_derived_exports.py -u grace-mar`** + **`validate-integrity.py --user grace-mar`** if manifests / PRP / handoff suggest staleness (report only unless they ask to fix). Deliver: **short ordered checklist** + **one** prescribed next action (or "clean / no action"). **Pending RECURSION-GATE candidates** are **not** repository hygiene — use **menu D**. |
| **C** | **Daily brief** | **Only when chosen** — Step 1 **never** runs the generator. **(1) Generate** (when today's `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` is missing, or the operator asks for refresh): `python3 scripts/generate_work_politics_daily_brief.py -u grace-mar -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md`. **Monday / full** cadence → run generator on **C**; **Tue–Fri** → generate if missing, else summarize from disk unless refresh requested. **(2) Putin — last 48 hours:** per [daily-brief-putin-watch.md](../work-strategy/daily-brief-putin-watch.md) — web scan; **update §1d** (`## 1d. Putin — last 48 hours`) **in the daily brief file** (edit markdown after generation). **(3) Deliver** path + **short summary** + **one** concrete next action suggested by the brief. **Ship:** committing the brief is operator lane. |
| **D** | **RECURSION-GATE** | **`users/grace-mar/recursion-gate.md`** — the **gated pipeline** queue for the Record. Follow [gate-review-pass](../../../.cursor/skills/gate-review-pass/SKILL.md): pending vs processed, **top 1–3** items to review first, duplicate/stale hints, escalation signals; optional `python3 scripts/operator_gate_review_pass.py -u grace-mar`. **Read-only** — **no merge** into SELF/EVIDENCE/prompt without companion approval; on approve, operator runs `process_approved_candidates.py`. **Not** menu **B** (git/export hygiene) or **E** (work-territory recommendations). |
| **E** | **Work-dev *or* work-strategy *or* work-politics** — **or system pick** | **Normal:** Pick **exactly one** sub-lane (state it in the first line; if the operator names one, follow that). **After the reply, exit to normal workflow by default**; do **not** re-offer the full menu unless the operator says **`stay in coffee`**. **(1) Work-dev** — `docs/skill-work/work-dev/`: read [work-dev-sources.md](../work-dev/work-dev-sources.md); **real-time** spot-check of listed sources **only when this sub-lane is chosen**; deliver **delta** + **one** concrete next step. **(2) Work-strategy** — `docs/skill-work/work-strategy/` (non-Rome lane): daily-brief pointers, Putin watch, calendar, STRATEGY/current-events — **one** next step. **Vatican / Holy See / ROME-PASS / work-strategy-rome** → **menu I** (dedicated); do **not** treat Rome as satisfied by generic **E → work-strategy** alone. **(3) Work-politics** — run **KY-4 Polymarket + poll search + Massie X** per [polling-and-markets.md](../work-politics/polling-and-markets.md) and `.cursor/skills/politics-massie/SKILL.md` (weight per cadence). Then: brief registry, campaign, queue — **one** next step. **[Companion survey](#companion-survey-track)** defaults under **E** when the operator opened with **coffee survey**. **Signing-off Step 1** (handoff-weighted): if the operator picks **E** **without** naming work-dev / work-strategy / work-politics, deliver **one** **system pick** — quick boundary/integrity glance, commit–push grouping, derived-export refresh pointer, weekly-brief carryover, `@usa_first_ky` queue, companion survey pointer, or optional **Rome** carryover line — **one** clear recommendation; read-only unless they ask to implement. **Not** duplicating **A** / **B** / **C** / **D**; Jiang = **G**; skills = **H**; Rome = **I**. |
| **G** | **work-jiang / Predictive History** | Ground in Step 1 PH momentum block. [`users/grace-mar/work-jiang.md`](../../../users/grace-mar/work-jiang.md); [`warmup-sparks.yaml`](../../../research/external/work-jiang/metadata/warmup-sparks.yaml); optional `warmup_jiang_pulse.py`. **One** next step. **Exits to normal workflow** unless **`stay in coffee`**. **Not** a substitute for **E** work-politics intel. |
| **H** | **Skills / meta pipeline** | [skills-portable/skill-candidates.md](../../../skills-portable/skill-candidates.md), discovery ladder, [extract-skill-from-session](../../../.cursor/skills/extract-skill-from-session/SKILL.md), [portable-skills-sync](../../../.cursor/skills/portable-skills-sync/SKILL.md). Optional receipt line. **Not** Record merge. |
| **I** | **work-strategy-rome** | **Always** this lane — develops `docs/skill-work/work-strategy/work-strategy-rome/`. Ground in [README.md](../work-strategy/work-strategy-rome/README.md), [ROME-PASS.md](../work-strategy/work-strategy-rome/ROME-PASS.md), [manifest.md](../work-strategy/work-strategy-rome/manifest.md), [notes/](../work-strategy/work-strategy-rome/notes/) and [notes/exemplars/](../work-strategy/work-strategy-rome/notes/exemplars/). **When chosen:** run or advance a **ROME-PASS**-shaped slice (source order, boundaries, output blocks per ROME-PASS) **or** ship **one** concrete develop action (new dated note, exemplar-shaped pass, thesis-stub line, `daily-brief-focus.md` hook, manifest backlog tick). **WORK only** — no SELF/EVIDENCE/prompt merge without gate + companion approval; no unsourced papal claims. **Exits to normal workflow** after the reply unless **`stay in coffee`**. **Not** **E** work-politics KY-4 stack; **not** **G** Jiang. |
| **F** | **End coffee → normal workflow** | **Formally closes** the coffee session without choosing **A–I** lettered work. Transition to normal chat/work until the next **coffee**. Does **not** replace **signing-off Step 1** (handoff) when the operator already ran **`coffee`** with signing-off intent — **F** is only “exit the hub.” |

**When A is chosen**, the reply must end with a **Reconciliation code** block:

```markdown
### Reconciliation code
- **Upstream (grace-mar → companion-self):** *(specific paths + one line each, or "none — …")*
- **Downstream (companion-self → grace-mar):** *(specific paths + adopt command if any, or "none — …")*
```

---

<a id="signing-off-intent"></a>

## Signing-off intent (closeout merged — no separate menu)

**Trigger:** Operator says **`coffee`** (or **`hey`**) with **signing-off** intent — end of session, wrapping the day, stepping away.

**Step 1:** Handoff-weighted — `python3 scripts/operator_coffee.py -u <id> --mode closeout` or `operator_handoff_check.py` (see [coffee SKILL.md](../../../.cursor/skills/coffee/SKILL.md)). Same paste + short paragraph as before.

**Step 2:** The **same** menu as work-start (**order A, B, C, D, E, G, H, I, F**). There is **no** separate closeout menu and **no** closeout-only letter.

**Per-letter add-ons when Step 1 was signing-off** (optional emphasis — do not duplicate the whole handoff block):

| Letter | Signing-off add-on |
|--------|---------------------|
| **A** | Same template/boundary track; one line on **gated** Record boundary if helpful. |
| **B** | Prefer **handoff** **Derived / export churn** and **git status** from Step 1; [handoff-check SKILL.md](../../../.cursor/skills/handoff-check/SKILL.md). |
| **C** | Brief generator + §1d **only** if **C** chosen; optional pointer to **next** brief day. |
| **D** | Deepen from handoff **`## RECURSION-GATE (pending)`** when present. |
| **E** | If **no** sub-lane named → **system pick** (see **E** row in table above). If sub-lane named → normal **E** track. |
| **G** | Ground in handoff **`## Predictive History — night closeout`** when present. |
| **H** | Same as work-start; optional “next session” skills backlog line. |
| **I** | Optional one line: **Rome** / Vatican watch carryover or **next ROME-PASS** if Step 1 or thread flagged it. |
| **F** | Exit hub only. |

---

<a id="companion-survey-track"></a>

## Companion survey track

**When:** Operator chose **coffee E** with **work-politics** sub-lane and the pick is survey — or they began with **coffee survey** and then chose **E** (default survey under **E** / work-politics). **Signing-off intent + E** without a sub-lane → **system pick** may include survey as the one recommendation.

**Goal:** Refresh **self-curiosity (IX-B)** and **self-personality (IX-C)** on a **cadence** (typical: **monthly micro** 3–5 questions, or **quarterly** longer refinement), without bypassing the gated pipeline.

**Operator / agent actions (read-only unless operator switches to ship):**

1. **Scope** — Pick one wave type: **micro** (few questions, one candidate per answer cluster) vs **theme** (one candidate synthesizing a short battery). Prefer **split candidates** (one mergeable gate block per theme) like the Abigail refinement pattern: `CANDIDATE-0092`–`0097`-style rows.
2. **Grounding** — Each staged block must carry **literal companion answers** (or transcript pointer) under `source_exchange`; no inferred facts beyond the log.
3. **Draft** — Output **ready-to-paste YAML blocks** with `status: pending` for operator/companion review.
4. **Close the loop** — Optionally suggest **one** `suggested_followup` the Voice or parent can try in real life after merges.
5. **Merge** — Companion **approve** in gate → operator runs `python3 scripts/process_approved_candidates.py -u grace-mar --quick CANDIDATE-XXXX --approved-by companion`. **Agent does not merge** without approval.

**Cadence hint for Step 1:** If helpful, mention "last survey wave" from recent **Processed** blocks or session memory.
