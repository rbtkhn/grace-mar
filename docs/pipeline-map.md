# Pipeline Map

**Purpose:** Diagram the feedback loops that feed the cognitive fork — which modules feed which, where data is transformed, and where loops exist or are missing.

**See also:** [architecture.md](architecture.md), [grace-mar.mdc](../.cursor/rules/grace-mar.mdc)

---

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           INPUT CHANNELS                                         │
├─────────────────────────────────┬───────────────────────────────────────────────┤
│  Channel 1: Bot (Automated)     │  Channel 2: Operator (Manual)                  │
│  Telegram → Analyst → PENDING   │  "We [did X]" → Cursor → PENDING               │
└────────────────┬────────────────┴───────────────────────┬───────────────────────┘
                 │                                        │
                 └────────────────────┬───────────────────┘
                                      ▼
                         ┌─────────────────────────┐
                         │     PENDING-REVIEW      │
                         │  (integration moment:   │
                         │   user approve/reject)  │
                         └────────────┬────────────┘
                                      │ approved
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           INTEGRATION                                            │
│  self.md  │  self-evidence.md (ACT-*)  │  SESSION-LOG  │  bot/prompt.py              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           FORK STATE                                             │
│  SELF (IX-A/B/C)  │  SKILLS (THINK/WRITE/WORK)  │  EVIDENCE (module logs)  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Recursive Learning Process

**Recursive learning** means the Record improves itself over time: each cycle refines the model of the person, and the refined Record shapes the next cycle's inputs and interpretations.

### Definition

The **recursive learning process** is:

1. **Input** — Activity (conversation, artifact, "we did X") enters the system.
2. **Signal detection** — Analyst compares input to current Record; identifies new knowledge, curiosity, personality.
3. **Staging** — Candidates written to PENDING-REVIEW.
4. **Integration moment** — User approves or rejects.
5. **Merge** — Approved content integrated into SELF, EVIDENCE, prompt.
6. **Updated Record** — Fork state now reflects the new content.
7. **Cycle repeats** — Next input is analyzed *against the updated Record* (dedup, richer context). Voice responses use the updated profile. Proposed activities (future) could use SKILLS container edge.

**Recursion** = The output of step 6 becomes input to step 1 (indirectly): the Record influences what gets detected (analyst dedup), what the Voice says (SYSTEM_PROMPT), and—when implemented—what activities get proposed (container edge).

### Current vs. Full Recursion

| Loop | Status | Description |
|------|--------|-------------|
| **Forward** (input → Record) | ✅ Implemented | Activity → detect → stage → approve → merge |
| **Record → Voice** | ✅ Implemented | Prompt embeds Record; Voice speaks from it |
| **Record → Analyst** | ✅ Implemented | Dedup list prevents re-staging known content |
| **Record → Proposed activities** | ❌ Not implemented | SKILLS container edge could drive "propose activity at edge" |

The edge→quest loop (Record proposes activities at the container boundary) would close the recursion: the Record would influence *what the companion is invited to do next*, creating new input. See Gaps below.

### Cybernetic Framing

The pipeline is a **cybernetic loop** (Wiener): feedback corrects drift. Entropy (forgotten details, LLM leak, stale profile) is countered by sustained input and approval. Session continuity (read SESSION-LOG, PENDING-REVIEW before starting) closes the loop across sessions.

---

## Channel 1: Bot Pipeline

```
User message (Telegram)
        │
        ▼
┌───────────────────┐
│  Grace-Mar reply  │  ← SYSTEM_PROMPT (SELF, SKILLS, EVIDENCE inline)
└─────────┬─────────┘
          │
          ├──[if lookup triggered]──► LIBRARY query first → if hit: REPHRASE; if miss: LOOKUP_PROMPT → REPHRASE_PROMPT → reply
          │
          ▼
┌───────────────────┐
│  Analyst (async)  │  ← ANALYST_PROMPT, compares to profile for dedup
└─────────┬─────────┘
          │
          ├──[signal found]──► stage_candidate() → pending-review.md
          └──[NONE]──────────► (no staging)
```

**Bot feeds:** SELF (IX-A Knowledge, IX-B Curiosity, IX-C Personality) via lookup and conversation signals. Does **not** directly feed SKILLS modules or EVIDENCE module logs (THINK/WRITE/WORK).

**Bot produces:** ACT-* entries (activity log) when candidates are approved. Each approved candidate becomes an ACT-* + SELF entry + prompt.py update.

---

## Channel 2: Operator Pipeline

```
User says "we [did X]" (Cursor)
        │
        ▼
┌───────────────────┐
│  Signal detection │  Manual analysis — identify knowledge, curiosity, personality
│  (human + AI)     │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  Stage candidate  │  Write to pending-review.md with analysis
└─────────┬─────────┘
          │
          ▼
    [same integration as Channel 1]
```

**Operator feeds:** Any observed activity — school work, art, overheard moments, real-world events. Same destination: PENDING-REVIEW → SELF, EVIDENCE (ACT-*), etc.

---

## Pillar Evidence Flows

### WRITE (EVIDENCE § II. WRITING LOG)

```
Physical artifact (handwritten)
        │
        ▼
┌───────────────────┐
│  User captures    │  Photograph → save to artifacts/
│  (manual)         │  Add entry to self-evidence.md Writing Log
└─────────┬─────────┘
          │
          ├──► skills.md WRITE (vocabulary, complexity, style)
          └──► SELF.linguistic_style, SELF.interests, SELF.emotional_patterns
```

**Automation:** None. Fully manual. No bot feed.

---

### READ (EVIDENCE § I. READING LIST)

```
Books / articles consumed
        │
        ▼
┌───────────────────┐
│  User logs        │  Add entry to self-evidence.md Reading List
│  (manual)         │  (Currently: 0 entries)
└─────────┬─────────┘
          │
          ├──► skills.md THINK (comprehension, vocabulary, interests)
          └──► SELF.interests, SELF.preferences, SELF.values
```

**Automation:** None. Fully manual. **Gap:** Bot conversations about books could feed interest signals, but those go to SELF IX-B (curiosity), not to THINK module. No structured READ evidence from bot.

---

### WORK creation (EVIDENCE § III. CREATION LOG — BUILD container)

```
Physical artifact (artwork, collage, etc.)
        │
        ▼
┌───────────────────┐
│  User captures    │  Photograph → save to artifacts/
│  (manual)         │  Add entry to self-evidence.md Creation Log
└─────────┬─────────┘
          │
          ├──► skills.md BUILD (originality, elaboration, flexibility)
          └──► SELF.reasoning_patterns, SELF.interests
```

**Automation:** None. Fully manual. No bot feed.

---

## SELF ← Pillar Feedback (from ARCHITECTURE)

| Pillar activity | Feeds SELF |
|-----------------|------------|
| WRITE | linguistic_style (primary), interests, emotional_patterns |
| THINK | interests, preferences, values |
| WORK (creation) | reasoning_patterns, interests |

---

## Integration Step (File Update Protocol)

The approval step is the **integration moment** — the conscious gate where the companion (Mind) chooses what enters the Record. When candidates are **approved**, merge into **all** of:

| File | Update |
|------|--------|
| `users/[id]/self.md` | IX-A, IX-B, IX-C entries (merged) |
| `users/[id]/self-evidence.md` | New ACT-* in Activity Log |
| `users/[id]/pending-review.md` | Move candidate to Processed |
| `users/[id]/session-log.md` | Session record |
| `bot/prompt.py` | YOUR KNOWLEDGE, YOUR CURIOSITY, YOUR PERSONALITY + analyst dedup list |

---

## Gaps and Missing Loops

| Gap | Description | Potential fix |
|-----|-------------|---------------|
| **THINK has no bot feed** | Bot conversations mention books, but THINK module (comprehension, vocabulary) has no automated input. Reading List is empty. | Add analyst signal for "book discussed" → stage candidate that could create READ-* or link to interest. Or: operator workflow for "we finished [book]." |
| **WRITE / WORK (creation) fully manual** | No automation for artifact capture. User must photograph, save, and write EVIDENCE entry. | Optional: upload flow (e.g. Telegram photo → staging for EVIDENCE), or template script for new WRITE/WORK entries. |
| **Edge → quest feedback** | Container edge (SKILLS) could drive "propose activity" but there is no automated quest generator. | Future: script that reads SKILLS, infers edge, outputs suggested activities. |
| ~~No pipeline event log~~ | ~~Staging and approval implicit in file edits~~ | ✅ Implemented: `pipeline-events.jsonl` — bot emits `staged`; operator runs `emit_pipeline_event.py applied CANDIDATE-XX` when processing. |

---

## Counterfactual Pack (Emulation Harness)

`scripts/run_counterfactual_harness.py` runs adversarial probes against the emulation. Probes stress the knowledge boundary, LLM-leak resistance, and in-scope behavior. Run before prompt changes to detect regressions.

```bash
python scripts/run_counterfactual_harness.py
```

---

## Loop Summary

| Loop | Exists? | Frequency |
|------|---------|-----------|
| Bot → Analyst → PENDING → Integration → SELF, prompt | ✅ Yes | Per exchange (when signal found) |
| Operator → PENDING → Integration → SELF, EVIDENCE | ✅ Yes | Per "we [did X]" |
| WRITE artifact → EVIDENCE → SKILLS, SELF | ✅ Yes | Manual, per artifact |
| READ artifact → EVIDENCE → SKILLS, SELF | ⚠️ Sparse | Manual, 0 entries so far |
| WORK (creation) artifact → EVIDENCE → SKILLS, SELF | ✅ Yes | Manual, per artifact |
| SKILLS/edge → propose activity → artifact → EVIDENCE | ❌ No | Not implemented. Would close recursive loop. |

---

*Last updated: February 2026*
