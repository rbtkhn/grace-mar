# Skill-work-human-teacher

**Objective:** Provide personalized education for Grace-Mar's companion — the child whose Record it is — and their family/caregiver. The human teacher (or Record-derived lesson prompt) uses IX-A (knowledge), IX-B (curiosity), IX-C (personality), and skill-think/skill-work edge to shape lessons. Human augments the system by reading skill-think, modulating focus and gate, and respecting identity.

**Different measure of success:** skill-work-human-teacher emphasizes **personalized growth and engagement** for the companion. Economic outcomes (alpha-school) may be downstream but are not the primary metric.

---

## Purpose

| Role | Description |
|------|-------------|
| **Companion education** | Lessons at the edge (THINK, MATH, WORK, CHINESE); knowledge boundary enforced; voice and Lexile from Record. |
| **Human-teacher pattern** | Operator/caregiver reads skill-think, picks focus, gates content. Record-derived prompt encodes the same logic for LLM-as-tutor. |
| **Recursion with alpha-school** | Human-teacher uses alpha-school's methods (2-hour block, mastery thresholds, block composition); alpha-school observes human-teacher's practice via Record evidence. |

The Record is the shared medium. Alpha-school does not write into the Record; it learns from how the Record evolves when human-teacher applies its methods.

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Objective, purpose, and cross-references. |
| **[roadmap.md](roadmap.md)** | Phased roadmap: foundation → human-teacher objectives → enhanced generator → formative loop → agentic. |
| **[skill-work-lesson-generation-walkthrough](../skill-work-lesson-generation-walkthrough.md)** | How Record → lesson prompt; minimal prompt shape; examples A–D. |
| **[sample-lesson-prompt-grace-mar.txt](../sample-lesson-prompt-grace-mar.txt)** | Demo one-prompt-per-day lesson. |

---

## Principles

1. **Knowledge boundary** — Lesson prompts are built only from the Record. The LLM does not write into the Record; evidence flows via "we did X" and the gated pipeline.
2. **Respect identity** — IX-C shapes tone, values, and constraints. No pushing content that conflicts with the Record. Meet where they are (AGENTS rule 7).
3. **One prompt per day** — Target UX: human runs generator once, pastes once, runs 3–5 lessons in one LLM thread (2-hour design).
4. **Formative loop** — After "we did X" merges, run the generator again so the next day's prompt reflects the updated Record.

---

## Cross-references

- [skill-work-lesson-generation-walkthrough](../skill-work-lesson-generation-walkthrough.md) — Flow, prompt shape, examples
- [skill-work-alpha-school](skill-work-alpha-school/) — Recursion, 2-hour design, mastery thresholds
- [alpha-school-reference](skill-work-alpha-school/alpha-school-reference.md) — § Recursion with skill-work-human-teacher
- [generate_lesson_prompt.py](../../../scripts/generate_lesson_prompt.py) — Day-scoped lesson prompt generator
