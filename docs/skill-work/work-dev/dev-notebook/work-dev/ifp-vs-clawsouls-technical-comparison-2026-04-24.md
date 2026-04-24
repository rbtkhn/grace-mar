# Technical Comparison: Grace-Mar Identity Fork Protocol (IFP) vs. ClawSouls / SoulClaw / SoulSpec

**Report as of:** 2026-04-24  
**Territory:** WORK / dev-notebook spec capture — **not** SELF, **not** EVIDENCE, **not** Voice knowledge.  
**Scope:** Third-party and ecosystem behavior described here is based on **operator research and public material as of the report date**; it is not continuous verification. For the IFP overview, see [identity-fork-protocol-ifp-2026-04-24.md](identity-fork-protocol-ifp-2026-04-24.md).

---

## 1. Core Purpose & Scope

- **ClawSouls (SoulClaw / SoulSpec ecosystem)**: Agent-centric persistent **persona/identity** for AI agents. Focuses on making agents consistent, shareable, and "alive" across sessions, models, and platforms (WhatsApp, Telegram, CLI, etc.). The "Soul" defines **who the agent is** (personality, values, boundaries, tone). Primary goal: character continuity + marketplace of forkable agent templates. SoulClaw is an enhanced fork of OpenClaw optimized for this.
- **Grace-Mar IFP**: Human-centric **sovereign durable identity Record**. Treats the human's SELF, evidence, skills, and library as a git-style forkable truth layer. Focuses on **human governance** over personal identity/memory in an adversarial multi-agent world. Primary goal: prevent drift, enforce sovereignty, and enable safe runtime experimentation without canonical mutation.

**Key distinction**: ClawSouls builds *agent souls*. IFP governs *human identity sovereignty*.

## 2. Identity Representation & Storage

| Aspect | ClawSouls / SoulSpec / SoulClaw | Grace-Mar IFP |
|--------|----------------------------------|-----------------|
| **Core Files** | `soul.json` (metadata) + `SOUL.md` (personality, principles, boundaries) + `IDENTITY.md`, `STYLE.md`, `AGENTS.md` | Structured Record directories: `users/<id>/self.md`, `SELF-LIBRARY/`, `SKILLS/`, `EVIDENCE/` (plus supporting docs) — see repo layout, not a literal re-list here |
| **Format** | Lightweight Markdown package (Soul Spec v0.5) | Plain Markdown + git (human-readable, versioned) |
| **Loading** | Injected fresh **every session** (tiered bootstrap in SoulClaw for token savings) | Canonical Record is the single source of truth; runtime complements use explicit exports |
| **Mutability** | T0 identity (`SOUL.md`/`IDENTITY.md`) declared immutable in SoulClaw; requires human authorization | Strictly immutable without human/companion merge via recursion-gate |

## 3. Forking Model

- **ClawSouls**: Fully git-native and marketplace-driven. Users `npx clawsouls install <soul>`, fork the soul directory, edit, and `npx clawsouls publish`. 80–200+ community souls. Explicit "Agent Identity Fork" problem acknowledged in their blog (divergence of cloned personas via unique memories/experiences). Supports symmetric/asymmetric/cascading forks with optional sync policies.
- **IFP**: Git-style forking of the entire personal **human** Record. Any fork can diverge safely; merges are deliberate and governed. Designed for adversarial portability (e.g., handoff to another runtime or human fork).

**Distinction**: ClawSouls forks *agent personas* for sharing/swarming. IFP forks *human identity* for sovereignty and recovery.

## 4. Merge / Governance Model (The Critical Divergence)

- **ClawSouls**:
  - Agents can write to mutable memory layers (`MEMORY.md`, dated files).
  - SoulClaw adds auto-promotion rules (frequency, rule-based) + weekly human review for T1 core memory.
  - T0 Soul remains human-authorized only.
  - No hard "agents stage only" rule; agents participate in their own memory curation via tools.
- **IFP (Sovereign Merge Rule)**: Absolute invariant — **agents/runtimes may only stage proposals** (inbox, recursion-gate candidates). Human or human-gated companion performs **all** merges into canonical Record. No agent write access to SELF/EVIDENCE/SKILLS.

This is IFP's strongest innovation: mechanical enforcement of human sovereignty where ClawSouls relies on softer human-review prompts + SoulScan validation.

## 5. Memory vs. Identity Boundaries

- **ClawSouls**: Explicit **4-tier Soul Memory** (SoulClaw):
  - T0: Immutable identity (SOUL/IDENTITY.md)
  - T1: Core evergreen memory (MEMORY.md)
  - T2: Working memory (dated .md with temporal decay, half-life 23 days)
  - T3: Ephemeral session context
  - Semantic search (Ollama embeddings + SQLite), auto-promotion, swarm sync.
- **IFP**: Strict **Runtime vs Record membrane** (membrane v1).
  - Canonical Record = durable truth (human-gated).
  - Runtime complements = ephemeral/derived only.
  - All artifacts are non-canonical, rebuildable, and receipted.

**Distinction**: ClawSouls unifies agent identity + memory in one layered system (with some immutability). IFP enforces a hard boundary between runtime state and human Record.

## 6. Runtime Separation & Artifacts

- **ClawSouls**: No dedicated runtime/record membrane. SoulClaw uses contained runtime (`OPENCLAW_STATE_DIR`) and tiered loading, but the agent operates directly on its workspace files.
- **IFP**: Explicit export/import paths only (in this repo, e.g. [`scripts/runtime/export_runtime_context.py`](../../../../../scripts/runtime/export_runtime_context.py) and [`scripts/runtime/import_runtime_observation.py`](../../../../../scripts/runtime/import_runtime_observation.py)). Mandatory `runtime-complement-receipt.v1.json` with `canonical_surfaces_touched: false`. All derived outputs live in `/artifacts/` under policy modes (Derived, Rebuild, etc.).

## 7. Provenance, Receipts, Schemas & Observability

- **ClawSouls**: SoulScan (53 automated security/persona checks before `soul apply`). Persona drift detection + auto-reinforcement. Versioned Soul Spec.
- **IFP**: Full `artifact-rationale.v1.json` + run receipts + execution receipts. Every artifact declares producer, policy mode, rebuild command, and membrane compliance. Operator dashboards + recursion-gate workflow.

IFP provides stronger auditability and rebuildability guarantees.

## 8. Security & Drift Handling

- **ClawSouls**: SoulScan + inline security pipeline + drift scoring. Addresses "semantic persistence" malware (editing SOUL.md).
- **IFP**: Assumes adversarial runtimes by design. Hard membrane + receipts prevent unauthorized canonical changes. No reliance on agent self-policing.

## Summary of Innovations in Grace-Mar IFP

ClawSouls excels at **agent personality portability and consistency** — a mature, community-driven system for building lively, shareable AI souls with practical memory tiers and drift controls. It is the strongest existing implementation of persistent agent identity via Markdown.

**IFP's unique innovations** (none of which appear in ClawSouls or SoulSpec):

1. **Enforceable Sovereign Merge Rule** with mechanical staging-only for all runtimes/agents.
2. **Hard Runtime vs Record membrane** + receipted compliance flags.
3. **Human-sovereign identity Record** (not agent persona) as the canonical truth layer.
4. **Artifact interface protocol** making *all* derived outputs explicitly non-canonical and self-describing.

In short: ClawSouls solves "how do we give agents a consistent soul?"  
IFP solves "how do we keep the *human's* identity sovereign when surrounded by powerful agents?"

They are complementary rather than competitive — a SoulClaw-style persona could run safely *inside* an IFP runtime complement, with proposals staged for human review.

Would you like a side-by-side code/schema example, a proposed integration path, or deeper dive into any axis?

---

## Links (grace-mar)

- [IFP spec capture (2026-04-24)](identity-fork-protocol-ifp-2026-04-24.md)
- [AGENTS.md](../../../../../AGENTS.md)
- [Recursion gate](../../../../../users/grace-mar/recursion-gate.md)
- [Workbench](../../workbench/README.md)
- [Interface artifacts / derived-output policy](../../interface-artifacts/README.md)
- [work-dev README (territory)](../../README.md)
- [known-gaps / control plane](../../known-gaps.md)
