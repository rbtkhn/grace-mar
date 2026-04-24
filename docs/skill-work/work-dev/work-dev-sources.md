# work-dev — sources

YouTube channels, podcasts, newsletters, and **web reference outlets** the operator tracks for **work-dev framing** (integration, offers, partner vocabulary, landscape awareness). **Not** Record truth and **not** a substitute for [integration-status.md](integration-status.md) — see [external-signals.md](external-signals.md).

**Per-video registry (titles + canonical watch URLs, machine-readable JSON):** [research/external/work-dev/youtube-indexes/](../../../research/external/work-dev/youtube-indexes/) — one folder per channel; refresh listing with `fetch_youtube_channel_transcripts.py --index-only` (see that README). Each channel has **`ingestion.json`**: operator marks whether an episode has been **manually ingested** (digest/transcript in-repo) and links artifact paths; `render_youtube_work_dev_catalog.py` writes **`CHANNEL-CATALOG.md`** and **`episode-catalog.json`** with an `ingested` field per video. Keeps provenance for long-horizon research. The table below stays **channel-level** so this page stays scannable.

**Principle:** [Work modules — authorized sources lists](../work-modules-sources-principle.md).

**Companion-self ↔ Open Brain (OB1) bridge (planning):** [ob1-companion-self-bridge-consolidated.md](ob1-companion-self-bridge-consolidated.md) — single reference for bidirectional integration, governance, feasibility study scope, and document bundle (WORK lane; authoritative bundle may later live in companion-self).

---

## Channels and newsletters

| Source | URL | Notes |
|--------|-----|-------|
| AI News & Strategy Daily (Nate B Jones) | https://www.youtube.com/@NateBJones | AI news and strategy with a builder / PM / career lens; **digest (seven skills / K-shaped market):** [transcripts/nate-b-jones-ai-job-market-seven-skills-2026.md](../../../research/external/work-dev/transcripts/nate-b-jones-ai-job-market-seven-skills-2026.md); **operator lane (job log / worksheets, not Record):** [work-career/README.md](../work-career/README.md) |
| Peter H. Diamandis | https://www.youtube.com/@peterdiamandis | Long-horizon exponential and moonshot discourse |
| The Innermost Loop (Dr. Alex Wissner-Gross) | https://theinnermostloop.substack.com/ | Substack — high-velocity intelligence / event-horizon curation; by Dr. Alex Wissner-Gross |
| Open Brain (OB1) | https://github.com/NateBJones-Projects/OB1 | Persistent AI memory system — one Supabase + pgvector database, one MCP protocol, any AI client; community extensions, skills, recipes, dashboards; strong contribution scaffolding (metadata schema, automated PR review, skill composition); reference for skill validation and composition recipe patterns borrowed into companion-self |
| 01-MediaMap (ekristof) | https://github.com/ekristof/01-mediamap | ~1,877-link structured political media reference (Left through Right + supporting); curated work-dev subset below |

Add rows above or below as you like.

**Video list (titles + publication dates):** from repo root, with `yt-dlp` installed (`pip install -e ".[youtube-research]"`), run  
`python3 scripts/fetch_youtube_channel_transcripts.py --channel "<URL>/videos" --index-only --enrich-metadata -o <output-dir>`  
Outputs `CHANNEL-VIDEO-INDEX.md` and `index.json`. Use `--enrich-metadata` so dates are filled (flat listing alone often omits them).

---

## AI / Tech Journalism

Landscape awareness for agent stack, AI infrastructure, platform shifts. Curated from [01-mediamap](https://github.com/ekristof/01-mediamap).

| Source | URL | Notes |
|--------|-----|-------|
| 404 Media | https://www.404media.co/ | Investigative tech journalism; paywalled; strong on platform accountability and AI supply chain |
| TechCrunch | https://techcrunch.com/ | Startup / VC / AI news; useful for tracking competitor launches and funding rounds |
| Hacker News | https://news.ycombinator.com/ | Developer community signal; also in [daily-brief RSS](../../work-strategy/daily-brief-config.json) (tier 3) — web view for manual drill-down |
| ZDNet | https://www.zdnet.com/ | Enterprise tech; AI deployment patterns and vendor analysis |
| The Register | https://www.theregister.com/ | UK tech with editorial bite; good for infrastructure and cloud coverage |
| Engadget | https://www.engadget.com/ | Consumer tech and AI product launches |
| Fast Company | https://www.fastcompany.com/ | Innovation / design / business model patterns |
| Inc. Magazine | https://www.inc.com/ | Small-business and startup execution; unit-economics lens |

## Tech Policy and Governance

Directly relevant to companion-self positioning — governed state, authority, inspectability, AI regulation.

| Source | URL | Notes |
|--------|-----|-------|
| Tech Policy Press | https://www.techpolicy.press/ | AI governance, platform regulation, digital rights; closest to companion-self's governance thesis |
| Internet Policy Review | https://policyreview.info/ | Academic-grade internet regulation and digital policy analysis |
| Center for Humane Technology | https://www.humanetech.com/ | AI ethics and safety framing; aligns with companion-self's humane-purpose guardrails |
| Tech Transparency Project | https://www.techtransparencyproject.org/ | Platform accountability research; inspectability framing |
| New America | https://www.newamerica.org/ | Tech policy think tank; AI and open-source governance reports |

## Cybersecurity / OSINT

Agent security, sandbox thinking, trust surfaces, threat intelligence.

| Source | URL | Notes |
|--------|-----|-------|
| CyberScoop | https://www.cyberscoop.com/ | Cybersecurity policy and government tech security |
| Bleeping Computer | https://www.bleepingcomputer.com/ | Security news, vulnerability disclosures, practical threat intelligence |
| Bellingcat | https://www.bellingcat.com/ | OSINT investigations; methodology reference for provenance and verification |
| The Record (Recorded Future) | https://therecord.media/ | Threat intelligence journalism; nation-state and infrastructure attack coverage |
| OSINT Insider *(Substack)* | https://osintinsider.com/ | Open-source intelligence techniques and tooling; relevant to sandbox observability |

## Economic Data and FinOps

Compute ledger, unit economics, benchmarking, macro context for pricing.

| Source | URL | Notes |
|--------|-----|-------|
| NBER | https://www.nber.org/ | National Bureau of Economic Research; working papers on productivity, AI economics |
| Trading Economics | https://tradingeconomics.com/ | Macro indicators and cross-country data; useful for compute-cost benchmarking context |
| S&P Global Market Intelligence | https://www.spglobal.com/marketintelligence/en/news-insights/latest-news-headlines/ | Market data and sector analysis; enterprise AI adoption signals |
| FINVIZ | https://finviz.com/ | Financial visualization and screening; quick market context |
| Apricitas Economics *(Substack)* | https://www.apricitas.io/ | Data-driven economic analysis; labor, productivity, and tech-sector macro |
| Harvard Business Review | https://hbr.org/ | Business strategy, management, and AI adoption case studies |

## Data, Rationality, and Reference

Observability surfaces, analysis tools, critical thinking for system design.

| Source | URL | Notes |
|--------|-----|-------|
| FlowingData | https://flowingdata.com/ | Data visualization techniques and examples; reference for observability UI |
| Information is Beautiful | https://informationisbeautiful.net/ | Visual data storytelling; dashboard and presentation patterns |
| Statista | https://www.statista.com/ | Statistics and market data; quick-lookup for sizing and benchmarks |
| USAFacts | https://usafacts.org/ | Non-partisan US government data; useful for policy-context lookups |
| Less Wrong | https://www.lesswrong.com/ | AI safety, rationality, decision theory; alignment and agent-reliability framing |
| Farnam Street | https://fs.blog/ | Mental models and decision-making; system-design thinking |

## Source Evaluation

Useful for the [fact-check skill](../../../.cursor/skills/fact-check/SKILL.md) and evaluating source quality programmatically.

| Source | URL | Notes |
|--------|-----|-------|
| Ad Fontes Media | https://adfontesmedia.com/ | Media bias and reliability ratings; structured data for source-quality lookup |
| Media Bias/Fact Check (MBFC) | https://mediabiasfactcheck.com/ | Bias and factual-reporting scores; widest coverage of outlets |
| Google Fact Check Explorer | https://toolbox.google.com/factcheck/explorer | Aggregated fact-check results across organizations; API-queryable |

---

**Mediamap exclusions:** ~1,840 links covering politically-aligned outlets (Left through Right), colleges, book lists, polling, news aggregators, and civics education were excluded. Several (Cook Political Report, BallotPedia, OpenSecrets, C-SPAN, Lawfare, War on the Rocks, Foreign Affairs, etc.) belong in **work-politics** or **work-strategy** — worth a separate pass to backfill those lanes.

**Parallel (work-politics):** [../work-politics/work-politics-sources.md](../work-politics/work-politics-sources.md)

**BrewMind (Philippines pilot):** These feeds are also bundled for **micro-lesson / curriculum depth** in [../work-cici/brewmind-philippines-onboarding-guide.md](../work-cici/brewmind-philippines-onboarding-guide.md) § *Operator depth — work-dev sources* — PH-facing AI content online is thin; **canonical list stays this file**.
