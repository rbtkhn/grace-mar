# Analysis: Grace-Mar Evidence Module and Redundancy Audit

**Purpose:** Analyze the Record's **evidence** layer — scope, terminology, linkage to SELF/SKILLS — and audit `users/grace-mar` for redundant or overlapping files.

**Sources:** `users/grace-mar/self-evidence.md`, `docs/id-taxonomy.md`, `docs/evidence-template.md`, `docs/conceptual-framework.md`  
**Date:** 2026-02-26

---

## 1. Terminology: "Self-Evidence" vs EVIDENCE

**"Self-evidence"** is not a canonical term in grace-mar. ID-TAXONOMY and CONCEPTUAL-FRAMEWORK define companion self as:

- self-knowledge, self-curiosity, self-personality  
- self-skill-write, self-skill-read, self-skill-work  
- self-archive, self-library, self-memory, self-voice  

There is no **self-evidence** label. The Record module that holds raw activity is **EVIDENCE** (`self-evidence.md`).

**EVIDENCE** = the canonical activity log. It is the *source* for SELF (IX-A/B/C via `evidence_id`) and SKILLS (WRITE/READ/WORK samples). It holds:

| Section | Prefix | Description |
|---------|--------|-------------|
| I. Reading List | READ-* | Books, articles consumed |
| II. Writing Log | WRITE-* | Writing samples, journals, stories |
| III. Creation Log | CREATE-* | Artwork, collages, creative output |
| IV. Media Log | MEDIA-* | Movies, shows, games |
| V. Activity Log | ACT-* | Bot exchanges, lookups, physical artifacts |

Raw evidence → pipeline → SELF/SKILLS. EVIDENCE is canonical; SELF and SKILLS derive from it.

---

## 2. Evidence vs Other User Logs

| File | Role | Scope | Part of Record? |
|------|------|-------|-----------------|
| **self-evidence.md** | Raw activity logs (READ, WRITE, CREATE, MEDIA, ACT) | Entry-level | Yes |
| **session-log.md** | Session chronicle — dates, participants, what was merged | Session-level | Yes |
| **session-transcript.md** | Raw conversation log for operator continuity | Real-time append | No |
| **self-archive.md** | Gated log of approved activity (voice, non-voice) | Merge-time append | Yes |
| **journal.md** | Curated daily highlights, first-person, public-suitable | Derived from evidence | Yes |
| **companion-context.md** | Companion (human) artistic style, personality | Working context | No |

**Distinctions:**

- **self-evidence.md** vs **journal.md** — Evidence holds raw entries; journal is curated first-person summary with `source_id` links. Journal derives from evidence. Different format and purpose.
- **session-log.md** vs **self-evidence.md** — Session-log is session grain (what happened in session X); evidence is entry grain (ACT-0001, WRITE-0006). Different grain; session-log references evidence IDs.
- **session-transcript.md** vs **self-archive.md** — Session-transcript is real-time operator continuity; self-archive is gated subset appended on merge. Approved exchanges appear in both at different stages; different lifecycles (transcript can rotate; archive is permanent).
- **companion-context.md** — Human companion context (artistic style, personality). Derived from ACT-0036. Working file for operator; not part of child's Record.

---

## 3. File Inventory and Redundancy Status

### Canonical Record

| File | Purpose | Redundancy |
|------|---------|------------|
| self.md | Identity, IX-A/B/C | None |
| skills.md | WRITE, READ, BUILD containers | None |
| self-evidence.md | Raw activity logs | None |
| library.md | Curated lookup sources | None |
| pending-review.md | Pipeline staging | None |
| self-archive.md | Gated approved activity | None |
| session-log.md | Session chronicle | None |
| journal.md | Daily highlights (derived) | None |

### Working / Context

| File | Purpose | Redundancy |
|------|---------|------------|
| session-transcript.md | Raw conversation log, operator continuity | None — different lifecycle from self-archive |
| memory.md | Ephemeral session context | None |
| companion-context.md | Companion artistic style, personality | None — human context, not Record |

### Seed / Survey

| File | Purpose | Redundancy |
|------|---------|------------|
| survey-capture.md | Seed survey capture template (Q1–Q4 preferences) | None — template for capture; data merged to self.md |
| seed-phase-2-survey.md | Artistic style survey | None — distinct instrument |
| seed-phase-3-survey.md | Later survey | None — distinct instrument |

### Pipeline / Ledger

| File | Purpose | Redundancy |
|------|---------|------------|
| pipeline-events.jsonl | Append-only pipeline audit (staged, applied, rejected) | None |
| merge-receipts.jsonl | Merge run receipts (approved_by, checksum, candidates) | None — different detail from pipeline-events |
| compute-ledger.jsonl | Token usage | None |

### Exports / Derived Outputs

| File | Purpose | Redundancy |
|------|---------|------------|
| llms.txt | PRP anchor for LLM instantiation | By design — copy for consumption |
| curriculum_profile.json | Curriculum export | By design |
| symbolic_identity.json | Symbolic identity export | By design |
| fork-manifest.json | Fork manifest | By design |
| manifest.json | Manifest export | By design |
| user.md | OpenClaw export | By design — regenerable from SELF |

Exports duplicate content by design; they are outputs for different consumers. Not redundant in the problematic sense.

### One-off / Analysis

| File | Purpose | Redundancy |
|------|---------|------------|
| analysis-homework-samples-2026-02-24.md | Homework analysis | Working doc; archive candidate after use |
| audit-grok-transcript-2026-02-24.md | Audit transcript | Working doc; archive candidate after use |
| notes/2026-02-25-telegram-log.md | One-off manual capture of Telegram chat | May overlap with session-transcript if bot appends; one-off paste for operator. Archive after use. |

---

## 4. Conclusion

- **No problematic redundancy** — Canonical Record files (evidence, session-log, self-archive, journal) have distinct roles and grain.
- **"Self-evidence"** — Not a standard term; use **EVIDENCE** for the Record's activity log.
- **Exports** — Derived copies by design; not redundancy issues.
- **One-off artifacts** — `analysis-homework-samples-2026-02-24.md`, `audit-grok-transcript-2026-02-24.md`, `notes/2026-02-25-telegram-log.md` are candidates for archival or pruning after use, not for deletion as redundant.
