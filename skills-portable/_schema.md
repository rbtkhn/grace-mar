# Portable skill schema (grace-mar)

## Folder

```text
skills-portable/<skill-name>/
  SKILL.md              # required
  examples/             # optional — few-shots, long samples
  HOSTS.md              # optional — install notes per vendor
```

## Frontmatter (portable `SKILL.md`)

| Key | Required | Notes |
|-----|----------|--------|
| `name` | yes | Stable id; folder name should match. |
| `description` | yes | **Single line.** Triggers, in/out contract, output shape hints (agent routing). |
| `portable` | yes | `true` — marks inclusion in sync manifest. |
| `version` | yes | Semver string for export/changelog. |
| `tags` | no | e.g. `[operator, work-politics]` for mirrors. |
| `requires` | no | Skill dependencies, e.g. `[handoff-check]`. Validator checks that listed skills exist under `.cursor/skills/`. |

## Body rules (portable core)

- Prefer **placeholders** for repo roots and script names in the main methodology.
- Put **grace-mar paths** only in `.cursor/skills/.../CURSOR_APPENDIX.md`, not in the portable core.
- **Forbidden substrings** in core (enforced by `sync_portable_skills.py --verify` when configured): instance user dirs, merge scripts — keep those in the appendix.

## Generated `.cursor/skills/.../SKILL.md`

- Appends appendix under heading `## Cursor / grace-mar instance`.
- Adds `portable_source` and `synced_by` to frontmatter for audit.

## Versioning

Bump `version` in portable `SKILL.md` when methodology meaningfully changes; re-run sync before commit.
