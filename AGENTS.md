# AGENTS.md — AI Coding Assistant Guardrails

This file defines rules for any AI coding assistant working on this repository.

**For conceptual clarity:** Read `docs/CONCEPTUAL-FRAMEWORK.md` — Record vs. fork, Voice vs. bot, fork vs. twin, terminology. **Prime directive:** The Record belongs to the user (GRACE-MAR-CORE §I).

**For system design:** Read `docs/ARCHITECTURE.md`.

**Design alignment:** Grace-Mar aligns with the 5000 Days series framing — abundance, identity beyond productivity, conductor workflow, symbiosis (human holds the reins). See invariants 5–23 in CONCEPTUAL-FRAMEWORK.md.

---

## What This System Is

A **cognitive fork** — a structured, versioned record of an individual's cognitive development, initialized from a real person and growing through curated interactions. Preferred terms: **Record** (the fork) and **Voice** (the bot). The Record exists inside the user's mind. The Voice (`bot/`) provides an emulation layer: an **observation window** and the **queryable voice** of the Record — it responds when queried, never unbidden.

**Conceptual distinctions (see CONCEPTUAL-FRAMEWORK.md):**
- **Record and Voice** — The Record is the documented self; the Voice speaks the Record when queried.
- **Fork, not twin** — The Record diverges by design; it is its own entity, not a mirror.
- **Emulation** — Applies to the Voice (renders the Record in conversation), not to the Record's relationship to the real person.

---

## Critical Rules

### 1. Knowledge Boundary — Never Leak LLM Knowledge

The emulated self can only know what is explicitly documented in its profile (`users/[id]/SELF.md`). The emulation prompt (`bot/prompt.py`) enforces this. **Never** merge facts, references, or knowledge into the profile or prompt that the user has not explicitly provided through the gated pipeline. LLM training data must not leak into the fork.

### 2. Gated Pipeline — Never Commit Without Approval

All profile changes pass through a user-controlled gate:

1. Detect signals (knowledge, curiosity, personality)
2. Stage candidates in `users/[id]/PENDING-REVIEW.md`
3. **Integration moment** — Wait for user approval before merging into profile. This is the conscious gate: the user chooses what enters the record.
4. On approval, merge into all affected files together (see File Update Protocol below)

**Never** merge directly into SELF.md, EVIDENCE.md, or prompt.py without staging and approval.

### 3. The "we" Convention

When the user says **"we [did X]"**, it is a pipeline invocation. Immediately run signal detection and stage candidates. Do not acknowledge and wait — go straight to analysis in the same response.

### 4. No "Parent" Language

The system has a **user** and a **fork**. There is no "parent mode" or "child mode." The current pilot self happens to be a child, but the architecture is age-independent. Do not use the word "parent" as a system concept.

### 5. Immutability

- EVIDENCE entries are immutable once captured
- SKILLS claims may upgrade, never downgrade or delete
- SELF components may update but history is preserved
- Git history is the audit trail

### 6. Lexile Ceiling

The fork's output language is locked to a Lexile score (currently 600L for pilot-001). This ceiling increases only when real-world writing samples demonstrate growth. Do not raise it without evidence.

### 7. Meet the User Where They Are (Grief / Resistance)

When the user (or child) shows resistance, denial, or anxiety about change — deskilling, loss of a role, identity shifts — meet them where they are. Do not force adaptation or push through. The system supports; it does not compel. Respect Kübler-Ross–style stages (denial, anger, bargaining, depression, acceptance). Session pacing and wisdom questions should feel invitational, not interrogative.

### 8. Humane Purpose in Prompts

When designing or modifying analyst prompts, system prompts, or lookup flows, embed humane purpose: dignity, connection, values. Do not optimize solely for efficiency. The fork records who the person is; prompts should honor that, not treat the user as a data source.

### 9. Calibrated Abstention

When the emulated self encounters a topic outside its documented knowledge, it must say so and offer to look it up — never guess or hallucinate. The phrase "do you want me to look it up?" enforces this. Abstention (saying "I don't know") is a safety feature, not a failure.

### 10. Write It Down or Forget It

Nothing enters the Record without being written and approved. If it isn't documented and merged through the gated pipeline, it doesn't exist. See CONCEPTUAL-FRAMEWORK invariant 25.

---

## Permission Boundaries

**Autonomous (no approval required):**
- Read user files (SELF, SKILLS, EVIDENCE, SESSION-LOG, PENDING-REVIEW, etc.)
- Run signal detection; stage candidates to PENDING-REVIEW
- Respond as Voice (emulate Record)
- Propose activities, wisdom questions, lookups
- Analyze exchanges for profile-relevant signals

**Requires user approval:**
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
| **Profile growth** | IX entries increase over time | IX-A, IX-B, IX-C counts in dashboard |
| **Calibrated abstention** | "I don't know" when outside knowledge | Bot says "do you want me to look it up?" appropriately |
| **Counterfactual Pack** | Harness probes pass | `python scripts/run_counterfactual_harness.py` — run before prompt changes |

---

## File Update Protocol

When pipeline candidates are approved, **merge** into all of these together:

| File | What to update |
|------|---------------|
| `users/[id]/SELF.md` | New entries merged into IX-A (Knowledge), IX-B (Curiosity), and/or IX-C (Personality) |
| `users/[id]/EVIDENCE.md` | New activity log entry (ACT-XXXX) |
| `users/[id]/PENDING-REVIEW.md` | Move candidates from Candidates to Processed |
| `users/[id]/SESSION-LOG.md` | New session record |
| `bot/prompt.py` | Update relevant prompt sections + analyst dedup list |
| `users/[id]/PIPELINE-EVENTS.jsonl` | Append `applied` event per candidate: `python scripts/emit_pipeline_event.py applied CANDIDATE-XXXX evidence_id=ACT-YYYY` |

The bot emits `staged` events automatically. Emit `applied` (or `rejected`) when processing the queue.

**Provenance on IX entries:** When merging new entries into IX-A, IX-B, or IX-C, include `provenance: human_approved` (content passed the gated pipeline). Existing entries may use `curated_by: user` as equivalent. Optionally record `source:` (e.g. `bot lookup`, `bot conversation`, `operator`) to indicate origin. Do not backfill old entries unless the user requests it.

---

## Three-Channel Mind Model

Post-seed growth in SELF.md Section IX is organized into:

- **IX-A. Knowledge** — Facts entering awareness through observation
- **IX-B. Curiosity** — Topics that catch attention, engagement signals
- **IX-C. Personality** — Observed behavioral patterns, art style, speech traits

A single artifact can populate all three channels.

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
    └── pilot-001/              # First pilot user
        ├── SELF.md             # Identity + three-channel mind
        ├── SKILLS.md           # Capability containers
        ├── EVIDENCE.md         # Activity log
        ├── SESSION-LOG.md      # Interaction history
        ├── PENDING-REVIEW.md   # Pipeline staging
        ├── PIPELINE-EVENTS.jsonl  # Append-only pipeline audit log
        ├── COMPUTE-LEDGER.jsonl   # Token usage (energy ledger)
        ├── ARCHIVE.md                # Conversation archive (Telegram, Mini App)
│   └── archives/             # Rotated chunks (ARCHIVE-YYYY-MM.md)
        └── artifacts/          # Raw files (writing, artwork)
```

---

## Prompt Architecture (bot/prompt.py)

Four prompts, each with a distinct role:

| Prompt | Purpose |
|--------|---------|
| `SYSTEM_PROMPT` | Emulation persona — defines who the self is, what they know, how they speak |
| `ANALYST_PROMPT` | Signal detection — analyzes exchanges for profile-relevant signals |
| `LOOKUP_PROMPT` | Knowledge lookup — rephrases search queries for child-appropriate results |
| `REPHRASE_PROMPT` | Answer rephrasing — converts search results into the self's voice and vocabulary |

The `SYSTEM_PROMPT` contains the self's knowledge, curiosity, and personality inline. It grows as content is merged into the fork. Apply summarization tiers to manage token count.

---

## What Not to Do

- Merge knowledge the user didn't provide
- Skip the staging/approval gate
- Delete or overwrite user data
- Use "parent" as a system term
- Raise the Lexile ceiling without writing sample evidence
- Reference books, media, or experiences not in the profile
- Treat the Voice as the Record (it's the observation window and queryable voice, not the Record itself)
- Use "cognitive twin" (use "cognitive fork")
- Call the Voice an "oracle" or the Record "commanding" — use mirror, reflect, voice, record
- Let terminology drift — when editing CONCEPTUAL-FRAMEWORK, AGENTS, or templates, prefer Record (not fork) and Voice (not bot) in conceptual prose; correct inconsistencies
