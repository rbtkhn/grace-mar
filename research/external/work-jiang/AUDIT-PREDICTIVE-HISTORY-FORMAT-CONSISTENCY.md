# Predictive History — format and registry consistency audit

Operator WORK lane. **Not** Record / Voice knowledge. This file summarizes **naming**, **front matter**, **volume stubs**, and **`sources.yaml`** shape across Predictive History corpora under `research/external/work-jiang/`.

**Machine scan:** `python3 scripts/work_jiang/audit_predictive_history_format.py` (read-only, always exit 0).

**Validator:** `python3 scripts/work_jiang/validate_work_jiang.py` — default CI pass clean as of audit authorship; optional `python3 scripts/work_jiang/validate_work_jiang.py --require-analysis-frontmatter` checks parseable YAML on every `analysis/*.md` and validates `chapter_candidates` against known chapter IDs from `metadata/book-architecture.yaml`.

**Recorded check (2026-04-06):** `validate_work_jiang.py` and `validate_work_jiang.py --require-analysis-frontmatter` both **exit 0** after Volume IV memo batch; `render_analysis_backlog.py` regenerated [`ANALYSIS-BACKLOG.md`](ANALYSIS-BACKLOG.md).

---

## 1. Volume book stubs (`book/VOLUME-*.md`)

| File | Role |
|------|------|
| [VOLUME-II-CIVILIZATION.md](book/VOLUME-II-CIVILIZATION.md) | Civilization corpus + Part II divergence pointer |
| [VOLUME-III-SECRET-HISTORY.md](book/VOLUME-III-SECRET-HISTORY.md) | Secret History `sh-*` spine |
| [VOLUME-IV-GAME-THEORY.md](book/VOLUME-IV-GAME-THEORY.md) | Game Theory `gt-*` (canonical counts live here) |
| [VOLUME-V-GREAT-BOOKS.md](book/VOLUME-V-GREAT-BOOKS.md) | Great Books `gb-*` |
| [VOLUME-VI-INTERVIEWS.md](book/VOLUME-VI-INTERVIEWS.md) | Interviews `vi-*`; naming exception when no YouTube id |
| [VOLUME-VII-ESSAYS.md](book/VOLUME-VII-ESSAYS.md) | Substack essays `es-*`; `essay-<slug>-analysis.md` |
| [VOLUME-I-QUOTE-FORWARD-PILOT.md](book/VOLUME-I-QUOTE-FORWARD-PILOT.md) | Pilot / quote-forward (not full volume spec) |

**Cross-volume tables** in each stub should match **`metadata/sources.yaml`** (episode counts, ingest ranges). Stale rows are easy when one volume moves (e.g. Game Theory **#18**).

**Book-track operator docs:** `docs/skill-work/work-jiang/volume-ii-book-track-conventions.md` through `volume-vii-book-track-conventions.md` — should stay aligned with `metadata/book-architecture.yaml` and `metadata/source-map.yaml`.

---

## 2. Analysis memo naming

| Corpus | Pattern | Notes |
|--------|---------|--------|
| YouTube lectures (Geo, Civ, Game Theory, Great Books, most Interviews) | `{video_id}-{series}-{NN}-analysis.md` | `series` segment uses hyphenated slug matching lecture filenames (`geo-strategy`, `civilization`, `game-theory`, `great-books`, `interviews`) |
| Interviews without `watch?v=` in lecture | `interviews-NN-analysis.md` | Documented in [VOLUME-VI-INTERVIEWS.md](book/VOLUME-VI-INTERVIEWS.md) |
| Substack essays | `essay-<slug>-analysis.md` | [VOLUME-VII-ESSAYS.md](book/VOLUME-VII-ESSAYS.md); slug matches `substack/essays/<slug>.md` |

Do **not** bulk-rename analysis files without updating **`analysis_path`** in `sources.yaml` (and any render caches).

---

## 3. YAML front matter (lecture memos)

**Recommended keys** for **video-lecture** analysis memos (Game Theory reference: `analysis/hE4l9WyLF3U-game-theory-01-analysis.md`):

- `analysis_id` — usually same as `source_id` (`gt-01`, …)
- `video_id` — YouTube id; must match `sources.yaml` for that `source_id`
- `source_id` — registry id
- `canonical_url` — lecture URL from registry
- `series` — e.g. `game-theory`
- `episode` — integer episode index
- `chapter_candidates` — list of chapter ids (e.g. `[gt-ch01]`); should be non-empty when `source-map.yaml` maps exactly one chapter to that source (enables `--require-analysis-frontmatter` checks)
- `appendix_candidates`, `themes` — lists (may be empty)
- `status` — typically `complete` when memo is usable
- `quality_level` — e.g. `draft`

**Essay memos** often omit `source_id` / `episode` in front matter today; the audit script flags them when scored against lecture keys — treat as **documented gap** optional to normalize later.

---

## 4. Registry rules (`sources.yaml`)

For each source row:

- **`analysis_path`** — relative path under `work-jiang/` to the memo; must exist on disk when `status.analysis` is `complete`
- **`status.analysis`** — `complete` vs `missing` must agree with presence of a substantive memo and `analysis_path`
- **`chapter_mapping`** — book-track field; distinct from `chapter_candidates` inside memos

**Lockstep:** When adding a memo, set **`analysis_path`** and **`status.analysis: complete`** together (mirror existing `gt-01` / `gt-16` / `gt-18` rows).

---

## 5. Machine scan snapshot (embedded)

Run `python3 scripts/work_jiang/audit_predictive_history_format.py` to refresh. Representative output at audit creation:

### Per-series counts

| series | total | analysis complete | analysis missing | analysis_path null |
|--------|-------|-------------------|------------------|-------------------|
| civilization | 60 | 2 | 58 | 58 |
| essays | 33 | 33 | 0 | 0 |
| game-theory | 18 | 18 | 0 | 0 |
| geo-strategy | 20 | 13 | 7 | 7 |
| great-books | 8 | 8 | 0 | 0 |
| interviews | 12 | 12 | 0 | 0 |
| secret-history | 28 | 1 | 27 | 27 |

### Findings from structural checks

- **Essay analyses:** many lack `source_id` / `episode` in front matter (optional normalization for Volume VII).
- **Empty `chapter_candidates`:** several memos have `[]` where `source_map` maps a **single** chapter — normalization candidates (Game Theory **gt-16** fixed in 2026-04 batch; interviews/geo/great-books/civ-20 rows remain backlog).

---

## 6. Recommended waves (after this audit)

1. **Volume IV Game Theory** — finish `gt-02`–`gt-15`, `gt-17` memos + registry (closed corpus, book spine wired).
2. **Remaining Geo-Strategy** — seven memos (`analysis_path` null).
3. **Secret History** — twenty-seven memos.
4. **Civilization** — fifty-eight memos (largest).

**Avoid** running `normalize_analysis_frontmatter.py` blindly for non–geo-strategy series until that script is generalized (it historically assumed `series: geo-strategy`).

---

*Operator lane — not Voice knowledge until merged through the gate.*
