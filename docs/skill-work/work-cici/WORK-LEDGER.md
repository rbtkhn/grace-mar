# WORK-LEDGER — work-cici

**Status:** WORK only — optional **judgment / compounding** layer for the advisor module.  
**Scaffold source:** [work-template/WORK-LEDGER.md](../work-template/WORK-LEDGER.md).  
**Canonical daily surface:** [SYNC-DAILY.md](SYNC-DAILY.md); navigation hub [INDEX.md](INDEX.md).

**Rule:** Additive-first. Do not silently rewrite durable lane memory.

**Not:** Xavier’s Record (her repo); not Grace-Mar Record truth. Promotion to SELF / EVIDENCE / prompt uses the **appropriate** repo’s **RECURSION-GATE** + companion approval + merge script per [AGENTS.md](../../../AGENTS.md).

---

## I. CORE

### Territory identity

- **Lane name:** work-cici  
- **Purpose:** Coordinate operator/advisor work with Xavier (SMM, BrewMind, mirrors, runbooks) in grace-mar — without hosting her cognitive fork.  
- **Primary operator use-case:** Daily sync, mirror alignment, employee work profile / skills portfolio, content plans vs capability rubric, template drift awareness.  
- **Boundary summary:** See [README.md](README.md) governance block and [LANES.md](LANES.md).  
- **Promotion gate (her Record):** Her `recursion-gate.md` + `process_approved_candidates.py` **in her repository**. **Grace-Mar** gate only if a change is explicitly for grace-mar identity/Voice.

### Decision style

- **Default mode:** Pointer-heavy; long playbooks stay in linked docs ([INDEX.md](INDEX.md)).  
- **Preferred synthesis style:** Mirror scores + one combined next action ([SYNC-DAILY.md](SYNC-DAILY.md)).  
- **Escalation threshold:** Stale mirror logs (3+ days without sync-log row), template alignment `major drift`, or rubric vs plan mismatch blocking execution.  
- **Known failure modes:** Treating advisor markdown as Record; copying `users/grace-mar/**` into her tree — [LEAKAGE-CHECKLIST.md](LEAKAGE-CHECKLIST.md).

---

## II. LANE-SPECIFIC CORE

### Current focus

- See [SYNC-DAILY.md](SYNC-DAILY.md) and [DAILY-OPS-CARD.md](DAILY-OPS-CARD.md).  
- Employee profile / skills portfolio: [xavier-work-profile.md](xavier-work-profile.md) (update on hiring milestones, scope changes, or tooling upskill).

### Active priorities / capabilities / constraints

- Content plans and KPI logs: [INDEX.md](INDEX.md) (BrewMind + week plans).  
- Work profile / portfolio: [xavier-work-profile.md](xavier-work-profile.md).  
- Capability evaluation: [xavier-smm-capability-rubric.md](xavier-smm-capability-rubric.md).  
- Mirrors: [work-dev-mirror/SYNC-LOG.md](work-dev-mirror/SYNC-LOG.md), [work-politics-mirror/SYNC-LOG.md](work-politics-mirror/SYNC-LOG.md).

### Known blind spots

- Framing-audit and multi-frame registries are **partial** (see [work-template/MAPPING.md](../work-template/MAPPING.md) work-cici subsection when present).

---

## II-A. ACTIVE WATCHES

**Entry format:** Watch · First noticed · Current status · Latest evidence · Framing note · Primary implication · Contradiction / caution.

**Entries**

- **Watch:** Mirror sync staleness guardrail  
- **First noticed:** 2026-04-04  
- **Current status:** watch  
- **Latest evidence:** [SYNC-DAILY.md](SYNC-DAILY.md) — if either mirror has no new sync-log row for 3+ days, mark `stale sync state: yes` and run a forced relevance scan.  
- **Framing note:** Mirrors are the operational spine for pulling work-dev / work-politics into Xavier-ready language.  
- **Primary implication:** Stale logs hide drift and block trustworthy daily ops cards.  
- **Contradiction / caution:** Operator may intentionally pause sync during travel; retire this watch row or add a dated exception rather than deleting the guardrail.

- **Watch:** Template alignment (companion-self vs grace-mar)  
- **First noticed:** 2026-04-04  
- **Current status:** watch  
- **Latest evidence:** [SYNC-DAILY.md](SYNC-DAILY.md) § Template alignment check; deep audit: [work-companion-self/README.md](../work-companion-self/README.md), `scripts/template_diff.py`.  
- **Framing note:** Advisor module should not silently diverge from template semantics that affect instance onboarding.  
- **Primary implication:** Pin `main` or a tag; batch reconciliation when drift is material.  
- **Contradiction / caution:** Instance-only WORK under `docs/skill-work/**` is expected; not every manifest diff requires a merge slice.

- **Watch:** Content plan vs SMM capability rubric  
- **First noticed:** 2026-04-04  
- **Current status:** watch  
- **Latest evidence:** [content-plan-week2-2026-03-31.md](content-plan-week2-2026-03-31.md) + [xavier-smm-capability-rubric.md](xavier-smm-capability-rubric.md).  
- **Framing note:** Plans assume execution bandwidth and channel maturity; rubric grounds honest gaps.  
- **Primary implication:** Before expanding scope, reconcile rubric scores with week KPI envelope.  
- **Contradiction / caution:** Rubric is operator judgment, not a performance review file for the Record.

---

## II-B. MEDIUM-TERM ROADMAP

Horizon: **not** next week — revisit when bandwidth allows; does not block daily [cici-notebook](cici-notebook/README.md) or [cici_journal_ob1_digest.py](../../scripts/cici_journal_ob1_digest.py) (GitHub API, no local clone required).

| Item | Intent | Notes |
|------|--------|--------|
| **Cici in grace-mar workspace** | Edit or cross-search **[Cici](https://github.com/Xavier-x01/Cici)** (Xavier’s OB1 **instance** repo) from the same Cursor workspace as grace-mar — e.g. sibling clone, `research/external/cici/` checkout, multi-root workspace, or symlink — plus optional **Cursor rule** (`globs` on that path) and/or **skill** for “Cici session” ritual (pull, branch, doc checklist). | Decide **submodule vs sibling clone** (avoid silent `git status` noise unless policy is clear). **Leakage / secrets** rules unchanged ([LEAKAGE-CHECKLIST.md](LEAKAGE-CHECKLIST.md)). Complements API digest; does not replace it. |

---

## III. LEARNING LEDGER

Stable heuristics and extended sections live in [README.md](README.md), [ALIGNMENT.md](ALIGNMENT.md), and [INDEX.md](INDEX.md). Append here only for short operator shorthand that does not fit those files.

---

## IV. LOCAL MEMORY / EXECUTION LOG

Prefer [work-cici-history.md](work-cici-history.md) for dated milestones and [SYNC-DAILY.md](SYNC-DAILY.md) for the daily snapshot.

---

## V. PROMOTION / RETIREMENT RECORD

Sparse changelog only — date, pointer, one line why (do not duplicate full II-A rows here).

- *(empty until used)*
