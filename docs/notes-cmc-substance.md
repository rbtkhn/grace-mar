# CMC Intellectual Substance — Lessons for the Cognitive System

Lessons drawn from the **content** of civilization_memory CHINA files (CIV–CORE, CIV–DOCTRINE, CIV–STATE, CIV–SCHOLAR), not just their structure. Source: [civilization_memory/content/civilizations/CHINA](https://github.com/rbtkhn/civilization_memory/tree/main/content/civilizations/CHINA).

---

## 1. Identity as axioms; knowledge as derived

**CMC:** CORE opens with "Civilizational Identity & Prime Axioms" (continuity, mandate, absorption, harmony-over-freedom, civilization-as-administration). They are **locked** — they define what the entity *is*, not episodic facts.

**Grace-Mar application:** Treat the Record as two layers: (1) **Stable identity** — who the companion is (values, reasoning style, linguistic fingerprint), updated rarely and only through the gate; (2) **Accreted knowledge/curiosity** — IX-A, IX-B, EVIDENCE, updated by pipeline. Identity is axiom-like; knowledge is derived and evidence-linked.

---

## 2. Continuity: stack layers, don't reset

**CMC:** "China does not exit historical layers; it stacks and reuses them." Active memory layers (Zhou, Qin–Han, Tang, …) remain in play. "Every reform is interpreted through inherited memory before execution."

**Grace-Mar application:** The Record is additive and layered. New content is interpreted **through** existing SELF/EVIDENCE before merge; no "forget and restart." Aligns with derivation log, EVIDENCE immutability, and "history preserved" in SELF.

---

## 3. Doctrine = Scholar synthesis + explicit human acceptance

**CMC:** Doctrine is **derived exclusively from** SCHOLAR syntheses that were **explicitly accepted as doctrine via DIB–CHINA** (human gate). "This file does NOT learn, does NOT synthesize, does NOT evolve autonomously."

**Grace-Mar application:** Exact model of the gated pipeline: stage (Scholar/analyst) → human approval (DIB / companion) → merge into canonical layer (Doctrine / SELF). Canonical beliefs live in a file that does not learn on its own.

---

## 4. Doctrine carries hard constraints (falsification conditions)

**CMC:** Each doctrine has **Hard constraints** — conditions under which it would be wrong or narrow (e.g. "If X routinely failed, doctrine scope narrows").

**Grace-Mar application:** IX entries (or future "doctrine" entries) could carry explicit **scope/constraint**: when the belief does *not* apply or when it would be invalid. Improves precision and auditability.

---

## 5. Scholar: ledger only; no closure

**CMC:** "It is not a strategist, governor, or interpreter. It has no innate cognition. It makes no assumptions. It **records learning events, not conclusions**." Non-synthesis rule: may record contradictions, juxtapose models, preserve tensions; may **not** resolve contradictions or produce unified theories.

**Grace-Mar application:** The analyst/staging layer records what was extracted and preserves tensions; it does not silently resolve conflicts. Closure lives only in the gated canonical layer (AGENTS 5a contradiction preservation).

---

## 6. Zero prior belief; only ingested content

**CMC:** "Starting Knowledge: ZERO. Assumed Priors: NONE. The SCHOLAR learns **only from MEM files explicitly ingested**. Absence of ingestion equals absence of belief."

**Grace-Mar application:** Knowledge boundary: no belief without evidence; no LLM leakage. The Voice only "knows" what is in the Record (and what it is explicitly allowed to look up). Already enforced in prompt and pipeline.

---

## 7. MEM facts authoritative over Scholar interpretation

**CMC:** "MEM facts are authoritative; SCHOLAR constraints are interpretive. When a MEM assertion contradicts an established SCHOLAR pattern, flag the anomaly explicitly. Authority substitution and silent reconciliation are forbidden."

**Grace-Mar application:** Evidence (EVIDENCE) over interpretation (SELF) when they conflict. Flag the tension; preserve both; never silently overwrite (contradiction preservation).

---

## 8. State learns from present; doesn't feed Scholar unless relayed

**CMC:** STATE "learns from the present" and provides "structured decision-relevant options." "Information does **not** feed back into Scholar except via **explicit relay**."

**Grace-Mar application:** Session (present interaction) can stage but must not write to SELF directly. Moving from "State" into the Record happens only via explicit relay (e.g. "we did X" → stage → approve → merge). One-way flow by default.

---

## 9. Duty of competence: completeness, not one answer

**CMC:** "Duty of competence: surface **all material options** through [three perspectives]. Failure to apply any perspective = completeness violation. When the decision involves a commitment, the option set **MUST** include at least one option at the accommodation/reversal end."

**Grace-Mar application:** When the Voice answers or suggests, it can have a **completeness obligation**: surface all **documented** relevant angles from the Record; when there are conflicting beliefs, offer both (or "some think X, others Y") rather than picking one. Reinforces abstention and contradiction preservation in behavior.

---

## 10. Three perspectives; tensions preserved

**CMC:** STATE uses three perspectives (legitimacy, power, liability); "**Tensions between perspectives (preserved, not resolved)**" — e.g. legitimacy vs power, power vs liability.

**Grace-Mar application:** When the Record holds multiple views on the same topic, the Voice can present them as perspectives and leave the tension explicit instead of collapsing to one answer.

---

## 11. Mandatory structured outputs (verdict block)

**CMC:** CORE requires a **mandatory verdict block** — a fixed set of outputs (MSI, PLS, SOC, etc.) that the engine must produce.

**Grace-Mar application:** Define a **response contract** for the Voice: e.g. every answer must (1) stay inside knowledge boundary or explicitly abstain, (2) cite or imply source (Record vs lookup), (3) when relevant, preserve multiple perspectives. Makes Voice behavior auditable.

---

## Summary table

| # | CMC idea | Grace-Mar application |
|---|----------|------------------------|
| 1 | Identity = locked axioms; knowledge = derived | Stable identity layer vs accreted IX-A/B/C |
| 2 | Stack layers; interpret through inherited memory | Additive Record; new input through existing SELF |
| 3 | Doctrine = synthesis + human acceptance only | Stage → approve → merge; canonical file doesn't learn |
| 4 | Hard constraints per doctrine | Optional scope/constraint on IX entries |
| 5 | Scholar: ledger only; record tensions, don't resolve | Analyst stages; preserve contradictions |
| 6 | Zero prior belief; only ingested | Knowledge boundary; no LLM leakage |
| 7 | MEM authoritative over Scholar; flag anomalies | EVIDENCE over SELF; flag, don't silently reconcile |
| 8 | State → Scholar only by explicit relay | Session stages; only explicit pipeline writes to Record |
| 9 | Duty of competence: all options, include reversal | Surface all documented angles; include abstain/lookup |
| 10 | Three perspectives; tensions preserved | Present multiple Record perspectives; don't collapse |
| 11 | Mandatory verdict/response contract | Minimal structured guarantees per Voice response |

---

See also: [IMPLEMENTABLE-INSIGHTS](implementable-insights.md) (structure/skills), [IMPLEMENTABLE-OPTIMIZATIONS-FROM-CMC](implementable-optimizations-from-cmc.md) (proposed code and prompt changes).
