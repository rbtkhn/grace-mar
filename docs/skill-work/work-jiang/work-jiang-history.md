# work-jiang-history — operator log

> **Append-only** log for the **work-jiang** territory (`research/external/work-jiang/`, extractors, lane CI). **Not** Record truth; **not** companion [self-memory](../../../users/grace-mar/self-memory.md). **Rotatable.**

**Distinct from:** [work-jiang-sources.md](work-jiang-sources.md). **Operator rhythm:** [coffee](../../../.cursor/skills/coffee/SKILL.md) (**`coffee`**; legacy **`hey`** still works). **Per-lane log:** this file — [work-modules-history-principle.md](../work-modules-history-principle.md).

## How to append

- **`## YYYY-MM-DD`**; note feature phases, `scripts/work_jiang/` changes, verification commands run, PR scope.
- Use [LANE-CI.md](LANE-CI.md) and [work-jiang-feature-checklist](../../../.cursor/skills/work-jiang-feature-checklist/SKILL.md) as guardrails.

## Log

### 2026-04-01

- **JIANG–VOICE (v0.1):** Teaching emulation contract for Predictive History — `research/external/work-jiang/docs/templates/JIANG–VOICE.md`, bridge `jiang-voice.md`, Cursor rule `.cursor/rules/jiang-voice.mdc`. Human-curated; transcript audits to expand § IV markers.

### 2026-04-02

- **Interviews #12 YouTube wired:** `oErKnj_uyPA`, `publication_date` 2026-04-01 (yt-dlp); analysis memo `oErKnj_uyPA-interviews-12-analysis.md`; registry transcript stays **pending** until `## Full transcript` placeholder is replaced (`build_source_registry.py` heuristic).
- **Interviews #12 captions:** Fetched tier-1 en (`quality` ~0.95) into `youtube-channels/vi-12-j-shapiro/`; `sync_verbatim_transcripts.py` with `--transcript-root` → `verbatim-transcripts/interviews-12-*.md`; diff-howto `intake/DIFF-vi-12-caption-vs-paste.md`.
- **Interviews #12 transcript merged:** `lectures/interviews-12-…md` `## Full transcript` filled from verbatim via `emit_interview_dialogue_from_verbatim.py` (heuristic Jay/Jiang labels); registry `vi-12` transcript + curated_lecture **complete**.
- **Volume VI Interviews #12 ingest prep:** Jay Shapiro long-form interview (truth / myth / biography / eschatology thread). Scaffold: `lectures/interviews-12-j-shapiro-truth-myth-personal-path.md`, `analysis/oErKnj_uyPA-interviews-12-analysis.md`, `intake/PREP-interviews-12-j-shapiro-truth-and-myth.md`; registry `vi-12`, `vi-ch12` in `book-architecture.yaml` + `source-map.yaml`. `build_source_registry.py`: interviews without `video_id` get `transcript: pending`, `curated_lecture: stub`; placeholder `## Full transcript` keeps pending/stub even after URL wired. `emit_volume6_chapters_yaml.py`: episode kind/priority maps extended past 11.

_(Append below this line.)_

### 2026-04-07

- **Interviews #13 ingested (PBD Podcast #772):** `vi-13` / `vi-ch13` — `lectures/interviews-13-pbd-podcast-772-jiang.md` (operator transcript from grace-mar ingest; one speaker label fix); YouTube `Wio--7_GIOs`, upload date 20260407; VTT `youtube-channels/valuetainment-network/transcripts/Wio--7_GIOs.en.vtt`; draft analysis `analysis/Wio--7_GIOs-interviews-13-analysis.md`; evidence pack `evidence-packs/vi-ch13.md`; `book-architecture.yaml` (`part_2.after_chapter: vi-ch13`), `source-map.yaml`, `CHAPTER-QUEUE-VOLUME-VI.md` (vi-ch12 + vi-ch13 sections), `ANALYSIS-BACKLOG.md` row.
- **`normalize_analysis_frontmatter.py`:** Skips `essay-*-analysis.md`, `interviews-NN-analysis.md` (no leading video id), `*-civmem-analysis.md`, `*-psy-hist-analysis.md`, and Substack front matter (`source_kind` / `series: substack`); adds `--only-glob` (fnmatch on basename) so `--write` no longer clobbers Volume VII essay YAML.

### 2026-04-06

- **Volume VII Substack — World War Trump (initial ingest, numbering superseded):** First landed as `es-32` / `es-ch32`; after **SH #9** insert see bullets below (`es-33` / `es-ch33`, `jiang-ES33-*`). Canonical: [World War Trump](https://predictivehistory.substack.com/p/world-war-trump).
- **World War Trump — analysis + predictions:** Filled `essay-world-war-trump-analysis.md` (thesis, terms, 13 claims, tensions, CIV-MEM stub). Registry predictions renamed to `jiang-ES33-001`–`003` after **Secret History #9** essay insert renumbered Volume VII (`es-33` / `es-ch33` for World War Trump). `book-architecture.yaml` `es-ch33` lists those `prediction_ids`.
- **Volume VII — Secret History #9 (Substack) ingested:** `substack/essays/secret-history-10-the-war-of-heaven.md` (canonical URL `/p/secret-history-10-the-war-of-heaven`; post title **#9**), `analysis/essay-secret-history-10-the-war-of-heaven-analysis.md`, crosswalk + arc in `substack/README.md`; `es-20` / `es-ch20`. **`build_source_registry.py`:** merge preserved fields by **`lecture_path`** (not `source_id`); **skip `publication_date` merge** for `substack/essays/*`. Registry + `emit_volume7` + `source-map` `es-ch33`; evidence packs `es-ch20`, `es-ch32`, `es-ch33`.

### 2026-04-08

- **Game Theory #19 ingested:** `gt-19` / `gt-ch19` — `lectures/game-theory-19-the-hollywood-pentagon-complex.md` (YouTube auto-captions → plain text; VTT `youtube-channels/predictive-history/transcripts/0HYET47Cc-E.en.auto.vtt`); `sources.yaml`, `source-map.yaml`, `book-architecture.yaml` (`part_2.after_chapter: gt-ch19`); stub analysis `analysis/0HYET47Cc-E-game-theory-19-analysis.md` (`status: missing`); evidence pack `evidence-packs/gt-ch19.md`; `ANALYSIS-BACKLOG.md` row; `CHANNEL-VIDEO-INDEX.md` +1 row; `VOLUME-IV-GAME-THEORY.md` corpus note. `validate_work_jiang.py` PASS; `render_status_dashboard.py` refreshed `STATUS.md`.
