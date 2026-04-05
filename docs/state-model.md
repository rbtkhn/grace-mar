# State model

Companion-Self uses a **three-layer** model for where information lives and how it may change. It makes explicit what is otherwise easy to blur in agentic systems: **raw inputs**, **operational context for reasoning**, and **durable governed commitments**.

---

## 1. Evidence Layer

Raw observations, uploads, notes, transcripts, external files, logs, and other source materials.

**Properties:**

- May be incomplete, conflicting, or noisy.
- Should preserve provenance when practical.
- Is **not** equivalent to governed state.

---

## 2. Prepared Context Layer

Normalized, cleaned, structured, or compressed artifacts **derived from evidence** for agent use (retrieval, prompts, analysis).

**Properties:**

- Optimized for reasoning and tooling, not for moral or legal authority by itself.
- May include summaries, staged text, extracted fields, or context bundles.
- Remains **subordinate to evidence provenance** (traceable where practical).
- Is **not** equivalent to governed state.

---

## 3. Governed State Layer

Durable state that affects future companion behavior and commitments **after** visible governance where required.

**Examples:**

- Seed-phase activation artifacts (validated, reviewed).
- Approved post-seed change objects (change-review decisions merged).
- Stable operating commitments in the **Record** (identity, curiosity, personality, skills, evidence spine).
- Durable pedagogical, memory-governance, or safety commitments that the protocol treats as binding.

**Properties:**

- Cannot be silently overwritten when materially important.
- Must be updated through **governed pathways** (gate, change review, documented activation handoff).
- Prior state, reasoning, and decision trace should be preserved or diffable; contradictions should stay visible, not flattened.

---

## Doctrine

1. **No raw evidence becomes governed state directly.**
2. **No prepared context becomes governed state automatically.**
3. **Meaningful durable change** must pass through a **visible** proposal/review path (see [change-review.md](change-review.md), [Identity Fork Protocol](identity-fork-protocol.md) in instances).

---

## Relationship to Record and Voice (instance vocabulary)

This template also uses **Record** and **Voice** in [concept.md](concept.md):

| State model layer | Typical instance mapping |
|-------------------|---------------------------|
| **Evidence** | Raw session transcripts, uploads, operator logs, external docs, unmerged intake — before or outside the gated Record. |
| **Prepared context** | Analyst drafts, PRP bundles, normalized markdown for tools, retrieval chunks, **self-memory** (ephemeral continuity — not the Record). |
| **Governed state** | **Record** (e.g. `self.md`, split SELF files, skills, **EVIDENCE** spine after merge), approved seed outputs at activation, outcomes of **change review**. |

**Voice** renders the Record when queried; it is not a fourth layer — it reflects **governed state** under the knowledge boundary.

See also: [evidence-layer.md](evidence-layer.md), [prepared-context-layer.md](prepared-context-layer.md), [governed-state-layer.md](governed-state-layer.md), [prepared-context-doctrine.md](prepared-context-doctrine.md), [evidence-to-context-pipeline.md](evidence-to-context-pipeline.md).
