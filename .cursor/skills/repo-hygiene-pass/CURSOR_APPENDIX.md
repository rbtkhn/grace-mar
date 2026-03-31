Grace-mar paths and command notes for this repository (from `.cursor/skills/repo-hygiene-pass/`).

| Topic | Path |
|--------|------|
| Portable manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
| Skill backlog | [skills-portable/skill-candidates.md](../../../skills-portable/skill-candidates.md) |
| Sync implementation | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Work-dev module | [docs/skill-work/work-dev/README.md](../../../docs/skill-work/work-dev/README.md) |
| Git lane conventions | [docs/operator-agent-lanes.md](../../../docs/operator-agent-lanes.md) |

**Commit grouping reminder:** split by intent first, then by destination; keep local scratch dirs in `.git/info/exclude` unless the operator asks for a tracked ignore.

**Push-prep quick check:** `git status -sb` then `git log --oneline origin/main..HEAD` before `git push origin main`.

**Rollback-safe default:** prefer follow-up fix commits or `git revert` on shared branches; avoid reset/force unless explicitly requested.
