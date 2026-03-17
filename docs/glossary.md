# Glossary — Grace-Mar

Short definitions for contributors and tooling. **Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md).

| Term | Definition |
|------|------------|
| **Grace-Mar** | The system and product name: a cognitive-fork platform that maintains versioned, evidence-grounded records of an individual's cognitive development, with a gated pipeline and queryable Voice. |
| **Cognitive fork** | A versioned branch from a snapshot of a person; it diverges by design and has its own history. The Record is the fork. |
| **Record** | The documented self: identity, knowledge, curiosity, personality, and evidence. Lives in the companion's mind as a mental model; data in `users/[id]/self.md`, `self-evidence.md`, and related files. The agent may stage; only the companion may merge into the Record. |
| **Voice** | The queryable interface that speaks the Record — e.g. the Telegram/WeChat bot. It responds when queried, never unbidden; it renders the Record in conversation (emulation). |
| **Mind** (companion) | The human whose Record it is; the sovereign in the tricameral model (Mind, Record, Voice). Preferred term in conceptual prose: **companion**. |
| **recursion-gate** | The staging file (`users/[id]/recursion-gate.md`) and the concept: candidates sit above `## Processed` until the companion approves; on approval they are merged and moved below Processed. |

For full terminology and invariants, see [conceptual-framework.md](conceptual-framework.md) and [canonical-paths.md](canonical-paths.md).
