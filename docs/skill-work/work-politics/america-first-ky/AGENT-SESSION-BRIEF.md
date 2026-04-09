# Agent session brief — America First KY guardrail stress-test (Mount Sinai–inspired)

**For:** Next Cursor / agent session  
**Goal:** Extend WORK methodology for factorial guardrail stress-testing **without** violating repo governance (AGENTS.md, gated Record, analytical-lenses discipline).

---

## Do not run the circulated shell block

A terminal one-liner has been shared that:

- Creates `work-politics/america-first-ky` at **repo root** — **wrong**. Canonical path is `docs/skill-work/work-politics/america-first-ky/` (this folder).
- **Appends** fake functions to `scripts/governance_checker.py` — **reject**. That file is a **regex scanner** for merge/SELF violations, not a reasoning engine. Undefined helpers would **break CI**.
- **Appends** to `users/grace-mar/skills.md` — **reject**. Record file; use **RECURSION-GATE** + `process_approved_candidates.py` only after companion approval.
- Logs traces to `self-evidence/guardrail-flywheel.md` — **reject** for routine runs. Use WORK docs + optional ACT- via gate only.
- Introduces automated **“reasoning-output alignment score”** in checker — **reject** unless separately designed as WORK-only metrics (analytical lenses manifest: discipline is **operator/process**, not automated drift scoring in checker).

**Status:** Compliant docs are **already added** in this folder. Remaining work is **integration and optional tooling**, not the shell script.

---

## What is already done (this commit / folder)

| Artifact | Path |
|----------|------|
| Proactive loop | [proactive-loop.md](proactive-loop.md) — scheduled-loop discipline, gated primitives, loop logging |
| Daily loop template | [templates/daily-loop-brief.md](templates/daily-loop-brief.md) |
| Loop history (WORK) | [loop-history.md](loop-history.md) — append-only; not `self-evidence.md` |
| Massie WORK voice | [massie-advisor-prompt.md](massie-advisor-prompt.md) — not `bot/prompt.py` |
| Cron / habit examples | [scheduled-habit.md](scheduled-habit.md) |
| Loop event helper | [emit_loop_event.py](../../../scripts/emit_loop_event.py) — subprocess wrapper for `loop_cycle_*` |
| Framework | [guardrail-stress-test.md](guardrail-stress-test.md) |
| Template | [stress-test-brief-template.md](stress-test-brief-template.md) |
| Index | [README.md](README.md) |

**Do not** re-paste the circulated shell block that creates `work-politics/` at repo root or patches `governance_checker.py` / `skills.md` — see § “Do not run” above. Use the files in this table instead.

**Science citation:** Framework is **inspired by** Mount Sinai / Nature Medicine ChatGPT Health factorial safety evaluation (2026). Political use is **analogical**; not medical advice.

---

## RECURSION-GATE

**CANDIDATE-0089** (pending) should be in `users/grace-mar/recursion-gate.md` for optional Record-adjacent / skills bullet on approval. **Do not** edit `skills.md` until approved.

---

## Recommended next tasks (in order)

**Status (2026-03-20):** Items 1–5 implemented — weekly brief §8 + account-x wiring, `scripts/scaffold_stress_test_brief.py`, pipeline-event notes in [README.md](README.md), advisor one-pager [guardrail-stress-test-advisor-one-pager.md](../../../externals/massie/guardrail-stress-test-advisor-one-pager.md), governance + canonical-path checks passed.

**Follow-up:** Operator skills + `docs/operator-skills.md` now surface §8 / `america-first-ky` for `weekly-brief-run`, `operator_work_politics_pulse.py`, and `coffee` related-file discovery.

1. **Wire templates into operator habit**  
   - Add a short § to [weekly-brief-template.md](../weekly-brief-template.md) or [account-x.md](../account-x.md): “High-stakes briefs → complete `america-first-ky/stress-test-brief-template.md`.”  
   - **Done:** §8 in weekly template; paragraph under account-x workflow.

2. **Optional: prototype script** (no checker integration)  
   - e.g. `scripts/scaffold_stress_test_brief.py` that copies the template to `docs/skill-work/work-politics/america-first-ky/stress-test-brief-YYYY-MM-DD.md` with issue slug.  
   - Must not write Record files.  
   - **Done:** [scaffold_stress_test_brief.py](../../../../scripts/scaffold_stress_test_brief.py)

   **Daily loop brief:** [scaffold_daily_loop_brief.py](../../../../scripts/scaffold_daily_loop_brief.py) copies [templates/daily-loop-brief.md](templates/daily-loop-brief.md) to a dated file (optional slug). **Done.**

3. **Pipeline events**  
   - Document only; operators run `emit_pipeline_event.py` with types like `stress_test_passed` / `stress_test_failed`. No change **required** to `emit_pipeline_event.py` (it already accepts arbitrary `event_type`).  
   - **Done:** [README.md § Pipeline events](README.md#pipeline-events-operator-only-audit)

4. **External pack**  
   - Optional one-pager in `docs/externals/massie/` summarizing “four failure modes + factorial table” for advisors (no internal paths if desired).  
   - **Done:** [guardrail-stress-test-advisor-one-pager.md](../../../externals/massie/guardrail-stress-test-advisor-one-pager.md)

5. **Verification**  
   - `python scripts/governance_checker.py`  
   - `python scripts/assert_canonical_paths.py`  
   - **Done:** both exit 0 (re-run after future edits).

---

## Explicit non-goals

- No merge into `self.md` / `self-evidence.md` / `prompt.py` from this session without gate + script.
- No new automated enforcement in `governance_checker.py` for semantic “alignment.”
- No `self-evidence` flywheel file for full traces.

---

## Re-entry prompt for operator

Paste into a new chat:

> Read `docs/skill-work/work-politics/america-first-ky/AGENT-SESSION-BRIEF.md` and [proactive-loop.md](proactive-loop.md). Complete any remaining “Recommended next tasks.” Do not patch `governance_checker.py` with fake alignment functions or append `skills.md` directly. Stage any Record change via RECURSION-GATE only.
