# Portable skill drafts

**Purpose:** Hold **step 2** of the skill ladder — a full `SKILL.md` body (or near-final) **before** it is wired into [manifest.yaml](../manifest.yaml).

**Convention**

- One folder per skill: `_drafts/<skill-name>/SKILL.md` (optional `notes.md`).
- Keep the portable core **free of** instance-only paths in the body; use a placeholder table like the pilot in `skills-portable/massie-x-news-search-draft/SKILL.md`.
- When ready: move the core to `skills-portable/<skill-name>/SKILL.md`, add a `CURSOR_APPENDIX.md` under `.cursor/skills/<skill-name>/` if needed, register in `manifest.yaml`, run `python3 scripts/sync_portable_skills.py --verify` then sync.

**Do not** commit secrets or companion-only content here; drafts are normal git text.
