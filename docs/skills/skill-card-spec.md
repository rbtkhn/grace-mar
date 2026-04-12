# Skill card spec (v1)

**Purpose:** Define **skill cards** — small **derived** JSON/Markdown summaries of portable Cursor skills for faster operator and agent context loading. Cards are **not** canonical skill bodies and **do not** replace [`skills-portable/`](../../skills-portable/) sources or generated [`.cursor/skills/`](../../.cursor/skills/) files.

**Schema:** [`schema-registry/skill-card.v1.json`](../../schema-registry/skill-card.v1.json)

**Builder:** [`scripts/build_skill_cards.py`](../../scripts/build_skill_cards.py)

---

## Fields

| Field | Meaning |
|-------|---------|
| `skill_id` | Stable id — matches portable `name` in YAML frontmatter (and manifest `name`). |
| `title` | Human title — first Markdown `#` heading body in the portable `SKILL.md` after frontmatter, else `name`. |
| `purpose` | One-line intent — YAML `description` from frontmatter. |
| `runtime_snippet` | Short excerpt of the portable body (whitespace-normalized, capped) for paste into a session. |
| `operator_view` | Grace-Mar operator hint — first ~500 characters of [`.cursor/skills/<id>/CURSOR_APPENDIX.md`](../../.cursor/skills/) when present; else a pointer to the portable file. |
| `source_path` | Repo-relative path to the **canonical portable** skill file: `skills-portable/<id>/SKILL.md`. |
| `last_updated` | ISO 8601 UTC timestamp from portable `SKILL.md` file mtime. |

---

## Input resolution (canonical order)

1. **Manifest** — [`skills-portable/manifest.yaml`](../../skills-portable/manifest.yaml) lists skills with `source`, `appendix`, `target`. Only skills **listed in the manifest** are emitted (same closure as [`sync_portable_skills.py`](../../scripts/sync_portable_skills.py)).
2. **Portable body** — For each row, read `skills-portable/<skill>/SKILL.md` (via `source` in manifest). Frontmatter + Markdown body drive `purpose`, `title`, `runtime_snippet`.
3. **Generated Cursor skill** — **Not** used as a source for card text (avoids duplicating the assembled file). Cards always recover to **portable** `source_path`.
4. **Appendix** — Optional operator paths table: read `appendix` from manifest if that file exists for `operator_view`.

Cards are **derived**: re-run the builder after skill edits; do not hand-edit emitted JSON except for local experiments (prefer changing the portable skill).

---

## Output layout

Default output directory: `artifacts/skill-cards/` (see [`artifacts/README.md`](../../artifacts/README.md)).

---

## Governance

Skill cards are **WORK / operator** artifacts. They must **not** introduce facts into SELF, EVIDENCE, or `bot/prompt.py` without the normal gate. They may cite paths to governed files for recovery only.
