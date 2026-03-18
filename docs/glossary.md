# Glossary — Grace-Mar

Short definitions for contributors and tooling. **Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md).

| Term | Definition |
|------|------------|
| **Grace-Mar** | The system and product name: a cognitive fork platform that maintains versioned, evidence-grounded records of an individual's cognitive development, with a gated pipeline and a queryable **Voice**. |
| **Cognitive fork** | A versioned branch from a snapshot of a person; it diverges by design and has its own history. The **Record** is the fork. |
| **companion** | The human whose Record it is; the sovereign in the tricameral model (**Mind**, **Record**, **Voice**). |
| **Record** | The documented self: identity, knowledge, curiosity, personality, and evidence. Lives in the companion's mind as a mental model; data in `users/[id]/self.md`, `self-evidence.md`, and related files. The agent may stage; only the companion may merge into the Record. |
| **Voice** | The queryable interface that speaks the Record — e.g. the Telegram/WeChat bot. It responds when queried, never unbidden; it renders the Record in conversation (**emulation**). |
| **tricameral mind** | Grace-Mar’s mind structure: **Mind** (human, sovereign), **Record** (documented self), **Voice** (queryable interface). |
| **companion self** | A dual-meaning shorthand: (1) the companion’s self externalized in the Record (their knowledge/curiosity/personality), and (2) the Record+Voice that accompanies them and speaks when queried. |
| **recursion-gate** (gate) | The staging surface and concept: candidates sit above `## Processed` in `users/[id]/recursion-gate.md` until the companion approves; on approval they are merged and moved below Processed. |
| **SELF / SKILLS / EVIDENCE** (modules) | Conceptual module names. On disk: `self.md`, `skills.md`, `self-evidence.md`. |
| **SELF-KNOWLEDGE** | Identity-facing knowledge in SELF — what the companion knows *about herself* (IX-A and related); not domain corpora. See [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md). |
| **SELF-LIBRARY** | Reference-facing governed library (`self-library.md`): return-to sources and domain shelves. **Parallel to identity**, not a subset of SELF-KNOWLEDGE. |
| **CIV-MEM** | Civilizational-memory **sub-library** inside SELF-LIBRARY (LIB scopes + hybrid corpus). Never treated as SELF-KNOWLEDGE. |

For full terminology and invariants, see [conceptual-framework.md](conceptual-framework.md), [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md), and [canonical-paths.md](canonical-paths.md).
