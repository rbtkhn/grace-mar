# Agent reliability playbook (work-build-ai)

**Purpose:** Encode failure patterns observed in rigorous agent evaluations (including clinical triage studies) so work-build-ai engagements and Grace-Mar-adjacent agent design treat **correct action** as the metric—not average accuracy or plausible reasoning traces.

**Pattern lens:** Findings from structured evaluations of conversational health tools illustrate behaviors that appear across **domains** (finance, ops, political consulting, OpenClaw workflows). This doc does **not** make medical claims; it uses those studies as a **lens** for agent failure modes.

**See also:** [variation-types.md](variation-types.md) (factorial stressors), [known-gaps.md](known-gaps.md) (BUILD-AI-GAP-005+), [scripts/counterfactual_pack/readme.md](../../../scripts/counterfactual_pack/readme.md) (Voice harness slice).

---

## Four failure modes

### 1. Inverted-U (tails vs middle)

Agents often perform well on **textbook** and **obviously trivial** cases. Failures cluster at **distribution edges**: presentations that are subtly off-template, or benign-looking cases that mimic high severity.

- **So what:** Aggregate accuracy (e.g. “87%”) **hides** tail failures where stakes are often highest.
- **So what for work-build-ai:** No engagement is “eval complete” on a single happy path. Inventory **high-stakes tails** explicitly (see [delivery-playbook](delivery-playbook.md)).

### 2. Reasoning vs action mismatch

Internal or displayed “reasoning” may **correctly identify** a situation while the **final recommendation contradicts** it (e.g. acknowledge urgency, then advise delay). Research on chain-of-thought **faithfulness** shows reasoning traces are **not** reliable audits of why the model chose an action.

- **So what:** Do not treat CoT as compliance or safety evidence.
- **So what for work-build-ai:** Add **deterministic checks**: if structured analysis says X and output classifies or acts as not-X, **escalate**—use rules or human review, not “ask the model if it’s consistent.”

### 3. Social / narrative anchoring

Unstructured framing (“the patient looks fine,” “VP is confident this vendor is right”) can **shift** recommendations even when **structured facts** are unchanged—often subtly, case-by-case defensible but **systematically biased**.

- **So what:** Separate **facts** from **opinion / social pressure** in prompts and handback payloads.
- **So what for work-build-ai:** Use [variation-types.md](variation-types.md) to A/B the same scenario with and without anchoring text; measure shift.

### 4. Guardrails on vibes, not risk

Safety or policy layers may trigger on **tone or keywords** rather than on a **risk taxonomy** (what must never be missed).

- **So what:** Test guardrails against **true positives** and **false negatives**, not just “looks safe.”
- **So what for work-build-ai:** Define **must-catch** outcomes per workflow; eval against those—not generic “blocked bad words.”

---

## Four-layer mitigation architecture

| Layer | Intent | Work-build-ai hook |
|-------|--------|-------------------|
| **1. Progressive autonomy** | High-confidence low-stakes → agent; tails → human or shadow mode until proven. | Name **autonomy tier** per workflow in architecture phase; shadow agent vs human on edge cases. |
| **2. Deterministic validation** | Rules / code compare **stated analysis** vs **action or classification**; flag mismatch. | Handback schemas, post-stage scripts, or human checklist—not LLM-self-critique alone. |
| **3. Eval flywheel** | Bias toward **flagging** on risk; review false positives; **sample passed runs** and turn misses into new cases. | After each sprint, add failed or near-miss runs to scenario library. |
| **4. Factorial stress** | Same base scenario × controlled variations (anchoring, time pressure, contradiction). | Use [variation-types.md](variation-types.md); one pilot workflow per engagement when stakes warrant. |

---

## Grace-Mar mapping

| Mechanism | Role |
|-----------|------|
| **Companion gate** | Human approval before Record merge—limits irreversible harm from bad staging. |
| **Stage-only OpenClaw** | Artifacts enter as candidates; blast radius bounded vs auto-merge. |
| **Counterfactual harness** | Small **tail/abstain/over-offer** slice for **Voice** (`run_counterfactual_harness.py`), including **CF-ANCH-*** anchoring-stress probes. Not a full factorial library for arbitrary client agents. |
| **Knowledge boundary** | Voice must not invent profile facts—aligns with failure mode 2/4 at companion scale. |

---

## Vocabulary (use in SOWs and reviews)

- **Tail scenario** — High stakes or ambiguous; not the average case.
- **Factorial variation** — Same scenario + one stressor; compare outputs.
- **Progressive autonomy** — Expand agent scope only as evals justify.
- **Deterministic validation** — Non-LLM check that action matches stated risk/analysis.

---

*Last updated: March 2026*
