# work-politics — sources

YouTube channels, podcasts, newsletters, and **web** surfaces (e.g. prediction markets) the operator tracks for **work-politics framing** (briefs, message discipline, opposition context, pulse, media narrative). **Not** [principal-profile.md](principal-profile.md) as fact baseline, **not** Record truth, **not** a substitute for [brief-source-registry.md](brief-source-registry.md) — shipped briefs still need **cited** sources per territory rules.

**Principle:** [Work modules — authorized sources lists](../work-modules-sources-principle.md).

**Territory boundary:** Keep this list separate from [work-dev sources](../work-dev/work-dev-sources.md) unless the same feed genuinely serves both lanes (then you may duplicate the row with **lane-specific notes**).

| Source | URL | Notes |
|--------|-----|-------|
| Rep. Thomas Massie (official X) | https://x.com/RepThomasMassie | Principal public feed; same lane as [brief-source-registry.md](brief-source-registry.md) @RepThomasMassie row — cite dates on bullets in briefs |
| America First Kentucky (@usa_first_ky) | https://x.com/usa_first_ky | Unofficial analysis / message-support account (operator lane); not the campaign or office — see [account-x.md](account-x.md) |
| Polymarket (KY-04) | https://polymarket.com/event/ky-04-republican-primary-winner | Implied odds + **volume**; also [GE party market](https://polymarket.com/event/ky-04-house-election-winner). Protocol: [polling-and-markets.md](polling-and-markets.md) — cite **price row / order book**, not Polymarket’s AI “Market Context” blurb |
| Robert Barnes (@Barnes_Law) | https://x.com/Barnes_Law | Major political commentator and operative (not only legal); broad campaign and narrative lens — still verify before client-facing or posted use |

**Optional additions (add a row when you want them in the authorized list):**

- **Primary opponent(s) / Gallrein** — X accounts named in [opposition-brief.md](opposition-brief.md); track narrative, never cite without receipts.
- **Kentucky / KY-4 local press** — e.g. state or district outlets you standardize on for earned media (set handles in [brief-source-registry.md](brief-source-registry.md) “Local KY news” when stable).
- **War-powers / civil-liberties ally accounts** — if you use a fixed list for message research (Khanna, etc.), add here so provenance is explicit.

Add rows above or below as you like.

**Video list (titles + publication dates):** from repo root, with `yt-dlp` installed (`pip install -e ".[youtube-research]"`):

```bash
python3 scripts/fetch_youtube_channel_transcripts.py \
  --channel "<URL>/videos" \
  --index-only --enrich-metadata \
  -o research/external/youtube-channels/<your-slug>
```

Outputs `CHANNEL-VIDEO-INDEX.md` and `index.json`. Use `--enrich-metadata` so publication dates are filled. Prefer a dedicated output directory per channel; raw `transcripts/*.txt` are often gitignored (see [youtube-channels README](../../../research/external/youtube-channels/predictive-history/README.md) pattern).
