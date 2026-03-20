# Guardrail stress-test — advisor one-pager (message discipline)

**Purpose:** Reduce predictable failures when drafting or approving **high-stakes** political messaging (war powers, congressional ethics, sensitive economic or border claims). Methodology is **analogical** to factorial safety evaluation in structured AI triage research (e.g. independent 2026 work on clinical triage systems); this document is **not** medical advice.

**When to use:** Before final sign-off on briefs or social copy that could move markets, votes, or legal narratives if wrong or overconfident.

---

## Four failure modes (human checks)

| # | Mode | What goes wrong |
|---|------|-----------------|
| 1 | **Tail risk (“inverted U”)** | Strong on routine framing; **silent or weak** on rare but consequential scenarios (e.g. sudden shock + a war-powers vote). |
| 2 | **Reasoning vs output** | Internal notes flag a constitutional, ethics, or sourcing problem, but the **published** line softens or contradicts that tier of concern. |
| 3 | **Social anchoring** | Donor cues, poll toplines, or authority vibes **shift the conclusion** without new evidence. |
| 4 | **Guardrails on “vibe”** | Red-team or tone checks block emotional heat but **miss material** legal or corruption risk. |

---

## Factorial table (same facts, controlled pressure)

On one **base scenario** (one factual spine), document **variations** in a small table — same core facts, different pressures:

| Variation knob | Example |
|----------------|---------|
| Baseline | No extra pressure |
| + Social pressure | “Donor / colleague says it’s fine” |
| + Time pressure | “Vote in 48h” / “post tonight” |
| + Tail injection | Relevant shock (e.g. energy/chokepoint) |
| + Noisy polling | Contradictory or misleading poll framing |

**Pass criterion:** The **stated recommendation** for each row stays **consistent** with the **same risk tier** as your risk notes (no silent downgrade). Mismatch → **do not ship**; escalate.

---

## Operator sign-off

- **Reasoning–output alignment:** PASS / FAIL  
- If FAIL: revise or hold; do not publish the guarded line until PASS.  
- Optional audit log: team pipeline ledger may record `stress_test_passed` / `stress_test_failed` for traceability (tooling varies by organization).

---

*Internal implementation detail for staff using this repo: full WORK spec and template filenames live in the operator workspace; this page stays path-agnostic for advisor packets.*
