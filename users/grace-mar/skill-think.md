# skill-think — PILOT-001

Intake, learning, comprehension (multimodal).
Part of SKILLS. See [skill-write](skill-write.md), [skill-work](skill-work.md).

**Module intent:** THINK captures capability from evidence. When WORK has horizon goals (e.g. SAT ≥ 1200), THINK prioritizes content and assessments that move the companion toward those goals. WORK reads THINK state to measure progress. Human-gated; evidence-linked.

---

## THINK Container

```yaml
status: ACTIVE (first Tier 4 evidence: WRITE-0001 as retell)
letters: yes (all 26)
reads_words: yes
reads_sentences: yes
reads_pages: yes
sounds_out_unfamiliar: yes
retells_stories: yes     # CONFIRMED — WRITE-0001 retells Madeline from memory with high accuracy
vocabulary_level: 2
comprehension_level: 3    # UPGRADED — retell captures key elements, characters, sequence, and character traits (bravery)
inference_level: null     # not yet assessed
edge: "Longer independent text; early chapter books; inference questions; retelling with explicit sentence structure"
gaps: []
notes: "WRITE-0001 confirms strong literary recall — ~40 words of Madeline reconstructed from memory with key elements intact (setting, characters, traits, action). Captures meaning not just words — paraphrases verse into prose. Collaborative reading preferred (Phase 2) despite independent capability."
```

---

## MATH (contextual — not a module, but tracked)

```yaml
status: SEED (parent-reported, Tier 5)
counts_to: 100
addition: yes (single digit)
subtraction: yes (single digit)
tells_time: no           # EDGE
days_of_week: yes (forward AND backward)
edge: "Telling time; place value; double-digit operations"
notes: "Days of week backward is a strong sequential reasoning signal."
```

---

## CHINESE (contextual)

```yaml
status: SEED (parent-reported, Tier 5)
oral_conversational: yes  # daily home use, full back-and-forth
counts_in_chinese: yes    # at least to 10
character_recognition: no # EDGE — literacy not started
character_writing: no
edge: "First character recognition; expanding vocabulary beyond home context"
notes: "Strong oral. Literacy is a clear future growth area."
```

---

## SAT READINESS (aligned with skill-work horizon goal)

WORK goal: SAT ≥ 1200. THINK tracks dimensions that map to SAT domains; proposes content at the edge to progress.

**Companion level:** Age 6, first grade. Use general principles that work now and scale over time. No SAT-specific mechanics (test stems, formal MC design, test-prep framing). Developmentally appropriate.

```yaml
sat_readiness:
  target: 1200
  target_date: null      # e.g. "2031" when companion would typically take SAT
  source: "skill-work.md work_goals.horizon"
  companion_level: "age 6, first grade"

  # General principles — developmentally appropriate; scale with age
  general_principles:
    comprehension: "Content at the edge — slightly challenging, stretch without overload"
    inference: "Why do you think that? What will happen next? Build reasoning through conversation"
    vocabulary: "New words in context — talk about what they mean when they appear in stories"
    evidence: "What in the story makes you say that? Evidence-based thinking from the start"
    question_format: "Simple choices when useful — 'Which one, A or B?' — scale to more options later; no formal MC test design"
    note: "Same principles apply at 6 and at 16; sophistication increases with development"

  # EBRW Reading — maps from THINK + Lexile (self.md)
  ebrw_reading:
    current_lexile_input: "400L-500L"   # from self.md; SAT passages ~1100L-1400L
    current_comprehension: 3
    current_vocabulary: 2
    current_inference: null             # not yet assessed
    trajectory: "Increase Lexile by ~100L/year; inference via 'why?' and 'what in the story shows that?'"
    next_milestones:
      - "600L input — early chapter books, short nonfiction"
      - "800L — middle-grade nonfiction; inference questions"
      - "1000L — complex passages; evidence-based reasoning"
      - "1200L — SAT-like passage difficulty"

  # Math — maps from MATH block
  math:
    current: "Single-digit add/sub; counts to 100"
    trajectory: "Place value → double-digit ops → word problems → algebra readiness"
    next_milestones:
      - "Telling time; place value"
      - "Double-digit add/sub; simple multiplication"
      - "Word problems; multi-step reasoning"
      - "Pre-algebra concepts"

  # Strategy: apply general principles at current edge
  strategy:
    - "Prioritize READ evidence at or slightly above current Lexile edge"
    - "Inference through conversation: 'why?', 'what in the story makes you say that?', 'what will happen next?'"
    - "Vocabulary in context — capture new words as they appear; talk about meaning"
    - "Simple choices when appropriate (2–3 options); scale format as companion grows"
    - "Tag READ evidence with sat_domain when applicable (reading, math)"
    - "WORK reads this block + THINK/MATH containers to synthesize progress"
```
