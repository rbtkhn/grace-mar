# Positioning — Governed State OS

**Territory:** work-dev  
**Status:** Draft  
**Date:** 2026-04-06  
**Origin:** External six-layer agent-infrastructure analysis mapped against companion-self and grace-mar repos.

---

## The read

An external analysis mapped companion-self and grace-mar against a six-layer agent infrastructure thesis (compute/sandbox → identity/comms → memory/state → tools/integration → provisioning/billing → orchestration/coordination). The core finding:

> Companion-Self is best understood as a template for layer 3 plus governance around layer 6. Grace-Mar is best understood as the live instance / operator-facing control plane prototype.

The analyst's one-line positioning:

> **Companion-Self is a governed state OS for companions. Grace-Mar is the first runtime instance of that OS.**

And the strength identification:

> "We know how to make agentic systems legible, governable, and durable over time."

These framings are accurate and useful. They translate internal architecture language into market-facing vocabulary without distorting what the system actually does.

---

## What makes the framing work

**"Governed state, not mere memory"** is the sharpest distinction. Most AI memory systems blur raw logs, summaries, and durable identity into one bucket. Companion-self explicitly separates Evidence, Prepared Context, and Governed State, and says meaningful change must pass through visible proposal/review paths. That separation is architecturally simple but philosophically rare — it requires a commitment to *who may change what* that most agent builders skip.

**"OS" language fits** because companion-self defines more than storage: it defines authority classes, observability expectations, action receipts, formation stages, readiness checks, and state-transition rules. That is closer to an operating system's process model than to a database schema.

**"First runtime instance"** captures Grace-Mar's role precisely. It inherits the template, adds the active channels (Telegram, WeChat), operationalizes the gated pipeline with real signal detection and candidate staging, and layers on WORK territories, lane boundaries, cadence tooling, and integration surfaces. Grace-Mar proves the OS runs; companion-self proves the OS ports.

---

## The strategic fork

The external analysis assumed one trajectory: climb the six-layer stack by adding orchestration, FinOps, agent identity, and capability contracts. That is a coherent path. But it is not the only one, and it is not the one the repos currently express.

### Path A — Companion-first

**Thesis:** The governance model exists to serve a person — a child, in the first instance — not to manage fleets of autonomous agents. The six-layer gaps (compute, agent-native identity, middleware, billing) are gaps only if the goal is infrastructure. If the goal is *the best governed companion system*, the gaps are someone else's problem.

**What this path builds:**
- Deeper Record and Voice fidelity (linguistic authenticity, lexile tracking, self-library, civ-mem)
- Better companion UX (chat-first, one-tap, bounded sessions per [chat-first-design.md](../../chat-first-design.md))
- Richer export and portability (PRP, OpenClaw handback, manifest, runtime bundle)
- More instances (companion-self template → new forks for new companions)

**What this path accepts:**
- Depends on external compute substrates (E2B, Daytona, whatever wins layer 1)
- Identity stays companion-centric, not agent-native
- Integrations stay internal tooling, not middleware
- Orchestration stays operator-cognitive, not Kubernetes-shaped

**Moat:** The governance model + a live instance with years of evidence is hard to replicate by engineering alone. It requires philosophical commitment and accumulated state.

### Path B — Infrastructure-first

**Thesis:** The governance model is the real product, and companions are the proof of concept. The market for governed agent state, authority boundaries, and inspectable orchestration is large and underbuilt. Companion-self becomes the open-source protocol; a company builds the managed infrastructure layer.

**What this path builds:**
- Agent-native identity plane (signed roles, delegated scopes, capability passports)
- Capability contracts for tools (schema, auth, failure policy, cost hint, review requirement)
- Agent FinOps (per-agent spend, per-task cost, confidence-adjusted outcome, approval thresholds)
- Orchestration substrate (scheduler, lifecycle manager, conflict/merge queues, supervisor hierarchies)

**What this path risks:**
- Diluting the companion commitment that makes the governance model credible
- Competing on infrastructure against better-funded companies (E2B, Composio, etc.)
- Losing the "we built this for a child" narrative that is both true and strategically distinctive

**Moat:** First mover on governed state as infrastructure — but only if the governance depth survives the abstraction into a general platform.

### Path C — Both, sequenced

**Thesis:** Stay companion-first for the current phase. Let the governance model mature on real instances. Extract the reusable primitives (state separation, gate protocol, receipt model, authority classes) into companion-self as portable doctrine. When the primitives are proven and the market is ready, offer them as infrastructure — without rebuilding from scratch, because the protocol already exists.

**What this requires:**
- Discipline about which work is companion-deepening and which is infrastructure-extracting
- Clean separation between grace-mar (instance) and companion-self (template/protocol)
- Not prematurely abstracting for a market that may not be ready
- Tracking the six-layer landscape so the extraction timing is informed

This is the path the repos currently express, whether or not it was named as such.

---

## Gap map (from external analysis)

Accurate as of 2026-04-06. Framed as gaps only relative to the six-layer infrastructure thesis — they may not be gaps relative to companion-first goals.

| Layer | Status | Notes |
|-------|--------|-------|
| 1. Compute / sandbox | Not owned | Above this layer by design. Sandbox adapter (wrap external sandboxes with governance model) is the pragmatic move if needed. |
| 2. Identity / comms | Companion-centric | Real operational identity via per-user namespaces and bot channels. Not agent-native identity (verifiable machine identity, agent-to-agent auth). Companion-centric is intentional. |
| 3. Memory / state | **Strong** | Distinguished Evidence, Prepared Context, Governed State. Seed-phase formation pipeline. Gated profile pipeline with signal detection, staging, review, integration. Strongest differentiation. |
| 4. Tools / integration | Internal tooling | integrations surface, work territories, integration-status, readiness checks, continuity tooling. Not yet middleware-grade (no capability contracts, normalized auth, standardized retries, connector health). |
| 5. Provisioning / billing | Mostly absent | compute-ledger artifact exists (transparency to operator/companion). Not per-agent spend, approval thresholds, or billing policy. Cleanest greenfield opportunity. |
| 6. Orchestration / coordination | Doctrine-rich, infrastructure-poor | Authority classes, receipts, lane boundaries, readiness checks, handback tooling. Not scheduler, lifecycle manager, conflict queues, or multi-agent supervisor hierarchies. |

---

## Accepted framings (use externally)

- **"Governed state OS for companions"** — use when positioning to technical audiences who understand OS-level state management
- **"Governed state, not mere memory"** — use when differentiating from AI memory startups
- **"We know how to make agentic systems legible, governable, and durable over time"** — use as capability statement
- **"The companion is always the gate"** — use when discussing trust and authority (already in README)
- **"Record = infrastructure, not tool"** — already in [design-notes.md](../../design-notes.md) §1

---

## Cross-references

- [design-notes.md](../../design-notes.md) — White paper inputs, control-grid vs sovereignty, comprehension lock-in
- [offers.md](offers.md) — Current sellable surfaces (diagnostic, architecture pass, sprint)
- [target-registry.md](target-registry.md) — Buyer segments
- [agentic-environment-principles.md](agentic-environment-principles.md) — Environment-first: policy + continuity + gate + observability before prompt
- [agent-surface-template.yaml](agent-surface-template.yaml) — Agent surface axes and trust fields
- [INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md) — One-loop spec for the integration layer
- [three-compounding-loops.md](three-compounding-loops.md) — Record vs WORK vs CI compounding
- companion-self `docs/skill-work/work-dev/README.md` — Template mirror

---

## Revision log

| Date | Change |
|------|--------|
| 2026-04-06 | Initial draft from external six-layer analysis response. |
