# Handoff — Volume V (Great Books) transcript ingest

**Re-entry prompt (paste into a new agent thread):**

> Ingest **Predictive History Volume V — Great Books**: wire `series: great-books`, `gb-*` sources, and `lectures/great-books-NN-*.md` per `HANDOFF-volume-v-great-books-ingest.md`. Then add lectures **#1–#7** from `@PredictiveHistory` (video IDs in that doc), operator transcripts as needed, `build_source_registry`, ASR normalizer, `validate_work_jiang.py --require-analysis-frontmatter`, set `publication_date` from `yt-dlp`, commit work-jiang only.

**Lane:** operator research (`research/external/work-jiang/`). Not Record / RECURSION-GATE unless operator routes there.

---

## 1. Volume status (before you start)

| Item | State |
|------|--------|
| `book/VOLUME-V-GREAT-BOOKS.md` | Title registered; corpus **not** in `sources.yaml` yet |
| Channel | **Great Books #1–#7** appear in `youtube-channels/predictive-history/CHANNEL-VIDEO-INDEX.md` |
| Lecture files | **None** under `lectures/great-books-*.md` yet |

Decisions to **confirm with operator** (or apply consistently and document):

- **`series` key:** `great-books` (kebab; matches `assemble_context_pack.py` `gb` → `great-books` once `gb-01`… exist).
- **`source_id` pattern:** `gb-01` … `gb-99` (two-digit episode).
- **Filename pattern:** `lectures/great-books-NN-<kebab-slug>.md` (same convention as [WORKFLOW-transcripts.md](WORKFLOW-transcripts.md) § Multi-series).

---

## 2. Code / metadata wiring (do before first `great-books-*.md` lands)

Mirror **Game Theory** / **Volume IV** wiring:

1. **`scripts/work_jiang/build_source_registry.py`**
   - Add `GB_NAME = re.compile(r"^great-books-(\d+)-", re.I)`.
   - After the `game-theory` block, glob `great-books-*.md`, append sources with `series: great-books`, `source_id: gb-{ep:02d}` (same `status` shape as `gt-*`).
   - In the final loop over `sources`, add `if s["source_id"].startswith("gb-"):` mirroring `gt-` / `sh-` / `civ-` (`chapter_mapping` = `complete` if `source_id` ∈ `mapped_ids` else `not_started`).

2. **`scripts/work_jiang/validate_work_jiang.py`**
   - Add `GREAT_BOOKS_LECTURE = re.compile(r"^great-books-(\d{2})-(.+)\.md$", re.I)`.
   - In the lecture_path loop, add `elif series == "great-books":` (filename vs `episode` check).
   - Add `("great-books-*.md", "great-books")` to the orphan-lecture glob tuple so unregistered files fail CI.

3. **`scripts/work_jiang/normalize_lecture_transcript_asr.py`**
   - Add `great-books` to `--series` choices; pass through to `detect_series` / `asr_light_clean`.

4. **`scripts/work_jiang/asr_light_clean.py`** (+ **`asr_transcript_replacements.py`** if you want a dedicated tier)
   - `detect_series_from_basename`: `great-books-` → `great-books`.
   - `normalize_transcript_text`: `elif series == "great-books":` — can use empty `GREAT_BOOKS_REPLACEMENTS: list[tuple[str, str]] = []` at first (same as early Game Theory).

5. **`scripts/work_jiang/ingest_lecture.py`** (optional but useful)
   - Accept `great-books` / `gb` aliases like `game-theory` / `gt`.

6. **`scripts/work_jiang/channel_video_lookup.py`** (optional)
   - Add `great-books` / `gb` branch so `lookup_series_episode` can resolve **Great Books #N** from the channel index.

7. **Docs (small deltas)**
   - [WORKFLOW-transcripts.md](WORKFLOW-transcripts.md): add **Great Books (Vol. V)** row — `series: great-books`, `gb-01` …, `lectures/great-books-NN-*.md`; extend normalizer bullet.
   - [book/VOLUME-V-GREAT-BOOKS.md](book/VOLUME-V-GREAT-BOOKS.md): mark checklist item 1–2 done once registry + filenames exist; note first ingest batch **#1–#7**.
   - [README.md](README.md): one clause for Volume V corpus path (mirror III / IV).

---

## 3. Canonical Great Books **#1–#7** (from channel index snapshot)

Use **lecture episode order**, not the index table’s sort order.

| Ep | `video_id` | Suggested slug stem (operator may shorten) |
|----|------------|-----------------------------------------------|
| 1 | `TsD-8FGA84A` | `great-books-01-secrets-of-the-universe` |
| 2 | `Ft2CuowGuYc` | `great-books-02-homer-and-the-invention-of-the-human` |
| 3 | `XRP407WsA0w` | `great-books-03-poets-and-prophets` |
| 4 | `dkzr5A8IlLA` | `great-books-04-the-conscious-universe` |
| 5 | `gXlcR7uHHdA` | `great-books-05-the-odyssey` |
| 6 | `aS-NfPSPMu8` | `great-books-06-the-intimacy-of-love` |
| 7 | `EBWTRvjZ1dw` | `great-books-07-the-anti-homer` |

**Metadata:**

```bash
yt-dlp --print "%(id)s %(upload_date)s %(title)s" "https://www.youtube.com/watch?v=<video_id>"
```

Set each row’s `publication_date` in `sources.yaml` as `YYYYMMDD` → `YYYY-MM-DD` after `build_source_registry.py` merge (same pattern as Game Theory).

---

## 4. Per-lecture ingest recipe (after tooling works)

For each episode:

1. Create `lectures/great-books-NN-<slug>.md` using the same front-matter pattern as [game-theory-01-the-dating-game.md](lectures/game-theory-01-the-dating-game.md): `#` title, Speaker, Audience, **Series: Great Books #N**, **Date (YouTube upload)**, Topic, **Source** line with `watch?v=`, Transcript note, At a glance, tags, `## Full transcript`.
2. `python3 scripts/work_jiang/build_source_registry.py` — rebuilds **all** lecture series into `metadata/sources.yaml` (no per-series flag).
3. `python3 scripts/work_jiang/normalize_lecture_transcript_asr.py research/external/work-jiang/lectures/great-books-NN-….md` (dry-run, then `--write`).
4. `python3 scripts/work_jiang/validate_work_jiang.py --require-analysis-frontmatter`

Optional full generator stack (when touching many metadata surfaces): see [.cursor/skills/work-jiang-feature-checklist/SKILL.md](../../../.cursor/skills/work-jiang-feature-checklist/SKILL.md) § Canonical verify block — trim if you only added lectures + YAML.

---

## 5. Commit scope

Prefer a single focused commit, e.g.:

- `work-jiang: wire Great Books (Vol. V) series + ingest #1–#7`

or split **tooling** vs **lectures** if the diff is huge.

---

## 6. Follow-ups (not blocking first ingest)

- `metadata/book-architecture.yaml`: optional nested `volume_5_great_books` stub (like `volume_4_game_theory`).
- `quote-candidates-great-books.yaml` / `extract_quote_candidates.py` series branch — only if quote mining should include Great Books early.
- ASR audit log rows in `ASR-AUDIT-LOG.md` if you run a formal audit pass.

---

*Operator lane — not Voice knowledge until merged through the gate.*
