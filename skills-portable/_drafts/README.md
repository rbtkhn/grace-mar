# Portable skill drafts

**Purpose:** Hold **step 2** of the skill ladder — a full `SKILL.md` body (or near-final) **before** it is wired into [manifest.yaml](../manifest.yaml).

**Convention**

- One folder per skill: `_drafts/<skill-name>/SKILL.md` (optional `notes.md`).
- Keep the portable core **free of** instance-only paths in the body; use a placeholder table like the pilot in `skills-portable/politics-massie/SKILL.md`.
- When ready: move the core to `skills-portable/<skill-name>/SKILL.md`, add a `CURSOR_APPENDIX.md` under `.cursor/skills/<skill-name>/` if needed, register in `manifest.yaml`, run `python3 scripts/sync_portable_skills.py --verify` then sync.

**Do not** commit secrets or companion-only content here; drafts are normal git text.

## Current drafts (inventory)

| Folder | Status | Notes |
|--------|--------|--------|
| `persian-regime-adaptive-strategy/` | Active draft | Triggers: `regime strategy`, `persian strategy`, `regime switch` — CIV-MEM Persian regime modes (tolerance / parity / compression). |
| `russian-endurance-compression-strategy/` | Active draft | Triggers: `endurance strategy`, `russian strategy`, `compression strategy` — endurance + rupture-regeneration lens; pairs with Persian draft. |
| `skill-narrative/` | **Likely duplicate** | Canonical portable core lives under [`../skill-narrative/`](../skill-narrative/); remove this copy after diff if redundant. |
| `repo-feedback-prompt/` | **Ready to promote** (≥2 reuses logged in SKILL § Promotion) | Triggers: `repo feedback prompt`, `OSS feedback prompt`, `constructive GitHub prompt` — verify upstream docs, drop redundant gaps, one-screen maintainer message. |
