# Skill Evaluation Clinic

The Skill Evaluation Clinic is a governed evaluation layer for Grace-Mar skills. It may inspect skills, score them against local rubric checks, and generate candidate improvement notes. It may not rewrite, approve, or merge canonical skill files.

## Purpose

The clinic adapts the useful pattern from self-improving agent systems while preserving Grace-Mar's governance model:

```text
inspect skill → score skill → identify risks → produce candidate note → stage for human review
```

not:

```text
inspect skill → mutate skill → silently accept change
```

## Non-negotiable constraints

The clinic may:

- read skill files;
- evaluate clarity, boundary safety, evidence posture, and gate awareness;
- produce JSON and Markdown reports;
- produce candidate improvement notes.

The clinic may not:

- edit canonical skill files;
- approve candidates;
- merge candidates;
- rewrite Record surfaces;
- treat generated suggestions as accepted changes.

## Evaluation dimensions

| Dimension | Meaning |
|-----------|---------|
| `boundary_safety` | Does the skill respect runtime/work/Record boundaries? |
| `evidence_posture` | Does it ask for evidence, sources, receipts, or warrants where appropriate? |
| `gate_awareness` | Does it avoid claiming merge/approval authority? |
| `operator_clarity` | Is it clear when and how the operator should use it? |
| `failure_mode_awareness` | Does it describe known risks, misuse cases, or limitations? |

## Output artifacts

Reports should be written under:

`artifacts/skill-evals/`

These reports are **derived artifacts**. They are not canonical Record updates.

## Basic command

Run from the repository root (paths are resolved relative to the current working directory):

```bash
python3 scripts/runtime/skill_eval_clinic.py \
  --skill docs/skill-work/work-strategy/STRATEGY.md \
  --out artifacts/skill-evals/strategy-skill-eval.json \
  --markdown artifacts/skill-evals/strategy-skill-eval.md
```

## Design principle

The clinic improves **review quality**, not authority level. Its job is to make candidate improvements easier to judge.

JSON output conforms to [`schemas/skill-eval-report.v1.schema.json`](../../../schemas/skill-eval-report.v1.schema.json).

## See also

- [`scripts/runtime/skill_eval_clinic.py`](../../../scripts/runtime/skill_eval_clinic.py)
