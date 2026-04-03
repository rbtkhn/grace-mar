# Coffee — menu and protocol reference

Detailed **A–E** (five mode) definitions, **signing-off** (merged closeout) add-ons, cadence tables, explicit phrase modifiers, and companion survey track. The executable trigger contract lives in [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md); this file holds the full protocol specification.

**Exit:** There is **no** “close hub” letter. The operator leaves coffee by normal chat, **no menu**, or the next task.

---

## Context paste budgets (operator)

**Not** Record truth. JSON under [`config/context_budgets/`](../../../config/context_budgets/) caps ritual paste size: **`coffee.json`** drives collapsed **Last dream** line count, optional civ-mem / coffee-rollup lines, and session-tail depth in **`scripts/operator_daily_warmup.py`**; **`dream.json`** drives **`scripts/auto_dream.py`** civ-mem echo limits, rollup allow, and integrity/governance suppress rules before **`last-dream.json`** is written. Defaults keep the collapsed Last dream block thin; opt in with **`--show-civ-mem`** / **`--show-rollup`** on `operator_daily_warmup.py`, or forward the same flags from **`operator_coffee.py`** / **`operator_reentry_stack.py`**. Approximate footprint: **`python3 scripts/audit_context_tax.py -u grace-mar`**. See [`config/context_budgets/README.md`](../../../config/context_budgets/README.md) and [`docs/skill-work/work-dream/README.md`](../work-dream/README.md) (handoff fields).

---

## Cadence by weekday

Default rhythm (operator can override any day):

| Day | Mode | What to run |
|-----|------|-------------|
| **Monday** | **Full** | Complete coffee flow: operator + harness + branch snapshot in Step 1. **Internet intel** (Polymarket, independent polls, Massie X): **not** Step 1 — run on **menu A — Today** (full Monday weight) or explicit request. **Daily brief:** **menu A** only (part of **Today**). |
| **Tuesday–Friday** | **Lighter** | Same Step 1 as Monday (scripts + branch snapshot). **Polling + Polymarket + Massie X:** only when **A / Today** (compact) or explicit request. **Daily brief:** **menu A** only (Step 1 one-lines the path pattern). |
| **Sunday** | **Week ahead (~10 min)** | Lighter coffee (week-ahead focus, not Monday-full). Focus: **FEC / compliance dates** and **voter registration** — use **last on-disk** `daily-brief-*.md` calendar slice if present, else [brief-source-registry.md](../work-politics/brief-source-registry.md) (`needs_refresh`, `watch`). **Generating** today's brief remains **menu A**. Optional: skim `pol-pulse` / weekly-brief readiness. |
| **Friday** | **Lighter + post-mortem** | Same as Tue–Fri **plus** two lines at the end of the reply: **(1)** What repeated this week? **(2)** What to drop from the routine? |

If the operator says **`coffee`** on a **Sunday** (or legacy **`hey`**), default to **week-ahead** mode unless they ask for the full Monday stack. Still run **Step 1** scaled to that mode, then **Step 2** with the full **A–E** menu (labels can be shorter; meanings unchanged).

---

## Explicit phrases (override default cadence when stated)

**`coffee light`** (or clear equivalent; legacy **`hey light`** still works):

- Run **`operator_daily_warmup.py`** and, when instance state matters, **`harness_warmup.py`**.
- **Internet intel** (Polymarket, polls, Massie X) is **never** Step 1 — same as full coffee; choose **A — Today** when you want it (or ask explicitly). **Light** keeps **branch snapshot** compact (one line unless multiple branches).
- **Daily brief:** **do not** generate in Step 1 — one-line pointer to **menu A** and path pattern `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` (e.g. `daily-brief-2026-03-29.md`).
- Deliver a **compact brief** from script outputs + thread context; then **full Step 2** menu **A, B, C, D, E**. On later turns, **A, B, or E** re-offer the full menu unless the operator says otherwise; **C** and **D** exit to normal workflow by default after the reply. **Build (B):** **compact** hygiene (branch + `git status` + one prescribed action or "clean") — not a full sweep unless the operator asks.

**`coffee minimal`** (or clear equivalent; legacy **`hey minimal`** still works):

- Run **`harness_warmup.py`** only when instance state matters; **do not** run `operator_daily_warmup.py` unless the operator asks.
- Step 1 has **no** Polymarket / Massie X / poll web search unless the operator **explicitly** asks in the same message. **Daily brief** still **only** via **menu A** (never Step 1).
- Optional **one-line** gate pointer (e.g. pending count from warmup output if already pasted, or "see `users/grace-mar/recursion-gate.md`").
- Still output **full Step 2** menu **A, B, C, D, E**. On later turns, **A, B, or E** re-offer the full menu unless the operator says otherwise; **C** and **D** exit to normal workflow by default after the reply. **Build (B):** **minimal** hygiene — extend the Step 1 branch line with `git status -sb` + **one** next action (or "clean"); no unrelated sweeps.

**`coffee survey`** (or **`coffee + survey`** / clear equivalent; legacy **`hey survey`** still works):

- Run **Step 1** using the same cadence or explicit phrases as if they had said plain **coffee** (they may combine with **coffee light** or **minimal** — apply both: thin work-politics steps *and* survey intent).
- In the **Step 1 warmup brief**, add a short **Companion survey** block (2–4 lines): purpose (IX-B / IX-C refinement), suggested cadence hint (e.g. **monthly micro** 3–5 questions vs **quarterly** deeper pass), pointer that execution is **menu A — Today** this session unless they choose another letter first.
- **Step 2** remains the **same fixed menu** **A, B, C, D, E** (do not drop letters). When the operator chooses **A**, run the [Companion survey track](#companion-survey-track) for that turn (skip Polymarket/Massie unless the operator also wants intel in the same turn). After the survey turn, exit to normal workflow by default unless the operator says **`stay in coffee`**.
- **Pipeline:** survey work **stages** `recursion-gate.md` candidates only — **no merge** without companion approval; same rule as the rest of this skill.

---

<a id="ah-table"></a>

## A–E menu — work-start (full definitions)

The **first** coffee reply ends **Step 2** with **exactly five lettered options — A through E**, presented **A, B, C, D, E**. **Follow-up behavior:** **A, B, and E** re-offer the same full menu by default; **C** and **D** exit to normal workflow by default after the reply. Wording may vary; **roles must not**.

**Micro-hints (one line under the menu):** `Micro-hints: B+skills/meta | E=gate/template/boundary`

| Letter | Mode | What it means when chosen |
|--------|------|---------------------------|
| **A** | **Today** | **Operational picture — only when A is chosen** (Step 1 never runs the brief generator or KY-4 web intel). **(1) Daily brief:** When today's `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` is missing, or the operator asks for refresh: `python3 scripts/generate_work_politics_daily_brief.py -u grace-mar -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md`. **Monday / full** cadence → run generator on **A**; **Tue–Fri** → generate if missing, else summarize from disk unless refresh requested. **(2) Putin — last 48 hours:** per [daily-brief-putin-watch.md](../work-strategy/daily-brief-putin-watch.md) — web scan; **update §1d** (`## 1d. Putin — last 48 hours`) **in the daily brief file** (edit markdown after generation). **(3) Work-politics intel:** run **KY-4 Polymarket + poll search + Massie X** per [polling-and-markets.md](../work-politics/polling-and-markets.md) and `.cursor/skills/politics-massie/SKILL.md` (weight per cadence) **unless** this turn is **survey-only** (`coffee survey` + operator wants survey without markets — honor that). **(4)** Brief registry, campaign, queue — **one** next step. **Ship:** committing the brief is operator lane. **Not** template-only parity ( **E** ); **not** Rome-only depth ( **C** ). |
| **B** | **Build** | **work-dev + repository hygiene** when chosen. **(1) Work-dev** — `docs/skill-work/work-dev/`: read [work-dev-sources.md](../work-dev/work-dev-sources.md); **real-time** spot-check of listed sources **only when this sub-lane is in scope**; deliver **delta** + **one** concrete next step. **(2) Hygiene** — builds on Step 1 branch snapshot: [git-branch-hygiene.md](../work-dev/git-branch-hygiene.md) (merge vs delete vs update from `main`); **`git status -sb`** and **uncommitted grouping** (align with [handoff-check](../../../.cursor/skills/handoff-check/SKILL.md)); optional **`git worktree list`**; **commit / push** plan (read-only unless operator ships); optional **`python3 scripts/refresh_derived_exports.py -u grace-mar`** + **`validate-integrity.py --user grace-mar`** if manifests / PRP / handoff suggest staleness (report only unless they ask to fix). **Pending RECURSION-GATE candidates** are **not** Build hygiene — use **E — Steward** (gate). **Skills / meta:** [skills-portable/skill-candidates.md](../../../skills-portable/skill-candidates.md), [extract-skill-from-session](../../../.cursor/skills/extract-skill-from-session/SKILL.md), [portable-skills-sync](../../../.cursor/skills/portable-skills-sync/SKILL.md) — invoke when the operator says **skills** / **meta** with **B** or asks for skills after a Build turn. |
| **C** | **Compass** | **work-strategy** + **work-strategy-rome** — **one** next step. **(1) work-strategy** (non-Rome): `docs/skill-work/work-strategy/` — daily-brief pointers, calendar, STRATEGY, current-events — **one** next step. **(2) work-strategy-rome** — **always in scope here:** [work-strategy-rome/README.md](../work-strategy/work-strategy-rome/README.md), [ROME-PASS.md](../work-strategy/work-strategy-rome/ROME-PASS.md), [manifest.md](../work-strategy/work-strategy-rome/manifest.md), notes / exemplars. ROME-PASS-shaped slice **or** **one** concrete develop action (dated note, exemplar pass, thesis stub, manifest tick). **WORK only** — no SELF/EVIDENCE/prompt merge without gate + companion approval; no unsourced papal claims. **Exits to normal workflow** after the reply unless **`stay in coffee`**. **Not** KY-4 intel stack ( **A** ); **not** Jiang ( **D** ). |
| **D** | **Book** | **work-jiang / Predictive History.** Ground in Step 1 PH momentum block. [`users/grace-mar/work-jiang.md`](../../../users/grace-mar/work-jiang.md); [`warmup-sparks.yaml`](../../../research/external/work-jiang/metadata/warmup-sparks.yaml); optional `warmup_jiang_pulse.py`. **One** next step. **Exits to normal workflow** unless **`stay in coffee`**. **Not** a substitute for **A** work-politics intel. |
| **E** | **Steward** | **RECURSION-GATE + template / boundary audit** — **single-track default (mandatory):** if the operator says **E** only, run **exactly one** track: **gate** when there is ≥1 pending candidate in `recursion-gate.md`; otherwise **template/boundary**. **`both`** in one turn only if they explicitly ask. **First line:** name the track (**gate** or **template/boundary**). **(1) Gate** — `users/grace-mar/recursion-gate.md`; [gate-review-pass](../../../.cursor/skills/gate-review-pass/SKILL.md); optional `python3 scripts/operator_gate_review_pass.py -u grace-mar`. **Read-only** — **no merge** without companion approval. **(2) Template / boundary** — **grace-mar vs companion-self:** `python scripts/template_diff.py` (see `--help`) → [`audit-report.md`](../work-companion-self/audit-report.md) or `--use-manifest` → [`audit-report-manifest.md`](../work-companion-self/audit-report-manifest.md). Read [audit-grace-mar-vs-companion-self-template.md](../../audit-grace-mar-vs-companion-self-template.md), [MERGING-FROM-COMPANION-SELF.md](../../merging-from-companion-self.md), [work-companion-self/README.md](../work-companion-self/README.md). **Boundary** — [audit-boundary-grace-mar-companion-self.md](../../audit-boundary-grace-mar-companion-self.md), [fork isolation](../../fork-isolation-and-multi-tenant.md); THINK/WRITE vs WORK — [skills-modularity.md](../../skills-modularity.md). Optional: `python3 scripts/validate-integrity.py --user grace-mar` if drift flagged. **Not** duplicating **A** / **B** / **C** / **D** as primary work. |

**When the Steward turn includes template/boundary / companion-self parity**, the reply must end with a **Reconciliation code** block:

```markdown
### Reconciliation code
- **Upstream (grace-mar → companion-self):** *(specific paths + one line each, or "none — …")*
- **Downstream (companion-self → grace-mar):** *(specific paths + adopt command if any, or "none — …")*
```

Per [work-companion-self § Reconciliation code audit](../work-companion-self/README.md#reconciliation-code-audit-upstream-and-downstream).

---

<a id="signing-off-intent"></a>

## Signing-off intent (closeout merged — no separate menu)

**Trigger:** Operator says **`coffee`** (or **`hey`**) with **signing-off** intent — end of session, wrapping the day, stepping away.

**Step 1:** Handoff-weighted — `python3 scripts/operator_coffee.py -u <id> --mode closeout` or `operator_handoff_check.py` (see [coffee SKILL.md](../../../.cursor/skills/coffee/SKILL.md)). Same paste + short paragraph as before.

**Step 2:** The **same** menu as work-start (**order A, B, C, D, E**). There is **no** separate closeout menu and **no** closeout-only letter.

**Per-letter add-ons when Step 1 was signing-off** (optional emphasis — do not duplicate the whole handoff block):

| Letter | Signing-off add-on |
|--------|---------------------|
| **A** | Brief + intel **only** if **A** chosen; optional pointer to **next** brief day. |
| **B** | Prefer **handoff** **Derived / export churn** and **git status** from Step 1; [handoff-check SKILL.md](../../../.cursor/skills/handoff-check/SKILL.md). |
| **C** | Optional Rome / strategy carryover line. |
| **D** | Ground in handoff **`## Predictive History — night closeout`** when present. |
| **E** | Same **single-track default** as work-start (**gate** if pending candidates, else **template/boundary**); **both** only if explicit. |

---

<a id="companion-survey-track"></a>

## Companion survey track

**When:** Operator chose **coffee A — Today** and the pick is survey — or they began with **coffee survey** and then chose **A** (default survey under **Today**). **Signing-off intent + E** without a sub-track → **system pick** may include survey as the one recommendation.

**Goal:** Refresh **self-curiosity (IX-B)** and **self-personality (IX-C)** on a **cadence** (typical: **monthly micro** 3–5 questions, or **quarterly** longer refinement), without bypassing the gated pipeline.

**Operator / agent actions (read-only unless operator switches to ship):**

1. **Scope** — Pick one wave type: **micro** (few questions, one candidate per answer cluster) vs **theme** (one candidate synthesizing a short battery). Prefer **split candidates** (one mergeable gate block per theme) like the Abigail refinement pattern: `CANDIDATE-0092`–`0097`-style rows.
2. **Grounding** — Each staged block must carry **literal companion answers** (or transcript pointer) under `source_exchange`; no inferred facts beyond the log.
3. **Draft** — Output **ready-to-paste YAML blocks** with `status: pending` for operator/companion review.
4. **Close the loop** — Optionally suggest **one** `suggested_followup` the Voice or parent can try in real life after merges.
5. **Merge** — Companion **approve** in gate → operator runs `python3 scripts/process_approved_candidates.py -u grace-mar --quick CANDIDATE-XXXX --approved-by companion`. **Agent does not merge** without approval.

**Cadence hint for Step 1:** If helpful, mention "last survey wave" from recent **Processed** blocks or session memory.
