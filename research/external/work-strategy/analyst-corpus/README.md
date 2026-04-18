# Analyst corpus (work-strategy) — registry + optional notes

**Purpose:** One **cross-analyst index** for transcripts and digests you ingest regularly. Physical transcript files still live under **[../transcripts/README.md](../transcripts/README.md)** unless you deliberately place a note-only file here.

**Not** companion Record. **Not** Voice knowledge. Triangulate before any public or campaign-facing claim.

---

## Layout

| Path | Role |
|------|------|
| **[INDEX.md](INDEX.md)** | Master table — one row per ingested appearance (or per file if one file = one episode). |
| **`transcripts/*.md`** | Default location for full transcript + Perceiver summary (existing convention). |
| **`analysts/<slug>/`** (optional) | Per-analyst add-ons: `RECURRING-MOVES.md`, `VERIFY.md`, links to triangulation stubs under `docs/skill-work/work-strategy/`. **No requirement** to create this until an analyst is high-volume. |

**`<slug>`** — lowercase kebab-case, stable over time: `theodore-postol`, `pape`, `mercouris`.

---

## Workflow

1. Add or update **`../transcripts/<file>.md`** using the header + Perceiver + hooks pattern in [transcripts README](../transcripts/README.md).
2. Append a row to **[INDEX.md](INDEX.md)** in the **Active table** (newest ingest at the **top** of the table body unless you prefer chronological bottom — stay consistent).
3. If the analyst accrues **repeated rhetorical moves** or **verify checklists**, add **`analysts/<slug>/RECURRING-MOVES.md`** and link it from the **notes_path** column (create the file in the same PR/commit when useful).
4. **Git** — after transcript + INDEX are correct, follow **[Commit policy (ingest → git)](../transcripts/README.md#commit-policy-ingest--git)** in the transcripts README (**local commit** by default on ingest; **push** only when asked).

---

## Relation to future skills

A meta-skill (e.g. analyst-ingest) can point here: **INDEX** for discovery, **transcripts/** for evidence, **`analysts/<slug>/`** for method notes. Per-analyst Cursor skills stay optional — see operator discussion; avoid duplicating INDEX inside every skill.

---

## See also

- [work-strategy README](../../../../docs/skill-work/work-strategy/README.md)
- [current-events-analysis.md](../../../../docs/skill-work/work-strategy/current-events-analysis.md)
- [transcripts README](../transcripts/README.md)
