---
name: portable-skills-sync
description: "Sync portable skill cores into generated host Cursor SKILL.md files: manifest-driven assembly, optional host appendix, verify step before write. Triggers: skills-portable edit, manifest.yaml, CURSOR_APPENDIX, portable pipeline, run sync, verify portable skills."
portable: true
version: 1.0.0
tags:
  - operator
  - work-dev
---

# Portable skills — sync to Cursor (host)

Use this skill when **editing or adding** skills that follow the **portable core + host appendix** pattern: methodology lives under `skills-portable/<skill>/SKILL.md`; instance-specific paths and commands live in a separate appendix file; the editor-facing `SKILL.md` under `.cursor/skills/` is **generated** — do not hand-edit it.

## Layout (generic)

| Piece | Role |
|-------|--------|
| `skills-portable/<skill>/SKILL.md` | **Portable core** — frontmatter (`portable: true`, `name`, one-line `description`, `version`, optional `tags`) + methodology. **No** instance user directories or gated merge script names in the body (your manifest may forbid substrings — see verify step). |
| `.cursor/skills/<skill>/CURSOR_APPENDIX.md` | **Host-only** — real paths, doc links, commands for **this** clone. |
| `skills-portable/manifest.yaml` | **Registry** — maps `source`, optional `appendix`, `target`, and optional `verify_forbidden_substrings` for the portable **body** only. |
| `.cursor/skills/<skill>/SKILL.md` | **Output** — frontmatter gains `portable_source` and `synced_by`; body = core + `## Cursor / … instance` + appendix. |

## When to run

- After any change to a portable core, `manifest.yaml`, or a `CURSOR_APPENDIX.md`.
- Before **commit** of skill changes (so the generated file matches source).
- When the operator says **verify portable skills**, **run skill sync**, or **regenerate Cursor skills**.

## Workflow

1. **Edit** the portable core and/or appendix; add or adjust a **manifest** entry if the skill is new.
2. **Verify** (no writes): run the repo’s sync script with `--verify`. Fix any reported issues (forbidden substring in portable body, multi-line `description`, missing `portable: true`).
3. **Sync**: run the same script without `--verify` to write targets.
4. **Commit** together: portable `SKILL.md`, appendix, `manifest.yaml`, and generated `.cursor/skills/.../SKILL.md` (plus any doc cross-links you touched).

## Commands (from repository root)

Replace `scripts/` if your tree uses a different path.

```bash
python3 scripts/sync_portable_skills.py --verify
python3 scripts/sync_portable_skills.py
python3 scripts/sync_portable_skills.py --dry-run
python3 scripts/sync_portable_skills.py --skill <skill-name>
```

## Guardrails

- **Never** edit the generated `.cursor/skills/<skill>/SKILL.md` by hand — the next sync will overwrite it.
- Keep **policy and Record merge** details out of the portable core; they belong in host docs or the appendix.
- If `--verify` fails on **description**, ensure the YAML `description` value is a **single line** (no literal newline inside the string).

## Related concepts

- **Discovery ladder:** pointer backlog → `_drafts/` → portable core + manifest (see your repo’s `skills-portable/README.md` if present).
- **Extract from session:** turning a thread into a new skill often starts a draft under `_drafts/` before manifest registration.
