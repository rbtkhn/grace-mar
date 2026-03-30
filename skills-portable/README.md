# Portable skills (grace-mar)

**Purpose:** Vendor-neutral **skill cores** you can copy into other hosts (ChatGPT custom instructions, Copilot skill packs, another Cursor repo) without dragging grace-mar-only paths into the default body.

**Canonical layout**

| Path | Role |
|------|------|
| `skills-portable/<skill-name>/SKILL.md` | Portable core: frontmatter + methodology (minimal instance paths) |
| `.cursor/skills/<skill-name>/CURSOR_APPENDIX.md` | **grace-mar only:** repo paths, script commands, internal doc links |
| `.cursor/skills/<skill-name>/SKILL.md` | **Generated** — do not hand-edit; run sync (see below) |

**Regenerate Cursor skill files**

```bash
python3 scripts/sync_portable_skills.py
python3 scripts/sync_portable_skills.py --dry-run
python3 scripts/sync_portable_skills.py --verify
```

**Consume outside grace-mar**

1. Copy `skills-portable/<skill>/SKILL.md` (and optional `examples/` if present).
2. Add your own appendix: paths to *your* policy docs, account rules, and compliance notes.
3. Keep `description` as **one line** (many hosts break multi-line YAML).

**Spec:** [_schema.md](_schema.md) · **Manifest:** [manifest.yaml](manifest.yaml)
