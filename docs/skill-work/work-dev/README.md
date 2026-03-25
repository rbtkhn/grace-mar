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
| **[INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md)** | **One-loop spec:** read order → export → stage-only → merge; script index; companion gate invariant. |
| **[PARALLEL-MACRO-ACTIONS.md](PARALLEL-MACRO-ACTIONS.md)** | Non-interfering parallel agent branches; `scripts/integration_macro_actions.py`. |
| **[operator_depth_hint.py](../../../scripts/operator_depth_hint.py)** | When pipeline velocity (approvals / merges in a rolling window) crosses tiers, emit a harness hint toward depth docs; `operator_daily_warmup` prints a one-liner summary. Operator-only; not part of the Record. |
| **[integration-status.md](integration-status.md)** | Implemented vs partial vs documented-only status table for the integration. |
| **[known-gaps.md](known-gaps.md)** | Explicit spec-to-implementation gaps and suggested fixes. |
| **[provenance-checklist.md](provenance-checklist.md)** | Repeatable verification path for export, handback, and audit integrity. |
| **[openclaw-integration.md](../../openclaw-integration.md)** | Full integration guide — export, continuity, handback, staging, permission summary. |
| **[economic-benchmarks.md](economic-benchmarks.md)** | Benchmarks for cost, value flow, and gate health — priority five and full set. |
| **[quality-gates-narrative.md](quality-gates-narrative.md)** | Evals as **product**: “green = within boundary” map (harness, integrity, continuity CI, gate health) + partner one-liner; future dashboard concept. |
| **[session-continuity-contract.md](session-continuity-contract.md)** | Continuity as **explicit contract**: which files, which scripts, what CI proves — **not** “the agent remembers.” |
| **[safety-story-ux.md](safety-story-ux.md)** | **Safety story** as product: visible pending/approved, receipts, staged vs merged — audit continuity as primary comfort, not admin trivia. |
| **[external-signals.md](external-signals.md)** | Moonshots / GTC–class discourse → **work-dev** lens (OpenClaw, enterprise trust, inference economics, portability); links shared [external-tech-scan](../work-strategy/external-tech-scan.md). |
| **[agentic-environment-principles.md](agentic-environment-principles.md)** | **Environment-first:** policy + continuity + gate + observability before prompt; canonical Record files before clever retrieval; high-leverage “boring” work (lanes, dashboard feeds). |
| **[agent-surface-template.yaml](agent-surface-template.yaml)** | **Agent surface axes** (runtime / orchestration / interface) + Grace-Mar trust fields; `python scripts/work_dev/agent_surface_checklist.py` to print; `--validate` for structure. |
| **[research-moonshots-237.md](research-moonshots-237.md)** | Research notes from Moonshots #237 (Alex Finn) — identity, memory, security, hierarchy, actionable takeaways. |
| **[research-no-priors-karpathy-end-of-coding.md](research-no-priors-karpathy-end-of-coding.md)** | No Priors / Karpathy — agents, claws, auto-research, “end of coding”; transcript in [work-dev transcripts](../../../research/external/work-dev/transcripts/); work-dev alignment table + guardrails. |
| **[research-agent-readable-writable-commerce.md](research-agent-readable-writable-commerce.md)** | McKinsey / agent commerce / “agent readable & writable” stack; transcript in [work-dev research](../../../research/external/work-dev/transcripts/); positioning + guardrails. |
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
4. **Session continuity** — **Contract, not vibes:** read `session-log.md`, `recursion-gate.md`, and recent `self-evidence.md` (or run `continuity_read_log.py` / `harness_warmup.py` as documented). Do not assume the agent remembers; see [session-continuity-contract.md](session-continuity-contract.md).
5. **Handback provenance** — Inbound staging includes advisory constitutional check against INTENT; events emitted for audit.
6. **Portable synthesis** — Merge-approved truth in-repo; refresh exports after merges so OpenClaw never becomes the only place “who the companion is” lives.
7. **Agent reliability** — Do not treat chain-of-thought or internal traces as audit. For consequential agent work outside the companion Voice, use **tail scenarios**, **factorial variations**, and **deterministic checks** (see [agent-reliability-playbook.md](agent-reliability-playbook.md)).
8. **Visible safety state** — Users fear **silent failure**; foreground **pending vs approved**, **receipts**, **last merge**, **OpenClaw staged vs Record merged** — not chat-only reassurance. See [safety-story-ux.md](safety-story-ux.md).

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
7. For **how evals are packaged as product** (operator + partner narrative), read [quality-gates-narrative.md](quality-gates-narrative.md).
8. For **session continuity as explicit steps** (files / scripts / CI vs implicit memory), read [session-continuity-contract.md](session-continuity-contract.md).
9. For **audit continuity as the safety story** (visible pipeline state vs “trust the chat”), read [safety-story-ux.md](safety-story-ux.md).
10. For **long-form tech media** (podcasts, keynotes) translated into integration + offers vocabulary — not as specs — read [external-signals.md](external-signals.md) and the shared table in [../work-strategy/external-tech-scan.md](../work-strategy/external-tech-scan.md). Example ingest: [research-no-priors-karpathy-end-of-coding.md](research-no-priors-karpathy-end-of-coding.md) (No Priors / Karpathy — agents, claws, auto-research).

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
8. For **partner-facing safety framing** (silent-failure class, inspectable state), pull lines from [proof-ledger.md](proof-ledger.md) and [safety-story-ux.md](safety-story-ux.md).

---

## Cross-references

Other work territories (e.g. [work-politics](../work-politics/README.md)) share the same RECURSION-GATE and companion-approval rule; they use territory tags for batch merge (e.g. `--territory work-politics`).

- [OpenClaw Integration Guide](../../openclaw-integration.md) — Full spec
- [Crypto roadmap](../../crypto-roadmap.md) — authority, settlement, and access layer
- [Architecture](../../architecture.md) — Record structure, harness
- [AGENTS.md](../../../AGENTS.md) — Knowledge boundary, gated pipeline
- [INTENT](../../intent-template.md) — Constitutional context for handback
