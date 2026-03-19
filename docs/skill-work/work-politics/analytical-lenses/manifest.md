# Analytical lenses manifest — work-politics (WORK only)

**Status:** Operator methodology. **Not** part of SELF, SELF-LIBRARY identity, or Voice unless the companion explicitly approves merges through RECURSION-GATE.

**Purpose:** Triangulated read-only **editorial lenses** for current-events and brief work. They enrich perspective; they do not replace human strategy, compliance review, or final approval for anything public-facing.

---

## Authorized trio (2026-03)

| Lens file | Role |
|-----------|------|
| [lens-structural-realism.md](lens-structural-realism.md) | Long-horizon structure, incentives, security dilemmas |
| [lens-operational-diplomatic.md](lens-operational-diplomatic.md) | Near-term signals, feasibility, diplomatic/military narrative |
| [lens-institutional-domestic.md](lens-institutional-domestic.md) | Domestic institutions, law and incentives, who benefits |

Run all **three** on the **same neutral fact summary** when using this framework. Do not treat one lens as authoritative alone.

---

## Rules (human-enforced)

1. **Parallel inputs** — Each lens answers from the same neutral fact summary (no lens-specific cherry-picking of unrelated facts).
2. **Outputs are drafts** — Grace-Mar core / operator performs final synthesis; nothing ships without human sign-off ([consulting-charter.md](../consulting-charter.md), [civ-mem-draft-protocol.md](../civ-mem-draft-protocol.md)).
3. **Contradictions are signal** — Where lenses disagree, **surface the tension**; do not flatten for narrative smoothness. Aligns with contradiction preservation in the [CONTRADICTION-ENGINE-SPEC](../../../CONTRADICTION-ENGINE-SPEC.md) spirit.
4. **No automated governance hooks** — This workflow is **not** enforced by `governance_checker.py` (that script scans Python for risky Record writes). Discipline is operator/process.
5. **Logging** — Do **not** append full deliberation traces to `self-evidence.md`. Use:
   - **WORK docs** (this folder, brief markdown, content queue notes), and/or
   - **`session-transcript.md`** / operator logs for session continuity, and/or
   - **Optional ACT- milestone** via RECURSION-GATE when the companion wants an audit line (“we published triangulated brief vN”) — merge only after approval and `process_approved_candidates.py`.
6. **Knowledge boundary** — Lenses do not expand what the Voice “knows.” Do not compile lens personas into `bot/prompt.py` unless the companion gates that explicitly ([knowledge-boundary-framework.md](../../../knowledge-boundary-framework.md)).
7. **CIV-MEM** — Final synthesis may cite governed library / CMC lookups like any other WAP draft; citations do not auto-enter the Record.

---

## Disclaimer

Lens labels reference **well-known analytical styles** for operator clarity only. They **do not** speak for, endorse, or impersonate any person; no affiliation is implied. See each lens file.

---

## Optional Record pointer (`skills.md`)

If the companion wants a **capability note** linking to this methodology, add it via **RECURSION-GATE** (stage → approve → `process_approved_candidates.py`). Do **not** edit `skills.md` directly without that path. A pending WAP candidate may exist for a minimal IX-A WORK line + audit; a dedicated skills claim would require a candidate shaped for whatever the merge script supports (today: primarily SELF IX / prompt / EVIDENCE).

---

## See also

- [template-three-lenses.md](template-three-lenses.md) — paste block for briefs and threads
- [work-politics README](../README.md) — territory and gate sync
