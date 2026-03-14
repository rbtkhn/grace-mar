# OpenClaw Integration Guide

How to connect GRACE-MAR (cognitive fork / Record) with OpenClaw (personal agent workspace) so that:
- The Record feeds OpenClaw's identity layer (who it serves)
- Session continuity spans both systems
- OpenClaw artifacts can feed the grace-mar pipeline
- Staging automation stays gated — companion remains the approval gate

---

## Overview

| Use Case | What it does | Permission |
|----------|--------------|------------|
| **Record as identity source** | Export SELF → user.md or SOUL.md | Export script (read-only) |
| **Session continuity** | OpenClaw reads SESSION-LOG, RECURSION-GATE, EVIDENCE | Read-only |
| **Artifacts as evidence** | OpenClaw outputs → "we did X" → pipeline | User invokes pipeline |
| **Staging automation** | OpenClaw skill/cron stages to RECURSION-GATE | Stage only, never merge |

**Invariant:** The companion is always the gate. OpenClaw can stage; it cannot merge into the Record.

**Adapter note:** OpenClaw is a **runtime adapter**, not the architecture. The canonical export contract is now the Grace-Mar **runtime bundle** (`record`, `runtime`, `audit`, `policy` lanes). OpenClaw-compatible flat files remain as compatibility outputs on top of that contract.

### Comprehension lock-in and portability

Enterprise AI products increasingly aim to become the **system of record for organizational understanding** — synthesis across CRM, code, chat, and docs. That layer is hard to export; **comprehension lock-in** is switching cost from *understanding*, not just from data tables. Grace-Mar is the **companion-scale inverse**: the **Record** (git, human-approved merges) is canonical; **OpenClaw consumes exports** (USER.md, intent snapshot, PRP) — it does not own the fork. Refresh exports after pipeline merges so downstream workspaces stay aligned; if you ever leave OpenClaw, **SELF + EVIDENCE + PRP** remain. See [design-notes §2.5](design-notes.md#25-control-grid-vs-grace-mar--sovereignty-as-positioning), [implementable-insights §10](implementable-insights.md#10-comprehension-lock-in-vs-companion-owned-synthesis).

---

## 1. Record as Identity Source

The grace-mar Record (self.md + selected SKILLS) can populate OpenClaw's `user.md` or `SOUL.md` so the agent knows who it serves.

OpenClaw practitioners often "tell OpenClaw everything" — mission, goals, context — by hand. Grace-Mar provides a **canonical, evidence-linked identity layer** instead: the Record is the single source of truth, gated by the companion, and grows only through approved merges. Export replaces ad hoc briefing with a structured profile.

### Export Script

```bash
python scripts/export_user_identity.py --user grace-mar
python scripts/export_runtime_bundle.py --user grace-mar --mode adjunct_runtime -o ./runtime-bundle
```

Or use the integration hook (supports format + event emission):

```bash
python integrations/openclaw_hook.py --user grace-mar --format md+manifest --emit-event
```

Output: Markdown suitable for `user.md` or `SOUL.md`, containing:
- Identity (name, age, languages, location)
- Preferences and interests
- Linguistic style and vocabulary level
- Personality traits and values
- Post-seed growth (IX-A knowledge, IX-B curiosity, IX-C personality)
- Intent snapshot (`intent_snapshot.json`) for machine-readable goal/trade-off alignment
- Constitution prefix in `user.md` (derived from INTENT) for downstream alignment context

### Runtime bundle lanes

The generic bundle export is the portable source contract:

| Lane | What OpenClaw should use |
|------|--------------------------|
| **record** | identity export, fork export, PRP |
| **policy** | intent snapshot, manifest-declared constraints |
| **runtime** | warmup digest and light continuity surfaces |
| **audit** | optional replay and provenance files for oversight |

OpenClaw does not need to consume every lane. The important rule is that `runtime` aids must stay labeled **non-canonical**, while `record` remains the source of identity truth.

### Sync Options

| Approach | When to use |
|----------|-------------|
| **Manual** | Run export and paste into user.md when profile changes |
| **Pre-session** | Run export as part of OpenClaw startup before agent runs |
| **Cron** | Export on commit (e.g. post-merge hook) if workspace is shared |

### Runtime modes

OpenClaw can consume Grace-Mar in any of these declared runtime modes:

| Mode | What to send OpenClaw |
|------|------------------------|
| **`adjunct_runtime`** | `USER.md`, manifest, intent snapshot, light warmup/runtime aids |
| **`primary_runtime`** | same as above plus fuller runtime and audit lanes |
| **`portable_bundle_only`** | bundle for transfer or inspection without assuming a live OpenClaw session |

These modes change packaging depth, not sovereignty. OpenClaw still stages only.

### Post-merge optional trigger

`process_approved_candidates.py` supports optional OpenClaw export after successful merge:

```bash
python scripts/process_approved_candidates.py --apply --approved-by <name> --receipt <receipt.json> --export-openclaw --openclaw-format md+manifest
```

### What NOT to export

- Raw EVIDENCE content (too large, not identity-defining)
- Session logs (temporal, not identity)
- RECURSION-GATE (staging, not canonical)

Exception: the **runtime bundle** may include bounded continuity aids such as warmup output or `memory.md`, but only inside the explicit `runtime/` lane and only with non-canonical labeling.

### Trajectory export (optional RL / research)

For **local** tooling that expects multi-turn JSONL (e.g. [OpenClaw-RL](https://github.com/Gen-Verse/OpenClaw-RL)-style pipelines), Grace-Mar provides a **read-only** exporter — it does **not** train models or merge into the Record.

```bash
python scripts/export_conversation_trajectories.py -u grace-mar -o /tmp/traj.jsonl
python scripts/export_conversation_trajectories.py -u grace-mar --last-n 500   # cap size
python scripts/export_conversation_trajectories.py -u grace-mar --no-pipeline-events
```

Each line: `turn`, `role`, `channel`, `text`, `ts`, `user_id`, and optionally `pipeline_events` (staged/applied/rejected near that turn). **Policy before any upload or shared RL:** [openclaw-rl-boundary.md](openclaw-rl-boundary.md) (minors, secrets, green/yellow/red).

---

## 2. Session Continuity (Startup Checklist)

When running in a shared workspace or OpenClaw session, read these grace-mar files **before** starting work:

| File | Purpose |
|------|---------|
| `users/[id]/session-log.md` | Last session summary; what happened |
| `users/[id]/recursion-gate.md` | Any staged candidates awaiting approval |
| `users/[id]/self-evidence.md` (last 1–2 entries) | Recent context for activities |

### OpenClaw Startup Additions

If OpenClaw has a startup checklist (e.g. `active-tasks.md`, `HEARTBEAT.md`), add:

```
Grace-Mar continuity (if users/grace-mar exists):
- [ ] Read last SESSION-LOG entry
- [ ] Check RECURSION-GATE — any candidates to process?
- [ ] Skim last 1–2 EVIDENCE entries
```

This checklist supports human-in-the-loop oversight — analogous to orchestration patterns (e.g. a "chief of staff" agent checking subordinates). The companion or operator stays aware of staged work and recent evidence before OpenClaw runs.

### Any harness startup (Cursor, Codex, Claude Code, new chat)

New agent sessions start with **no memory** unless you feed the repo state. Run:

```bash
python scripts/harness_warmup.py -u grace-mar
python scripts/harness_warmup.py -u grace-mar --tail 8
```

Paste the markdown block into the **first message** of the session. Output includes: **pending RECURSION-GATE** candidates (IDs + summaries; scans full gate file), **last ACT-*** from EVIDENCE (date + summary), **session-log tail** (narrative lines only — skips embedded ` ``` ` YAML blocks). `--compact` = one paragraph. See script docstring for full behavior.

### Oversight cadence (long sessions)

For OpenClaw sessions running longer than a few hours, run a **heartbeat** periodically:

```bash
python scripts/openclaw_heartbeat.py -u grace-mar
```

Output: pending candidate count, last evidence date, last session. Add to OpenClaw cron or run manually every 2–4 hours. Keeps the human gate relevant during long autonomous runs.

### Workspace Layout

Two patterns:

**A. grace-mar as subdir of OpenClaw**
```
openclaw/
├── user.md           # ← populated from grace-mar export
├── active-tasks.md
├── memory/
└── grace-mar/        # ← symlink or copy of grace-mar repo
    └── users/grace-mar/
```

**B. OpenClaw and grace-mar sibling repos**
```
workspace/
├── openclaw/
└── grace-mar/
```
Export script path: `../grace-mar/scripts/export_user_identity.py`

### Deployment topology: local vs VPS

| Topology | Grace-Mar | OpenClaw | Notes |
|----------|-----------|----------|-------|
| **Local–local** | On companion/operator machine | Same machine or sibling dir | Preferred. Export and handback run locally; provenance and security are simplest. |
| **Local–VPS** | Local | OpenClaw on cloud/VPS | Export can be pulled by remote agent. Handback from VPS to Grace-Mar requires provenance metadata (`source: openclaw`) and raises trust/security questions — document the handback path and avoid staging untrusted content. |

When OpenClaw runs on a VPS, keys and agent state live in the cloud; injection and hijack risks are higher than on fresh local hardware. Prefer local-to-local when possible.

---

## 3. Artifacts as Evidence

OpenClaw-produced artifacts (writing, drawings, summaries) can feed the grace-mar pipeline via the **"we" convention**.

### Workflow

1. User creates something with OpenClaw (e.g. story, research summary, drawing)
2. User says: "we wrote a story about volcanoes today" (optionally attaching the file)
3. Operator (Cursor session or pipeline) runs signal detection
4. Candidates staged to RECURSION-GATE
5. User approves; merge into SELF, EVIDENCE, SESSION-LOG

### Path Convention

If OpenClaw writes to `outputs/` or `memory/`, you can reference:

```
"we wrote a story — it's in openclaw/outputs/volcano-story.md"
```

The pipeline treats this like any other "we did X" + artifact. The operator loads the file and runs analyst logic.

### No Automatic Ingestion

Artifacts do **not** auto-ingest. The companion must explicitly invoke the pipeline ("we did X") and approve any candidates. This preserves the gate.

### Stage-only inbound hook (OpenClaw -> Grace-Mar)

Use `integrations/openclaw_stage.py` to send OpenClaw output to `/stage` with provenance metadata:

```bash
python integrations/openclaw_stage.py --user grace-mar --artifact ./outputs/session-note.md
python integrations/openclaw_stage.py --user grace-mar --text "we explored fractions in OpenClaw"
```

This path only stages to `RECURSION-GATE`; it never merges into the Record.
Inbound payloads also run an advisory constitutional check against `INTENT.md` and emit
`intent_constitutional_critique` events (`advisory_clear` or `advisory_flagged`).

### Debate packet workflow (Phase C)

When repeated cross-agent conflicts appear for the same intent rule across sources
(for example, Voice vs OpenClaw), operators can stage a debate packet for explicit
human arbitration:

```bash
/intent_debate
/intent_debate INTENT-RULE-001 30
/resolve_debate DEBATE-0001 revise_rule
```

Debate packets are stage-only artifacts in `RECURSION-GATE`; resolving them emits
`intent_debate_packet_resolved` events and does not auto-merge Record content.

---

## 4. Staging Automation (OpenClaw Skill / Cron)

An OpenClaw skill or cron job can run signal detection and **stage** candidates to RECURSION-GATE. It must **never** merge.

### What the Agent May Do

- Read SELF, EVIDENCE, SESSION-LOG
- Analyze exchanges or artifacts for profile-relevant signals
- Write new candidates to RECURSION-GATE in the correct format

### What the Agent May NOT Do

- Merge into SELF, EVIDENCE, or prompt.py
- Change `status: approved` or move candidates to Processed
- Delete or overwrite existing profile content

### RECURSION-GATE Candidate Format

Each candidate uses this structure (see `users/grace-mar/recursion-gate.md`):

```yaml
status: pending
mind_category: knowledge | curiosity | personality
signal_type: <e.g. new_interest, lookup, linguistic>
summary: <one-line description>
profile_target: <e.g. IX-A, IX-B, IX-C>
suggested_entry: <proposed self.md text>
evidence: <ACT-XXXX or artifact reference>
```

Agents append to the **Candidates** section. The companion reviews and changes `status` to `approved` or `rejected`, then tells the operator to "process the review queue."

### Analyst Logic

Signal detection follows the same logic as `bot/prompt.py` ANALYST_PROMPT:

| Signal | mind_category | Profile target |
|--------|---------------|----------------|
| Fact learned, looked up | knowledge | IX-A |
| Topic engagement, new interest | curiosity | IX-B |
| Linguistic habit, behavior, value | personality | IX-C |

---

## 5. Permission Summary

| Action | Agent | User |
|--------|-------|------|
| Export Record → user.md | ✅ (read + transform) | — |
| Read SESSION-LOG, RECURSION-GATE, EVIDENCE | ✅ | ✅ |
| Stage candidates to RECURSION-GATE | ✅ | ✅ |
| Approve/reject candidates | ❌ | ✅ |
| Merge into SELF, EVIDENCE, prompt | ❌ | ✅ |
| Invoke "we did X" pipeline | — | ✅ (operator assists) |

### 5.5 Security Considerations

- **Third-party OpenClaw skills** — Community skills and plugins are a major attack surface. Prefer Grace-Mar's native tooling (`openclaw_hook`, `openclaw_stage`) over third-party Record-sync skills. If you use a skill for staging, audit it; better: point OpenClaw at the behavior and have it build its own version.
- **Injection and hijack** — OpenClaw agents can be targeted (e.g. malicious sites, prompt injection). Inbound handback runs an advisory constitutional check before staging. Never auto-merge from OpenClaw; the companion gate is the defense.
- **Local preferred** — Running OpenClaw locally (e.g. Mac Mini, Mac Studio) is generally more secure than on a VPS. See [Deployment topology](#deployment-topology-local-vs-vps) above.

---

## 6. Quick Reference

**Export identity:**
```bash
python scripts/export_user_identity.py --user grace-mar -o openclaw/user.md
python integrations/openclaw_hook.py --user grace-mar --format md+manifest --emit-event
python scripts/export_runtime_bundle.py --user grace-mar --mode adjunct_runtime -o openclaw/runtime-bundle
```

**Session continuity (read first):**
- `users/grace-mar/session-log.md`
- `users/grace-mar/recursion-gate.md`
- `users/grace-mar/self-evidence.md` (last entries)

**Pipeline invocation:**
- User: "we [did X]" [+ optional artifact path]
- Operator: Run signal detection → stage → companion approves → merge

**Operator bot command:**
- `/openclaw_export [format] [output_dir]`
- Example: `/openclaw_export json+md ../openclaw`

---

## 7. School Transfer

When the companion switches schools, the Record moves with them. See **[PORTABILITY](portability.md)** for:

- Ownership principle (Record belongs to the companion)
- Transfer checklist
- Handoff format (identity vs. full fork)
- Revocation guidance for the previous school

Export commands used for handoff:
```bash
python scripts/export_user_identity.py -u grace-mar -o handoff-identity.md
python scripts/export_fork.py -u grace-mar -o handoff-fork.json
```

---

## Research

- [work-build-ai/research-moonshots-237.md](skill-work/work-build-ai/research-moonshots-237.md) — Moonshots #237 (Alex Finn): identity, memory, security, hierarchy.

---

*Document version: 1.0*
*Last updated: February 2026*
