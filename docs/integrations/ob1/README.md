# OB1 (Open Brain) Integration

**Status:** Doctrine locked. Implementation deferred until demand triggers fire.

This directory defines the **asymmetric bridge** between a companion-self instance (git-based, human-gated Record) and an OB1 deployment (Supabase + pgvector, MCP, thoughts). The bridge is asymmetric by design: companion-self is the authority for durable identity; OB1 is a mixed-trust runtime and memory surface.

**Upstream:** [NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1)
**Consolidated planning note:** [ob1-companion-self-bridge-consolidated.md](../../skill-work/work-dev/ob1-companion-self-bridge-consolidated.md)

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
| [mapping.md](mapping.md) | Canonical object schemas for export bundles and import proposals |
| [trust-tiers.md](trust-tiers.md) | Trust classification system with handling rules per tier |

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

---

## Scope boundary

- **This directory:** Doctrine, architecture, schemas, runbooks (locked)
- **companion-self repo:** Canonical implementation home when scripts are built
- **grace-mar:** This directory + pointer; no duplicated core logic
- **Not here:** OB1 internal configuration, Supabase schema, MCP server setup
