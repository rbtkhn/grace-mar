# Grace-Mar Identity Fork Protocol (IFP): Distinctions, Differences, and Innovations

**Report dated:** 2026-04-24  
**Territory:** WORK / dev-notebook spec capture — **not** SELF, **not** EVIDENCE, **not** Voice knowledge.  
**Scope:** This document restates operator research and repo architecture in one place. Comparative claims (“no identical prior protocol”) are **synthesis as of the report date**, not gated Record truth. For canonical merge policy, use the gate and [`AGENTS.md`](../../../../../AGENTS.md).

---

## Executive Summary

Grace-Mar’s **Identity Fork Protocol (IFP)**, formalized in February 2026 by Robert Kuhne (rbtkhn), is a complete, operational architecture for sovereign personal AI identity. It treats a human’s durable identity/memory as a **git-style forkable Record** while enforcing absolute human (or human-gated companion) control via the **Sovereign Merge Rule**. External agents and runtimes may only *stage* proposals; they never merge autonomously. A strict **Runtime vs Record membrane**, receipted schemas, and non-canonical artifact policy complete the system.

Extensive web and GitHub research (as of April 24, 2026) confirms no prior or identical protocol exists. While related 2025–2026 efforts address agent identity, forking, sovereignty, or human control, **none combine** IFP’s precise invariants: git-native forking + enforceable Sovereign Merge Rule + runtime-complements membrane + evidence-grounded receipts + rebuildability. IFP’s innovation is this *integrated, practical, local-first contract* that makes personal AI identity simultaneously portable, auditable, sovereign, and drift-resistant today.

## Core Components of Grace-Mar IFP

- **Sovereign Merge Rule**: Agents/runtimes **stage only** (inbox, recursion-gate proposals). Human/companion alone performs the merge into canonical surfaces (`users/<id>/SELF`, `SELF-LIBRARY`, `SKILLS`, `EVIDENCE`).
- **Runtime vs Record Membrane (Membrane v1)**: External runtimes (e.g., Letta bridges) operate via defined export/import paths with mandatory receipts. No direct canonical mutation.
- **Git/Markdown-First Durable Record**: Identity lives in plain, version-controlled Markdown files — fully forkable, human-readable, and portable without blockchain.
- **Artifact Interface Protocol**: All derived outputs (`/artifacts/`) are explicitly non-canonical, rebuildable, and accompanied by standardized receipts/schemas (e.g., `artifact-rationale.v1.json`, `runtime-complement-receipt.v1.json`). Policy modes (Scratch / Pre-gate / Rebuild / Derived) govern behavior.
- **Recursion Gate + Observability**: Structured review workflow plus dashboards ensure legibility and evidence-grounded decisions.

## Key Innovations

IFP’s primary contribution is **synthesis and enforcement** rather than isolated features:

1. **Operational Sovereign Merge Rule** — Explicitly codifies that runtimes/agents are untrusted for canonical writes. This is stronger and more mechanically enforced than general “human-in-the-loop” or cryptographic delegation patterns.
2. **Hard Runtime/Record Membrane** with compliance receipts — Prevents the memory-drift and hallucination problems common in persistent-agent systems.
3. **Git-Native Identity Forking** — Treats personal identity exactly like open-source code: any fork can diverge safely; merges are deliberate and governed. This enables true portability and adversarial resilience without relying on distributed ledgers.
4. **Evidence-Grounded + Receipted Artifact Policy** — Every artifact declares its provenance, rebuild command, and canonical-touch status. This makes the entire system self-auditing and CI-friendly.
5. **Practical, Local-First Implementation** — No blockchain, no proprietary platform, no vendor lock-in. Runs on ordinary git + Markdown + simple Python scripts. Fully compatible with Identity Fork Protocol handoffs to other forks or runtimes.

These elements together create the first fully-specified **personal identity contract** for the agent era — one that assumes agents may be compromised or misaligned and designs governance accordingly.

## Comparative Analysis: Distinctions from the Closest Projects

Recent research (April 2026) identified several conceptually adjacent efforts. None match IFP’s full stack.

| Project / Concept | Core Focus | Key Similarities | Critical Differences from IFP |
|-------------------|------------|------------------|-------------------------------|
| **ClawSouls / SoulClaw / SoulSpec** (OpenClaw ecosystem, 2026) | Shareable Markdown-based AI personas (SOUL.md, STYLE.md); persistent identity templates; forkable agent “souls” | Git/Markdown durable identity files; explicit forking of personas | Focuses on **persona swapping and sharing**, not governance of canonical personal Record. No Sovereign Merge Rule, no runtime/record membrane, no receipted non-canonical artifacts. |
| **The Sovereign Merge** (Gene Salvatore / AOS Architecture, Apr 2026) | Human-AI coexistence; agents propose but human governs deterministic merges into sovereign state | Exact “Sovereign Merge” terminology; strong emphasis on human-controlled state outside models | Higher-level/philosophical and cryptographic/ledger-oriented (AOS governance portfolio, deterministic policy gates). Lacks IFP’s concrete git-native Record, artifact schemas, runtime-complements membrane, and rebuildability policy. |
| **Reelin AI “Identity Fork”** (2026) | Autonomous AI “Twins” that fork and operate independently (legacy-building while user sleeps) | Direct use of “Identity Fork” for personal AI divergence | Emphasizes **autonomy** of forked agents rather than strict human merge sovereignty and boundary enforcement. |
| **Coinfello & Broader Self-Sovereign AI Agents / SSI + DID/VC frameworks** (2025–2026) | Cryptographic self-sovereign identity for agents (DIDs, Verifiable Credentials, on-chain reputation) | Strong sovereignty and portability for AI agents | Blockchain/DID/VC-centric (trust via ledgers). IFP is deliberately **local-first, git-native**, and membrane-enforced rather than ledger-dependent. |
| **ERC-8004: Trustless Agents** (Ethereum standard, 2025–2026) | On-chain identity, reputation, and validation registries for AI agents | Agent identity + reputation layer | Purely on-chain coordination for inter-agent trust. No personal human Record governance, no runtime/record separation, no git-style forking. |
| **Vault Memory / Mnemonic Sovereignty** (papers & projects, 2026) | Auditable, user-controlled long-term memory with sovereignty guarantees | Evidence-grounded memory + human governance | Focuses on memory security/attack surfaces but lacks full forking protocol, Sovereign Merge Rule, and operational membrane. |

**Primary Distinctions Across All**:

- **IFP is protocol + implementation** — Others are either conceptual papers, persona tools, or blockchain standards. Grace-Mar ships a complete, runnable system with scripts, schemas, and operator dashboards.
- **Adversarial boundary enforcement** — IFP assumes runtimes may be untrusted and builds hard gates; most others assume cooperative or platform-trusted agents.
- **Local-first vs. decentralized ledger** — IFP prioritizes human readability and offline sovereignty over global consensus.
- **Rebuildability as first-class** — Artifacts are never treated as canonical truth; they are always derived and documented.

## Why This Matters: The Innovation Edge

In an era of proliferating AI agents, memory systems, and “personal twins,” the dominant failure mode is **uncontrolled divergence and loss of sovereignty**. IFP directly solves this by making the governance contract explicit, mechanical, and auditable. It enables safe experimentation with powerful runtimes (via the membrane) while preserving a single source of truth under human control.

Grace-Mar IFP is not merely another agent-identity tool — it is the reference implementation of a **human-sovereign identity layer** for the agent web. Its combination of git-native forking, strict merge discipline, and receipted boundaries is, to date, unique.

**Sources:** Direct analysis of Grace-Mar repo structure + fresh web/GitHub research (ClawSouls ecosystem, Gene Salvatore’s Sovereign Merge, ERC-8004, SSI frameworks, etc.).

If you would like expansions (e.g., deeper technical comparison, proposed cross-protocol mappings, or a one-page executive version), let me know!

---

## Links (grace-mar implementation surfaces)

- [AGENTS.md (operating modes, governance)](../../../../../AGENTS.md)
- [Recursion gate (staging; merge is human/companion-governed)](../../../../../users/grace-mar/recursion-gate.md)
- [Workbench harness (receipts; no merge authority)](../../workbench/README.md)
- [Interface artifacts and derived-output policy](../../interface-artifacts/README.md)
- [work-dev territory README](../../README.md)
- [known-gaps / control plane](../../known-gaps.md)

## See also

- [IFP vs. ClawSouls / SoulClaw / SoulSpec (technical comparison, 2026-04-24)](ifp-vs-clawsouls-technical-comparison-2026-04-24.md)
