# Work-Dev Lane Scope Checklist

Use this before opening a PR or committing in `work-dev` lane.

## Scope guardrails

- Confirm intent: this commit is `work-dev` only.
- Keep `work-jiang` changes out unless explicitly planned and labeled as cross-lane.
- Prefer one lane per commit; if unavoidable, split into separate commits by lane.

## Pre-commit checks

- `git status --short` and verify all staged paths belong to `work-dev` scope.
- `git diff --name-only --cached` and scan for accidental lane bleed.
- Run targeted tests for changed `work-dev` scripts/docs.

## Path ownership hints

Typical `work-dev` paths:

- `docs/skill-work/work-dev/`
- `research/external/work-dev/`
- `scripts/operator_*` and `scripts/*integration*` when tied to work-dev operations
- `tests/test_*` for work-dev utilities

Potential cross-lane bleed to watch:

- `research/external/work-jiang/`
- `users/grace-mar/work-jiang.md`
- `scripts/work_jiang/`

## Commit hygiene

- Use a lane-scoped commit title (example: `work-dev: ...`).
- In commit body, name any intentional cross-lane exceptions explicitly.
- If cross-lane changes appear accidentally, unstage and split before commit.
