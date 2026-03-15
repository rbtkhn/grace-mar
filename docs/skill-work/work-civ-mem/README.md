# work-civ-mem

**Objective:** Manage and improve the `civilization_memory` repository from Grace-Mar as a bounded stewardship territory: audit drift, maintain workflow clarity, prepare contributions, and keep repo-management work aligned with the broader Companion Self product strategy.

`civilization_memory` is a separate repository and canon for civilizational history, strategy, governance, and tooling. `work-civ-mem` is Grace-Mar's management surface for that repository, not a replacement for its internal `STATE` / `SCHOLAR` operating modes.

---

## Purpose

| Role | Description |
|------|-------------|
| **Repository stewardship** | Track the health, structure, validation surfaces, and maintenance needs of `civilization_memory`. |
| **Audit and drift detection** | Identify governance drift, stale docs, broken workflows, or repo-management gaps before they accumulate. |
| **Contribution preparation** | Prepare bounded fixes, doc updates, workflow notes, and future patches for the `civilization_memory` repo. |
| **Strategic alignment** | Keep CMC repo-management work legible inside Grace-Mar while capturing adjacent Companion Self product priorities without mixing them into CMC scope. |

---

## Boundary

This territory distinguishes three things clearly:

1. **`civilization_memory`** — the managed external repository and canonical CMC system.
2. **`work-civ-mem`** — Grace-Mar's stewardship territory for managing that repository.
3. **Companion Self product priorities** — adjacent strategic concerns that may inform the roadmap, but are not owned by CMC and are not part of this territory's first-pass implementation.

So `work-civ-mem` is about **repository management**, not about importing CMC operations into Grace-Mar, not about turning Grace-Mar into a `STATE` / `SCHOLAR` console, and not about collapsing product strategy into civilizational analysis.

---

## How CMC Is Useful Inside Grace-Mar

Civilization memory has **no monetary purpose**. Its purpose is **pure understanding of history**, which can help leaders’ wisdom. Inside Grace-Mar it functions as an **external civilizational reference surface**, not as part of the companion's Record. It can support lookup, curriculum design, historical explanation, strategic analogy, and work territories that need deeper structured context about civilizations, institutions, continuity, and decline. Grace-Mar may consult it when civilizational context helps the companion think, learn, plan, or build, but nothing from `civilization_memory` becomes Grace-Mar's personal knowledge unless it is explicitly surfaced and approved through the normal gate. In this way, `civilization_memory` functions as a high-quality external corpus and thinking aid, while the Record remains companion-specific, evidence-linked, and sovereign.

### Typical useful scenarios

- **History lookup** — structured reference for Rome, China, dynasties, empires, pharaohs, and other civilizational topics
- **Curriculum design** — source material for `work-alpha-school` history sequencing, reading paths, or comparison units
- **Strategic analogy** — external historical context for institutional, political, or civilizational pattern analysis
- **Work support** — input for `work-civ-mem`, `work-political-consulting`, operator research, and strategy writing  
  - WAP: [civ-mem-draft-protocol.md](../work-political-consulting/civ-mem-draft-protocol.md) (human-always-approves on any ship)
- **Library and canon support** — a return-to reference source inside `self-library`

### Safe vs unsafe boundary

**Safe uses:**
- external lookup source
- curriculum and reading-path support
- structured historical input for work territories
- source of questions, analogies, and explanatory context

**Unsafe uses:**
- treating CMC content as Grace-Mar's personal knowledge by default
- merging CMC facts directly into `IX-A` without explicit engagement and approval
- letting CMC silently redefine the companion's worldview or the Voice's undocumented knowledge
- confusing external civilizational corpus with internal documented self

Compressed rule: `civilization_memory` is a reference corpus and work aid, not part of Grace-Mar's personal Record by default.

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Objective, purpose, boundary, and principles for `work-civ-mem`. |
| **[roadmap.md](roadmap.md)** | Phased path from manual repo stewardship to bounded autonomous maintenance. |
| **[workspace.md](workspace.md)** | Lightweight runbook: start points, core repo surfaces, validation commands, and default stewardship loop. |
| **[audit-report.md](audit-report.md)** | Initial baseline audit snapshot for repo strengths, likely risks, and next stewardship steps. |

---

## Principles

1. **Repository, not Record** — `civilization_memory` is a managed external repo/project, not part of Grace-Mar's Record.
2. **Human-gated stewardship** — Grace-Mar may read, analyze, draft, and prepare contributions, but upstream changes remain human-approved.
3. **Preserve CMC governance** — No silent reinterpretation of CMC modes, doctrines, or internal rules from the Grace-Mar side.
4. **No mixed-scope drift** — Keep repo management, civilizational operations, and Companion Self product strategy distinct.
5. **Auditability first** — Track repo-management work through explicit docs, reports, and future contribution surfaces rather than ad hoc memory.
6. **Future leverage stays explicit** — Adjacent product priorities may be recorded in the roadmap, but they are not implied commitments for this territory's first pass.

---

## Repo Touchpoints

Primary management touchpoints in `civilization_memory`:

- `README.md` — repo structure, taxonomy, operating modes, governance principles
- `docs/` — architecture, governance, guides, templates
- `content/` — civilization corpus, scholar ledgers, archive
- `tools/` and `scripts/` — console, validation, index/search, maintenance commands

Canonical validation commands currently exposed by the repo:

```bash
tools/cmc-governance-checks.sh .
python3 tools/cmc-validate-corpus.py --changed-only
python3 tools/cmc-index-search.py build
python3 tools/cmc-index-search.py query "your terms"
```

---

## Cross-references

- [`docs/skill-work/README.md`](../README.md) — parent work territory index
- [`repos/civilization_memory/README.md`](../../../repos/civilization_memory/README.md) — managed repository overview
- [`docs/cmc-routing.md`](../../cmc-routing.md) — current Grace-Mar routing surface that already references CMC
- [`docs/development-handoff.md`](../../development-handoff.md) — active territory and session continuity
