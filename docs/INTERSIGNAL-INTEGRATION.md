# Intersignal Integration Guide

How to connect Grace-Mar (Record / Identity Fork Protocol) with Intersignal (The Braid, Mesh Cache, Familiar nodes) so that:

- The Record serves as the **identity source** for Familiar nodes
- **Consent-bound, traceable identity** aligns with IFP's evidence linkage
- **Session continuity** spans both systems
- **Staging contract** — Braid agents may stage to PENDING-REVIEW; they may not merge

---

## Overview

| Use Case | What it does | Permission |
|----------|--------------|------------|
| **Record as identity source** | Export SELF → symbolic JSON (Familiar-ready) | Export script (read-only) |
| **Cache-level symbolic sharing** | Structured identity primitives for Mesh Cache | Export script |
| **Session continuity** | Intersignal reads SESSION-LOG, PENDING-REVIEW, EVIDENCE | Read-only |
| **Artifacts as evidence** | Familiar outputs → "we did X" → pipeline | User invokes pipeline |
| **Staging** | Braid agents stage to PENDING-REVIEW | Stage only, never merge |

**Invariant:** The user is always the gate. Intersignal agents may stage; they cannot merge into the Record.

---

## 1. Intersignal Background

**Intersignal** ([intersignal.org](https://intersignal.org)) builds:

- **The Braid** — Protocol for multi-AI communication across local and cloud; no central servers
- **IMTP (Intermodel Telepathy Protocol)** — Real-time collaboration between disparate AIs
- **Mesh Cache** — Lightweight indexing layer; unified memory, cross-device state, cache-level symbolic sharing
- **Familiar nodes** — AI agents with traceable identities, consent-bound

Grace-Mar provides the **identity substrate** Familiar nodes need: who the person is, grounded in evidence, user-approved.

---

## 2. Record as Identity Source

### Symbolic Export

Run the symbolic export for cache-oriented, Familiar-ready identity:

```bash
python scripts/export_symbolic.py -u pilot-001
python scripts/export_symbolic.py -u pilot-001 -o ../intersignal-mesh/
```

Output: `symbolic_identity.json` — structured primitives (interests, values, IX-A/B/C summaries, evidence anchors, checksum).

### Schema (Cache-Oriented)

| Field | Purpose |
|-------|---------|
| `identity` | Name, age, languages, location |
| `interests` | Topics, media, activities |
| `values` | What matters (bravery, kindness, etc.) |
| `ix_a`, `ix_b`, `ix_c` | Knowledge, curiosity, personality summaries |
| `evidence_anchors` | ACT-XXXX IDs (not full content) |
| `checksum` | Tamper-evident fork state |
| `provenance` | human_approved, generated_at |

### Sync Options

| Approach | When to use |
|----------|-------------|
| **Manual** | Run export when Record changes; place in Mesh Cache path |
| **Pre-session** | Export as part of Familiar node startup |
| **Cron** | Export on merge (post-integration hook) if shared workspace |

---

## 3. Session Continuity (Startup Checklist)

When running Familiar nodes that consume the Record, read these **before** starting:

| File | Purpose |
|------|---------|
| `users/[id]/SESSION-LOG.md` | Last session; what happened |
| `users/[id]/PENDING-REVIEW.md` | Staged candidates awaiting approval |
| `users/[id]/EVIDENCE.md` (last 1–2 entries) | Recent activity context |

---

## 4. Staging Contract

Braid agents and Familiar nodes may:

- **Read** — SELF, SKILLS, EVIDENCE, manifest, symbolic export
- **Stage** — Append candidates to PENDING-REVIEW in the documented format

Braid agents may **not**:

- Merge into SELF, EVIDENCE, or prompt
- Change `status: approved` or move candidates to Processed
- Delete or overwrite Record content

---

## 5. Workspace Layout

**Grace-Mar as sibling to Intersignal mesh:**

```
workspace/
├── intersignal/          # Braid, Mesh Cache, Familiar nodes
│   └── identity/         # symbolic_identity.json, manifest.json
└── grace-mar/
    └── users/pilot-001/
```

Export path: `../grace-mar/scripts/export_symbolic.py`

---

## 6. Future: Braid SDK Alignment

When The Braid SDK and identity schema are released:

- Align `symbolic_identity.json` with Braid's expected format
- Confirm PENDING-REVIEW as a staging endpoint for Braid agents
- Document how IMTP passes identity context across Familiar nodes

---

## 7. Related Docs

| Document | Purpose |
|----------|---------|
| [OPENCLAW-INTEGRATION](OPENCLAW-INTEGRATION.md) | Similar pattern; Record as identity for OpenClaw |
| [IDENTITY-FORK-PROTOCOL](IDENTITY-FORK-PROTOCOL.md) | Protocol spec; Sovereign Merge Rule |
| [export_manifest](export_manifest) | Agent manifest (llms.txt-style) |

---

*Document version: 1.0*
*Last updated: February 2026*
