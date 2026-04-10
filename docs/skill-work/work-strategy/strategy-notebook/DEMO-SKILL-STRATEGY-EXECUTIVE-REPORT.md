# Executive report — `skill-strategy` transcript demo (implementation)

**Audience:** Operator / work-strategy stakeholders  
**Date:** 2026-04-10  
**Subject:** Outcomes of delivering a **runnable calibration** for [`skill-strategy`](../../../../.cursor/skills/skill-strategy/SKILL.md) using three ingested analyst transcripts  
**Scope:** WORK territory only — not companion Record, not public campaign copy

---

## Executive summary

1. **Delivered:** A single operator playbook ([`DEMO-SKILL-STRATEGY-TRANSCRIPTS.md`](DEMO-SKILL-STRATEGY-TRANSCRIPTS.md)), a **read-only preflight script** ([`scripts/demo_skill_strategy_transcripts_check.sh`](../../../../scripts/demo_skill_strategy_transcripts_check.sh)), and **discoverability** links from the strategy-notebook [`README.md`](README.md) and [`work-strategy-history.md`](../work-strategy-history.md). Baseline commit: `601be32`.

2. **Corpus:** Three **2026-04-10** transcript digests are present and indexed (Diesen × Mearsheimer; Mercouris Good Friday; Davis × Crooke). The preflight script confirms on-disk presence; it does **not** judge analytical quality.

3. **Design intent:** The demo exercises **notebook-first** judgment, **strategy + verify** on at least one load-bearing claim, **compression** across three sources without triple recap, and an **explicit tri-frame** (Mercouris → Mearsheimer → Barnes) aligned with [Recipe C](../minds/MINDS-SKILL-STRATEGY-PATTERNS.md) — satisfying [granular minds](../../../../.cursor/rules/strategy-minds-granular.mdc) by requiring an explicit **“Tri-frame, strict”** (or LEARN MODE) trigger.

4. **Live calibration results:** **Not recorded in this repository.** Phases 1–5 are **operator-executed** in Cursor; pass/fail scores belong in the **results log template** at the bottom of the demo doc (or appended to `days.md` / a scratch file). This report therefore summarizes **delivery and readiness**, not a completed scoring run.

5. **Recommendation:** Run the full track (~75–110 minutes estimated) once, archive the filled **results log** next to this file (e.g. `demo-runs/skill-strategy-results-YYYY-MM-DD.md`), and only then treat **skill-strategy** calibration as **evidence-backed** for process audits.

---

## Objectives (what “success” meant for this initiative)

| Objective | Status |
|-----------|--------|
| Reproducible steps an operator can follow without ad hoc invention | **Met** — phased prompts and pass/fail tables in demo doc |
| Grounding in real ingested artifacts (not chat-only) | **Met** — three repo paths fixed in script and doc |
| Demonstrate **verify** discipline for fragile numbers | **Designed** — Phase 2; execution pending |
| Demonstrate **three minds** without defaulting tri-frame on every pass | **Designed** — Phase 4 explicit trigger; execution pending |
| Avoid Record merge and STRATEGY.md drift during demo | **Designed** — Phase 5 negative tests; execution pending |

---

## Deliverables

| Artifact | Role |
|----------|------|
| [`DEMO-SKILL-STRATEGY-TRANSCRIPTS.md`](DEMO-SKILL-STRATEGY-TRANSCRIPTS.md) | End-to-end script: Phases 0–5, rubric, results template |
| [`scripts/demo_skill_strategy_transcripts_check.sh`](../../../../scripts/demo_skill_strategy_transcripts_check.sh) | Preflight: exit 0 iff all three digest files exist |
| [`README.md`](README.md) (strategy-notebook) | Demo / calibration pointer |
| [`work-strategy-history.md`](../work-strategy-history.md) | Lane log line (2026-04-10) |

---

## Verification performed (automated)

- **Preflight script:** Confirms paths to the three digest markdown files. **Does not** validate URLs inside digests, Perceiver word counts, or analyst claims.

---

## What a completed run will prove (when logged)

When the operator finishes Phases 1–5 and fills the rubric, the **demonstrated capabilities** are:

- **Notebook-primary** synthesis linked to inputs (not duplicate Perceiver blocks).
- **Web verification** subsection for at least one time- or market-sensitive claim (Phase 2).
- **Cross-transcript compression** without triple narrative (Phase 3).
- **Tri-frame** with all three trimmed minds and corpus-tied sentences (Phase 4).
- **Boundary compliance:** refusal patterns on unverified facts and unpromoted STRATEGY edits (Phase 5).

---

## Risks and limitations

| Risk | Mitigation |
|------|------------|
| Demo fatigue / skipped Phase 4 | Full demo is labeled **recommended**; partial runs must be marked **partial** in the results log |
| Paywalled or moving sources (e.g. FT quotes in Mercouris digest) | Phase 2 allows substituting another verifiable claim; doc says so |
| Agent noncompliance with boundaries | Phase 5 negative prompts are explicit; failures should be noted in results log |
| Confusion between Recipe C **analysis order** (M → M → B) and SKILL **menu order** (B → M → M) | Clarified inside [`DEMO-SKILL-STRATEGY-TRANSCRIPTS.md`](DEMO-SKILL-STRATEGY-TRANSCRIPTS.md) |

---

## Next actions

1. Run `bash scripts/demo_skill_strategy_transcripts_check.sh` from repo root before each session.
2. Execute Phases 0–5 per the demo doc; paste prompts in Cursor as written.
3. Save the **results log template** output to a dated file under `strategy-notebook/demo-runs/` (optional folder) or append scored subsections to [`chapters/2026-04/days.md`](chapters/2026-04/days.md).
4. Optionally append a one-line summary row to this executive report or to `work-strategy-history.md` when a **full** run completes.

---

## Appendix — rubric snapshot (from demo doc)

Criteria scored Pass / Fail / Notes: notebook-primary; verify discipline; links complete; tri-frame / three minds; contradiction preservation; no STRATEGY touch; WORK boundary; anti–triple recap. Per-mind spot check: Mercouris, Mearsheimer, Barnes each corpus-tied in Phase 4.

---

*This file is an implementation and readiness summary. Replace or extend with a “Calibration run — YYYY-MM-DD” section after the first completed scored run.*
