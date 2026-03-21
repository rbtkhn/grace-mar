# work-dev

**Objective:** Connect Grace-Mar (Record + Voice) with OpenClaw (personal agent workspace) so the Record feeds OpenClaw's identity layer, session continuity spans both systems, and OpenClaw artifacts can feed the grace-mar pipeline — with the companion always as gate.

This territory **merges** the former **work-build-ai** (same scope, same invariants). All work-build-ai content lives here; references elsewhere may still say "work-build-ai" for legacy links.

---

## Purpose

| Role | Description |
|------|-------------|
| **Record as identity source** | Export SELF → user.md or SOUL.md so OpenClaw knows who it serves. Constitution prefix from INTENT. |
| **Session continuity** | OpenClaw reads SESSION-LOG, RECURSION-GATE, EVIDENCE before starting work. |
| **Artifacts as evidence** | OpenClaw outputs → "we did X" → pipeline. User invokes; operator stages; companion approves. |
| **Staging automation** | OpenClaw skill/cron can stage to RECURSION-GATE. Stage only; never merge. |

**Invariant:** The companion is always the gate. OpenClaw can stage; it cannot merge into the Record. This is non-negotiable: OpenClaw or downstream systems must never become control-grid infrastructure that centralizes identity or removes human approval. Companion sovereignty over the Record is preserved regardless of integration depth.

**Comprehension lock-in:** Enterprise stacks are racing to host *synthesis* (who-knows-what-across-systems) inside vendor runtimes — understanding that does not export cleanly. Grace-Mar’s counter at companion scale: **approved Record + export** (USER.md, PRP, manifest) so identity and documented understanding stay **portable** and **gate-kept**, not trapped in one agent’s memory. See [design-notes §2.5](../../design-notes.md#25-control-grid-vs-grace-mar--sovereignty-as-positioning) and [implementable-insights §10](../../implementable-insights.md#10-comprehension-lock-in-vs-companion-owned-synthesis).

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Objective, scope, and principles for work-dev (includes former work-build-ai). |
| **[three-compounding-loops.md](three-compounding-loops.md)** | Record vs WORK vs CI — how compounding works in each loop and how they must interact (gate, no draft-as-truth). |
| **[workspace.md](workspace.md)** | Canonical operator entrypoint: current state, blockers, next actions, and file map. |
| **[operator_depth_hint.py](../../../scripts/operator_depth_hint.py)** | When pipeline velocity (approvals / merges in a rolling window) crosses tiers, emit a harness hint toward depth docs; `operator_daily_warmup` prints a one-liner summary. Operator-only; not part of the Record. |
| **[integration-status.md](integration-status.md)** | Implemented vs partial vs documented-only status table for the integration. |
| **[known-gaps.md](known-gaps.md)** | Explicit spec-to-implementation gaps and suggested fixes. |
| **[provenance-checklist.md](provenance-checklist.md)** | Repeatable verification path for export, handback, and audit integrity. |
| **[openclaw-integration.md](../../openclaw-integration.md)** | Full integration guide — export, continuity, handback, staging, permission summary. |
| **[economic-benchmarks.md](economic-benchmarks.md)** | Benchmarks for cost, value flow, and gate health — priority five and full set. |
| **[research-moonshots-237.md](research-moonshots-237.md)** | Research notes from Moonshots #237 (Alex Finn) — identity, memory, security, hierarchy, actionable takeaways. |
| **[offers.md](offers.md)** | First-pass business-layer offers and commercial framing. |
| **[target-registry.md](target-registry.md)** | Buyer segments for the future company path. |
| **[proof-ledger.md](proof-ledger.md)** | Reusable proof lines from internal work and future client work. |
| **[engagement-model.md](engagement-model.md)** | How work should be packaged commercially. |
| **[delivery-playbook.md](delivery-playbook.md)** | Default service delivery phases. |
| **[agent-reliability-playbook.md](agent-reliability-playbook.md)** | Agent failure modes (tails, reasoning vs action, anchoring, guardrails) and four-layer mitigation. |
| **[variation-types.md](variation-types.md)** | Factorial stressor templates for evals across client workflows. |
| **[claude-code-wat-crosswalk.md](claude-code-wat-crosswalk.md)** | WAT / agentic-IDE practice mapped to delivery, reliability, gate, and handover. |
| **[brief-ai-ambition-six-unlocks.md](brief-ai-ambition-six-unlocks.md)** | One-pager: ambition frame vs cost-reduction, Jevons paradox, six people-focused unlocks for boards/leadership. |
| **[brief-claude-1m-context-context-rot.md](brief-claude-1m-context-context-rot.md)** | Reference: Claude 1M context (Opus/Sonnet 4.6), context rot, eight-needle test, when to clear, pricing. |
| **[partner-channel.md](partner-channel.md)** | Borrowed-authority / partner path for growth. |
| **[objection-log.md](objection-log.md)** | Market-learning and positioning feedback loop. |
| **[crypto-roadmap.md](../../crypto-roadmap.md)** | Cross-cutting roadmap for using cryptocurrency as an authority, settlement, and access layer. |

---

## Principles

1. **Companion sovereignty** — Merge authority stays with the companion. OpenClaw stages; companion approves.
2. **Knowledge boundary** — Voice responses use only what is documented in the Record. No LLM inference into identity facts.
3. **Stage-only automation** — OpenClaw skills may read, analyze, and stage candidates. They may not merge into SELF, EVIDENCE, or prompt.
4. **Session continuity** — When running shared workspace, read SESSION-LOG, RECURSION-GATE, and recent EVIDENCE before starting. Keep the loop closed.
5. **Handback provenance** — Inbound staging includes advisory constitutional check against INTENT; events emitted for audit.
6. **Portable synthesis** — Merge-approved truth in-repo; refresh exports after merges so OpenClaw never becomes the only place “who the companion is” lives.
7. **Agent reliability** — Do not treat chain-of-thought or internal traces as audit. For consequential agent work outside the companion Voice, use **tail scenarios**, **factorial variations**, and **deterministic checks** (see [agent-reliability-playbook.md](agent-reliability-playbook.md)).

---

## Quick Reference

**Export identity:**
```bash
python integrations/openclaw_hook.py --user grace-mar --format md+manifest --emit-event
```

**Handback (stage only):**
```bash
python integrations/openclaw_stage.py --user grace-mar --text "we explored X in OpenClaw"
python integrations/openclaw_stage.py --user grace-mar --artifact ./outputs/session-note.md
```

---

## Operator path

Use this order when actively working on the territory:

1. Open [workspace.md](workspace.md) for the current state and canonical file map.
2. Check [integration-status.md](integration-status.md) before assuming a capability is operational.
3. Read [known-gaps.md](known-gaps.md) before claiming provenance, benchmark, or continuity coverage.
4. Use [provenance-checklist.md](provenance-checklist.md) when validating export or handback behavior.
5. Use [economic-benchmarks.md](economic-benchmarks.md) only with its current instrumentation labels in mind.
6. For agent eval posture on Voice, run `python scripts/run_counterfactual_harness.py` (includes anchoring-stress probes CF-ANCH-*).

---

## Business path

Use this order when the question is how work-dev could become a real company rather than just a territory:

1. Open [offers.md](offers.md) and choose the first sellable diagnostic or architecture pass.
2. Confirm the target segment in [target-registry.md](target-registry.md).
3. Pull proof lines from [proof-ledger.md](proof-ledger.md).
4. Check [engagement-model.md](engagement-model.md) before inventing pricing or retainers.
5. Use [delivery-playbook.md](delivery-playbook.md) to keep implementation bounded.
6. Use [partner-channel.md](partner-channel.md) for borrowed-authority growth paths.
7. Log real objections in [objection-log.md](objection-log.md).

---

## Cross-references

Other work territories (e.g. [work-politics](../work-politics/README.md)) share the same RECURSION-GATE and companion-approval rule; they use territory tags for batch merge (e.g. `--territory wap`).

- [OpenClaw Integration Guide](../../openclaw-integration.md) — Full spec
- [Crypto roadmap](../../crypto-roadmap.md) — authority, settlement, and access layer
- [Architecture](../../architecture.md) — Record structure, harness
- [AGENTS.md](../../../AGENTS.md) — Knowledge boundary, gated pipeline
- [INTENT](../../intent-template.md) — Constitutional context for handback
