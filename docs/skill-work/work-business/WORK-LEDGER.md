# WORK-LEDGER — work-business

**Status:** WORK only — judgment / compounding layer for business planning, accounting, and marketing.
**Scaffold source:** [work-template/WORK-LEDGER.md](../work-template/WORK-LEDGER.md).
**Canonical daily surface:** [README.md](README.md); navigation via contents table there.

**Rule:** Additive-first. Do not silently rewrite durable lane memory.

**Not:** Record truth. Promotion to SELF / EVIDENCE / prompt uses RECURSION-GATE + companion approval + merge script per [AGENTS.md](../../../AGENTS.md).

---

## I. CORE

### Territory identity

- **Lane name:** work-business
- **Purpose:** Business planning, accounting (real bookkeeping), marketing, and market research for operator-owned ventures (Grace Gems, future ventures).
- **Primary operator use-case:** Record transactions, generate P&L summaries, plan marketing campaigns, track venture health.
- **Boundary summary:** Instance-specific to grace-mar. Nothing syncs to companion-self. See [README.md](README.md).
- **Promotion gate:** Grace-Mar `recursion-gate.md` + `process_approved_candidates.py` only if a WORK insight should affect the Record.

### Decision style

- **Default mode:** Structured accounting data (JSONL) + venture-specific planning docs.
- **Preferred synthesis style:** P&L summaries + category breakdowns via `business_ledger_summary.py`.
- **Escalation threshold:** Ledger >30 days without a transaction (staleness); tax prep deadline approaching without summary run; marketing plan >90 days without review.
- **Known failure modes:** Treating ledger data as Record truth; syncing accounting to companion-self; mixing venture financials across slugs.

---

## II. LANE-SPECIFIC CORE

### Current focus

- Grace Gems (Etsy) — accounting setup, marketing plan, operational docs.
- Accounting infrastructure: ledger, chart of accounts, summary scripts.

### Active priorities / capabilities / constraints

- Accounting: [accounting/README.md](accounting/README.md), [chart-of-accounts.md](accounting/chart-of-accounts.md).
- Marketing: [marketing/README.md](marketing/README.md), [grace-gems/marketing-plan.md](grace-gems/marketing-plan.md).
- Grace Gems context: [grace-gems/README.md](grace-gems/README.md).

### Known blind spots

- No Etsy API integration yet (Phase 3 in [grace-gems/roadmap.md](grace-gems/roadmap.md)).
- No automated receipt capture.

---

## II-A. ACTIVE WATCHES

**Entry format:** Watch · First noticed · Current status · Latest evidence · Framing note · Primary implication · Contradiction / caution.

**Entries**

- **Watch:** Ledger staleness guardrail
- **First noticed:** 2026-04-06
- **Current status:** watch
- **Latest evidence:** `users/grace-mar/business-ledger.jsonl` — if no new transaction for 30+ days, flag for operator review.
- **Framing note:** Regular transaction recording is the foundation; everything else (P&L, tax prep, budget tracking) depends on it.
- **Primary implication:** Stale ledger means financial picture is incomplete.
- **Contradiction / caution:** Low-volume months are normal for seasonal businesses; staleness ≠ inactivity.

- **Watch:** Tax prep deadline awareness
- **First noticed:** 2026-04-06
- **Current status:** watch
- **Latest evidence:** Schedule C due with personal return (April 15 or extension).
- **Framing note:** Run `--by tax_category` summary at year-end and before filing.
- **Primary implication:** Missing tax categories on transactions makes prep harder.
- **Contradiction / caution:** Tax strategy is accountant territory; ledger provides data, not advice.

- **Watch:** Marketing plan freshness
- **First noticed:** 2026-04-06
- **Current status:** watch
- **Latest evidence:** [grace-gems/marketing-plan.md](grace-gems/marketing-plan.md) — review quarterly; update before seasonal peaks.
- **Framing note:** Marketing plans that don't reflect current Etsy algorithm or ad performance drift into fiction.
- **Primary implication:** Outdated plans waste ad spend.
- **Contradiction / caution:** Plan freshness ≠ plan quality; a stable plan with good metrics doesn't need churn.

---

## III. LEARNING LEDGER

Stable heuristics live in [README.md](README.md), [accounting/README.md](accounting/README.md), and [grace-gems/README.md](grace-gems/README.md). Append here only for short operator shorthand.

---

## IV. LOCAL MEMORY / EXECUTION LOG

Prefer [work-business-history.md](work-business-history.md) for dated milestones.

---

## V. PROMOTION / RETIREMENT RECORD

- *(empty until used)*
