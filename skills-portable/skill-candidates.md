# Skill candidates backlog (pointer log)

**Purpose:** Make **skill discovery** cheap. One line per idea beats a blank page. This file is **not** the Record; it is operator / execution-layer memory. Trim or archive rows when stale.

**Ladder (see [README](README.md)):** (1) line here → (2) draft under [`_drafts/`](_drafts/) → (3) promote portable core + manifest + `sync_portable_skills.py`.

**How to append:** Add a row under **Log** (newest first or oldest first — pick one habit; default **newest at bottom**).

| Field | What to write |
|--------|----------------|
| **Date** | `YYYY-MM-DD` (local) |
| **Working name** | `hyphenated-skill-name` (draft) |
| **Trigger** | When the agent or you should invoke it (one short phrase) |
| **Pointer** | Transcript path, session id, commit hash, or “this thread” |

---

## Log

| Date | Working name | Trigger | Pointer |
|------|--------------|---------|---------|
| 2026-03-29 | portable-skills-sync | After changing `skills-portable/**`, `manifest.yaml`, or a `CURSOR_APPENDIX.md`; before commit — run `--verify` then sync | `scripts/sync_portable_skills.py`; scaffold commits `2d2f2b5`, discovery wiring `6c74036` |
