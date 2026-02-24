# BUILD Probe Questions

**Purpose:** Propose multiple-choice questions generated from SELF + SKILLS + EVIDENCE (and optionally archive) that **probe or test dimensions which can populate or evidence the BUILD container** — planning, execution, making, creation (originality, elaboration, flexibility), and decision-making.

**Status:** Design proposal. No implementation yet.

**Governed by:** [SKILLS-TEMPLATE](SKILLS-TEMPLATE.md) (BUILD section), [AGENTS.md](../AGENTS.md) (knowledge boundary, stage-only).

---

## 1. BUILD dimensions to probe

Questions should target one or more of these BUILD dimensions. All content must be grounded in the Record (no external knowledge).

| Dimension | What it evidences | Example question type |
|-----------|--------------------|------------------------|
| **Planning** | Goals, order of steps, "what first/next" | "You want to draw the Nine-Colored Deer. What do you do first?" |
| **Execution** | Follow-through, next step in a process | "You're building a Lego set. You finished step 4. What do you do next?" |
| **Making** | Following instructions, assembly, method | "When you build with Legos, how do you do it?" |
| **Originality (creation)** | Novel combinations, "what if" across known stories | "What if the Nine-Colored Deer met Madeline? Where would they meet?" |
| **Elaboration (creation)** | Adding detail, richness, signature choices | "You're drawing an animal. What do you add to make it special?" |
| **Flexibility (creation)** | Adapting within constraints, own choices | "You have to draw a deer from a story. You can add one thing that's not in the book. What do you add?" |
| **Decision-making** | Trade-offs, picking one option with a reason | "You can show class one drawing: Nine-Colored Deer OR astronaut on the moon. Why might you pick the deer?" |
| **Collaboration** (optional) | Role, teamwork, "who does what" | "You and a friend make a lemonade stand. What could you do while your friend pours?" |

---

## 2. Record context for generation

Questions MUST be generated only from:

- **SELF.md** — Identity, preferences (favorites, activities), interests, values, reasoning patterns, narrative, **art patterns** (VIII or IX-C), IX-A (knowledge), IX-B (curiosity), IX-C (personality).
- **SKILLS.md** — BUILD container: edge, creation dimensions (originality, elaboration, flexibility), planning/execution (if any), gaps.
- **EVIDENCE.md** — Recent CREATE-* and ACT-* entries (titles, descriptions, dimensions already captured).
- **Archive** (optional) — Recent conversation snippets so questions don’t repeat what was just discussed.

Same **knowledge boundary** as existing homework: no facts outside the Record. Lexile ~600L for pilot-001.

---

## 3. Question format (aligned with existing homework)

Reuse the same JSON shape as `HOMEWORK_PROMPT` for one-at-a-time, A/B/C/D delivery. Add a **BUILD-specific** field so responses can be tagged for pipeline/staging:

```json
{
  "q": "When you build with Legos, how do you do it?",
  "options": [
    "A) Follow the instructions step by step",
    "B) Make whatever I want",
    "C) Look at the picture on the box first",
    "D) Mix both — follow some then add my own"
  ],
  "correct": "A",
  "topic": "making",
  "hint": "You like to follow the steps and build with structure.",
  "build_dimension": "making"
}
```

**build_dimension** (optional but recommended): one of `planning` | `execution` | `making` | `originality` | `elaboration` | `flexibility` | `decision_making` | `collaboration`. Used to tag the session or ledger for BUILD evidence.

For **originality** / "what if" questions, there may be multiple plausible "correct" answers (any creative combination from the Record). Options: (a) accept any of 2–3 options as correct, or (b) treat as open-ended and log the answer as BUILD creation evidence without right/wrong.

---

## 4. Example questions (pilot-001, Record-grounded)

Below are concrete examples drawn from SELF + SKILLS + EVIDENCE for pilot-001. Each is keyed to a BUILD dimension.

### Planning

- **q:** You want to draw the Nine-Colored Deer like you did before. What do you do first?  
  **options:** A) Get paper and crayons  B) Draw the mountains  C) Draw the deer  D) Add the rainbow scarf  
  **correct:** A  
  **build_dimension:** planning  
  **hint:** First you get your materials, then you draw.

- **q:** You and a friend want to make a lemonade stand. What is the first thing you need?  
  **options:** A) Lemonade  B) A table  C) A plan for who does what  D) A sign  
  **correct:** A (or C — both show planning)  
  **build_dimension:** planning  

### Execution

- **q:** You're building a Lego set. You just finished step 4. What do you do next?  
  **options:** A) Go to step 5  B) Play with what you built  C) Start over  D) Put it away  
  **correct:** A  
  **build_dimension:** execution  
  **hint:** You like to follow the steps one by one.

### Making

- **q:** When you build something with Legos, how do you do it?  
  **options:** A) Follow the instructions step by step  B) Make whatever I want  C) Look at the picture on the box first  D) Mix both — follow some then add my own  
  **correct:** A  
  **build_dimension:** making  
  **hint:** You like to follow the instructions and build with structure. (From SELF: "Legos — follows instructions (methodical).")

### Originality (creation)

- **q:** What if the Nine-Colored Deer met Madeline in Paris? Where could they meet?  
  **options:** A) At the zoo  B) On a mountain  C) In the big house with the twelve girls  D) At the Eiffel Tower  
  **correct:** Any of B, C, D (all plausible from Record; A ties to Madeline’s zoo). Accept multiple.  
  **build_dimension:** originality  

- **q:** What if Roz from The Wild Robot came to your ocean with the octopus and the fish? What might happen?  
  **options:** A) They'd be friends  B) They'd hide  C) They'd build something together  D) They'd share the water  
  **correct:** A or C (creation/combo from Record).  
  **build_dimension:** originality  

### Elaboration (creation)

- **q:** You're drawing an animal. What do you add to make it special, like you did with the Nine-Colored Deer?  
  **options:** A) A rainbow scarf  B) Eyelashes  C) A whole world around it (mountains, sky)  D) All of those  
  **correct:** D  
  **build_dimension:** elaboration  
  **hint:** You add scarves, eyelashes, and a complete world around your characters.

### Flexibility (creation)

- **q:** The story says the deer is on a mountain. You get to add one thing that's not in the book. What do you add?  
  **options:** A) A rainbow scarf  B) Hearts on the deer  C) A halo behind its head  D) Any of those — they're all from your own choices  
  **correct:** D  
  **build_dimension:** flexibility  
  **hint:** You added scarf, hearts, and halo from your own imagination. (From CREATE-0001.)

### Decision-making

- **q:** You can show your class only one drawing: your Nine-Colored Deer OR your astronaut on the moon. Why might you pick the deer?  
  **options:** A) Because it's kind and brave and beautiful  B) Because it's from a Chinese story  C) Because you made it from a word book with no pictures  D) Any of those  
  **correct:** D  
  **build_dimension:** decision_making  
  **hint:** You like the deer because it's kind, brave, and beautiful — and you imagined it yourself.

---

## 5. How responses could populate BUILD

1. **Session log** — Run a "BUILD probe" session (e.g. 6–8 questions per batch). Log which questions were shown, which dimension, and the companion’s answer (and correct/incorrect if applicable).
2. **Activity evidence** — Treat the session as an activity: e.g. "Companion completed BUILD probe (planning, making, elaboration, decision-making)." Stage an ACT-* or a dedicated BUILD-probe log entry; operator can merge into EVIDENCE and optionally update SKILLS BUILD (e.g. planning_level, execution_level) when approved.
3. **Staging** — When merging, link BUILD probe results to BUILD container: e.g. "planning: 1–2 (can order steps for familiar task); making: observed (follows Lego instructions); elaboration: 4 (confirmed); decision_making: 1 (can give reason for choice)." All via gated pipeline — stage to PENDING-REVIEW, companion approves.
4. **"What if" / originality** — Open-ended or multi-correct answers don’t get a single right/wrong; they serve as **creation** evidence (originality/flexibility). Operator or analyst can stage: "Companion combined Nine-Colored Deer + Madeline / Roz + ocean in BUILD probe."

---

## 6. Implementation options

| Option | Description |
|--------|-------------|
| **A. New prompt + command** | Add `BUILD_PROBE_PROMPT` in `bot/prompt.py` and `_load_build_probe_context()` in `bot/core.py` (SELF excerpts + SKILLS BUILD + recent CREATE/ACT). New command or button: `/buildprobe` or "Build quiz." Reuse homework-style flow: one question at a time, A/B/C/D, session state, optional BUILD_PROBE_LEDGER.jsonl. |
| **B. Mode in homework** | Extend homework: operator or companion chooses "Knowledge quiz" vs "Build quiz." Same UX, different prompt and context; questions tagged with `build_dimension` and logged separately for BUILD evidence. |
| **C. Script-only** | Script (e.g. `scripts/generate_build_probe.py`) that reads SELF + SKILLS + EVIDENCE, outputs a JSON array of BUILD probe questions for operator to use in conversation or paste into a future bot flow. No bot changes. |

Recommendation: **A** for full integration (probe → session → staging → BUILD); **C** for a quick, script-only way to generate and review questions.

---

## 7. Summary

- **BUILD probe questions** are multiple-choice (and optionally multi-correct for "what if") questions generated **only** from SELF + SKILLS + EVIDENCE (and optionally archive).
- They **probe** planning, execution, making, originality, elaboration, flexibility, decision-making, and optionally collaboration.
- Answers can be used to **evidence** BUILD container growth via session log + staged ACT/BUILD candidates, with merge only after companion approval.
- Schema extends existing homework JSON with `build_dimension`; same one-at-a-time, A/B/C/D UX keeps the experience consistent and Lexile-safe.

---

*BUILD Probe Questions · Design proposal · February 2026*
