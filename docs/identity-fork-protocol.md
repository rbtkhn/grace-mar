# Identity Fork Protocol (IFP) — v1.0

**A sovereign, evidence-linked, agent-consumable identity layer for the agent web.**

*Protocol · Reference Implementation: Grace-Mar*
*Version 1.0 · February 2026*

---

Terminology primer: see [glossary.md](glossary.md) for canonical definitions (Record, Voice, companion, gate/recursion-gate).

## Abstract

Agents and platforms need identity data to personalize and to act on behalf of users, but today they scrape, infer, or hallucinate — there is no standard for companion-owned, evidence-grounded identity. This protocol defines that standard: a **Record** that includes **SELF** (identity + **SELF-KNOWLEDGE**) and, as a **separate governed surface**, **SELF-LIBRARY** (reference domains, including **CIV-MEM** — not identity), plus evidence linking; a **gate** (the companion approves every merge; the agent may stage, not merge); and **export** (manifest, profile, and logical **self_knowledge** / **self_library** buckets). See [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md). The companion remains sovereign.

---

## 1. Protocol Definition

This document is the **canonical protocol specification**. Implementations and extensions reference it for mechanism; governance is in GRACE-MAR-CORE.

The **Identity Fork Protocol (IFP)** defines a standard for companion-owned, evidence-grounded identity records that agents and platforms can consume without owning. It is vendor-neutral: no single platform controls identity. The companion is the gate.

**Scope:**
- Identity schema (who they are + what they can do) and **SELF-LIBRARY** as reference surface (gated separately in review semantics via `proposal_class`)
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

- **Stage** — Propose candidates for addition to the Record (e.g., RECURSION-GATE)
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

**Continual learning** is implemented as human-gated writes to SELF and EVIDENCE; the model does not self-edit memory or weights. The only way new knowledge or personality enters the Record is via staging and companion-approved merge.

---

## 3. Identity Schema

### 3.1 Modules

| Module | Contains | Purpose |
|--------|----------|---------|
| **SELF** | Identity, personality, preferences, values, narrative, post-seed growth (IX-A, IX-B, IX-C); **SELF-KNOWLEDGE** = identity-facing IX-A | Who they ARE |
| **SELF-LIBRARY** | `self-library.md` — governed reference domains; **CIV-MEM** = subdomain | What governed reference the fork carries (**not** identity) |
| **SKILLS** | THINK and WRITE capability containers | What the Record can evidence about what they CAN DO |
| **EVIDENCE** | Activity log, writing log, creation log, media log | Raw artifacts; immutable once captured |
| **INTENT** | Goal hierarchy, trade-off rules, escalation boundaries, cross-agent policy scope | What the system should WANT to optimize |

**Separate work layer:** `work-*` territories and instance work contexts sit adjacent to the Record. They may use broader model/tool capability, but Record updates remain gated.

### 3.2 Post-Seed Growth (Three-Dimension Mind)

| Dimension | Section | What it captures |
|---------|---------|------------------|
| **IX-A** | SELF-KNOWLEDGE | Identity-facing facts entering awareness (from conversation, READ-nnn, teaching). **Not** civilization corpora or domain libraries — those live in **SELF-LIBRARY** (CIV-MEM subdomain). |
| **IX-B** | Curiosity | Topics that catch attention, engagement signals |
| **IX-C** | Personality | Observed behavioral patterns, speech traits, emotional patterns, aesthetic tendencies, and value expressions; contradictions preserved with provenance |

### 3.3 Evidence Linking

Every claim in SELF (IX-A, IX-B, IX-C) must reference evidence:

- `evidence_id: ACT-XXXX` — links to EVIDENCE activity log
- `provenance: human_approved` — passed through gated pipeline

No claim may exist without traceability to an artifact or approved source.

For `IX-C`, implementations may enrich entries with optional metadata such as `facet`, `evidence_strength`, `stability`, `valence`, `tension_with`, `scope`, and `constraint`. These fields refine interpretation, but the core contract remains unchanged: personality is stored as observed, evidence-linked, human-approved entries rather than as a personality-test summary.

### 3.4 Skill Executor Model (THINK/WRITE + separate work layer)

The SKILLS module may be operationalized as two semi-independent executors:
`THINK` and `WRITE`. **Standard labels:** **self-skill-think** and **self-skill-write** (see [ID-TAXONOMY](id-taxonomy.md#standard-capability-labels-self-skill-)).

The work / execution layer is separate. It may have its own territory-specific executors, but those are not self-skill modules.

- They may use distinct heuristics, prompts, and evaluation criteria.
- They are capability-specialized, not identity-sovereign.
- They share one constitutional boundary: companion-owned Record, gated merge, evidence linkage, and knowledge boundary.

Normative constraints:

1. `THINK`/`WRITE` and any work executor may stage candidates only; they may not merge.
2. All staged outputs must remain evidence-linked and reviewable.
3. Divergent executor recommendations are allowed; companion approval is the resolution layer.
4. Executor behavior is shaped by the SELF three-dimension mind:
   - IX-A (Knowledge): what is treated as known.
   - IX-B (Curiosity): what is prioritized for exploration.
   - IX-C (Personality): style, tone, and interaction posture.
5. `THINK` is explicitly multimodal and must not be treated as text-only:
   - Accepted inputs include text, video, music/audio, images/diagrams/maps, and mixed media.
   - Staged THINK-derived candidates should include modality provenance (for example `input_modality`, source/artifact reference).
   - Evidence linkage and knowledge-boundary rules apply equally to every modality.

### 3.5 Proposal classes (review semantics)

Candidates SHOULD declare **`proposal_class`** so reviewers separate **identity** edits from **library** edits:

| `proposal_class` | Use when |
|------------------|----------|
| `SELF_KNOWLEDGE_ADD` / `SELF_KNOWLEDGE_REVISE` | New or changed **identity-facing** IX-A line (or equivalent SELF knowledge) |
| `SELF_LIBRARY_ADD` / `SELF_LIBRARY_REVISE` | New or changed LIB row or shelf policy **outside** CIV-MEM |
| `CIV_MEM_ADD` / `CIV_MEM_REVISE` | New or changed **CIV-MEM** domain material (LIB stubs, civ-mem corpus pointers) |

**IX-B / IX-C** may use `SELF_KNOWLEDGE_ADD` or finer labels in tooling; merge mechanics unchanged. Optional YAML line on gate blocks:

```yaml
proposal_class: CIV_MEM_ADD   # example
```

Implementations may warn when `mind_category: knowledge` candidates look like domain dumps without `CIV_MEM_*` routing to library. See [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md).

**Bot analyst:** Staged YAML includes `proposal_class: SELF_KNOWLEDGE_ADD` by default (conversation → identity queue). Library/civ-mem edits are usually **operator-staged** with `CIV_MEM_ADD` / `SELF_LIBRARY_ADD`. The Approval Inbox shows `proposal_class` (explicit or inferred).
</think>


<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
Shell

---

## 4. Gated Staging Contract

### 4.1 Workflow

1. **Detect** — Identify profile-relevant signals (knowledge, curiosity, personality)
2. **Stage** — Write candidates to RECURSION-GATE (or equivalent staging area)
3. **Review** — User approves, rejects, or modifies
4. **Merge** — Approved changes integrated into SELF, EVIDENCE, SESSION-LOG, prompt

### 4.2 Review Checklist (before approving)

- Is it grounded in something the companion actually said or did?
- No LLM inference beyond the exchange?
- No contradiction with existing Record?

**Pre-merge / pre-release condition checklist:** For a full condition-first checklist (all Record changes from RECURSION-GATE, companion approval, knowledge boundary, evidence linkage, File Update Protocol), see [condition-checklist.md](condition-checklist.md).

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

- **Readable** — List of consumable surfaces (SELF/IX-A, SKILLS/THINK, etc.)
- **Writable** — Staging area only; merge requires companion approval
- **Checksum** — Tamper-evident identifier of current fork state
- **Exports** — Commands to generate user.md, fork JSON, etc.

### 6.2 Export Formats

- **user.md / SOUL.md** — Condensed identity for agent consumption (OpenClaw, etc.)
- **manifest.json** — Machine-readable schema, readable/writable surfaces, checksum
- **intent_snapshot.json** — Machine-readable intent rules (goals, trade-offs, escalation, `applies_to`, `priority`, `conflict_strategy`)
- **fork JSON** — Full export for backup, portability, or migration
- **runtime bundle** — Runtime-neutral packaging of `record`, `runtime`, `audit`, and `policy` lanes for downstream harnesses

Exports are snapshots for **consumption** (e.g., by schools or agents that read the Record). No other instance of the Record or Voice may be deployed as an independent economic or social agent without explicit companion consent and, where feasible, a revocation path. See [INSTANCES-AND-RELEASE](instances-and-release.md).

### 6.3 Portable harness lanes

The reference implementation distinguishes four exportable lanes:

| Lane | Purpose | Canonical status |
|------|---------|------------------|
| **record** | identity, skills, evidence, library, PRP | Canonical |
| **runtime** | continuity aids for a live harness session | Non-canonical |
| **audit** | replay, integrity, provenance, and operator traces | Append-only operational history |
| **policy** | intent and constitutional alignment surfaces | Canonical policy, not identity |

This separation prevents runtime lock-in. A downstream harness may consume more than the `record` lane, but only the `record` lane defines the documented self.

### 6.4 Runtime modes

Implementations may declare a runtime mode in their machine-readable manifest:

| Runtime mode | Meaning |
|--------------|---------|
| **`adjunct_runtime`** | Downstream runtime assists alongside the canonical repo |
| **`primary_runtime`** | Downstream runtime is the main live operating surface, while the repo stays canonical |
| **`portable_bundle_only`** | Export package for transport, testing, or inspection without assuming a live runtime |

These are **packaging modes**, not autonomy modes. They may change export depth, continuity surfaces, or oversight cadence, but they do not alter merge authority. The Sovereign Merge Rule still governs every mode.

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
| [GRACE-MAR-CORE](grace-mar-core.md) | Canonical governance |
| [ARCHITECTURE](architecture.md) | Technical design |
| [WHITE-PAPER](white-paper.md) | Full narrative |
| [AGENTS](agents.md) | Implementation guardrails |

---

*Identity Fork Protocol · Sovereign, evidence-linked, agent-consumable*
