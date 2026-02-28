# Skill-work-alpha-school submodule

**Companion-Self template · Alpha reference and lesson-delivery pattern**

This submodule consolidates Alpha School reference material and the template's **Record-driven lesson** pattern for use by WORK, the Record, and instances. Cloned into grace-mar from [companion-self docs/skill-work/skill-work-alpha-school](https://github.com/rbtkhn/companion-self/tree/main/docs/skill-work/skill-work-alpha-school).

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **[alpha-school-reference.md](alpha-school-reference.md)** | Short reference: status of benchmarks (external, unverified, optional); how instances use metrics (Student UI, Export, Curriculum); 2-hour design constraint; **Record-driven prompts** (3–5 lessons via ChatGPT/Grok, transcript → skill-think). |
| **[alpha-school-benchmarks.yaml](alpha-school-benchmarks.yaml)** | **Structured benchmark data**: `target_market`, `success_metrics`, benchmarks (screen time, SAT, engagement, 2-hour block, value_creation). Evidence IDs and confidence; machine-friendly. Use for tooling and calibration. See *YAML usage* below. |
| **[insights-alpha-moonshots-233-for-business.md](insights-alpha-moonshots-233-for-business.md)** | Alpha/Moonshots #233 insights for business plan, white paper, and GTM (THINK/WRITE/WORK narrative). Optional for instances. |
| **[academic-literature-elementary-pedagogy.md](academic-literature-elementary-pedagogy.md)** | Top 10 influential academic papers on elementary pedagogy (past 25 years); why each is influential; relevance to Record-driven lessons and skill-work-alpha-school. |

---

## Why this submodule exists

- **Single place** for Alpha benchmarks, 2-hour target, and "how companion-self compares" so the template doesn't scatter Alpha content across multiple docs. Benchmarks are **data first** (YAML with evidence IDs); the Markdown reference is concise and scopes how instances use them.
- **Record-driven prompts** are documented in alpha-school-reference: prompt from Record → any LLM → transcript → skill-think. The schema's minimal prompt shape is in the template's [schema-record-api.md](https://github.com/rbtkhn/companion-self/blob/main/docs/schema-record-api.md#record-derived-lesson-prompt-minimal-shape).

---

## YAML usage

- **target_market** — Alpha School families; those who can’t afford Alpha; homeschoolers; self-motivated adults.
- **success_metrics** — screen_time_daily, sat_metrics, state_tests, engagement, value_creation.
- **Tools** — `scripts/load_alpha_school_benchmarks.py` loads the YAML; `scripts/export_curriculum.py --audience alpha-school` adds `alpha_school_context` (target_market, success_metrics, screen_time_target_minutes, value_creation_description) to `curriculum_profile.json`.

---

## Cross-references

- Template: [Long-term objective](https://github.com/rbtkhn/companion-self/blob/main/long-term-objective.md), [Schema and API contract](https://github.com/rbtkhn/companion-self/blob/main/docs/schema-record-api.md).
- Grace-Mar: [Market research (Alpha/Khan)](../market-research-alpha-khan.md), [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md).
