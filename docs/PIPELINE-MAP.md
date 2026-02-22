# Pipeline Map

**Purpose:** Diagram the feedback loops that feed the cognitive fork — which modules feed which, where data is transformed, and where loops exist or are missing.

**See also:** [ARCHITECTURE.md](ARCHITECTURE.md), [grace-mar.mdc](../.cursor/rules/grace-mar.mdc)

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
                         │  (user approve/reject)  │
                         └────────────┬────────────┘
                                      │ approved
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           INTEGRATION                                            │
│  SELF.md  │  EVIDENCE.md (ACT-*)  │  SESSION-LOG  │  bot/prompt.py              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           FORK STATE                                             │
│  SELF (IX-A/B/C)  │  SKILLS (READ/WRITE/IMAGINE)  │  EVIDENCE (pillar logs)     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

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
          ├──[signal found]──► stage_candidate() → PENDING-REVIEW.md
          └──[NONE]──────────► (no staging)
```

**Bot feeds:** SELF (IX-A Knowledge, IX-B Curiosity, IX-C Personality) via lookup and conversation signals. Does **not** directly feed SKILLS pillars or EVIDENCE pillar logs (READ/WRITE/IMAGINE).

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
│  Stage candidate  │  Write to PENDING-REVIEW.md with analysis
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
│  (manual)         │  Add entry to EVIDENCE.md Writing Log
└─────────┬─────────┘
          │
          ├──► SKILLS.md WRITE (vocabulary, complexity, style)
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
│  User logs        │  Add entry to EVIDENCE.md Reading List
│  (manual)         │  (Currently: 0 entries)
└─────────┬─────────┘
          │
          ├──► SKILLS.md READ (comprehension, vocabulary, interests)
          └──► SELF.interests, SELF.preferences, SELF.values
```

**Automation:** None. Fully manual. **Gap:** Bot conversations about books could feed interest signals, but those go to SELF IX-B (curiosity), not to READ pillar. No structured READ evidence from bot.

---

### IMAGINE (EVIDENCE § III. CREATION LOG)

```
Physical artifact (artwork, collage, etc.)
        │
        ▼
┌───────────────────┐
│  User captures    │  Photograph → save to artifacts/
│  (manual)         │  Add entry to EVIDENCE.md Creation Log
└─────────┬─────────┘
          │
          ├──► SKILLS.md IMAGINE (originality, elaboration, flexibility)
          └──► SELF.reasoning_patterns, SELF.interests
```

**Automation:** None. Fully manual. No bot feed.

---

## SELF ← Pillar Feedback (from ARCHITECTURE)

| Pillar activity | Feeds SELF |
|-----------------|------------|
| WRITE | linguistic_style (primary), interests, emotional_patterns |
| READ | interests, preferences, values |
| IMAGINE | reasoning_patterns, interests |

---

## Integration Step (File Update Protocol)

When candidates are **approved**, merge into **all** of:

| File | Update |
|------|--------|
| `users/[id]/SELF.md` | IX-A, IX-B, IX-C entries (merged) |
| `users/[id]/EVIDENCE.md` | New ACT-* in Activity Log |
| `users/[id]/PENDING-REVIEW.md` | Move candidate to Processed |
| `users/[id]/SESSION-LOG.md` | Session record |
| `bot/prompt.py` | YOUR KNOWLEDGE, YOUR CURIOSITY, YOUR PERSONALITY + analyst dedup list |

---

## Gaps and Missing Loops

| Gap | Description | Potential fix |
|-----|-------------|---------------|
| **READ has no bot feed** | Bot conversations mention books, but READ pillar (comprehension, vocabulary) has no automated input. Reading List is empty. | Add analyst signal for "book discussed" → stage candidate that could create READ-* or link to interest. Or: operator workflow for "we finished [book]." |
| **WRITE / IMAGINE fully manual** | No automation for artifact capture. User must photograph, save, and write EVIDENCE entry. | Optional: upload flow (e.g. Telegram photo → staging for EVIDENCE), or template script for new WRITE/IMAGINE entries. |
| **Edge → quest feedback** | Container edge (SKILLS) could drive "propose activity" but there is no automated quest generator. | Future: script that reads SKILLS, infers edge, outputs suggested activities. |
| ~~No pipeline event log~~ | ~~Staging and approval implicit in file edits~~ | ✅ Implemented: `PIPELINE-EVENTS.jsonl` — bot emits `staged`; operator runs `emit_pipeline_event.py applied CANDIDATE-XX` when processing. |

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
| IMAGINE artifact → EVIDENCE → SKILLS, SELF | ✅ Yes | Manual, per artifact |
| SKILLS/edge → propose activity → artifact → EVIDENCE | ❌ No | Not implemented |

---

*Last updated: February 2026*
