# In Civ-Mem: Difference Between STATE and SCHOLAR

**Purpose:** Clarify the distinction between **STATE** and **SCHOLAR** in the civilization_memory (CMC) model. These are internal operating modes of the *upstream* CMC system (e.g. `repos/civilization_memory` content/civilizations/CHINA). Grace-Mar’s copy in `docs/civilization-memory/` holds essays and notes; the STATE/SCHOLAR design comes from the upstream canon and is summarized here for reference. Full lessons for Grace-Mar: [docs/notes-cmc-substance.md](../../notes-cmc-substance.md).

---

## STATE

- **Learns from the present** — Operates on **live, current context**: the immediate situation, the decision at hand, the options in front of the actor.
- **Role** — Provides **structured decision-relevant options** (e.g. through perspectives such as legitimacy, power, liability). Surfaces choices; does not write the long-term record.
- **Tensions preserved** — Uses multiple perspectives; **tensions between perspectives are preserved, not resolved** (e.g. legitimacy vs power). No single “answer”; duty of competence is to surface all material options. This posture is named **polyphonic cognition** in civ-mem — see [concept-cognitive-polyphony.md](concept-cognitive-polyphony.md).
- **Does not feed Scholar by default** — Information from the present **does not** flow back into the long-term learning layer except via **explicit relay**. So “State” is the here-and-now; it does not update the ledger on its own.

**In Grace-Mar terms:** The **Session** (current conversation, present interaction) is like State. It can stage candidates to RECURSION-GATE, but it must not write to SELF or EVIDENCE directly. What happened “in session” only enters the Record when there is an explicit relay: stage → companion approval → merge (e.g. `process_approved_candidates`).

---

## SCHOLAR

- **Ledger only; no closure** — **Records learning events**, not conclusions. It is not a strategist, governor, or interpreter. It has no innate cognition; it makes no assumptions.
- **Non-synthesis rule** — May record contradictions, juxtapose models, preserve tensions; may **not** resolve contradictions or produce a single unified theory. “Scholar” is the layer that logs what was ingested and what patterns appear; it does not close the loop.
- **Zero prior belief** — Learns **only from MEM (memory) files explicitly ingested**. Absence of ingestion = absence of belief. No leakage from outside the corpus.
- **MEM authoritative over Scholar** — When an ingested fact (MEM) contradicts an established Scholar pattern, **flag the anomaly**; do not silently reconcile or substitute authority.
- **Doctrine comes from Scholar + human gate** — The canonical layer (Doctrine in CMC, SELF in Grace-Mar) is **derived exclusively from** Scholar syntheses that were **explicitly accepted** by a human (e.g. DIB in CMC, companion approval in Grace-Mar). The Doctrine/SELF file does not learn on its own.

**In Grace-Mar terms:** The **analyst** (signal detection, staging to RECURSION-GATE) is like Scholar: it records what was extracted and preserves contradictions; it does not merge. The **Record** (SELF, EVIDENCE) is the canonical layer that only changes when the companion approves what was staged — i.e. when Scholar output is explicitly accepted as “doctrine.”

---

## Summary Table

| | **STATE** | **SCHOLAR** |
|---|-----------|-------------|
| **Time** | Present, live context | Long-term; ingests MEM (memory) over time |
| **Role** | Decision-relevant options; multiple perspectives; tensions preserved | Ledger of learning events; record, don’t resolve |
| **Writes to canonical?** | No; only via **explicit relay** | No; only syntheses that are **explicitly accepted** (human gate) become Doctrine |
| **Grace-Mar analogue** | Session (current interaction); stages to gate, doesn’t write SELF | Analyst + staging; Record (SELF/EVIDENCE) only updates after companion approval |

**One line:** **STATE** = the present moment and the options it surfaces; it doesn’t write the long-term record unless explicitly relayed. **SCHOLAR** = the long-term learning ledger that records and preserves tensions and only affects the canonical layer when a human accepts its output.

**Product evolution:** STATE can be evolved into an **assistant brain product for heads of state** — see [state-evolved-assistant-brain-heads-of-state.md](../../skill-work/work-politics/state-evolved-assistant-brain-heads-of-state.md).
