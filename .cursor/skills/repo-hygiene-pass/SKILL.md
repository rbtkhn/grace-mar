---
name: repo-hygiene-pass
preferred_activation: hygiene pass
description: 'Run a commit-grouping hygiene pass: split changes by intent, stage one bucket at a time, and keep scratch noise out of production commits.'
portable: true
version: 0.1.0
tags:
- operator
- work-dev
- git
portable_source: skills-portable/repo-hygiene-pass/SKILL.md
synced_by: sync_portable_skills.py
---
# Repo Hygiene Pass

**Preferred activation (operator):** say **`hygiene pass`**.

Use this skill when the working tree has mixed changes and you want clean, intent-based commits.

## When to run

- Multiple unrelated changes are mixed in one status view.
- You need to separate feature/docs work from generated index churn.
- Scratch or local test folders keep showing up as untracked noise.

## Workflow

1. Run preflight:
   - `git status --short`
   - `git diff --name-only`
   - `git diff --cached --name-only`
2. Partition files into 2-4 buckets by intent:
   - main task bundle,
   - generated/index refresh,
   - scratch/local-only files,
   - optional follow-up bucket.
3. Commit bucket 1 only:
   - stage explicit paths (never broad `git add .` in mixed trees),
   - verify staged diff,
   - write a message that explains why.
4. Commit bucket 2 only (if needed), same pattern.
5. Keep scratch noise out of future commits:
   - prefer local excludes for machine-local dirs,
   - avoid adding team-wide ignores unless requested.
6. End with clean check:
   - `git status --short`
   - confirm remaining files are intentional.

## Guardrails

- Do not rewrite or revert unrelated user changes.
- Do not force-push or run destructive reset flows.
- Keep generated churn in separate commits from logic/docs changes.
- If uncertain whether a file is scratch or real, ask before excluding.


## Cursor / grace-mar instance

Grace-mar paths and command notes for this repository (from `.cursor/skills/repo-hygiene-pass/`).

| Topic | Path |
|--------|------|
| Portable manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
| Skill backlog | [skills-portable/skill-candidates.md](../../../skills-portable/skill-candidates.md) |
| Sync implementation | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Work-dev module | [docs/skill-work/work-dev/README.md](../../../docs/skill-work/work-dev/README.md) |
| Git lane conventions | [docs/operator-agent-lanes.md](../../../docs/operator-agent-lanes.md) |

**Commit grouping reminder:** split by intent first, then by destination; keep local scratch dirs in `.git/info/exclude` unless the operator asks for a tracked ignore.
