# Skill candidates backlog (pointer log)

**Purpose:** Make **skill discovery** cheap. One line per idea beats a blank page. This file is **not** the Record; it is operator / execution-layer memory. Trim or archive rows when stale.

**Ladder (see [README](README.md)):** (1) line here → (2) draft under [`_drafts/`](_drafts/) → (3) promote portable core + manifest + `sync_portable_skills.py`.

**Hygiene (doc-only loop):** On a quiet pass (e.g. monthly), **strike or mark** rows with **no draft** after **~90 days** unless you still intend to build them — or move the pointer to `_drafts/`. Promoted rows should read `*(promoted)*` like the examples below.

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
| 2026-03-29 | portable-skills-sync | *(promoted)* — use skill **`portable-skills-sync`** (`.cursor/skills/portable-skills-sync/SKILL.md`); same trigger | `skills-portable/portable-skills-sync/SKILL.md` + manifest |
| 2026-03-31 | work-jiang-ingest-fallback | *(promoted)* — use skill **`work-jiang-ingest-fallback`** (`.cursor/skills/work-jiang-ingest-fallback/SKILL.md`); same trigger | `skills-portable/work-jiang-ingest-fallback/SKILL.md` + manifest |
| 2026-03-31 | skill-narrative | *(promoted)* — use skill **`skill-narrative`** (`.cursor/skills/skill-narrative/SKILL.md`); trigger `narrative loop` | `skills-portable/skill-narrative/SKILL.md` + manifest |
| 2026-03-31 | repo-hygiene-pass | *(promoted)* — use skill **`repo-hygiene-pass`** (`.cursor/skills/repo-hygiene-pass/SKILL.md`); trigger `hygiene pass` | `skills-portable/repo-hygiene-pass/SKILL.md` + manifest |
| 2026-04-05 | memory-self-audit | `self-memory audit`, `audit MEMORY four dimensions`, `memory-self-audit` — run rubric + table for `users/<id>/self-memory.md` | `docs/memory-self-audit.md` (+ template §VIII); shipped `74ac84f`; full SKILL: `.cursor/skills/extract-skill-from-session/SKILL.md` |
| 2026-04-06 | work-jiang-volume-wiring-audit | `volume wiring audit`, `gt-* corpus audit`, `game theory book track drift` — cross-check `sources.yaml` / `source-map` / `book-architecture` / analysis memos / JSONL layers vs operator docs; patch drift (e.g. `volume-iv-book-track-conventions.md`, `VOLUME-IV-GAME-THEORY.md`) | shipped doc sync `a4967f9`; promote via `.cursor/skills/extract-skill-from-session/SKILL.md` |
| 2026-04-07 | template-sync-lockfile | `steward E` + implement → `template_diff.py --lock` — SHA-pinned lockfile for companion-self sync with direction detection (⬇ upstream / ⬆ instance / ⬆⬇ both) | this thread; `scripts/template_diff.py` `_git_blob_sha` + `template-sync.lock.json`; inspired by SynapCLI lockfile pattern |
| 2026-04-07 | search-evidence | `search evidence`, `find in evidence`, `what does the Record say about X` — TF-IDF search over self-archive.md entries; stdlib-only, no dependencies | `scripts/search_evidence.py`; 186 entries indexed; inspired by MemPalace eval → one-script alternative |
