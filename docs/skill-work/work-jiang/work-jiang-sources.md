# work-jiang — sources

**Authorized sources** for the **Predictive History** / Jiang book lane: primary public surfaces where lectures and updates ship. **Not** Voice knowledge until merged through the gate; curated corpus lives under [research/external/work-jiang/README.md](../../../research/external/work-jiang/README.md).

**Work-strategy spine:** Bulk caption sync and territory ownership are documented in [work-strategy/common-inputs.md § Predictive History](../work-strategy/common-inputs.md) and [youtube-channels/predictive-history/README.md](../../../research/external/youtube-channels/predictive-history/README.md) (**Work-strategy wiring**).

**Principle:** [Work modules — authorized sources lists](../work-modules-sources-principle.md).

| Source | URL | Notes |
|--------|-----|-------|
| Predictive History (YouTube) | https://www.youtube.com/@PredictiveHistory/videos | Canonical lecture channel; transcript pulls under [youtube-channels/predictive-history](../../../research/external/youtube-channels/predictive-history/README.md); **work-strategy–first** ingest — [common-inputs § PH](../work-strategy/common-inputs.md) |
| Predictive History (Substack) | https://predictivehistory.substack.com/ | Primary written surface — essays / newsletter by Professor Jiang (Predictive History); complements YouTube; subscriber count and cadence change on Substack |
| Jiang Xueqin (X / Twitter) | https://x.com/xueqinjiang | Principal public social; verify handle if it changes |
| Polymarket (optional instrument) | https://polymarket.com | **Not** a lecture source — optional **cross-check** when mapping predictions to liquid markets; protocol + safeguards: [prediction-tracking/PREDICTION-MARKETS-INTEGRATION.md](../../../research/external/work-jiang/prediction-tracking/PREDICTION-MARKETS-INTEGRATION.md) |

Add rows (e.g. Discord) as you like.

---

## Third-party references (non-canonical)

Fan- and analyst-built surfaces that help **follow what Jiang’s audience / follower community is doing** (mirrors, transcripts, scorecards, discourse). **Not** Jiang-official and **not** substitutes for the [operator curated corpus](../../../research/external/work-jiang/README.md) or [metadata/sources.yaml](../../../research/external/work-jiang/metadata/sources.yaml).

| Source | URL | Notes |
|--------|-----|-------|
| Jiang Prediction (unofficial) | https://jiangprediction.com/ | **Community pulse:** browsable subtitle-cleaned lectures + a public **prediction tracker** (by [@ethtachi](https://x.com/ethtachi)); site **disclaims** affiliation with Jiang or Predictive History. Handy to **follow along** with how part of the audience reads and scores the teaching arc — treat scores and counts as **their** project, not ground truth. **Mirror:** https://jiangs-predictions-and-archives.vercel.app/ |

**Video index:** `python3 scripts/fetch_youtube_channel_transcripts.py --channel "https://www.youtube.com/@PredictiveHistory/videos" --index-only --enrich-metadata -o research/external/youtube-channels/predictive-history`
