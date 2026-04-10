# OB1 (Open Brain) Integration

**Status:** Doctrine locked. Implementation deferred until demand triggers fire.

This directory defines the **asymmetric bridge** between a companion-self instance (git-based, human-gated Record) and an OB1 deployment (Supabase + pgvector, MCP, thoughts). The bridge is asymmetric by design: companion-self is the authority for durable identity; OB1 is a mixed-trust runtime and memory surface.

**Upstream:** [NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1)
**Consolidated planning note:** [ob1-companion-self-bridge-consolidated.md](../../skill-work/work-dev/ob1-companion-self-bridge-consolidated.md)

---

## Related: Cici instance (external)

Xavier’s OB1 **instance** repo **[Xavier-x01/Cici](https://github.com/Xavier-x01/Cici)** (config and docs; not grace-mar) implements **Phase 1 Git-first governed state**: a three-layer scaffold (**evidence** → **prepared context** → **governed state** under `users/<instance>/`), **proposal artifacts** and a lightweight review queue, **`config/authority-map.json`**, and CI validation. Its doctrine matches the pattern at a high level: **Git-managed governed state is canonical**; **Supabase** remains a supported **operational bridge** (vector search, MCP, dashboards)—**not** the sole durable source of truth if it diverges from governed files. See Cici [Governed State Model (Phase 1)](https://github.com/Xavier-x01/Cici#governed-state-model-phase-1) and [`docs/governed-state-doctrine.md`](https://github.com/Xavier-x01/Cici/blob/main/docs/governed-state-doctrine.md).

**Scope:** That wording describes **Cici’s** repo. **This** integration still treats **companion-self** as the authority for the **Record** in grace-mar; the bridge ADR and [architecture.md](architecture.md) are unchanged. The pointer is for **alignment** (inspectable, review-gated durable state vs mixed-trust runtime DB)—not a merge of Cici’s files into grace-mar.

---

## Core invariant

> OB1 may contribute candidate material; companion-self alone governs durable identity.

This constraint is non-negotiable. Every document, script, and test in this integration must preserve it.

---

## Documents

| Document | Purpose |
|----------|---------|
| [architecture.md](architecture.md) | Two-phase asymmetric bridge architecture, data flow, and safety model |
| [adr-asymmetric-bridge.md](adr-asymmetric-bridge.md) | Architecture Decision Record: why asymmetric, why stage-only return |
| [operator-runbook.md](operator-runbook.md) | Manual operator workflows for export and import-staging |
| [mapping.md](mapping.md) | Canonical object schemas for export bundles and import proposals; **conceptual map** [OB1, Cici, grace-mar](mapping.md#conceptual-map-ob1-cici-grace-mar) |
| [trust-tiers.md](trust-tiers.md) | Trust classification system with handling rules per tier |

### Upstream OB1 (reference spot-check)

Read-only summary from **[NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1)** public docs (as of repository `main`, captured for grace-mar orientation — re-verify before citing externally):

- **Positioning:** README describes Open Brain as persistent memory infrastructure (Supabase + vector + MCP): “One database, one AI gateway, one chat channel,” with a **curated extension learning path**, **community contributions** (recipes, skills, dashboards, integrations), Discord and Substack.
- **Contributing:** [CONTRIBUTING.md](https://github.com/NateBJones-Projects/OB1/blob/main/CONTRIBUTING.md) — **extensions** and **primitives** are **curated** (maintainer discussion / multi-extension justification); **recipes, schemas, dashboards, integrations, skills** are **open** for community PRs; **automated PR review** (structure, secrets, SQL safety, metadata) plus **human admin** review; **core `thoughts` / core MCP** changes are out of scope for contributors.
- **Implication for grace-mar:** OB1 is a strong **public platform and contribution hub** for the memory substrate; it is **not** a substitute for this repo’s Record governance. Use [mapping.md § Conceptual map](mapping.md#conceptual-map-ob1-cici-grace-mar) when comparing to Cici or grace-mar.

---

## Phases

| Phase | Direction | Status | Safety profile |
|-------|-----------|--------|----------------|
| **1** | companion-self → OB1 | Deferred (no OB1 instance deployed) | Safe: read-only export, OB1 is downstream consumer |
| **2** | OB1 → companion-self | Deferred (no OB1 instance deployed) | Requires care: stage to RECURSION-GATE only, never direct Record writes |

---

## Implementation triggers

Code implementation (PRs 3-12 from the evaluation) is deferred until **at least one** of these fires:

1. An OB1 Supabase instance is deployed for this companion
2. A downstream system requests Record data in OB1 format
3. OB1 upstream reaches a tagged stable release worth pinning to
4. Pipeline velocity exceeds 2 merges/week (indicating Record growth that benefits from a second runtime)

**Evaluation:** See the quantitative plan evaluation that produced this scope decision. Architecture and mapping are locked now; code waits for demand.

**Blocking prerequisite for PR 4 (exporter):** Run a **chunking spike** before shipping — see [architecture.md](architecture.md) § Known technical risks and [mapping.md](mapping.md) § Chunking guidance.

---

## Pilot success criteria (quantitative)

When the bridge reaches PR 12 (pilot), measure these before declaring success:

| Metric | Target | How to measure |
|--------|--------|----------------|
| **Export determinism** | 100% — identical output on repeated runs | Run export twice, diff manifests and fingerprints |
| **Retrieval precision (Phase 1)** | > 70% on 10 standard test queries | Manual evaluation: does OB1 return the right chunk for each query? |
| **Proposal false-positive rate (Phase 2)** | < 30% of staged proposals rejected | Track accept/reject ratio over first 50 proposals |
| **Duplicate proposal rate** | 0% after dedup | Re-run import on same OB1 export; no new proposals should appear |
| **Provenance completeness** | 100% of merged proposals traceable to OB1 thought ID | Audit `channel_key: operator:ob1-import` entries in gate |
| **Operator review time** | < 5 minutes per 10 proposals | Time the review session |
| **Review quality** | No rubber-stamping signal (> 15 sec per proposal average) | Log review duration per proposal |
| **Governance breach** | 0 — no direct writes to SELF/EVIDENCE/prompt from bridge scripts | Verify via git blame on governed files |

---

## Scope boundary

- **This directory:** Doctrine, architecture, schemas, runbooks (locked)
- **companion-self repo:** Canonical implementation home when scripts are built
- **grace-mar:** This directory + pointer; no duplicated core logic
- **Not here:** OB1 internal configuration, Supabase schema, MCP server setup
