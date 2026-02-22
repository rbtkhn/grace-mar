# Adaptive Curriculum Integration Guide

How to connect Grace-Mar (Record / Identity Fork Protocol) with adaptive curriculum systems — homeschool bots, Glide/Zapier stacks, Khan, IXL, or custom platforms — so that:

- The Record serves as the **identity layer** for personalizing lessons and activities
- Curriculum engines know what the student knows, what they're curious about, and their Lexile level
- Grace-Mar's Voice handles tutoring; curriculum systems deliver structured content
- Evidence flows back into the Record via the gated pipeline

---

## Overview

| Use Case | What it does | Permission |
|----------|--------------|------------|
| **Record as identity source** | Export curriculum-oriented view (IX-B, SKILLS edge, Lexile) | Export script (read-only) |
| **Lesson/activity personalization** | Curriculum engine reads Record to tailor content | Read-only |
| **Grace-Mar Voice tutoring** | Core tutoring in Grace-Mar (answers, explains) | Built-in |
| **Evidence loop** | Curriculum outputs → "we did X" → pipeline stages | User invokes pipeline |

**Invariant:** The user gates what enters the Record. Curriculum systems may propose; they cannot merge directly.

---

## 1. Why the Record as Identity Layer

Curriculum systems (homeschool bots, adaptive platforms) typically deliver *content* — lessons, activities, quizzes. They often lack a rich model of *who the student is*. Grace-Mar's Record provides:

- **IX-A (Knowledge)** — What the student has learned; avoids redundancy, surfaces gaps
- **IX-B (Curiosity)** — What they're drawn to; personalization hooks
- **IX-C (Personality)** — Behavioral patterns, style; tone alignment
- **SKILLS edge** — What they're ready to stretch into
- **Lexile** — Output ceiling; content must match
- **LIBRARY** — What they've read; extensions and "if you liked X"

Without this, curriculum is one-size-fits-all or requires manual configuration. With it, the engine can say: "She's curious about reptiles and gemstones → suggest crystal formation lab" or "She just learned Jupiter's Red Spot → extend with storm systems."

---

## 2. Record as Identity Source

### Curriculum Export

Run the curriculum-oriented export:

```bash
python scripts/export_curriculum.py -u pilot-001
python integrations/export_hook.py --target curriculum -u pilot-001 -o ../curriculum-stack/
```

Output: `curriculum_profile.json` — Lexile, knowledge/curiosity/personality, skills edge, interests, evidence anchors, library. Does not expose full Record content.

### Schema (Curriculum-Oriented)

| Field | Use for curriculum |
|-------|--------------------|
| `lexile_output` | Content level; match output ceiling (e.g. 600L) |
| `access_needs` | Assistive tool config: explanation_level_lexile, explanation_grade, dyslexia_friendly_font, preferred_read_speed. Tools like World Pen Scan can use these. |
| `identity` | Name, age — content level |
| `knowledge` | IX-A topics — don't repeat; build on |
| `curiosity` | IX-B topics — prioritize in activity suggestions |
| `personality` | IX-C summaries — tone, engagement style |
| `skills_edge` | READ/WRITE/BUILD/MATH/CHINESE edges — what to stretch into |
| `interests` | Topics to weave into lessons |
| `evidence_anchors` | Traceability; avoid duplicate evidence |
| `library` | Titles + scope — what they have access to; extensions |

### Alternative: Symbolic Export

For lighter footprint, `export_symbolic.py` (or `--target intersignal`) produces `symbolic_identity.json` with ix_a/ix_b/ix_c, interests, evidence anchors — no Lexile or skills edge.

---

## 3. Example: SparkPath

**SparkPath** (sparkpath.uk) is a microlesson library for homeschool parents and tutors: 120+ lessons across British, IB, Australian, Indian, Cambridge curricula, with AI marking and instant feedback on student work.

**Integration flow:**
- **Identity in** — SparkPath (or a lesson-selector) reads `curriculum_profile.json`. Curiosity (IX-B), knowledge (IX-A), skills edge, and Lexile drive which lessons to suggest. E.g. "Curious about reptiles, WRITE edge for narrative → suggest reptile fact sheet, then short story prompt."
- **Evidence out** — When the student completes a SparkPath lesson (creative task, quiz), the tutor or parent invokes "we did X" with the completion/feedback. Pipeline stages → user approves → EVIDENCE, SELF. SparkPath does the delivery and marking; Grace-Mar holds the long-term Record.

**Why it fits:** SparkPath provides structure, instant feedback, and progress summaries. Grace-Mar provides who the student *is* — the identity layer that personalizes which SparkPath lessons to assign and absorbs completion as evidence.

---

## 4. Assistive Tools as Signal Source

**Reading pens** (e.g. World Pen Scan), **speech-to-text**, and similar tools can feed the pipeline in two directions:

**Identity out** — Tools read `curriculum_profile.json` for `access_needs`: explanation grade level (from Lexile), dyslexia-friendly font preference, read-aloud speed. Tools adapt their output (e.g. "explain at 2nd grade") without exposing the full Record. *Example: World Pen Scan* uses `access_needs.explanation_grade` to set the AI reading buddy level.

**Evidence in** — Tools generate signals: **Vocabulary lookups** (words looked up) → "we looked up X, Y, Z" → pipeline stages. **"Tell me more" / curiosity** (topics explored) → IX-B candidates. **Session summaries** → EVIDENCE. Parent/tutor invokes "we did X" with the summary if the tool has no API.

---

## 5. Division of Labor

| Function | Grace-Mar | Curriculum system |
|----------|-----------|-------------------|
| **Tutoring** | Voice answers questions, explains, helps learn in-character | — |
| **Structured lessons** | — | Delivers math, English, science lessons |
| **Activities/labs** | — | Suggests explore activities, science labs |
| **Identity** | Record is source of truth | Reads Record to personalize |
| **Evidence** | Pipeline stages from "we did X" | Outputs (writing, photos) feed pipeline |

Grace-Mar teaches through conversation. The curriculum system delivers scheduled, structured content. Both use the same Record for identity.

---

## 6. Evidence Loop

When the student completes curriculum work (writing, lab, activity):

1. **Capture** — Photo, text, or completion flag
2. **Invoke pipeline** — User (or curriculum hook) says "we did X"
3. **Stage** — Analyst stages candidates to PENDING-REVIEW
4. **Approve** — User approves → EVIDENCE, SELF

Curriculum outputs become evidence. The Record grows from both Grace-Mar conversations and curriculum completion.

---

## 7. Workspace Layout

**Grace-Mar as sibling to curriculum stack:**

```
workspace/
├── grace-mar/
│   └── users/pilot-001/
└── curriculum-stack/          # Glide, Zapier, Sheets, etc.
    └── identity/              # symbolic_identity.json
```

Export path: `python ../grace-mar/scripts/export_symbolic.py -u pilot-001 -o identity/`

---

## 8. Related Docs

| Document | Purpose |
|----------|---------|
| [DESIGN-ROADMAP §10](DESIGN-ROADMAP.md#10-learning-path-from-record) | Learning path generation from Record |
| [INTERSIGNAL-INTEGRATION](INTERSIGNAL-INTEGRATION.md) | Similar pattern; symbolic export; identity substrate |
| [OPENCLAW-INTEGRATION](OPENCLAW-INTEGRATION.md) | Record as identity; session continuity |
| [JOURNAL-SCHEMA](JOURNAL-SCHEMA.md) | Journal entries; linguistic fingerprint |
| [ARCHITECTURE](ARCHITECTURE.md) | Pipeline, Record structure, gating |

---

*Document version: 1.0*
*Last updated: February 2026*
