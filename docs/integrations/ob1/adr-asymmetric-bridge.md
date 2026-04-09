# ADR: Asymmetric Bridge for OB1 Integration

**Status:** Accepted
**Date:** 2026-04-09
**Decision makers:** Operator
**Context:** companion-self ↔ OB1 integration design

---

## Context

OB1 (Open Brain) provides persistent AI memory via Supabase + pgvector with an MCP protocol. companion-self stores durable identity in a git repo with a human-gated pipeline (RECURSION-GATE → companion approval → merge). The question: how should these two systems exchange data?

---

## Decision

Build an **asymmetric bridge**, not a bidirectional sync.

- **companion-self is the authority** for identity and durable knowledge.
- **OB1 is a mixed-trust runtime** — useful for retrieval and AI memory, but its content is not pre-approved Record.
- **Phase 1 (export)** populates OB1 from companion-self. Safe: read-only, downstream consumer.
- **Phase 2 (import-staging)** lets OB1 thoughts enter companion-self as **staged proposals only**. Never direct Record writes.
- **No unattended sync loop.** Every transfer is manual and observable.

---

## Alternatives considered

### 1. Bidirectional sync (rejected)

A continuous sync loop where changes in either system propagate to the other.

**Rejected because:**
- Violates companion sovereignty — auto-merging OB1 content into the Record bypasses the gate.
- Creates conflict resolution complexity — which system wins on contradiction?
- Introduces drift risk — background sync can silently corrupt identity surfaces.
- No demand exists — neither system has content the other needs in real time.

### 2. OB1 as authoritative store (rejected)

Move the Record into OB1 and treat git as a downstream cache.

**Rejected because:**
- The gated pipeline (stage → approve → merge) is git-native and well-tested (97 candidates, 17 receipt-logged merges).
- OB1's trust model is mixed — it stores both grounded evidence and speculative agent output in the same surface.
- Supabase dependency would replace a self-contained git repo with a cloud service requirement.
- The Record's immutability guarantees (git history as audit trail) have no OB1 equivalent.

### 3. No integration (deferred, partially adopted)

Leave the systems independent. companion-self stays in git; OB1 stays in Supabase.

**Partially adopted:** Implementation is deferred until demand triggers fire. Architecture and mapping are locked now so the integration can be built quickly when needed without design drift.

---

## Consequences

**Positive:**
- companion-self sovereignty is preserved unconditionally.
- Export is safe and useful independently of import.
- The stage-only return flow reuses the proven RECURSION-GATE pipeline.
- Architecture is locked before code, preventing implementation drift.

**Negative:**
- OB1 content cannot enter the Record without operator effort (by design, but adds friction).
- Two-repo coordination (logic in companion-self, docs in grace-mar) requires discipline.
- Deferred implementation means no bridge code exists when an OB1 instance is deployed — but the mapping spec (PR 2) ensures fast implementation.

**Neutral:**
- The asymmetric model applies to any future mixed-trust runtime, not only OB1.
- Trust tiers and grounding filters are reusable for other import sources.

---

## Review triggers

Re-evaluate this ADR if:
- OB1 ships a governed/auditable thought layer that changes the trust model
- A second companion-self instance needs to share Record state (different problem)
- The companion requests autonomous import (would require a new ADR for bounded autonomy)
