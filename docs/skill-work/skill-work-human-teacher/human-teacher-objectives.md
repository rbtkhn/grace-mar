# Human-Teacher Objectives

**Purpose:** Formal list of objectives for the operator/caregiver when acting as human-teacher (without LLM) or when modulating LLM-derived prompts. Aligns with Phase 2 of [skill-work-human-teacher roadmap](roadmap.md).

**Design lens:** Agent maestro (structure provider) + evidence-first + augmentation. Human-teacher structures the session; LLM executes. See [educational-software-history-insights §K](../educational-software-history-insights.md#k-ai-era-insights-all-in-synthesis).

---

## 1. Pre-Session Objectives

### 1.1 Read skill-think before each session

- Skim `skill-think.md` (or THINK sections in skill-work) to recall the edge: reading, math, Chinese, WORK.
- Know what "just above current" means for today: Lexile input, math step, work edge.

### 1.2 Modulate focus

- Pick today's emphasis from THINK (reading/math/Chinese) or WORK.
- Use generator `--focus reading|math|work|integrated` when regenerating prompt.
- If human-teacher-led (no LLM), emphasize one area and stay at edge.

### 1.3 Gate content

- No facts, stories, or topics outside IX-A.
- Respect IX-C (personality, tone, resistance).
- If the learner asks about something undocumented, say "do you want me to look it up?" — do not invent.

### 1.4 Respect identity

- Values, tone, resistance. Meet where they are (AGENTS rule 7).
- If resistance appears, pause that line; optionally note in MEMORY (Resistance Notes); do not treat resistance as a problem to fix.

### 1.5 Toby bar (self-contained context)

State the session goal with enough context that the task is plausibly solvable without the agent going out and fetching more information. The lesson prompt should contain: WHO SHE IS, IX-A/B/C, edge, TODAY'S GOALS, rules. If the prompt is incomplete, regenerate with `--focus` or add missing Record excerpt. The generator emits a self-contained prompt; verify required sections are present before pasting into ChatGPT/Grok.

---

## 2. During-Session Objectives

### 2.1 Structure + execution

- **Human provides structure:** What to do, when, how. The lesson prompt encodes this.
- **LLM (or human-teacher) executes:** Runs the activities. One question at a time; hint from Record when stuck.
- Do not speculate or invent scenarios; base activities on what is documented in the Record.

### 2.2 Evidence-first

- Prefer observable outcomes over abstract claims.
- "We did [X]." — one line per activity for handback. Parent logs; analyst stages; Record updates.

### 2.3 Augmentation framing

- Tutor + agent = leverage, not replacement. Human-teacher + LLM augments; the Record documents growth.
- Emphasize visible progress (EVIDENCE) to counter "seen vs unseen" bias (we over-weight loss, under-weight creation).

---

## 3. Post-Session Objectives

### 3.1 Log what was done

- "We did [X]." — paste transcript or "We did X" lines into handback (extension, bot, or handback server).
- Ensures formative loop: next day's prompt reflects what was done.

### 3.2 Run /review if staged

- If anything was staged to recursion-gate, run /review in bot (or process queue per [OPERATOR-WEEKLY-REVIEW](../../operator-weekly-review.md)).
- Post-merge: regenerate lesson prompt for tomorrow.

---

## 4. Operator Checklist

| When | Action |
|------|--------|
| **Pre-session** | What's the edge today? Any resistance notes? Today's focus? Read skill-think. |
| **During** | Structure + execution. Evidence-first. No facts outside IX-A. Meet where they are. |
| **Post-session** | Log "we did X" (transcript handback). Run /review if staged. Regenerate prompt post-merge. |

---

## 5. Alpha-School Recursion

When human-teacher uses Alpha School methods (2-hour block, 4 segments, 90% mastery, vocabulary in context), reference [alpha-school-reference](../skill-work-alpha-school/alpha-school-reference.md). Document any alpha-school-specific adaptations in session notes or MEMORY.

---

## Related

- [Roadmap](roadmap.md) — Phases 1–5
- [Educational software history §K](../educational-software-history-insights.md#k-ai-era-insights-all-in-synthesis) — AI-era insights (agent maestro, Record as skills file, evidence over narrative)
- [AGENTS.md](../../../AGENTS.md) — Rule 7 (meet where they are), knowledge boundary, gated pipeline
