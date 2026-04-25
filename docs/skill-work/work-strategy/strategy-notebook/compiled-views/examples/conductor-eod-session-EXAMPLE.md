# Example: Conductor EOD rehearsal checklist (hypothetical)

**Status:** EXAMPLE ONLY — fake `expert_id`s. **Not** a live session log.

**Purpose:** A **rehearsal** template for the operator-as-conductor before/during an EOD strategy session. Optional **mode** labels suggest which “baton” emphasis fits the day — without replacing [SYNTHESIS-OPERATING-MODEL.md](../../SYNTHESIS-OPERATING-MODEL.md) session types A–D.

---

## Session preamble

- [ ] **Session type** chosen (SYNTHESIS § 2 — A/B/C/D).
- [ ] **Primary intent (L0):** one line — what Judgment must warrant tonight.
- [ ] **Optional mode** (pick zero or one as emphasis):  
  - **Toscanini** — truth-to-form / verify / anti-indulgence before naming convergences.  
  - **Furtwängler** — preserve tension and emergence; do not force the clean story too early.  
  - **Bernstein** — embodied operator voice and heat in Chronicle/Reflection/Foresight (still score-anchored).  
  - **Karajan** — month-arc polish; economical edits; total balance across voices.  
  - **Kleiber** — selective pass only; chosen hotspots; no promote unless deeply prepared.

---

## Conductor prompts (always optional; use as hygiene)

- [ ] **Toscanini:** What is actually supported here, and where is rhetoric outrunning the score?
- [ ] **Furtwängler:** Which tension still needs to breathe before I resolve it?
- [ ] **Bernstein:** What must feel alive and legible here, not just accurate?
- [ ] **Karajan:** What should be cut or rebalanced so the whole arc reads cleanly?
- [ ] **Kleiber:** What deserves disproportionate attention, and what is explicitly not getting deepened tonight?
- [ ] **Memory run:** 2–5 minutes — replay convergences/tensions from the last 7–30 days *before* re-opening raw walls.
- [ ] **Score pass:** skim Machine layer + last `strategy-page` tails for involved `expert_id`s.
- [ ] **Read-aloud:** read Judgment once aloud (or subvocalize) for rhythm and overstuffed sentences.

---

## Conducting steps (hypothetical experts)

Replace `expert_red`, `expert_blue` with real **`thread:`** ids when working.

1. [ ] **Review the score:** `experts/expert_red/thread.md`, `experts/expert_blue/thread.md` — Machine + latest Journal / pages.
2. [ ] **Compose or revise** `strategy-page` blocks — Chronicle / Reflection / References / Foresight per template; keep seams visible.
3. [ ] **`days.md` continuity:** one consolidated `## YYYY-MM-DD` when one logical EOD pass — [architecture § days.md date keys](../../STRATEGY-NOTEBOOK-ARCHITECTURE.md#days-md-date-semantics).
4. [ ] **Markers:** add or update `[watch]` / `[decision]` / `[promote]` only where operator-owned.
5. [ ] **Verify-forward** if any claim may leave WORK (D-session discipline).
6. [ ] **Compiled view (optional):** run `python3 scripts/compile_strategy_view.py`; narrative Symphony pass **after** bundle if wanted — **light touch** on overlay if rehearsal already carried interpretation.

---

## Closeout

- [ ] **Open** lists the wire to tomorrow.
- [ ] **Links** back-pointers to raw-input / briefs as needed.
- [ ] **No Machine fence edits** from conductor hand — scripts only.

---

## See also

- [SYNTHESIS-OPERATING-MODEL.md § Operator as conductor](../../SYNTHESIS-OPERATING-MODEL.md#8-operator-as-conductor)
- [compiled-views/README.md](../README.md)
