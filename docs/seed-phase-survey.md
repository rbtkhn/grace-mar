# Seed Phase — Survey prompts

**Companion-Self template · Intake copy**

Operators use these prompts to collect answers that map into seed-phase JSON artifacts. This doc is **not** the live Record.

See [seed-phase-artifacts.md](seed-phase-artifacts.md) for the file layout and [seed-phase.md](seed-phase.md) for the protocol.

---

## work-dev seed survey

Answers feed **`work_dev_seed.json`** (validated by **`schema-registry/work-dev-seed.v1.json`**). Map free-text lists into JSON arrays; use the schema enums for single-choice fields.

**Mapping hints**

| Question theme | JSON field | Enum / shape |
|----------------|------------|----------------|
| Involvement level | `development_involvement` | `none`, `light`, `regular`, `core` |
| Role modes | `development_role_modes` | `builder`, `architect`, `debugger`, `reviewer`, `researcher`, `integrator`, `other` (array, unique) |
| Work kinds | `work_modes` | `feature_design`, `implementation`, `debugging`, `architecture`, `refactoring`, `documentation`, `integration`, `research`, `code_review`, `other` (array, unique) |
| Companion help | `companion_help_priorities` | `brainstorming`, `planning`, `code_generation`, `review_and_critique`, `debugging`, `architecture_mapping`, `repo_audits`, `prioritization`, `technical_writing`, `other` (array, unique) |

1. Do you do software development or technical systems work?
   - Maps to `development_involvement`: no → `none`; occasionally → `light`; regularly → `regular`; major part of work → `core`.

2. Which of these best describe your development role? (multi-select)
   - builder / implementer → `builder`
   - architect / planner → `architect`
   - debugger / fixer → `debugger`
   - reviewer / auditor → `reviewer`
   - researcher / explorer → `researcher`
   - product / systems integrator → `integrator`
   - other (specify in `notes`)

3. What repositories, products, or systems are most important to your development work right now?
   - `primary_repos` and/or `systems_or_products` (string arrays).

4. Which languages or stacks do you actively use or care about?
   - `preferred_languages` (string array).

5. Which tools do you prefer for development work?
   - `preferred_tools` (string array).

6. What kinds of development work do you most often do? (multi-select)
   - Align labels with `work_modes` enum values above.

7. What kind of technical help do you want this companion to be best at? (multi-select)
   - Align labels with `companion_help_priorities` enum values above.

8. Are there any repositories, systems, languages, or workflows this companion should treat as especially important?
   - `active_focuses` and/or repeat structured fields as needed.

9. Are there any development preferences or constraints this companion should avoid violating?
   - `important_constraints` (string array).

10. Is development work central to this companion, secondary, or mostly absent?
    - Cross-check `development_involvement` and summarize in `notes` if nuance is needed.

After capture, set `evidence_basis` to `seed_survey` when answers are survey-driven; use `explicit_user_input` for direct statements only; `mixed` when both apply. Leave `none` only while no evidence is recorded yet.
