# Identity Fork Protocol (IFP) — v1.0

**A sovereign, evidence-linked, agent-consumable identity layer for the agent web.**

*Protocol · Reference Implementation: Grace-Mar*
*Version 1.0 · February 2026*

---

## Abstract

Agents and platforms need identity data to personalize and to act on behalf of users, but today they scrape, infer, or hallucinate — there is no standard for companion-owned, evidence-grounded identity. This protocol defines that standard: a **Record** (identity schema + evidence linking), a **gate** (the companion approves every merge; the agent may stage, not merge), and **export** (agent-consumable manifest and profile). The result is portable, companion-owned identity that any agent or platform can consume without owning; the companion remains sovereign.

---

## 1. Protocol Definition

This document is the **canonical protocol specification**. Implementations and extensions reference it for mechanism; governance is in GRACE-MAR-CORE.

The **Identity Fork Protocol (IFP)** defines a standard for companion-owned, evidence-grounded identity records that agents and platforms can consume without owning. It is vendor-neutral: no single platform controls identity. The companion is the gate.

**Scope:**
- Identity schema (who they are + what they can do)
- Gated staging contract (stage vs. merge)
- Evidence linking rules
- Knowledge boundary invariant
- Manifest and export specifications

**Reference implementation:** Grace-Mar (https://github.com/rbtkhn/grace-mar)

**Governance steward:** Grace-Mar maintains protocol spec, certification, and compliance.

**What is new:** The *combination* — evidence-linked identity + Sovereign Merge Rule + three-dimension mind (IX-A/B/C) + agent-native export — is the protocol's contribution. Schema format (markdown), LLMs, messaging, and tooling are borrowed; the contract and the invariants are the specification.

---

## 2. Core Doctrine: The Sovereign Merge Rule

> **The agent may stage. It may not merge.**

This is the sovereignty invariant. It is non-negotiable.

- **Stage** — Propose candidates for addition to the Record (e.g., PENDING-REVIEW)
- **Merge** — Commit changes to SELF, EVIDENCE, or canonical profile

Only the companion (or an explicitly delegated human) may merge. Agents, bots, and third-party systems may stage. The gate is architectural, not configurable.

**Why this matters:** Serious security assumes the agent may be an adversary. The Sovereign Merge Rule enforces that assumption. No amount of automation may bypass the gate.

**Normative clarification (v1.0):** The reference implementation (Grace-Mar) operates in manual-gate mode. Merge authority is human-only (companion or explicitly delegated human). No autonomous merge path is enabled in this implementation.

---

## 2.1 Process Over Prompt

The quality of outputs depends on **process**, not on model strength or prompt tuning. Without structured control, outputs degrade even when the model is capable. The pipeline enforces:

- **Bounded context** — Analyst receives the exchange; main model receives SELF + history; each participant gets exactly what they need
- **Facts first** — Analyst stages only what is grounded in observed words or actions; no inference beyond the exchange
- **Quality gates** — Staging → Review → Merge; no merge without explicit approval
- **Specialized roles** — Different prompts for detection, emulation, lookup, homework; each does one thing

This mirrors contextual engineering in AI-assisted coding: the model writes only at the implementation phase; research, design, and planning create the context. Here, the analyst detects; the companion gates; the merge integrates. Process controls outcome.

---

## 3. Identity Schema

### 3.1 Modules

| Module | Contains | Purpose |
|--------|----------|---------|
| **SELF** | Identity, personality, preferences, values, narrative, post-seed growth (IX-A, IX-B, IX-C) | Who they ARE |
| **SKILLS** | READ, WRITE, BUILD capability containers | What they CAN DO |
| **EVIDENCE** | Activity log, writing log, creation log, media log | Raw artifacts; immutable once captured |
| **INTENT** | Goal hierarchy, trade-off rules, escalation boundaries, cross-agent policy scope | What the system should WANT to optimize |

### 3.2 Post-Seed Growth (Three-Dimension Mind)

| Dimension | Section | What it captures |
|---------|---------|------------------|
| **IX-A** | Knowledge | Facts entering awareness through observation |
| **IX-B** | Curiosity | Topics that catch attention, engagement signals |
| **IX-C** | Personality | Observed behavioral patterns, art style, speech traits |

### 3.3 Evidence Linking

Every claim in SELF (IX-A, IX-B, IX-C) must reference evidence:

- `evidence_id: ACT-XXXX` — links to EVIDENCE activity log
- `provenance: human_approved` — passed through gated pipeline

No claim may exist without traceability to an artifact or approved source.

### 3.4 Skill Executor Model (READ/WRITE/BUILD)

The SKILLS module may be operationalized as three semi-independent executors:
`READ`, `WRITE`, and `BUILD`. **Standard labels:** **self-skill-read**, **self-skill-write**, **self-skill-build** (see [ID-TAXONOMY](ID-TAXONOMY.md#standard-capability-labels-self-skill-)).

- They may use distinct heuristics, prompts, and evaluation criteria.
- They are capability-specialized, not identity-sovereign.
- They share one constitutional boundary: companion-owned Record, gated merge, evidence linkage, and knowledge boundary.

Normative constraints:

1. `READ`/`WRITE`/`BUILD` may stage candidates only; they may not merge.
2. All staged outputs must remain evidence-linked and reviewable.
3. Divergent executor recommendations are allowed; companion approval is the resolution layer.
4. Executor behavior is shaped by the SELF three-dimension mind:
   - IX-A (Knowledge): what is treated as known.
   - IX-B (Curiosity): what is prioritized for exploration.
   - IX-C (Personality): style, tone, and interaction posture.
5. `READ` is explicitly multimodal and must not be treated as text-only:
   - Accepted inputs include text, video, music/audio, images/diagrams/maps, and mixed media.
   - Staged READ-derived candidates should include modality provenance (for example `input_modality`, source/artifact reference).
   - Evidence linkage and knowledge-boundary rules apply equally to every modality.

---

## 4. Gated Staging Contract

### 4.1 Workflow

1. **Detect** — Identify profile-relevant signals (knowledge, curiosity, personality)
2. **Stage** — Write candidates to PENDING-REVIEW (or equivalent staging area)
3. **Review** — User approves, rejects, or modifies
4. **Merge** — Approved changes integrated into SELF, EVIDENCE, SESSION-LOG, prompt

### 4.2 Review Checklist (before approving)

- Is it grounded in something the companion actually said or did?
- No LLM inference beyond the exchange?
- No contradiction with existing Record?

### 4.3 Staging Interface

- Agents may **append** to the staging area
- Agents may **not** modify or delete from canonical Record
- Staging format: machine-readable (YAML/JSON) with candidate ID, mind category, signal type, proposed action

### 4.4 Merge Authority

Merge is performed only by:
- The companion
- A human operator explicitly delegated by the companion

For this protocol version's reference implementation, merge remains human-only. Any automated path is an optional future extension and is out of scope for current compliance.

---

## 5. Knowledge Boundary Invariant

The Record may contain only what the companion has explicitly provided.

- **No LLM inference** — Facts, references, and knowledge from model training must not enter the Record
- **Calibrated abstention** — When queried outside documented knowledge, the system says "I don't know" and may offer to look up
- **Evidence linkage** — Every knowledge entry traces to ACT-XXXX or equivalent

This invariant is a **regulatory advantage**: COPPA-aligned (guardian/operator controls data for minors), GDPR-aligned (data sovereignty), and architecturally safer than platforms that auto-update profiles without consent.

---

## 6. Manifest and Export Specification

### 6.1 Agent Manifest (llms.txt-style)

Enables discoverability without full access:

- **Readable** — List of consumable surfaces (SELF/IX-A, SKILLS/READ, etc.)
- **Writable** — Staging area only; merge requires companion approval
- **Checksum** — Tamper-evident identifier of current fork state
- **Exports** — Commands to generate USER.md, fork JSON, etc.

### 6.2 Export Formats

- **USER.md / SOUL.md** — Condensed identity for agent consumption (OpenClaw, etc.)
- **manifest.json** — Machine-readable schema, readable/writable surfaces, checksum
- **intent_snapshot.json** — Machine-readable intent rules (goals, trade-offs, escalation, `applies_to`, `priority`, `conflict_strategy`)
- **fork JSON** — Full export for backup, portability, or migration

Exports are snapshots for **consumption** (e.g., by schools or agents that read the Record). No other instance of the Record or Voice may be deployed as an independent economic or social agent without explicit companion consent and, where feasible, a revocation path. See [INSTANCES-AND-RELEASE](INSTANCES-AND-RELEASE.md).

---

## 7. Vendor-Neutral Identity

IFP is **not a competitor** to AI schools or platforms. It is the identity layer that prevents vendor lock-in.

- **Alpha, Prisma, Synthesis** — Consumers of identity; they teach, IFP records
- **Families** — Own the Record; platforms consume it with consent
- **Agents** — Query identity for personalization; never own it

Grace-Mar is the reference implementation. Platforms may adopt IFP-compatible exports. Copying the schema strengthens the protocol; Grace-Mar certifies compliance.

---

## 8. Compliance Positioning

| Regulation | IFP Alignment |
|------------|---------------|
| **COPPA** | Guardian/operator controls linkage; explicit consent; no autonomous companion-facing merge |
| **GDPR** | User owns data; portable; export/delete rights architecturally supported |
| **Knowledge boundary** | No LLM leak = no training-data provenance in companion profile |

The gate is not philosophical — it is regulatory defensibility.

---

## 9. Future Extensions (Out of Scope for v1.0)

### 9.1 Fork Integrity Chain (Cryptographic)

```
entry_hash = sha256(prev_hash + canonical_entry_text)
```

- Store in LEDGER.jsonl
- Optional: snapshot signing (GPG/Ed25519), notarization
- Transforms Record from versioned documentation into tamper-evident identity ledger

### 9.2 Evidence Depth Score

- Artifact-linked claims count
- Cross-context linkage density
- Time-span of evidence
- Verification tier (self/attested/verified)

Quantifies identity robustness and audit strength. Time becomes moat.

### 9.3 Tiered Autonomy Modes (Future Extension — Not in Reference Implementation)

| Mode | Approval | Use case |
|------|----------|----------|
| **Bronze** | Manual every change | Maximum control |
| **Silver** | Human pre-authorized batch policy (still requires auditable human delegation) | Reduced friction |
| **Gold** | Staged batch approval weekly | Balanced |

Gate invariant preserved only if human merge authority remains explicit, auditable, and revocable. This section is exploratory and not part of current reference-implementation behavior.

---

## 10. Certification

Implementations that comply with:

- Sovereign Merge Rule
- Evidence linking rules
- Knowledge boundary invariant
- Manifest spec

May seek **Fork-Integrity Verified** certification from the protocol steward.

---

## Conclusion

We have proposed a protocol for companion-owned, evidence-linked identity: a Record (SELF, SKILLS, EVIDENCE) that grows only through a gated pipeline, a Sovereign Merge Rule that makes the companion the gate, and export formats that let agents and platforms consume identity without owning it. The combination is the contribution; the rest (markdown, LLMs, messaging, tooling) is borrowed. The result is portable, verifiable identity for the agent web — a primitive that can outlive any single implementation or organization.

---

## References

| Document | Purpose |
|----------|---------|
| [GRACE-MAR-CORE](GRACE-MAR-CORE.md) | Canonical governance |
| [ARCHITECTURE](ARCHITECTURE.md) | Technical design |
| [WHITE-PAPER](WHITE-PAPER.md) | Full narrative |
| [AGENTS](AGENTS.md) | Implementation guardrails |

---

*Identity Fork Protocol · Sovereign, evidence-linked, agent-consumable*
