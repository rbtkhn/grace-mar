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
