# work-xavier — interface (grace-mar ↔ companion-xavier)

**Purpose:** Staging and **contracts** for the **companion-xavier** logical instance, which lives in this repo as a **subtree**:

`docs/skill-work/work-xavier/companion-xavier/`

This folder (everything **above** that `companion-xavier/` child) is **not** Xavier’s Record. It holds **SEED-MANIFEST**, **LEAKAGE-CHECKLIST**, **ALIGNMENT**, handoff notes, and operator-facing navigation so you can reason about the seed without opening her tree first.

**Read first:** [INDEX.md](INDEX.md) · [ALIGNMENT.md](ALIGNMENT.md) · [LANES.md](LANES.md) · [TERMS-XAVIER.md](TERMS-XAVIER.md) · [COMPANION-SELF-SELF-LIBRARY-ALIGNMENT.md](COMPANION-SELF-SELF-LIBRARY-ALIGNMENT.md) (upstream template parity) · [Boundary audit](../../audit-boundary-grace-mar-companion-xavier-companion-self.md) (grace-mar · companion-self · companion-xavier)

**Never copy** `users/grace-mar/**` into the companion-xavier instance tree. See [LEAKAGE-CHECKLIST.md](LEAKAGE-CHECKLIST.md).

**Session 0:** [companion-xavier/docs/seed-survey/seed-survey-initiation.md](companion-xavier/docs/seed-survey/seed-survey-initiation.md) (MCQ) **before** first good morning — [GOOD-MORNING.md](GOOD-MORNING.md), [SESSION-0-OPERATOR.md](SESSION-0-OPERATOR.md).
**First-load onboarding:** [first-good-morning-runbook.md](first-good-morning-runbook.md) — operator script + Xavier startup script + completion checklist.
**No-terminal first day:** [DAY-1-NO-TERMINAL.md](DAY-1-NO-TERMINAL.md) — beginner-safe flow for first session.
**Learning system:** [LEARN-PATH.md](LEARN-PATH.md) · [LEARNING-OBJECTIVES-CONTROL-PLANE.md](LEARNING-OBJECTIVES-CONTROL-PLANE.md) · [PROMPT-PATTERNS.md](PROMPT-PATTERNS.md) · [CHECKLISTS.md](CHECKLISTS.md) · [GLOSSARY-FOR-BEGINNERS.md](GLOSSARY-FOR-BEGINNERS.md)
**Daily sync surface (Xavier-only):** [SYNC-DAILY.md](SYNC-DAILY.md) — single-page work-dev + work-politics sync status.
**work-dev mirror:** [work-dev-mirror/README.md](work-dev-mirror/README.md) — beginner-safe translation of `work-dev` operating patterns for Xavier.

**Execution pack (current):** [content-plan-week1-2026-03-24.md](content-plan-week1-2026-03-24.md) — KY-4 week plan with post cards, stress-test matrix, and human-approval ship protocol.
**3-month budget spec:** [content-spec-3-month-10000-budget.md](content-spec-3-month-10000-budget.md) — 12-week cadence, KPI definitions, escalation rules, and hard-cap `$10,000` allocation.
**Current sprint plan:** [week2-execution-2026-03-31.md](week2-execution-2026-03-31.md) — Week 2 post IDs, spend envelope (`$833` max), and KPI targets.
**Week 2 tracker:** [week2-kpi-budget-log-2026-03-31.md](week2-kpi-budget-log-2026-03-31.md) — fill daily spend, post-level performance, stress-test outcomes, and week-close retro.

---

## Governance contract (compact)

1. **Primary output:** `companion-xavier` is the product; `work-xavier` is the shared execution interface.
2. **Mirror scope:** mirror workflow docs, runbooks, checklists, and project ops artifacts; do **not** mirror identity Record prose across forks.
3. **System of record:** durable identity truth lives in `companion-xavier/users/xavier/*` and enters only through gated merge. Optional split model: `self-knowledge` (facts) and `self-identity` (durable commitments).
4. **Directionality:** default canonical flow is from approved/maintained interface docs into mirrored copies; conflicts require human resolution.
5. **Ownership (RACI):** agent drafts, Xavier/operator reviews, companion approves gated merges, human approves public ship.
6. **Promotion path:** draft -> `recursion-gate.md` candidates -> approval/rejection -> `process_approved_candidates.py --apply`.
7. **Safety classes:** low-risk formatting/doc sync can proceed with review; Record, prompt, and public claims require explicit human gate.
8. **Conflict policy:** when mirrored copies diverge, freeze merge of contested changes until source, intent, and path ownership are resolved.
9. **Security boundary:** no secrets/credentials in shared mirror docs; sensitive material stays in approved private surfaces only.
10. **Success metrics:** zero cross-fork leakage incidents, consistent weekly execution, bounded budget burn, and timely gate processing.
