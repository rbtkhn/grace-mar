# OpenClaw Integration Guide

How to connect GRACE-MAR (cognitive fork / Record) with OpenClaw (personal agent workspace) so that:
- The Record feeds OpenClaw's identity layer (who it serves)
- Session continuity spans both systems
- OpenClaw artifacts can feed the grace-mar pipeline
- Staging automation stays gated — user remains the approval gate

---

## Overview

| Use Case | What it does | Permission |
|----------|--------------|------------|
| **Record as identity source** | Export SELF → USER.md or SOUL.md | Export script (read-only) |
| **Session continuity** | OpenClaw reads SESSION-LOG, PENDING-REVIEW, EVIDENCE | Read-only |
| **Artifacts as evidence** | OpenClaw outputs → "we did X" → pipeline | User invokes pipeline |
| **Staging automation** | OpenClaw skill/cron stages to PENDING-REVIEW | Stage only, never merge |

**Invariant:** The user is always the gate. OpenClaw can stage; it cannot merge into the Record.

---

## 1. Record as Identity Source

The grace-mar Record (SELF.md + selected SKILLS) can populate OpenClaw's `USER.md` or `SOUL.md` so the agent knows who it serves.

### Export Script

```bash
python scripts/export_user_identity.py --user pilot-001
```

Output: Markdown suitable for `USER.md` or `SOUL.md`, containing:
- Identity (name, age, languages, location)
- Preferences and interests
- Linguistic style and vocabulary level
- Personality traits and values
- Post-seed growth (IX-A knowledge, IX-B curiosity, IX-C personality)

### Sync Options

| Approach | When to use |
|----------|-------------|
| **Manual** | Run export and paste into USER.md when profile changes |
| **Pre-session** | Run export as part of OpenClaw startup before agent runs |
| **Cron** | Export on commit (e.g. post-merge hook) if workspace is shared |

### What NOT to export

- Raw EVIDENCE content (too large, not identity-defining)
- Session logs (temporal, not identity)
- PENDING-REVIEW (staging, not canonical)

---

## 2. Session Continuity (Startup Checklist)

When running in a shared workspace or OpenClaw session, read these grace-mar files **before** starting work:

| File | Purpose |
|------|---------|
| `users/[id]/SESSION-LOG.md` | Last session summary; what happened |
| `users/[id]/PENDING-REVIEW.md` | Any staged candidates awaiting approval |
| `users/[id]/EVIDENCE.md` (last 1–2 entries) | Recent context for activities |

### OpenClaw Startup Additions

If OpenClaw has a startup checklist (e.g. `active-tasks.md`, `HEARTBEAT.md`), add:

```
Grace-Mar continuity (if users/pilot-001 exists):
- [ ] Read last SESSION-LOG entry
- [ ] Check PENDING-REVIEW — any candidates to process?
- [ ] Skim last 1–2 EVIDENCE entries
```

### Workspace Layout

Two patterns:

**A. grace-mar as subdir of OpenClaw**
```
openclaw/
├── USER.md           # ← populated from grace-mar export
├── active-tasks.md
├── memory/
└── grace-mar/        # ← symlink or copy of grace-mar repo
    └── users/pilot-001/
```

**B. OpenClaw and grace-mar sibling repos**
```
workspace/
├── openclaw/
└── grace-mar/
```
Export script path: `../grace-mar/scripts/export_user_identity.py`

---

## 3. Artifacts as Evidence

OpenClaw-produced artifacts (writing, drawings, summaries) can feed the grace-mar pipeline via the **"we" convention**.

### Workflow

1. User creates something with OpenClaw (e.g. story, research summary, drawing)
2. User says: "we wrote a story about volcanoes today" (optionally attaching the file)
3. Operator (Cursor session or pipeline) runs signal detection
4. Candidates staged to PENDING-REVIEW
5. User approves; merge into SELF, EVIDENCE, SESSION-LOG

### Path Convention

If OpenClaw writes to `outputs/` or `memory/`, you can reference:

```
"we wrote a story — it's in openclaw/outputs/volcano-story.md"
```

The pipeline treats this like any other "we did X" + artifact. The operator loads the file and runs analyst logic.

### No Automatic Ingestion

Artifacts do **not** auto-ingest. The user must explicitly invoke the pipeline ("we did X") and approve any candidates. This preserves the gate.

---

## 4. Staging Automation (OpenClaw Skill / Cron)

An OpenClaw skill or cron job can run signal detection and **stage** candidates to PENDING-REVIEW. It must **never** merge.

### What the Agent May Do

- Read SELF, EVIDENCE, SESSION-LOG
- Analyze exchanges or artifacts for profile-relevant signals
- Write new candidates to PENDING-REVIEW in the correct format

### What the Agent May NOT Do

- Merge into SELF, EVIDENCE, or prompt.py
- Change `status: approved` or move candidates to Processed
- Delete or overwrite existing profile content

### PENDING-REVIEW Candidate Format

Each candidate uses this structure (see `users/pilot-001/PENDING-REVIEW.md`):

```yaml
status: pending
mind_category: knowledge | curiosity | personality
signal_type: <e.g. new_interest, lookup, linguistic>
summary: <one-line description>
profile_target: <e.g. IX-A, IX-B, IX-C>
suggested_entry: <proposed SELF.md text>
evidence: <ACT-XXXX or artifact reference>
```

Agents append to the **Candidates** section. The user reviews and changes `status` to `approved` or `rejected`, then tells the operator to "process the review queue."

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
| Export Record → USER.md | ✅ (read + transform) | — |
| Read SESSION-LOG, PENDING-REVIEW, EVIDENCE | ✅ | ✅ |
| Stage candidates to PENDING-REVIEW | ✅ | ✅ |
| Approve/reject candidates | ❌ | ✅ |
| Merge into SELF, EVIDENCE, prompt | ❌ | ✅ |
| Invoke "we did X" pipeline | — | ✅ (operator assists) |

---

## 6. Quick Reference

**Export identity:**
```bash
python scripts/export_user_identity.py --user pilot-001 -o openclaw/USER.md
```

**Session continuity (read first):**
- `users/pilot-001/SESSION-LOG.md`
- `users/pilot-001/PENDING-REVIEW.md`
- `users/pilot-001/EVIDENCE.md` (last entries)

**Pipeline invocation:**
- User: "we [did X]" [+ optional artifact path]
- Operator: Run signal detection → stage → user approves → merge

---

## 7. School Transfer

When the user switches schools, the Record moves with them. See **[PORTABILITY](PORTABILITY.md)** for:

- Ownership principle (Record belongs to the user)
- Transfer checklist
- Handoff format (identity vs. full fork)
- Revocation guidance for the previous school

Export commands used for handoff:
```bash
python scripts/export_user_identity.py -u pilot-001 -o handoff-identity.md
python scripts/export_fork.py -u pilot-001 -o handoff-fork.json
```

---

*Document version: 1.0*
*Last updated: February 2026*
