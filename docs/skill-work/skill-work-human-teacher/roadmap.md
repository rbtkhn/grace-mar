# Skill-work-human-teacher — Roadmap

**Status:** Current state is Phase 1 (Record-derived prompts, script, sample). Phases 2–5 are aspirational; implementation aligns with AGENTS rules (gated pipeline, knowledge boundary, companion sovereignty).

---

## Phase 1 — Foundation (current)

**Scope:** Record-derived lesson prompts. One prompt per day. Human pastes into LLM; 3–5 lessons in one thread.

| Deliverable | Status | Description |
|-------------|--------|-------------|
| **Lesson prompt generator** | Done | `scripts/generate_lesson_prompt.py` — reads SELF, skill-think, skill-work; outputs one-prompt-per-day. |
| **Minimal prompt shape** | Done | §3 of [skill-work-lesson-generation-walkthrough](../skill-work-lesson-generation-walkthrough.md): role, who she is, IX-A, IX-B, edge, today's goals, rules. |
| **Sample prompt** | Done | [sample-lesson-prompt-grace-mar.txt](../sample-lesson-prompt-grace-mar.txt) — curated demo. Regenerate with generator. |
| **Walkthrough** | Done | [skill-work-lesson-generation-walkthrough](../skill-work-lesson-generation-walkthrough.md) — flow, examples A–D, IX-A/B/C usage. |

**Usage:** `python scripts/generate_lesson_prompt.py -u grace-mar -n Abby -o lesson.txt` — run once per day; regenerate after "we did X" merges.

---

## Phase 2 — Human-teacher objectives (formalize)

**Scope:** Document and codify the human-teacher pattern so the operator/caregiver has clear guidance when acting as teacher (without LLM) or when modulating LLM-derived prompts.

| Deliverable | Description |
|-------------|-------------|
| **Human-teacher objectives doc** | Done. [human-teacher-objectives.md](human-teacher-objectives.md): (1) read skill-think; (2) modulate focus; (3) gate content; (4) respect identity; (5) structure+execution, evidence-first, augmentation (All-In synthesis). |
| **Operator checklist** | Pre-session: "What's the edge today? Any resistance notes? Today's focus?" Post-session: "Log what we did — we did X." (Included in human-teacher-objectives.md.) |
| **Alpha-school recursion** | Explicitly reference alpha-school methods (2-hour block, 4 segments, 90% mastery, vocabulary in context) when human-teacher uses them. Document in alpha-school-reference. |

**Output:** `docs/skill-work/skill-work-human-teacher/human-teacher-objectives.md` (or section in README).

---

## Phase 3 — Enhanced generator

**Scope:** Generator improvements for flexibility and alpha-school alignment.

| Deliverable | Description |
|-------------|-------------|
| **Tier support** | `--tier elementary` (one prompt = full day) vs `--tier specialized` (one prompt = one subject/session, more Record excerpt). Grace-mar pilot is elementary. |
| **Alpha-school integration** | Optional `--alpha-school` flag: include 2-hour design, segment timing, mastery threshold (90%), block composition from alpha-school-benchmarks.yaml. |
| **Focus override** | `--focus reading|math|work|integrated` — emphasize one area when human wants to modulate. |
| **Rules appendix** | Generator pulls rules from a config or doc (vocabulary in context, 4 MC options when stuck, one-line log per activity) so updates propagate without code change. |

**Script:** `scripts/generate_lesson_prompt.py` — add args, read alpha-school YAML when requested.

---

## Phase 4 — Formative loop (transcript → skill-think)

**Scope:** Reduce friction for "we did X" and transcript handback so the Record stays current and the next day's prompt reflects what was done.

| Deliverable | Description |
|-------------|-------------|
| **Checkpoint handback** | Already supported: paste transcript with checkpoint markers → pipeline stages. Document in human-teacher flow: "After LLM session, paste transcript or say 'we did X'." |
| **Structured log format** | Optional: LLM outputs structured "We did [X]" lines; human copies block → handback server or bot. Script to parse and stage. |
| **Generator trigger** | Post-merge reminder or automation: "Record updated — run generate_lesson_prompt for tomorrow." Operator weekly review already covers this. |

**Cross-ref:** [OPERATOR-WEEKLY-REVIEW](../../operator-weekly-review.md), [handback_server](../../../scripts/handback_server.py), bot checkpoint flow.

---

## Phase 5 — Agentic proposals (future)

**Scope:** Agentic Voice proposes lesson focus or today's emphasis based on Record (edge, recent evidence, resistance notes). Companion/operator approves; generator consumes the proposal.

| Deliverable | Description |
|-------------|-------------|
| **Proactive focus suggestion** | Voice: "Based on your Record, today could focus on reading inference — you did well on place value yesterday. Want that?" Companion says yes/no. |
| **Resistance-aware** | Voice avoids proposing topics in MEMORY Resistance Notes unless companion raises them. |
| **Integration with generator** | Generator accepts optional `--proposal "focus: reading inference"` from agentic layer. Human still runs generator and pastes; proposal shapes the prompt. |

**Requires:** Agentic Voice (AGENTS.md notes future agentic). Companion remains sovereign — proposals, not prescriptions.

---

## Summary

| Phase | Scope | Key deliverables |
|-------|-------|------------------|
| **1 — Foundation** | Record-derived prompts, one per day | generate_lesson_prompt.py, walkthrough, sample |
| **2 — Human-teacher objectives** | Formalize operator pattern | human-teacher-objectives.md, checklist, alpha-school recursion |
| **3 — Enhanced generator** | Tier, alpha-school, focus override | Script args, rules config |
| **4 — Formative loop** | Transcript → skill-think | Checkpoint handback, structured log, post-merge reminder |
| **5 — Agentic proposals** | Voice proposes focus | Proactive suggestions, resistance-aware, generator integration |

---

## Related

- [Educational software history (1995–2025)](../educational-software-history-insights.md) — Cross-platform insights (Duolingo, Khan Academy, Alpha School, Khanmigo, etc.) mapped to formative loop, one prompt per day, tutor-as-guide, 4-option rule.

---

## Design guardrails (all phases)

1. **Knowledge boundary** — Prompts built only from Record. LLM never writes into Record.
2. **Gated pipeline** — Evidence ("we did X") stages; companion approves merge.
3. **Companion sovereignty** — Human-teacher and agentic proposals support; they do not compel.
4. **Meet where they are** — Respect resistance, deflection, pace. (AGENTS rule 7.)
5. **Recursion** — Alpha-school supplies methods; human-teacher applies them; Record evidence feeds back. Alpha-school does not write into Record.
