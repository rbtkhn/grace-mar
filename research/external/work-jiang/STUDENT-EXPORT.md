# Student export readiness (checklist)

Use this when the **main** Predictive History lane is stable enough to **derive** a separate student or RAG-oriented bundle (optional downstream repo or release artifact). Nothing here is required for day-to-day operator work.

1. **`validate_work_jiang`** — `python3 scripts/work_jiang/validate_work_jiang.py` exits **0** (includes rendered status drift vs `metadata/book-architecture.yaml` by default).
2. **`validate_book_consistency`** — `python3 scripts/work_jiang/validate_book_consistency.py --all` exits **0**, or you **document** any accepted **warnings** (e.g. missing outlines/drafts) in the bundle README.
3. **Architecture ↔ map** — For every chapter id you export, `metadata/book-architecture.yaml` and `metadata/source-map.yaml` list the **same** `source_ids`.
4. **Sources on disk** — Every exported `source_id` in `metadata/sources.yaml` has a resolvable `lecture_path` under this tree; include `video_id` / canonical URL in the bundle if students should open the **official** lecture.
5. **Evidence packs** — `evidence-packs/<chapter_id>.md` exists for each exported chapter (regenerate with `python3 scripts/work_jiang/build_evidence_pack.py --chapter <id>` when architecture changes).
6. **Prediction registry** — Every `prediction_id` listed on exported chapters exists in `prediction-tracking/registry/predictions.jsonl` (enforced by `validate_book_consistency` for architecture-linked ids).
7. **Link refresh** — Run `python3 scripts/work_jiang/link_supporting_registries.py` so `metadata/prediction-links.yaml` (and related link files) match the current `chapter_map` and registry rows.
8. **Scope and version** — State explicitly what the bundle contains (e.g. **Volume I** `ch01`–`ch20` only vs full multivolume) and pin **date or git revision** of the source repo in the bundle README.
9. **Redistribution** — Ship only content you may republish; if in doubt, bundle **your** summaries, registries, and **links** to YouTube/Substack rather than full third-party transcripts.
10. **Analysis honesty** — For a “curated study” claim, prefer chapters with `analysis_path` present and analysis **complete** in `sources.yaml`; otherwise label those chapters **transcript-primary** in the bundle README.

After this checklist passes for your chosen scope, any **chunk manifest / embeddings / student prompts** belong in a **generated export** or **separate repository**, not as a second hand-maintained corpus inside `work-jiang`.
