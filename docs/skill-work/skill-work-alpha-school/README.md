# Skill-work-alpha-school submodule

**Companion-Self template · Alpha reference and lesson-delivery pattern**

This submodule consolidates Alpha School reference material and the template’s **Record-driven lesson** pattern for use by WORK, the Record, and instances.

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **[alpha-school-reference.md](alpha-school-reference.md)** | Short reference: status of benchmarks (external, unverified, optional); how instances use metrics (Student UI, Export, Curriculum); 2-hour design constraint; **Record-driven prompts** (3–5 lessons via ChatGPT/Grok, transcript → skill-think). |
| **[alpha-school-benchmarks.yaml](alpha-school-benchmarks.yaml)** | **Structured benchmark data** (screen time, SAT, engagement, 2-hour block). Evidence IDs and confidence; machine-friendly. Use for tooling and calibration. |
| **[insights-alpha-moonshots-233-for-business.md](insights-alpha-moonshots-233-for-business.md)** | Alpha/Moonshots #233 insights for business plan, white paper, and GTM (THINK/WRITE/WORK narrative). Optional for instances. |

---

## Why this submodule exists

- **Single place** for Alpha benchmarks, 2-hour target, and “how companion-self compares” so the template doesn’t scatter Alpha content across multiple docs. Benchmarks are **data first** (YAML with evidence IDs); the Markdown reference is concise and scopes how instances use them.
- **Record-driven prompts** are documented in alpha-school-reference: prompt from Record → any LLM → transcript → skill-think. The schema’s minimal prompt shape is in [schema-record-api.md](../../schema-record-api.md#record-derived-lesson-prompt-minimal-shape).

---

## Cross-references

- [Long-term objective](../../long-term-objective.md) — Links to this submodule for Alpha reference.
- [Schema and API contract](../../schema-record-api.md) — Record shape, edge, **Record-derived lesson prompt (minimal shape)**.
- [Market research (TimeBack/Alpha/third-party)](../../market-research-timeback-alpha-thirdparty.md) — Template evaluation of 10 proposals; references this submodule.
