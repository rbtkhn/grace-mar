# OB1 Bridge — Trust Tiers

Classifies every object that crosses the bridge by the reliability of its content. Trust tiers determine **handling rules** — what review is required, what surfaces are eligible, and what can be rejected automatically.

**Related:** [mapping.md](mapping.md) (field definitions), [architecture.md](architecture.md) (safety model).

---

## Tier definitions

| Tier | Label | Definition | Examples |
|------|-------|------------|----------|
| **A** | Raw evidence | Content that directly reflects companion actions, statements, or artifacts with minimal interpretation. High confidence that it represents ground truth. | EVIDENCE entries (ACT, READ, WRITE, CREATE, MEDIA), companion-written text, artifact files, approved SELF content |
| **B** | Structured summary | Content derived from raw evidence through aggregation, formatting, or light synthesis. The underlying facts are grounded but the presentation involves editorial choices. | Structured IX-A/B/C entries derived from multiple signals, self-memory continuity notes, skill assessments built from evidence |
| **C** | Synthesized output | Content produced by an AI agent, model, or automated process. May contain useful signals but is not grounded in direct companion input. Mixed trust — requires filtering. | OB1 thoughts from agent sessions, model-generated summaries, auto-tagged metadata, speculative inferences |

---

## Handling rules by tier

### Tier A — Raw evidence

| Rule | Detail |
|------|--------|
| **Export to OB1** | Eligible by default. These are the highest-value chunks for OB1 retrieval. |
| **Import from OB1** | If OB1 holds Tier A content that originated from companion-self, it is likely a re-import. Dedup by fingerprint. If OB1 holds original Tier A content (e.g. companion typed directly into an OB1 client), treat as a new evidence candidate — stage to gate. |
| **Auto-reject** | Never. Tier A content always receives human review. |
| **Target surfaces** | `IX-A`, `IX-B`, `IX-C`, `evidence`. All Record surfaces are eligible. |
| **Review priority** | High. Tier A proposals should surface at the top of review queues. |

### Tier B — Structured summary

| Rule | Detail |
|------|--------|
| **Export to OB1** | Eligible but excluded by default (memory, work surfaces). Opt in with `--include memory` or `--include work`. |
| **Import from OB1** | Stage to gate with a note that content is derived, not raw. Reviewer should verify the underlying evidence exists. |
| **Auto-reject** | No, but flag if no grounding evidence is cited. |
| **Target surfaces** | `IX-A`, `IX-B`, `IX-C`, `memory`. Record surfaces require stronger justification than Tier A. `memory` is the safe default. |
| **Review priority** | Medium. Review after all Tier A proposals. |

### Tier C — Synthesized output

| Rule | Detail |
|------|--------|
| **Export to OB1** | Not exported by default. Work-territory content is operator-scoped and mixed-trust. |
| **Import from OB1** | Stage only if grounding score passes threshold. Most Tier C thoughts should be filtered before staging. |
| **Auto-reject** | Yes, if grounding score is below threshold. Threshold is configurable; default is conservative (reject unless clearly grounded). |
| **Target surfaces** | `memory` (ephemeral pointer) or `reject`. Tier C content does not enter Record surfaces without explicit operator override. |
| **Review priority** | Low. Review only after Tier A and B proposals are cleared. |

---

## Grounding score

The grounding score quantifies how well an OB1 thought connects to verifiable companion input. It is computed by the `score_grounding()` filter function.

| Score range | Interpretation | Default handling |
|-------------|---------------|------------------|
| 0.0 – 0.3 | Low grounding — likely model-generated, speculative, or generic | Auto-reject (Tier C) or flag for review (Tier B) |
| 0.3 – 0.6 | Partial grounding — some companion signal but mixed with inference | Stage with flag; reviewer decides |
| 0.6 – 1.0 | Strong grounding — clear companion input, specific details, verifiable | Stage normally |

### Grounding signals (inputs to score)

| Signal | Weight | Description |
|--------|--------|-------------|
| Companion-attributed text | High | The thought quotes or paraphrases something the companion said |
| Specific names, dates, or events | High | Concrete details that can be cross-referenced with EVIDENCE |
| First-person companion voice | Medium | Written from the companion's perspective, not an observer's |
| Temporal specificity | Medium | References a specific time, session, or activity |
| Generic or abstract language | Negative | Vague statements that could apply to anyone |
| Model hedging language | Negative | "It seems like," "perhaps," "based on our conversation" without specifics |
| Contradiction with existing Record | Flag | Does not reduce score but flags for explicit review |

---

## Trust tier assignment flow

```
OB1 thought
    │
    ▼
Is the content directly attributable
to a companion action or statement?
    │
    ├─ Yes ──> Tier A (raw evidence)
    │
    ▼
Is the content derived from identifiable
evidence through aggregation or formatting?
    │
    ├─ Yes ──> Tier B (structured summary)
    │
    ▼
Tier C (synthesized output)
    │
    ▼
Run grounding score
    │
    ├─ Score < 0.3 ──> Auto-reject
    ├─ Score 0.3-0.6 ──> Stage with flag
    └─ Score ≥ 0.6 ──> Stage normally
```

---

## Tier escalation and override

- **Tier can only be upgraded by the operator** during review. The import script assigns the initial tier; the reviewer may override upward (e.g. Tier C → Tier B if they recognize grounded content the filter missed).
- **Tier cannot be auto-upgraded.** No script or automated process may reclassify a thought to a higher tier without human review.
- **Override is logged.** If the operator overrides a tier assignment, the proposal object records `{ original_tier, override_tier, override_reason }`.

---

## Relationship to existing pipeline

Trust tiers are a **bridge-specific** classification. They do not replace or modify the existing RECURSION-GATE candidate model. The relationship:

| Bridge concept | Pipeline equivalent |
|----------------|-------------------|
| Tier A proposal | High-confidence candidate (knowledge, personality, evidence) |
| Tier B proposal | Candidate that may need additional evidence before merge |
| Tier C proposal (staged) | Low-confidence candidate; reviewer may reject or defer |
| Auto-rejected Tier C | Never becomes a candidate; filtered before gate |

The gate's `status: pending` / `approved` / `rejected` flow is unchanged. Trust tiers add pre-gate filtering and review prioritization, not a parallel governance track.
