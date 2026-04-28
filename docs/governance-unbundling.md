# Governance unbundling in cognitive forks

**Purpose:** Name how **routing**, **sensemaking**, and **accountability** split in companion-self style systems so agents and contributors know what may be automated versus what stays human-gated.

**Related:** [conceptual-framework.md](conceptual-framework.md), [identity-fork-protocol.md](identity-fork-protocol.md) (Sovereign Merge Rule), [glossary.md](glossary.md) (Approval Inbox). Numeric series forecasting (WORK lane): [docs/skill-work/work-forecast/README.md](skill-work/work-forecast/README.md).

---

Grace-Mar treats personal cognitive development as a governed process in the age of AI, analogous to how some organizations are unbundling traditional management.

Management has historically bundled three core functions:

- **Routing:** Aggregating and distributing information.
- **Sensemaking:** Filtering noise into signal, interpreting context, and translating between layers.
- **Accountability & feedback:** Maintaining ownership, long-running responsibility, coaching, and aligned growth.

Grace-Mar deliberately decomposes these functions at the individual level to preserve human authority while leveraging AI:

## Routing

Handled primarily by observation agents (Telegram/WeChat bots) and the LLM analyst. Raw signals are detected, structured into the three-dimension mind model (IX-A Knowledge, IX-B Curiosity, IX-C Personality), and staged as candidate proposals in `recursion-gate.md`. This layer is highly automatable. Operator-side runtime observations can also be staged with explicit lineage via `scripts/runtime/stage_candidate_from_observations.py` (see [docs/runtime/provenance-staging.md](runtime/provenance-staging.md)).

**Staging ≠ Voice parity:** Approved merges update `self.md`; **`bot/prompt.py`** and analyst dedup lists require their own verification—see [prompt-ix-sync.md](prompt-ix-sync.md).

## Sensemaking

Reserved for the human companion (or designated operator). During review in the **Approval Inbox** (pending candidates in `recursion-gate.md`), the human weighs each candidate against lived personal context, condition-derived ethics, long-term trajectory, and resistance signals. The LLM may propose interpretations, but final judgment remains strictly human.

## Accountability & feedback

Enforced through the **sovereign merge rule:** no change enters the core Record without explicit human approval. Rejection reasons create logged feedback loops that improve future routing and analysis. The companion retains full long-running ownership of the cognitive trajectory.

This unbundling captures AI speed in routing while protecting sensemaking and accountability behind the recursion gate. It aims to keep visible seams, evidence grounding, and clear trust boundaries.

**Design principle:** As AI capabilities increase, expand the **routing** layer where it is safe—but do not remove human **sensemaking** and **accountability** gates.

---

## Comparison with external org experiments (illustrative, 2026)

The rows below are **operator interpretive summaries** for positioning and learning—not verified facts in the Record, not investment or HR advice. Citations and nuance belong in external research notes.

| Organization | Routing | Sensemaking | Accountability & feedback | Observed outcomes (narrative) |
|--------------|---------|-------------|----------------------------|------------------------------|
| **Kimmy** (Moonshot AI) | Agents handle much routing (user feedback toward code) | Concentrated in a small founder set with wide spans | Self-reflection + high cultural intensity | Reported extreme speed with strain, anxiety, attrition risk |
| **Block** (Jack Dorsey) | AI “world model” for information flow | Time-bounded DRIs with authority | Player-coaches | Autonomy-focused; rollout still evolving |
| **Meta** | Agents assist routing inside hierarchy | Human, but compressed (wider spans) | Intensified performance feedback | Fast shipping; burnout / churn risk in public reporting |
| **Grace-Mar** | Agents + LLM analyst (signal detection & staging) | Human review in Approval Inbox | Sovereign merge rule + logged rejections | Human-led pace with explicit authority and legibility |

---

## Optional structured rejection feedback

To improve routing analytics without changing merge behavior, operators may add to rejected candidate YAML:

```yaml
rejection_category: routing_error   # optional; see scripts/rejection_feedback.py
```

Allowed keys align with `REJECTION_CATEGORIES` in [`scripts/rejection_feedback.py`](../scripts/rejection_feedback.py). If omitted, [`scripts/analyze_rejection_feedback.py`](../scripts/analyze_rejection_feedback.py) infers a bucket from `rejection_reason` text.
