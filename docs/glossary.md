# Glossary — Grace-Mar

Short definitions for contributors and tooling. **Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md).

**Narrative source of truth for the fork layout:** [architecture.md](architecture.md) § Core Principle. This glossary **locks terminology**; the one-line boundary rule below is **verbatim** from [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md).

| Term | Definition |
|------|------------|
| **Rule (identity vs reference)** | **SELF-KNOWLEDGE is identity-facing. SELF-LIBRARY is reference-facing.** CIV-MEM is inside SELF-LIBRARY, not SELF-KNOWLEDGE. |
| **Grace-Mar** | The system and product name: a cognitive fork platform that maintains versioned, evidence-grounded records of an individual's cognitive development, with a gated pipeline and a queryable **Voice**. |
| **Cognitive fork** | A versioned branch from a snapshot of a person; it diverges by design and has its own history. The **Record** is the fork. |
| **companion** | The human whose Record it is; the sovereign in the tricameral model (**Mind**, **Record**, **Voice**). |
| **Record** | Companion-owned **canonical data** with **four surfaces**: (1) **SELF** — identity + **SELF-KNOWLEDGE** (`self.md`, IX-A/B/C); (2) **SELF-LIBRARY** — **reference-facing** governed library (`self-library.md`), including **CIV-MEM** as a sub-library; (3) **SKILLS** (`skills.md`); (4) **EVIDENCE** (`self-archive.md`). Identity ≠ library: corpora live in SELF-LIBRARY, not in IX-A. Gate applies to merges into these surfaces. See [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md). |
| **Voice** | The queryable interface that speaks the Record — e.g. the Telegram/WeChat bot. It responds when queried, never unbidden; it renders the Record in conversation (**emulation**). |
| **tricameral mind** | Grace-Mar’s mind structure: **Mind** (human, sovereign), **Record** (documented self), **Voice** (queryable interface). |
| **companion self** | Two words — **conceptual** shorthand: (1) the companion’s self externalized in the Record (their knowledge/curiosity/personality), and (2) the Record+Voice that accompanies them and speaks when queried. **Not** the same as **companion-self** (hyphenated system name). |
| **companion-self** | **Always hyphenated.** Names the **template** repository and **intelligence-system** product surface (fork blueprint, upgrades, `users/_template/`). Use this spelling for the **system / entity**, never `companion self` or `companionself`. |
| **companion-xavier** | **Always hyphenated.** Names **Xavier’s instance** (fork, sovereign repo) as a **system entity**. Same rule: hyphenated marks a **named** cognitive-fork deployment, not the two-word **companion self** concept. |
| **recursion-gate** (gate) | The staging surface and concept: candidates sit above `## Processed` in `users/[id]/recursion-gate.md` until the companion approves; on approval they are merged and moved below Processed. |
| **SELF** | Identity surface: `self.md` — narrative, preferences, values, and post-seed **SELF-KNOWLEDGE** (IX-A), curiosity (IX-B), personality (IX-C). Not domain corpora. |
| **SELF / SKILLS / EVIDENCE** (modules) | Shorthand; full Record adds **SELF-LIBRARY**. On disk: `self.md`, `self-library.md`, `skills.md`, `self-archive.md` (EVIDENCE). |
| **SELF-KNOWLEDGE** | Identity-facing knowledge in SELF — what the companion knows *about herself* (IX-A and related); not domain corpora. See [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md). |
| **SELF-LIBRARY** | Reference-facing governed library (`self-library.md`): return-to sources and domain shelves. **Parallel to identity**, not a subset of SELF-KNOWLEDGE. |
| **Library (display)** | User-facing shorthand for the **SELF-LIBRARY** surface in prose and some exports; **canonical** system term remains **SELF-LIBRARY** and the on-disk file remains `self-library.md`. See `scripts/surface_aliases.py`. |
| **CIV-MEM** | Civilizational-memory **sub-library** inside SELF-LIBRARY (LIB scopes + hybrid corpus). Never treated as SELF-KNOWLEDGE. |
| **Library Domain Registry** | Canonical index (`docs/self-library-domains.md` + `.json`) of **installed reference domains** (e.g. CIV-MEM, LIB entries): surface, authority, invocation, mutation policy, freshness. Routable domains must be declared here. See [self-library-domains.md](self-library-domains.md). |
| **self-* (standard labels)** | **self-knowledge**, **self-library**, … — lowercase hyphenated labels for Record components; formal surfaces **SELF-KNOWLEDGE** / **SELF-LIBRARY** when disambiguating. See [id-taxonomy.md — Capitalization and format](id-taxonomy.md#capitalization-and-format). |

For full terminology and invariants, see [conceptual-framework.md](conceptual-framework.md), [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md), and [canonical-paths.md](canonical-paths.md).
