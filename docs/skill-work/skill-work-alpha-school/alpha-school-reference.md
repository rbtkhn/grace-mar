# Alpha School Reference (Skill-Work-Alpha-School Submodule)

**Companion-Self template.** This document points to **structured benchmark data** and states how instances may use it. Companion-Self does not replicate Alpha's model; these are **optional comparison targets** and design constraints.

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

| Dimension | Alpha's deliverable | Structured data key |
|-----------|---------------------|----------------------|
| Screen time | ~2 hours/day academic screen time | `screen_time_daily` |
| Outcome level | Top 1–2% (e.g. SAT seniors ~1535, whole school ~1410) | `sat_metrics`, `state_tests` |
| Experience | >90% "love school"; 40–60% prefer school to vacation | `engagement` |

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
- **Typical use:** 3–5 lessons per day (or per 2-hour block); transcript of the LLM session can flow into **skill-think** (self-skill-think) for processing and merge.
- **Minimal prompt shape and APIs:** See [schema-record-api.md](../../schema-record-api.md#record-derived-lesson-prompt-minimal-shape). Instances may implement a prompt generator from Record/export.

---

## Reference

- **Structured benchmarks:** [alpha-school-benchmarks.yaml](alpha-school-benchmarks.yaml)
- **Source:** Moonshots #233 — *This $40M AI Company Is Using AI Tutors to Teach 2 Hours/Day* (Alpha Schools).
- **Companion docs:** [recursive-self-learning-objectives](../recursive-self-learning-objectives.md), [insights-alpha-moonshots-233-for-business](insights-alpha-moonshots-233-for-business.md), [market-research-timeback-alpha-thirdparty](../../market-research-timeback-alpha-thirdparty.md).
