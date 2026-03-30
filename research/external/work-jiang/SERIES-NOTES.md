# Geo-Strategy series notes

Operator notes on series status and ingest.

## 2026-03-23 — Series resumed

Jiang has resumed the Geo-Strategy lecture series. Geo-Strategy #12 was previously the finale ("Geo-Strategy END"); new episodes (geo-13, geo-14, …) are expected.

**Ingested 2026-03-23:** geo-13 (US-Iran War Incoming), `8XdL-7tAqnU`; geo-14 (WWIII Begins, Let's Game Theory), `N4cs-8mrP_s`; geo-15 (The Messianic Calling), `bc9adtiIN_k`; geo-16 (Newton's Divine Plan), `Kw-TiN6dEcM`; geo-17 (The Universal Law of Game Theory), `5I2VPYPJJ68`; geo-18 (Is Putin the Übermensch?), `ZgvAHZqaawA`; geo-19 (When Eschatologies Converge), `YQ-xg1nIbMs`; geo-20 (Why the West is Doomed), `E83dpuyvpiM`. Transcripts operator-provided. Analysis pending.

**Next steps when more new videos are available:**
1. Refresh channel index: `python3 scripts/fetch_youtube_channel_transcripts.py --index-only --channel "https://www.youtube.com/@PredictiveHistory/videos" --output-dir research/external/youtube-channels/predictive-history`
2. Check [CHANNEL-VIDEO-INDEX.md](../youtube-channels/predictive-history/CHANNEL-VIDEO-INDEX.md) for new Geo-Strategy uploads
3. Add rows to `metadata/sources.yaml` (geo-13, geo-14, …) with `video_id`, `lecture_path`, etc.
4. Ingest lectures per [WORKFLOW-transcripts.md](WORKFLOW-transcripts.md)
5. Decide volume placement (Volume I extended vs. new appendix / Volume Ia)

## 2026-03-24 — Volume III naming

Volume Three title set by operator: **Secret History**.

**Next setup steps:**
1. Define the lecture corpus boundary for Volume III (`sources.yaml` series key + lecture filename convention).
2. Add a Volume III method note (Part I chapter discipline and Part II evaluation mode).
3. Decide whether Volume III uses prediction adjudication, divergence, or a separate Part II method.

## 2026-03-24 — Volume IV and V naming

Volume Four title set by operator: **Game Theory**.  
Volume Five title set by operator: **Great Books**.

**Next setup steps:**
1. Define lecture corpus boundaries for Volumes IV and V (`sources.yaml` series keys + lecture filename conventions).
2. Add method notes for each volume (Part I chapter discipline and Part II evaluation mode).

## 2026-03-25 — Volume IV (Game Theory) source corpus

**Game Theory #1–#16** ingested: `gt-01` … `gt-16` in `metadata/sources.yaml`, including **Game Theory #16: Pax Judaica Rising** (`0aASxQrJYuo`). Validator clean. Book lane: analysis, chapter mapping, Part II mode still per [book/VOLUME-IV-GAME-THEORY.md](book/VOLUME-IV-GAME-THEORY.md).

## 2026-03-27 — Cross-volume book quality doctrine

Added [book/BOOK-QUALITY-DOCTRINE.md](book/BOOK-QUALITY-DOCTRINE.md) as a continuity anchor for future agent sessions. Doctrine integrates ten editorial upgrades (argument map, thesis openings, steelman/rebuttal, falsification lines, voice charter) under a strict **no scope expansion** rule.

## 2026-03-27 — Volume VII — Essays (written newsletter)

**Essays** (Predictive History newsletter on Substack) are registered as **Volume VII** of the multivolume line. Corpus: `substack/essays/<slug>.md`; scope: [book/VOLUME-VII-ESSAYS.md](book/VOLUME-VII-ESSAYS.md); stub in `metadata/book-architecture.yaml` under `volume_7_essays`. Crosswalk: [substack/README.md](substack/README.md). Optional next step: add `sources.yaml` rows (`essay-*` or similar) if prediction-registry / chapter-map parity with lectures is desired.

## Volume V (Great Books) — next ingest

Handoff for wiring `great-books` / `gb-*` / `lectures/great-books-NN-*.md` and ingesting channel **Great Books** (historical doc through **#7**; corpus now **#1–#8**): [HANDOFF-volume-v-great-books-ingest.md](HANDOFF-volume-v-great-books-ingest.md).
3. Decide chapter-end box type per volume (prediction, divergence, or a dedicated box template).
