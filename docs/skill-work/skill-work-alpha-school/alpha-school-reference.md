# Alpha School Reference (Skill-Work-Alpha-School Submodule)

**Companion-Self template.** **skill-work-alpha-school** is a tool designed for its **target market**:

- **Alpha School families** — at or considering Alpha School
- **Can't afford Alpha School** — want Alpha-like design at lower cost
- **Homeschool** — structured benchmarks and 2-hour design for home learning
- **Self-motivated adults** — mastery-based, efficient learning for independent learners

Companion-Self does not replicate Alpha's model; these are **optional comparison targets** and design constraints. Cloned into grace-mar.

**Structured data:** Benchmarks are defined in **[alpha-school-benchmarks.yaml](alpha-school-benchmarks.yaml)** with provenance and evidence flags. Use the YAML for tooling and calibration; this doc summarizes and gives usage rules.

---

## Status of benchmarks

Benchmarks in the YAML:

- are **external** (Alpha School / Moonshots #233)
- are **not verified by Companion-Self**
- are **optional comparison targets**

They do not form part of the Record unless assimilated via the evidence pipeline. Instances decide whether to adopt them and how to interpret them.

---

## Primary deliverable (comparison target)

**Different measure of success.** skill-work-alpha-school includes **economic productivity and value creation** as success metrics — aligned with Alpha's life-skills workshops (entrepreneurship, passion projects, creators and contributors). skill-work-human-teacher, by contrast, emphasizes personalized growth and engagement for the companion; economic outcomes may be downstream but are not the primary metric.

| Dimension | Alpha's deliverable | Structured data key |
|-----------|---------------------|----------------------|
| Screen time | ~2 hours/day academic screen time | `screen_time_daily` |
| Outcome level | Top 1–2% (e.g. SAT seniors ~1535, whole school ~1410) | `sat_metrics`, `state_tests` |
| Experience | >90% "love school"; 40–60% prefer school to vacation | `engagement` |
| Economic productivity / value creation | Life-skills output; entrepreneurship; passion projects with real outcomes | `value_creation` |

See **alpha-school-benchmarks.yaml** for values, evidence IDs, and `verified` / `confidence` fields.

---

## Two-hour design constraint (Companion-Self)

Companion-Self is calibrated so that **screen-based learning is designed to fit within 2 hours per day**. This aligns with Alpha's 2-hour frame and provides a **common metric** for comparison. The 2 hours are a **ceiling** for mandatory screen-based learning, not a minimum to fill.

- **What counts as screen time:** Curriculum/tutor apps, student interface, Voice/chat in the learning flow, THINK/WRITE/screen WORK. Excluded: entertainment, non-learning screen use.
- **Block composition (reference):** In Alpha, ~4 segments of 25–30 min, 90% mastery to advance, 80–85% in-lesson success, no open chat during the block. YAML: `two_hour_block`.

---

## How instances should use these metrics

Instances **may** use the benchmarks as follows. None are required.

| Integration point | Use |
|--------------------|-----|
| **Student UI** | Show a "screen time target" (e.g. "Designed for up to 2 hours of screen-based learning per day") only if the instance config enables it. Do not imply benchmarks are verified. |
| **Export / curriculum profile** | Include `screen_time_target_minutes: 120` (or omit) when the instance has chosen the 2-hour target. Other benchmark fields may be added to export schema if the instance wants to compare. |
| **Curriculum / scoring** | Optionally compare progress vs benchmark (e.g. evidence-linked mastery, retention) **per 2-hour block**. Do not treat Alpha metrics as truth; treat as optional comparison. |
| **Record** | Benchmarks are not written into the Record unless the companion (or delegated human) approves evidence that cites them. External claims stay external. |

---

## Equivalent or comparable metrics (optional)

Without in-room guides, Companion-Self uses **Record- and system-based metrics** as comparables:

- **Mastery / level:** Evidence-linked progress; mastery per topic/level in the Record; export for curriculum/tutor.
- **Engagement:** Retention (e.g. week-4, month-3); evidence count; "time back" as proxy.
- **Placement / edge:** Seed-phase "where they are"; edge from Record (IX-A, IX-B, self-skill-*) for next steps.

---

## Record-driven prompts (lessons without Alpha's stack)

Companion-self can deliver **personalized lessons** via **Record-derived prompts** pasted into any LLM (e.g. ChatGPT, Grok). The prompt is built from the Record only: knowledge (IX-A), curiosity (IX-B), personality (IX-C), edge (THINK/WRITE/WORK). The LLM is the tutor; Companion-Self supplies context.

- **Knowledge boundary:** Prompt content is from the Record. No LLM inference is written back into the Record; evidence of what was done can be captured via "we did X" and merged through the gate.
- **Typical use:** 3–5 lessons per day (or per 2-hour block); transcript of the LLM session can flow into **skill-think** (self-skill-think) for processing and merge. **Ideal UX:** one prompt per day — the human pastes once and runs all lessons in one LLM thread (see [skill-work-lesson-generation-walkthrough](../skill-work-lesson-generation-walkthrough.md) §0).
- **Minimal prompt shape and APIs:** See template [schema-record-api.md](https://github.com/rbtkhn/companion-self/blob/main/docs/schema-record-api.md#record-derived-lesson-prompt-minimal-shape). Instances may implement a prompt generator from Record/export.

---

## Recursion with skill-work-human-teacher

Alpha-school and skill-work-human-teacher form a **bidirectional loop**:

- **Human-teacher → alpha-school:** The human teacher (or Record-derived prompt encoding the same logic) uses alpha-school's design constraints and methods — 2-hour block, segment composition, mastery thresholds, academic-literature mappings — to shape lessons. Alpha-school supplies the structural and pedagogical scaffolding.
- **Alpha-school ← human-teacher:** Alpha-school observes human-teacher's practice for feedback. Evidence in the Record ("we did X," evidence-linked progress, retention, edge movement) reflects what happens when those methods are applied. That evidence can inform how benchmarks and design principles are interpreted or refined. Alpha-school does not write into the Record directly; it learns from how the Record evolves when human-teacher applies its methods.

The Record is the shared medium. The recursion keeps alpha-school grounded in real practice rather than abstract targets.

---

## Reference

- **Structured benchmarks:** [alpha-school-benchmarks.yaml](alpha-school-benchmarks.yaml)
- **Source:** Moonshots #233 — *This $40M AI Company Is Using AI Tutors to Teach 2 Hours/Day* (Alpha Schools).
- **Academic literature:** [academic-literature-elementary-pedagogy](academic-literature-elementary-pedagogy.md) — top 10 influential papers on elementary pedagogy and relevance to Record-driven lessons.
- **Related:** [Educational software history (1995–2025)](../educational-software-history-insights.md) — Cross-platform insights from Rosetta Stone, Duolingo, Khan Academy, IXL, Alpha School, DreamBox, MOOCs, etc.; mapped to skill-work objectives and 2-hour design.
- **Companion docs:** [insights-alpha-moonshots-233-for-business](insights-alpha-moonshots-233-for-business.md), [market-research-alpha-khan](../../market-research-alpha-khan.md) (grace-mar). Template: [recursive-self-learning-objectives](https://github.com/rbtkhn/companion-self/blob/main/docs/recursive-self-learning-objectives.md), [market-research-timeback-alpha-thirdparty](https://github.com/rbtkhn/companion-self/blob/main/docs/market-research-timeback-alpha-thirdparty.md).
