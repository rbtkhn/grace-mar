# work-cici Deconfusion Inventory (2026-04-25)

Purpose: classify `Xavier` references in work-cici and keep only non-confusing legacy mentions.

Canonical legacy fence phrase: **Legacy note: formerly Xavier.**

| Path | Hit snippet | Category | Action |
|---|---|---|---|
| `README.md` | active prose mentions of Xavier in sync/session sections | Active-state text | Keep lane Cici-first; retain Xavier only in explicit legacy alias and compatibility notes. |
| `INDEX.md` | rows with historical filename references | Historical reference | Keep only where tied to actual legacy filenames; avoid active-role wording. |
| `LANES.md` | `users/xavier/` template path | Historical reference | Keep with explicit template-path explanation (not lane identity). |
| `SYNC-DAILY.md` | `xavier only`, `xavier-readiness` | Active-state text | Rewrite to Cici/advisor wording, preserve continuity note only. |
| `POST-RENAME-AUDIT.md` | legacy classification table | Historical reference | Keep and tighten as migration history container. |
| `TERMS-XAVIER.md`, `COMPANION-XAVIER-*`, `xavier-*.md` filenames | Legacy filenames | Historical reference | Keep names for compatibility, add one-line rationale where surfaced. |
| `evidence/*.md`, `.rtf` captures | source quotes and old titles | Frozen evidence quote/title | Keep verbatim; optionally preface with provenance note. |

## Allowed containers for legacy mentions

- README rename continuity section and legacy alias table
- Post-rename audit / history logs
- Explicit compatibility notes for unchanged filenames/scripts
- Evidence records with immutable source titles
