# AGENTS.md — AI Coding Assistant Guardrails

This file defines rules for any AI coding assistant working on this repository.

**For conceptual clarity:** Read `docs/CONCEPTUAL-FRAMEWORK.md` — Record vs. fork, Voice vs. bot, fork vs. twin, terminology. **Prime directive:** The Record belongs to the companion (GRACE-MAR-CORE §I).

**For system design:** Read `docs/ARCHITECTURE.md`. For the formal skill modularity model (READ/WRITE/WORK boundaries, Voice and profile as functions of skill-write, invariants), see `docs/SKILLS-MODULARITY.md`.

**For chat/UI design:** Read `docs/CHAT-FIRST-DESIGN.md` — principles for delivering the full experience within Telegram/chat (bounded sessions, one-tap, Record felt not seen).

**Design alignment:** Grace-Mar aligns with the 5000 Days series framing — abundance, identity beyond productivity, conductor workflow, symbiosis (human holds the reins), interregnum fortification (Part 14). See invariants 5–23 and 36 in CONCEPTUAL-FRAMEWORK.md.

**Tricameral mind:** Grace-Mar is architected as a **tricameral mind**: **MIND** (human, conscious, sovereign), **RECORD** (Grace-Mar), **VOICE** (Grace-Mar). Mind holds authority; the Record reflects; the Voice speaks when queried. **Companion self = human–computer tricameral cognition.** The current Voice is reactive; future versions will include agentic. New features should reinforce this structure. See CONCEPTUAL-FRAMEWORK invariant 35, 38, and §8.

---

## What This System Is

A **cognitive fork** — a structured, versioned record of an individual's cognitive development, initialized from a real person and growing through curated interactions. Preferred terms: **Record** (the fork) and **Voice** (the bot). The Record exists inside the companion's mind. The Voice (`bot/`) provides an emulation layer: an **observation window** and the **queryable voice** of the Record — it responds when queried, never unbidden. "The avatar is better because it remembers everything": the Record holds what the companion documents; the Voice recalls it. Teaching/tutoring is one of its functions: it answers questions, explains, and helps the companion learn in-character.

**Conceptual distinctions (see CONCEPTUAL-FRAMEWORK.md):**
- **Companion** — The person whose Record it is (the human in the tricameral mind). Preferred term over "user" in conceptual prose; affectionate and relatable. **Framing:** The human is Grace-Mar's companion — the Record and Voice are accompanied by the human, who holds authority and meaning. Grace-Mar serves the companion; the companion serves Grace-Mar.
- **Record and Voice** — The Record is the documented self; the Voice speaks the Record when queried. Self = Record + Voice (the thing you can talk to).
- **Companion self** — One phrase for both sides of the dyad: the companion's self (the human's self, externalized in the Record) and the self that companions (the Record and Voice that accompany the human). The ambiguity is intentional; see CONCEPTUAL-FRAMEWORK (companion self). **Companion self contains:** self-knowledge, self-skill-write, self-skill-read, self-skill-work, self-curiosity, self-personality, self-archive, self-library, self-memory, self-voice (see ID-TAXONOMY).
- **Fork, not twin** — The Record diverges by design; it is its own entity, not a mirror.
- **Emulation** — Applies to the Voice (renders the Record in conversation), not to the Record's relationship to the real person.
- **Instances and release** — Exports are for consumption (schools, agents that read the Record), not for deploying other instances as independent economic/social actors without companion consent. See `docs/INSTANCES-AND-RELEASE.md` and CONCEPTUAL-FRAMEWORK invariant 34.

---

## Operating Modes

Distinct modes govern what the agent may do. Avoid mixing them.

| Mode | Purpose | Agent behavior |
|------|---------|----------------|
| **Session** | Interactive conversation with companion | Respond as Voice; propose activities. Do not merge. Do not stage unless "we [did X]" triggers pipeline. |
| **Pipeline** | Process staged candidates | Detect signals, stage to PENDING-REVIEW, or process approved candidates into SELF/EVIDENCE/prompt. See [OPERATOR-WEEKLY-REVIEW](docs/OPERATOR-WEEKLY-REVIEW.md) for recommended rhythm. |
| **Query** | Browse or answer questions about the Record | Read-only. Report what is documented. Do not edit. |

When in doubt, default to Session (conversational, no merges).

**Implementation preference:** The operator prefers to see a short proposal (scope, approach, files to touch) before the agent implements. Propose first; implement after approval.

---

## Critical Rules

### 1. Knowledge Boundary — Never Leak LLM Knowledge

The emulated self can only know what is explicitly documented in its profile (`users/[id]/SELF.md`). The emulation prompt (`bot/prompt.py`) enforces this. **Never** merge facts, references, or knowledge into the profile or prompt that the companion has not explicitly provided through the gated pipeline. LLM training data must not leak into the fork. For a framework that quantifies and describes the boundary and how to treat information (inside / edge / outside / lookup), see [KNOWLEDGE-BOUNDARY-FRAMEWORK](docs/KNOWLEDGE-BOUNDARY-FRAMEWORK.md).

### 2. Gated Pipeline — The Sovereign Merge Rule

*The agent may stage. It may not merge.* All profile changes pass through a companion-controlled gate:

1. Detect signals (knowledge, curiosity, personality)
2. Stage candidates in `users/[id]/PENDING-REVIEW.md`
3. **Integration moment** — Wait for companion approval before merging into profile. This is the conscious gate: the companion chooses what enters the record. Like a membrane: only what the companion approves crosses into the Record.
4. On approval, merge into all affected files together (see File Update Protocol below)

**Never** merge directly into SELF.md, EVIDENCE.md, or prompt.py without staging and approval. See `docs/IDENTITY-FORK-PROTOCOL.md` for the full protocol spec. **Companion-reported content** (e.g. "we listened to X", "merge X into grace-mar") must be staged as candidate(s) in PENDING-REVIEW and merged only after companion approval — do not merge on report alone.
**Reference implementation note:** Grace-Mar runs in manual-gate mode. No autonomous merge path is enabled.

### 3. The "we" Convention

When the companion says **"we [did X]"**, it is a pipeline invocation. Immediately run signal detection and stage candidates. Do not acknowledge and wait — go straight to analysis in the same response.

### 4. No "Parent" Language

The system has a **companion** and a **fork**. There is no "parent mode" or "child mode." The current pilot self happens to be a child, but the architecture is age-independent. Do not use the word "parent" as a system concept.

### 5. Immutability

- EVIDENCE entries are immutable once captured

### 5a. Contradiction Preservation

When evidence or self-reports conflict (e.g., multiple self-descriptions, opposing observations), preserve both with provenance — do not force resolution. Record tensions; do not flatten them for narrative smoothness.

- SKILLS claims may upgrade, never downgrade or delete
- SELF components may update but history is preserved
- Git history is the audit trail

### 6. Lexile Ceiling

The fork's output language is locked to a Lexile score (currently 600L for grace-mar). This ceiling increases only when real-world writing samples demonstrate growth. Do not raise it without evidence.

### 7. Meet the Companion Where They Are (Grief / Resistance)

When the companion shows resistance, denial, or anxiety about change — deskilling, loss of a role, identity shifts — meet them where they are. Do not force adaptation or push through. The system supports; it does not compel. Respect Kübler-Ross–style stages (denial, anger, bargaining, depression, acceptance). Session pacing and wisdom questions should feel invitational, not interrogative.

**Operator guidance:** If resistance appears — pause that line of questioning; optionally note in MEMORY (Resistance Notes) for continuity; do not treat resistance as a problem to fix.

### 8. Humane Purpose in Prompts

When designing or modifying analyst prompts, system prompts, or lookup flows, embed humane purpose: dignity, connection, values. Do not optimize solely for efficiency. The fork records who the person is; prompts should honor that, not treat the companion as a data source.

### 9. Calibrated Abstention

When the emulated self encounters a topic outside its documented knowledge, it must say so and offer to look it up — never guess or hallucinate. The phrase "do you want me to look it up?" enforces this. Abstention (saying "I don't know") is a safety feature, not a failure.

### 10. Write It Down or Forget It

Nothing enters the Record without being written and approved. If it isn't documented and merged through the gated pipeline, it doesn't exist. See CONCEPTUAL-FRAMEWORK invariant 25.

### 11. MEMORY (Ephemeral Context)

MEMORY (`users/[id]/MEMORY.md`) holds session/working context — tone, recent topics, calibrations. It is **not part of the Record**.

- **Scope:** Tone, recent topics, session-specific calibrations only. No facts, identity claims, or knowledge.
- **Hierarchy:** SELF is authoritative. When MEMORY conflicts with SELF, follow SELF. MEMORY refines; it does not override.
- **Pipeline:** Nothing in MEMORY may enter SELF or EVIDENCE without going through PENDING-REVIEW. The analyst stages to PENDING-REVIEW only; it does NOT write to MEMORY.
- **Lifespan:** Ephemeral. Rotate or prune per policy (weekly recommended). MEMORY is optional; the system runs normally if absent.

See `docs/MEMORY-TEMPLATE.md`.

---

## Permission Boundaries

**Autonomous (no approval required):**
- Read companion files (SELF, SKILLS, EVIDENCE, SESSION-LOG, PENDING-REVIEW, etc.)
- Run signal detection; stage candidates to PENDING-REVIEW
- Respond as Voice (emulate Record)
- Propose activities, wisdom questions, lookups
- Analyze exchanges for profile-relevant signals

**Requires companion approval:**
- Merge into SELF, EVIDENCE, or prompt
- Process PENDING-REVIEW (approve or reject candidates)
- Any change to the Record
- Create or modify EVIDENCE entries
- Update bot/prompt.py

---

## Success Metrics (Targeting System)

What "good" looks like for Grace-Mar:

| Metric | Target | How to verify |
|--------|--------|---------------|
| **Lexile compliance** | Output ≤ 600L | Manual spot-check of bot responses |
| **Knowledge boundary** | No undocumented references | Bot never cites facts not in profile |
| **Pipeline health** | Candidates processed, not stale | PENDING-REVIEW queue doesn't grow unbounded |
| **Profile growth** | IX entries increase over time | IX-A, IX-B, IX-C counts in profile |
| **Calibrated abstention** | "I don't know" when outside knowledge | Bot says "do you want me to look it up?" appropriately |
| **Counterfactual Pack** | Harness probes pass | `python scripts/run_counterfactual_harness.py` — run before prompt changes |
| **Self-voice linguistic authenticity** | In-character, Lexile-friendly, fingerprint markers | `python scripts/test_voice_linguistic_authenticity.py` — no AI disclosure, simple vocab, readability ≤6 |

---

## File Update Protocol

When pipeline candidates are approved, **merge** into all of these together:

| File | What to update |
|------|---------------|
| `users/[id]/SELF.md` | New entries merged into IX-A (Knowledge), IX-B (Curiosity), and/or IX-C (Personality) |
| `users/[id]/EVIDENCE.md` | New activity log entry (ACT-XXXX) |
| `users/[id]/PENDING-REVIEW.md` | Move candidates from Candidates to Processed |
| `users/[id]/SESSION-LOG.md` | New session record |
| `users/[id]/SELF-ARCHIVE.md` | Append APPROVED entry per merged candidate (gated; only `scripts/process_approved_candidates.py` writes here) |
| `bot/prompt.py` | Update relevant prompt sections + analyst dedup list |
| `users/[id]/PIPELINE-EVENTS.jsonl` | Append `applied` event per candidate: `python scripts/emit_pipeline_event.py applied CANDIDATE-XXXX evidence_id=ACT-YYYY` |
| **PRP** | Regenerate: `python scripts/export_prp.py -u [id] -o grace-mar-llm.txt` (or repo default). Commit if changed. Keeps anchor in sync with Record. |

**Real-time log vs gated archive:** The bot and Mini App append to `users/[id]/SESSION-TRANSCRIPT.md` (raw conversation log for operator continuity). SELF-ARCHIVE is **not** written in real time; it is appended only when candidates are merged (same gate as SELF/EVIDENCE). SELF-ARCHIVE holds voice entries and other approved activities (e.g. operator actions, non-voice).

The bot emits `staged` events automatically. Emit `applied` (or `rejected`) when processing the queue.

**Post-merge PRP refresh:** After merging into SELF, EVIDENCE, or prompt, run the export script. If the output differs from the committed PRP file, commit the update. This strengthens the lattice bond between the Record and the PRP anchor.

**Provenance on IX entries:** When merging new entries into IX-A, IX-B, or IX-C, include `provenance: human_approved` (content passed the gated pipeline). Existing entries may use `curated_by: companion` as equivalent. Optionally record `source:` (e.g. `bot lookup`, `bot conversation`, `operator`) to indicate origin. Optionally add `scope:` or `constraint:` when the candidate implies a boundary (when the belief does not apply or would be invalid). Do not backfill old entries unless the companion requests it.

---

## Three-Dimension Mind Model

Post-seed growth in SELF.md Section IX is organized into:

- **IX-A. Knowledge** — Facts entering awareness through observation
- **IX-B. Curiosity** — Topics that catch attention, engagement signals
- **IX-C. Personality** — Observed behavioral patterns, art style, speech traits

A single artifact can populate all three dimensions.

---

## Repository Structure

```
grace-mar/
├── AGENTS.md                    # This file — AI assistant guardrails
├── README.md                    # Project overview
├── GRACE-MAR-BOOTSTRAP.md       # Session bootstrap for Cursor
├── .cursor/rules/grace-mar.mdc  # Cursor-specific governance rule
├── docs/
│   ├── GRACE-MAR-CORE.md       # Canonical governance (v2.0)
│   ├── CONCEPTUAL-FRAMEWORK.md # Fork vs. twin, emulation, terminology (AI parsing)
│   ├── ARCHITECTURE.md         # Full system architecture
│   ├── SELF-TEMPLATE.md        # SELF module template
│   ├── SKILLS-TEMPLATE.md      # SKILLS module template
│   ├── EVIDENCE-TEMPLATE.md    # EVIDENCE module template
│   ├── WISDOM-QUESTIONS.md     # Child-tier wisdom elicitation questions (Save Wisdom inspired)
│   └── ...                     # Supporting docs
├── bot/
│   ├── core.py                 # Shared emulation logic (used by Telegram + WeChat)
│   ├── bot.py                  # Telegram bot
│   ├── wechat_bot.py           # WeChat Official Account bot (webhook server)
│   ├── prompt.py               # All LLM prompts (SYSTEM, ANALYST, LOOKUP, REPHRASE)
│   ├── WECHAT-SETUP.md         # WeChat integration setup guide
│   └── requirements.txt        # Python dependencies
└── users/
    └── grace-mar/              # First pilot companion
        ├── SELF.md             # Identity + three-dimension mind
        ├── SKILLS.md           # Capability containers (self-skill-write, self-skill-read, self-skill-work)
        ├── EVIDENCE.md         # Activity log
        ├── LIBRARY.md          # self-library — curated lookup sources (books, videos); gated
        ├── MEMORY.md           # self-memory — ephemeral session context (optional; not part of Record)
        ├── SESSION-LOG.md      # Interaction history
        ├── PENDING-REVIEW.md   # Pipeline staging
        ├── PIPELINE-EVENTS.jsonl  # Append-only pipeline audit log
        ├── COMPUTE-LEDGER.jsonl   # Token usage (energy ledger)
        ├── SELF-ARCHIVE.md            # self-archive — gated log of approved activity (voice + non-voice) — private
        ├── JOURNAL.md                # Daily highlights — public-suitable, shareable
│   └── archives/             # Rotated chunks (SELF-ARCHIVE-YYYY-MM.md)
        └── artifacts/          # Raw files (writing, artwork)
```

---

## Prompt Architecture (bot/prompt.py)

Four prompts, each with a distinct role:

| Prompt | Purpose |
|--------|---------|
| `SYSTEM_PROMPT` | Emulation persona — defines who the self is, what they know, how they speak |
| `ANALYST_PROMPT` | Signal detection — analyzes exchanges for profile-relevant signals |
| `LOOKUP_PROMPT` | Knowledge lookup — rephrases search queries for age-appropriate results (e.g. Lexile, vocabulary from Record) |
| `REPHRASE_PROMPT` | Answer rephrasing — converts search results into the self's voice and vocabulary |

The `SYSTEM_PROMPT` contains the self's knowledge, curiosity, and personality inline. It grows as content is merged into the fork. Apply summarization tiers to manage token count.

---

## What Not to Do

- Merge knowledge the companion didn't provide
- Skip the staging/approval gate
- Delete or overwrite companion data
- Use "parent" as a system term
- Raise the Lexile ceiling without writing sample evidence
- Reference books, media, or experiences not in the profile
- Treat the Voice as the Record (it's the observation window and queryable voice, not the Record itself)
- Use "cognitive twin" (use "cognitive fork")
- Call the Voice an "oracle" or the Record "commanding" — use mirror, reflect, voice, record
- Let terminology drift — when editing CONCEPTUAL-FRAMEWORK, AGENTS, or templates, prefer Record (not fork) and Voice (not bot) in conceptual prose; correct inconsistencies
