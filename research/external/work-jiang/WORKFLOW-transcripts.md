# Work-jiang — systematic transcript intake & analysis

**Primary purpose:** Build the book **Predictive History** and propagate its ideas. Everything else in this lane—transcripts, registries, metrics, analysis artifacts—is **derivative or supportive** of that purpose.

Operator research for the Jiang book/site lane. **Not** Record truth until merged through the gate. See [users/grace-mar/work-jiang.md](../../../users/grace-mar/work-jiang.md) for project purpose.

---

## 1. What this workflow produces

For each video you care about, you want **three layers** on disk (names are conventions, not law):

| Layer | Purpose | Typical location |
|-------|---------|------------------|
| **Raw caption pull** | Machine transcript + provenance header | `research/external/youtube-channels/predictive-history/transcripts/` (often **gitignored**; see channel README) |
| **Lightly-cleaned verbatim** | Caption body + same systematic ASR replacements as curated (`asr_light_clean`); one file per lecture for **diff** vs curated / `## Full transcript` | `research/external/work-jiang/verbatim-transcripts/<same-basename-as-lecture>.md` — **generated** by `scripts/work_jiang/sync_verbatim_transcripts.py`; bodies usually **gitignored** (see [verbatim-transcripts/README.md](verbatim-transcripts/README.md)) |
| **Curated lecture file** | Human-readable archive: metadata, “at a glance,” optional full ASR, **canonical YouTube URL** | `research/external/work-jiang/lectures/<slug>.md` |
| **Analysis memo** | Structured read: claims, tags, lattice crosswalk, tensions, dependencies | `research/external/work-jiang/analysis/<video_id>-<short-slug>.md` (or append sections in one rolling doc — pick one pattern and keep it). Prefer **YAML front matter** (`chapter_candidates`, `source_id`, …) via `python3 scripts/work_jiang/normalize_analysis_frontmatter.py --write` after `build_source_registry.py` so book/site metadata stays machine-readable. |

Keeping **raw** and **curated** separate avoids mixing YouTube caption noise with your editorial summary.

**Longitudinal influence (optional):** To track how **public engagement** with Jiang material changes over time (views, likes, comment counts, channel subscribers), use [influence-tracking/README.md](influence-tracking/README.md) and `scripts/snapshot_youtube_video_metrics.py` → append-only `influence-tracking/snapshots/video-metrics.jsonl`. This measures **attention proxies**, not “impact” in a causal sense.

**Prediction accuracy (optional):** Log falsifiable claims in [prediction-tracking/registry/predictions.jsonl](prediction-tracking/registry/predictions.jsonl) with evaluation windows and evidence URLs; see [prediction-tracking/README.md](prediction-tracking/README.md). **Separate** from views/likes — a viral video can host a wrong forecast.

**Mainstream divergence (optional):** When a lecture asserts something **contested** vs a named consensus (historiography, IR, theology), add a row to [divergence-tracking/registry/divergences.jsonl](divergence-tracking/registry/divergences.jsonl); see [divergence-tracking/README.md](divergence-tracking/README.md). Always name **whose** mainstream.

---

## 2. Phase A — Acquire & register

1. **Fetch transcripts (sync CLI)** — Implementation lives in `scripts/youtube_transcripts/`; wrapper: `scripts/fetch_youtube_channel_transcripts.py`.  
   Deps: `pip install -e ".[youtube-research]"` (`yt-dlp`, `youtube-transcript-api`). Optional tiers: yt-dlp WebVTT, `whisper.cpp` (`--enable-whisper`, `WHISPER_CPP_*`). Optional metadata: `GOOGLE_API_KEY` / `YOUTUBE_DATA_API_KEY` for YouTube Data API v3 snippet/duration.

   ```bash
   python3 scripts/fetch_youtube_channel_transcripts.py \
     --channel "https://www.youtube.com/@PredictiveHistory/videos" \
     --output-dir research/external/youtube-channels/predictive-history \
     --resume --sleep 0.5
   ```

   - **`--input urls.txt`** — one channel, playlist, or watch URL per line (multi-series / multi-playlist).  
   - **`--dry-run --limit 200`** — list IDs/titles without downloading (queue planning).  
   - **`--resume`** — skip videos that already have a non-trivial `.txt`.  
   - **`--force`** — refetch even when manifest hash matches.  
   - **`transcript_manifest.json`** — `content_hash`, `quality`, `source_tier`, timestamps (dedup / incremental).  
   - Output: `transcripts/*.txt` + `index.json` + manifest. See [predictive-history/README.md](../../youtube-channels/predictive-history/README.md) for RQ/Redis, env vars, and rebuild-after-queue.  
   - **ASR fidelity:** Raw `.txt` lives under `predictive-history/transcripts/` (often gitignored). Use it to detect/fix caption errors before quoting in the book — see [ASR-VERIFICATION-RUBRIC.md](ASR-VERIFICATION-RUBRIC.md) and [predictive-history/transcripts/README.md](../../youtube-channels/predictive-history/transcripts/README.md).

2. **Optional parallel queue** — `pip install -e ".[transcript-pipeline]"`, Redis (`docker compose -f docker-compose.transcripts.yml up -d`), then `scripts/enqueue_youtube_transcripts.py` + `scripts/run_transcript_rq_worker.py`. Re-run the sync CLI afterward to refresh `index.json` (or use `--resume` to avoid re-downloads).

3. **Register intent** — note in your tracker or `work-jiang.md` **WORK GOALS** / `near_term` which series or episode IDs you are processing this week (operator choice).

### Multi-series (Predictive History)

The umbrella book line is **Predictive History** — **one volume per lecture series**. Geo-Strategy and **Civilization** are separate corpora; keep them distinct on disk and in metadata. For **Volume II** (Civilization), **Part II** is **Divergence** (historiographic comparison via `divergence-tracking`), not the Geo-Strategy **prediction** pass — see [book/VOLUME-II-CIVILIZATION.md](book/VOLUME-II-CIVILIZATION.md).

| Series | `series` (in `metadata/sources.yaml`) | `source_id` pattern | Curated lecture filename pattern |
|--------|----------------------------------------|---------------------|----------------------------------|
| Geo-Strategy | `geo-strategy` | `geo-01` … | `lectures/geo-strategy-NN-*.md` |
| Civilization | `civilization` | `civ-01` … | `lectures/civilization-NN-*.md` |
| Secret History (Vol. III) | `secret-history` | `sh-01` … | `lectures/secret-history-NN-*.md` |
| Game Theory (Vol. IV) | `game-theory` | `gt-01` … | `lectures/game-theory-NN-*.md` |
| Great Books (Vol. V) | `great-books` | `gb-01` … | `lectures/great-books-NN-*.md` |

**Curated lecture filename & slug (canonical rules):**

- **One file per episode.** The path under `lectures/` is the stable key for sorting and tooling:  
  **`lectures/<series-prefix>-<NN>-<kebab-slug>.md`**
  - **`<series-prefix>`** — exactly `geo-strategy`, `civilization`, `secret-history`, `game-theory`, or `great-books` (matches `series` in `sources.yaml`).
  - **`<NN>`** — **two-digit** episode index (`01`–`99`), zero-padded. It **must** match the numeric **`episode`** field for that row in `metadata/sources.yaml` (e.g. `episode: 4` → `…-04-…`).
  - **`<kebab-slug>`** — lowercase words separated by **hyphens**, ASCII; short human-readable topic (may include a date fragment for geo, e.g. `2024-04-24`). It does **not** need to mirror the YouTube title character-for-character.
- **Display title vs filename.** The first markdown **`# `** heading is the **display title** (usually aligned with the YouTube title). It may differ from `<kebab-slug>`; **`scripts/work_jiang/build_source_registry.py`** takes the title from the **first `# ` line** when rebuilding `sources.yaml`.
- **Do not** embed `video_id` in the curated lecture filename (optional for **analysis** memos only); join key remains **`video_id`** inside the file and in YAML.
- After adding a file, run **`python3 scripts/work_jiang/build_source_registry.py`** and **`python3 scripts/work_jiang/validate_work_jiang.py`** — the validator checks filename ↔ `episode` ↔ `series` and orphan `lectures/*.md` files.

- Add each processed episode to **`metadata/sources.yaml`** with stable `video_id`, paths, and status flags (same shape as Geo-Strategy rows).
- **Analysis memos** — same convention as Geo-Strategy (`analysis/<video_id>-<short-slug>.md`); include `series` / `source_id` in front matter when normalizing.
- **Intellectual chronology** (`metadata/chronology.yaml`) is currently scoped to the **Geo-Strategy** arc; Civilization sources do **not** need to appear there until you extend chronology for that volume (validator: every `geo-*` source must be covered; `civ-*` registers elsewhere).

---

## 3. Phase B — Normalize & link

For each target video:

0. **Sync lightly-cleaned verbatim files (after raw captions exist)** — Builds `verbatim-transcripts/<slug>.md` from `predictive-history/transcripts/{video_id}_*.txt`, matched to `lectures/<slug>.md` via `watch?v=` / `youtu.be/` URL. Default is dry-run (prints plan); `--write` creates files. Use for **diffing** caption text vs curated prose without opening raw headers by hand.

   ```bash
   python3 scripts/work_jiang/sync_verbatim_transcripts.py
   python3 scripts/work_jiang/sync_verbatim_transcripts.py --dry-run
   python3 scripts/work_jiang/sync_verbatim_transcripts.py --write
   ```

   See [verbatim-transcripts/README.md](verbatim-transcripts/README.md). Flow: **fetch raw** (Phase A) → **sync verbatim** → **diff** vs curated / rubric ([ASR-VERIFICATION-RUBRIC.md](ASR-VERIFICATION-RUBRIC.md)).

1. **Stable key** — use **`video_id`** (11 chars) as the join key between `index.json`, raw `.txt`, curated lecture, analysis memo, and verbatim file.

### Optional: verbatim appendix in curated lecture

If an episode needs **caption-faithful** excerpts in git without committing the full transcript file, append the section from [templates/verbatim-appendix-snippet.md](templates/verbatim-appendix-snippet.md). Full bulk captions remain in `predictive-history/transcripts/*.txt` (local).

2. **Canonical URL** — `https://www.youtube.com/watch?v=<video_id>` unless you have a playlist-specific URL; prefer **`@PredictiveHistory`** uploads when that is the source of truth (verify title/series match; avoid unrelated fan edits).

3. **Slug** — filesystem-safe stem, e.g. `geo-strategy-01-iran-strategy-matrix-2024-04-24` or `xEEpOxqdU5E-geo-strategy-01`; include **video_id** in analysis filename if you want grep-friendly linkage.

4. **Curated lecture file (when needed)** — If captions alone are insufficient (e.g. classroom Q&A, longer ASR), add or update `lectures/<slug>.md` with:
   - Speaker, audience, date (if stated), topic, **canonical Source** line  
   - Short **At a glance** before dumping full transcript  
   - **Tags** line for retrieval

   **Large paste / multi-part transcript:** Replace only the `## Full transcript` body in an existing file by piping or listing fragments (no `_c1.txt` chunk files required in the repo):

   ```bash
   cat part1.txt part2.txt | python3 scripts/work_jiang/merge_lecture_transcript.py \
     research/external/work-jiang/lectures/<slug>.md --write

   python3 scripts/work_jiang/merge_lecture_transcript.py lectures/<slug>.md -f a.txt -f b.txt --write --normalize
   ```

   `merge_lecture_transcript.py` preserves front matter; `--normalize` runs `normalize_lecture_transcript_asr.py --write` after the merge.

5. **ASR orthography pass (recommended)** — After pasting the full transcript under `## Full transcript`, run the normalizer so recurring mis-hearings (e.g. “Granicus”, “Memnon of Rhodes”, “Thebes” vs “thieves” on Civilization strands) are fixed without hand-editing every line:
   ```bash
   # from repo root; dry-run first (default) — reports substitution counts
   python3 scripts/work_jiang/normalize_lecture_transcript_asr.py \
     research/external/work-jiang/lectures/<slug>.md

   python3 scripts/work_jiang/normalize_lecture_transcript_asr.py \
     research/external/work-jiang/lectures/<slug>.md --write
   ```
   - **Series:** `civilization-*.md` gets **common** + **Civilization** replacement tiers; `geo-strategy-*.md` gets **common** only; `secret-history-*.md` gets **common** + **Secret History** (Roman / Volume III phrases — see `SECRET_HISTORY_REPLACEMENTS` in `asr_transcript_replacements.py`); `game-theory-*.md` gets **common** + **Game Theory** (Volume IV — see `GAME_THEORY_REPLACEMENTS`, often empty until ingests); `great-books-*.md` gets **common** + **Great Books** (Volume V — see `GREAT_BOOKS_REPLACEMENTS`, often empty until ingests). Detected from filename unless you override with `--series civilization|geo-strategy|secret-history|game-theory|great-books|none`.
   - **Scope:** Only the markdown **below** `## Full transcript` is rewritten unless you pass `--whole-file` (avoid touching curated topic headers).
   - **Tables:** Edit `scripts/work_jiang/asr_transcript_replacements.py` when a new episode introduces a systematic ASR error; keep longest phrases first in each list (the script sorts by length, but order matters for identical prefixes).
   - **Not automatic truth:** This is a **readability** aid; spot-check names and add manual fixes for one-off errors.
   - **Shared logic:** Replacement tables apply through `scripts/work_jiang/asr_light_clean.py` (also used by `sync_verbatim_transcripts.py` for the verbatim layer).

6. **ASR audit (targeted)** — For pull-quotes, names, numbers, and sensitive lines, follow [ASR-AUDIT-LOG.md](ASR-AUDIT-LOG.md): set **series** and depth **A/B/C**, run preconditions (`scripts/work_jiang/check_asr_audit_preconditions.py`), then the rubric’s targeted verification table; append fixes to the findings log. See [ASR-VERIFICATION-RUBRIC.md](ASR-VERIFICATION-RUBRIC.md).

---

## 4. Phase C — First pass (close read)

Read the raw pull (or curated transcript) once **without** structuring:

- **Genre** — e.g. Geo-Strategy, Game Theory, Civilization strand.  
- **Audience** — who is being addressed (affects rhetoric).  
- **Moves** — what the lecture *does* (define terms, historical analogy, prediction, normative claim).

Note **exposition** (what the philosophy asserts or teaches) vs **analysis** (predictions, comparisons, stress tests) — work-jiang keeps these separable for the eventual book/site.

---

## 5. Phase D — Structured extraction

Fill the **analysis memo** (see appendix template) with:

- **Thesis / aim** — one paragraph.  
- **Defined terms** — glossary bullets.  
- **Claims** — numbered; tag each as observation / interpretation / forecast where helpful.  
- **References** — events, books, wars, other lectures (internal cross-links by slug or video_id).  
- **Open questions** — what is left ambiguous or deferred to “future class.”

**Machine-readable JSON (recommended for LLM + registries):** add a sidecar `analysis/<video_id>-<slug>-analysis.json` per [lecture-analysis-json-schema.md](../../../docs/skill-work/work-jiang/lecture-analysis-json-schema.md). Validate with:

```bash
python3 scripts/work_jiang/validate_lecture_analysis_json.py path/to/-analysis.json
```

Optional: `python3 scripts/work_jiang/ingest_analysis_json_to_staging.py` to draft staging rows before editing `predictions.jsonl` / `divergences.jsonl`.

**Series plugins:** see [extractors.md](../../../docs/skill-work/work-jiang/extractors.md) — `scripts/work_jiang/extractors/`.

---

## 6. Phase E — Analytic passes (repeatable)

Run any subset per video; order is flexible.

1. **Internal consistency** — Do definitions stay stable? Do later claims depend on earlier ones?  
2. **CIV-MEM lattice** — Follow [CIV-MEM-LENS.md](CIV-MEM-LENS.md): **conditions**, **institutions**, **seams**, **continuity/memory**, **time structure**, **decline/stress**, then **multi-perspective**. [work-civ-mem](../../../docs/skill-work/work-civ-mem/README.md) / [`docs/civilization-memory/`](../../../docs/civilization-memory/README.md) are **retrieval surfaces** for analogy and vocabulary — not automatic truth; tag `{CMC: path}` if corpus text enters a shippable draft ([civ-mem-draft-protocol](../../../docs/skill-work/work-politics/civ-mem-draft-protocol.md)).  
3. **PSY-HIST lattice** — Follow [PSY-HIST-LENS.md](PSY-HIST-LENS.md): **macro variables**, **psychological inertia**, **cycle phase**, **Seldon crisis**, **predictability horizon**, **steering levers**, **validation protocol**. Dual-lens with CIV-MEM; see dual-lens workflow below.  
4. **Current-events grounding (optional)** — One short paragraph: where abstract claims meet a concrete episode; flag **ship** vs **draft** if anything could become public copy.  
5. **Book/site placement** — Outline hook: which chapter or site section this feeds; duplicates or contradictions vs other memos.

### Dual-lens (CIV-MEM + PSY-HIST) workflow

**Why dual-lens?** CIV-MEM answers *what is structured, by whom, and where are the seams?* — conditions, institutions, continuity, decline. PSY-HIST answers *what is predictable, over what horizon, and what are the leverage points?* — macro variables, cycle phase, Seldon crisis, steering levers. Together they produce an Integrated Operator Thesis: structure (CIV-MEM) + prediction/steering (PSY-HIST).

LLM-generated lens memos land in `analysis/pending/`; human review before promotion.

1. **Generate** — `python3 scripts/work_jiang/generate_civmem_memo.py --lecture <source_id>` and/or `generate_psy_hist_memo.py`, or `generate_dual_lenses.py --lecture <source_id>` for both.  
2. **Review** — Edit the draft in `analysis/pending/`; set `review_status: approved` in frontmatter.  
3. **Promote** — `python3 scripts/work_jiang/promote_reviewed_memo.py --id <source_id> --lens civ-mem` (or `--lens psy-hist`).  
4. **Rebuild** — Promote runs `build_source_registry` and `rebuild_all`; or run manually after batch promotion.

---

## 7. Phase F — Quality & provenance checks

Before treating a memo as “done for this sprint”:

- [ ] `video_id` and **canonical URL** match `index.json` / YouTube.  
- [ ] Raw pull path or fetch date noted if someone must reproduce.  
- [ ] Exposition vs analysis clearly separated where mixed.  
- [ ] No companion Record merge — operator lane only unless you run the gated pipeline.

---

## 8. Phase G — Queue discipline

- **Priority** — e.g. by series (Geo-Strategy first), or by dependency (earlier numbered lectures before updates).  
- **Batch size** — e.g. one analysis memo per session, or one *series* per week; avoid an unbounded backlog without a numbered queue.  
- **Stale pulls** — Re-run fetch with `--resume` after long gaps; captions can change.

---

## Appendix A — Analysis memo template (copy into `analysis/<video_id>-<slug>.md`)

```markdown
# Analysis — [short title]

- **video_id:**  
- **canonical_url:**  
- **series / episode:**  
- **raw_transcript:** path or `index.json` reference  
- **analyzed_at:** YYYY-MM-DD (operator)

## Thesis / aim

## Defined terms

## Claims (numbered)

1. …

## Internal tensions (if any)

## CIV-MEM lattice (full)

| Slot | Notes |
|------|--------|
| Conditions | |
| Institutions | |
| Seams / friction | |
| Continuity / memory | |
| Time structure | |
| Decline / stress | |
| Multi-perspective | |

## Cross-refs (other lectures / memos)

## Current-events tie-in (optional draft)

## Book/site outline hook

## Follow-ups
```

---

## Appendix B — Command quick reference

| Goal | Command |
|------|---------|
| **Ingest one lecture** (stdin / `--file` / `--fetch`) | `python3 scripts/work_jiang/ingest_lecture.py civilization 25 --file path.txt` · `cat t.txt \| python3 scripts/work_jiang/ingest_lecture.py civ 25` · `python3 scripts/work_jiang/ingest_lecture.py geo 3 --fetch` · `python3 scripts/work_jiang/ingest_lecture.py secret-history 1 --fetch` |
| **Post-ingest refresh** (registry + backlog + dashboard) | `python3 scripts/work_jiang/refresh_after_ingest.py` (also runs at end of `ingest_lecture.py` unless `--no-refresh`) |
| List channel videos | `python3 scripts/fetch_youtube_channel_transcripts.py --dry-run --limit 200` |
| Pull transcripts | `python3 scripts/fetch_youtube_channel_transcripts.py --resume --output-dir research/external/youtube-channels/predictive-history` |
| Manifest | `research/external/youtube-channels/predictive-history/index.json` |
| Validate analysis JSON | `python3 scripts/work_jiang/validate_lecture_analysis_json.py …/-analysis.json` |
| Rebuild prediction/divergence SQLite | `python3 scripts/work_jiang/rebuild_registry_db.py` |
| Query predictions (SQLite) | `python3 scripts/work_jiang/query_predictions.py --status contradicted` |
| Comparative sweep memo + gate draft | `python3 scripts/work_jiang/run_comparative_sweep.py` |
| Generate CIV-MEM memo (draft → pending) | `python3 scripts/work_jiang/generate_civmem_memo.py --lecture civ-21` |
| Generate PSY-HIST memo (draft → pending) | `python3 scripts/work_jiang/generate_psy_hist_memo.py --lecture geo-12` |
| Generate both lenses | `python3 scripts/work_jiang/generate_dual_lenses.py --lecture geo-12` |
| Promote reviewed memo | `python3 scripts/work_jiang/promote_reviewed_memo.py --id civ-21 --lens civ-mem` |
| Create dual-lens chapter scaffold | `python3 scripts/work_jiang/create_chapter_scaffold.py --chapter-id ch01 --dual-lens` |
| Migrate memo / JSON versions | `python3 scripts/work_jiang/migrate_analysis_memo.py --dry-run analysis/` |
| Lazy bump JSON schema major | `python3 scripts/work_jiang/validate_lecture_analysis_json.py --write-bump-major path/-analysis.json` |
| Optional GPU / API / registry env | [OFFLOAD-ENV.md](OFFLOAD-ENV.md) |

---

## Appendix C — Related docs

- [work-jiang README](README.md) — research tree  
- [Predictive History channel README](../youtube-channels/predictive-history/README.md) — fetch details, gitignore behavior  
- [work-civ-mem README](../../../docs/skill-work/work-civ-mem/README.md) — lattice as external reference, not automatic Record  
