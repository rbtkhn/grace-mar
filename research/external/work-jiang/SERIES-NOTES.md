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
