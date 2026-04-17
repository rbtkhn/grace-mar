# Portable working identity

Grace-Mar already functions as a governed portable working-identity system. The architecture is not aspirational — the core surfaces, exports, intake path, and governance are live. This document maps the portability layers to existing surfaces and states what remains.

---

## How the system provides portability today

| Capability | Implementation |
|---|---|
| Canonical Record surfaces | Four first-class surfaces: **SELF**, **SELF-LIBRARY**, **SKILLS**, **EVIDENCE** ([runtime-vs-record.md](runtime-vs-record.md)) |
| Runtime vs Record separation | Durable Record governed by the pipeline; runtime artifacts derived and rebuildable ([runtime-vs-record.md](runtime-vs-record.md)) |
| Prepared selective retrieval | Progressive-disclosure index, budgeted context, memory briefs ([prepared-context/](../prepared-context/), [progressive-disclosure.md](prepared-context/progressive-disclosure.md)) |
| PRP export | Single pasteable prompt encoding Record surfaces for any LLM ([portable-record-prompt.md](portable-record-prompt.md), [`scripts/export_prp.py`](../scripts/export_prp.py)) |
| Runtime bundle export | Structured bundle with record/, policy/, runtime/, audit/ ([`scripts/export_runtime_bundle.py`](../scripts/export_runtime_bundle.py)) |
| JSON fork export | Machine-readable Record snapshot ([`scripts/export_fork.py`](../scripts/export_fork.py), [EXPORT-CLI.md](EXPORT-CLI.md)) |
| Approval-gated durable change | Staging in `recursion-gate.md` → companion approval → merge script ([AGENTS.md](../AGENTS.md) §2, [identity-fork-protocol.md](identity-fork-protocol.md)) |

---

## Four-layer mapping

Portable working identity maps to four layers. Each layer has a canonical Grace-Mar surface.

| Layer | What it captures | Grace-Mar surface |
|---|---|---|
| **Domain encoding** | Reference knowledge, domain corpora, governed sources | SELF-LIBRARY (`users/<id>/self-library.md`, CIV-MEM scopes) |
| **Workflow calibration** | How the operator works: skills, lane defaults, prepared context, tool patterns | SKILLS (`users/<id>/self-skills.md`) + `prepared-context/` + `docs/skill-work/` lanes |
| **Behavioral calibration** | Identity, personality, knowledge, curiosity — who the companion is | SELF (`users/<id>/self.md`, IX-A / IX-B / IX-C) |
| **Artifact / demonstrated capability** | Evidence of what happened, what was produced, what was observed | EVIDENCE (`users/<id>/self-archive.md`) + artifact exports |

---

## Anti-duplication rule

New portability work must extend the existing PRP / export / prepared-context architecture. It must not create a second parallel portability stack. The existing surfaces and scripts are the portability system — not a predecessor to be replaced.

---

## Completeness

All documented export classes are operational. The portability stack — content formats, intake path, export contract, CLI wiring, MCP adapter, and demonstrated-capability export — is complete. See [docs/portable-record/current-capability-map.md](portable-record/current-capability-map.md) for the full inventory.

---

## Related

- [architecture.md](architecture.md) — system architecture
- [runtime-vs-record.md](runtime-vs-record.md) — what is canonical vs derived
- [portable-record-prompt.md](portable-record-prompt.md) — PRP export spec
- [EXPORT-CLI.md](EXPORT-CLI.md) — unified export CLI
- [portable-record/current-capability-map.md](portable-record/current-capability-map.md) — current-state capability inventory
- [portable-record/export-contract.md](portable-record/export-contract.md) — export classes and the portability surface
