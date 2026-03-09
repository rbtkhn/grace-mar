# Skill-work-openclaw

**Objective:** Connect Grace-Mar (Record + Voice) with OpenClaw (personal agent workspace) so the Record feeds OpenClaw's identity layer, session continuity spans both systems, and OpenClaw artifacts can feed the grace-mar pipeline — with the companion always as gate.

---

## Purpose

| Role | Description |
|------|-------------|
| **Record as identity source** | Export SELF → user.md or SOUL.md so OpenClaw knows who it serves. Constitution prefix from INTENT. |
| **Session continuity** | OpenClaw reads SESSION-LOG, RECURSION-GATE, EVIDENCE before starting work. |
| **Artifacts as evidence** | OpenClaw outputs → "we did X" → pipeline. User invokes; operator stages; companion approves. |
| **Staging automation** | OpenClaw skill/cron can stage to RECURSION-GATE. Stage only; never merge. |

**Invariant:** The companion is always the gate. OpenClaw can stage; it cannot merge into the Record. This is non-negotiable: OpenClaw or downstream systems must never become control-grid infrastructure that centralizes identity or removes human approval. Companion sovereignty over the Record is preserved regardless of integration depth.

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Objective, scope, and principles for skill-work-openclaw. |
| **[openclaw-integration.md](../../openclaw-integration.md)** | Full integration guide — export, continuity, handback, staging, permission summary. |
| **[economic-benchmarks.md](economic-benchmarks.md)** | Benchmarks for cost, value flow, and gate health — priority five and full set. |
| **[research-moonshots-237.md](research-moonshots-237.md)** | Research notes from Moonshots #237 (Alex Finn) — identity, memory, security, hierarchy, actionable takeaways. |

---

## Principles

1. **Companion sovereignty** — Merge authority stays with the companion. OpenClaw stages; companion approves.
2. **Knowledge boundary** — Voice responses use only what is documented in the Record. No LLM inference into identity facts.
3. **Stage-only automation** — OpenClaw skills may read, analyze, and stage candidates. They may not merge into SELF, EVIDENCE, or prompt.
4. **Session continuity** — When running shared workspace, read SESSION-LOG, RECURSION-GATE, and recent EVIDENCE before starting. Keep the loop closed.
5. **Handback provenance** — Inbound staging includes advisory constitutional check against INTENT; events emitted for audit.

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

## Cross-references

- [OpenClaw Integration Guide](../../openclaw-integration.md) — Full spec
- [Architecture](../../architecture.md) — Record structure, harness
- [AGENTS.md](../../../AGENTS.md) — Knowledge boundary, gated pipeline
- [INTENT](../../intent-template.md) — Constitutional context for handback
