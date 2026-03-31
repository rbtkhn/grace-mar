---
name: handoff-check
preferred_activation: handoff check
description: Run operator_handoff_check.py for RECURSION-GATE pending, Predictive History night closeout, commits, worktree noise, re-entry prompt — read-only. On **closeout coffee** (same trigger **coffee**, signing-off intent; legacy **hey** still works), this script is **coffee Step 1**; **Step 2** is the fixed **A–H** menu — **A–D** match work-start **coffee** (**D** = RECURSION-GATE); **E** = system pick; **G** = Jiang/PH; **H** = skills pipeline; **F** = end closeout. See `coffee` § *Coffee — closeout*, § *Shared A–C*, § *Shared D*, § *Shared G-H*. Also use when resuming work or checking safe-to-ignore before commit/push.
---

# Handoff Check

**Preferred activation (operator):** say **`handoff check`** (or **`use handoff-check`**).

Use this skill when the operator wants to pause or resume work without losing the active thread.

**Preset — closeout:** When the operator says **`coffee`** with **closeout intent** (session end, signing off; legacy **`hey`** still works), the agent runs **closeout Step 1** (this command + summary) then **closeout Step 2** (A–H menu) — **A–D** match work-start **coffee**; see [coffee/SKILL.md](../coffee/SKILL.md) § *Shared A–C*, § *Shared D*, § *Shared G-H*, § **Coffee — closeout**, and § **Coffee — closeout — multiple choice**. On follow-up turns, **A,B,C,D,E,G, or H** runs the track then **re-offers the full A–H menu** until **F** ends the closeout pass.

**Work-start coffee (related):** After **A,B,C,D, or H**, **re-offer the full A–H menu** by default until **F**. Concrete work-lane picks under **E** or **G** exit to normal workflow unless the operator says **`stay in coffee`** — same closeout distinction remains (work-start **D** = RECURSION-GATE; closeout **E** = system pick); see [coffee/SKILL.md](../coffee/SKILL.md) § *Coffee — multiple choice (A–H required)*.

## Default command

```bash
python3 scripts/operator_handoff_check.py -u grace-mar
```

**Cold-thread stack (optional):** `python3 scripts/operator_reentry_stack.py -u grace-mar` runs handoff check, then `operator_daily_warmup.py`, then `harness_warmup.py` (add `--compact` for a shorter harness). **One-line snapshot:** `python3 scripts/harness_warmup.py -u grace-mar --receipt`. See `bootstrap/grace-mar-bootstrap.md` § Re-entry stack.

## What to return

Summarize:

- **RECURSION-GATE** — pending totals (work-politics vs companion), listed items if any (script caps long queues), and the script’s **proposed** processing steps (`operator_gate_review_pass` → approve/reject in-file → `process_approved_candidates.py`); remind that **merge requires companion approval**
- **Predictive History (work-jiang)** — **`## Predictive History — night closeout`**: where the lane rests, suggested first lever tomorrow, rotating **Spark** (edit `research/external/work-jiang/metadata/warmup-sparks.yaml`), optional rebuild ritual; still read-only / not Record
- recently committed work
- meaningful local changes still in progress
- **`## Derived / export churn`** — PRP, manifest, ledger, etc. (regenerate or batch-commit vs editorial work)
- runtime-only noise that should stay uncommitted
- work-politics continuity if relevant
- the best next re-entry prompt
- **Skill discovery (one line, optional):** If the thread had a repeatable multi-step workflow, mention [skills-portable/skill-candidates.md](../../../skills-portable/skill-candidates.md) and **menu H** (skills / meta pipeline) / [extract-skill-from-session](../extract-skill-from-session/SKILL.md) — do not block the handoff on it.

## Guardrails

- Distinguish runtime noise from real local work before recommending any commit or push.
- This is a summary workflow only. Do not stage, commit, or merge as part of the handoff.
- If local changes mix unrelated threads, say so clearly.

## Related files

- `docs/operator-skills.md`
- `docs/development-handoff.md`
- `users/grace-mar/recursion-gate.md`
