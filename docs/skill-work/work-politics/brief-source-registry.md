# Brief source registry — work-politics

Structured intake surface for the weekly brief.

Update `Last checked` when you review a source. `Status` is for operator workflow, not Record truth.

---

| Source | Kind | Path / surface | Use for | Cadence | Last checked | Status | Notes |
|--------|------|----------------|---------|---------|--------------|--------|-------|
| KY election calendar | official | `calendar-2026.md` | Key dates, compliance reminders, GOTV timing | weekly | 2026-03-14 | ready | Canonical local copy of election + FEC timing |
| Principal profile | territory doc | `principal-profile.md` | Baseline race context, principal posture, issue grounding | weekly | 2026-03-14 | ready | Refresh if principal posture or race context changes |
| Opposition brief | territory doc | `opposition-brief.md` | Gallrein, Trump/MAGA, spending, narrative lines | twice-weekly | 2026-03-14 | needs_refresh | Still contains placeholders; update before relying on it heavily |
| Iran / war powers brief | issue brief | `iran-foreign-policy-brief.md` | War powers, Iran, Massie quotes, issue messaging | as-needed | 2026-03-14 | ready | Deepest issue brief currently in territory |
| **Tucker Carlson book (TCN transcripts)** | research ingest | [tucker-carlson-book/INDEX.md](../../../research/external/youtube-channels/tucker-carlson-book/INDEX.md) | **Base / media narrative** on Iran, Hormuz, war framing; long-form monologue + interview text for operator triangulation — **not** standalone cite for client copy | as-needed |  | watch | See [work-politics-sources.md](work-politics-sources.md) § Tucker Carlson Network; verify factual lines before ship |
| Revenue log | ops doc | `revenue-log.md` | Commercial/revenue continuity, active commitments | weekly | 2026-03-14 | ready | Use for revenue / offer status section |
| @RepThomasMassie X | live external | principal public X feed | Social highlights, current principal messaging | daily |  | watch | External source; check live before writing final brief |
| Gallrein / opposition social | live external | X, local campaign surfaces | Opposition narrative and activity | daily |  | watch | Track only with citations |
| FEC filings / notices | live external | FEC reporting surfaces | Spending, pre-primary filing, 48-hour notices | weekly |  | watch | Use when refreshing spending summary |
| Local KY news | live external | district / Kentucky press | District narrative, earned media, local events | weekly |  | watch | Add specific outlets as workflow stabilizes |
| **Polymarket KY-04** (primary + GE) | live external | [polling-and-markets.md](polling-and-markets.md) | Implied odds vs horserace; check **volume** | daily (hey) | 2026-04-07 | watch | Prices not Record truth; cite page prices, not AI “Market Context” blurbs |
| **Independent primary horserace polls** | live external | Search + [Ballotpedia](https://ballotpedia.org/) / outlets | Named pollster + toplines when published | as released |  | watch | Distinct from campaign internals; see [polling-and-markets.md](polling-and-markets.md) |
| **Recency pass (operator)** | workflow | See § Recency pass below | Forces brief to lean on **last 7–30 days**, not stale SEO | **every weekly brief** | 2026-03-14 | ready | Scaffold + generator §0; live bullets still operator |
| **Daily brief (work-politics + work-strategy)** | script + JSON | [work-strategy/daily-brief-template.md](../work-strategy/daily-brief-template.md), [work-strategy/daily-brief-config.json](../work-strategy/daily-brief-config.json), [work-strategy/daily-brief-jiang-layer.md](../work-strategy/daily-brief-jiang-layer.md), `scripts/generate_wap_daily_brief.py` | RSS ingest + **W** (campaign) + **S** (product/governance) scores; snapshot + strategy focus + **§1c** work-jiang hooks (slow layer) | **daily** (operator schedule) |  | watch | Not Voice; not SELF; complete synthesis in output before ship |
| **Principal literary sketch** | operator narrative | [principal-portrait-literary-sketch.md](principal-portrait-literary-sketch.md) | Long-form tone / message DNA only — **not** weekly fact intake; verify before donor or explainer copy ships | as-needed |  | draft | Churchill-register prose; see doc § claims to verify |

---

## Recency pass (last 7–30 days)

**Goal:** At least one full pass of the brief where every external bullet is **grounded in the last 7–30 days** (not evergreen search).

| Step | Action |
|------|--------|
| 1 | Pick window: **7d** (tight) or **30d** (standard) for this cycle. |
| 2 | **Principal X** — scroll @RepThomasMassie for the window only; note dates on bullets. |
| 3 | **Opposition / race** — X search + one local outlet archive filtered by date; same window. |
| 4 | **National hooks** (Iran, votes, etc.) — filter Google News or trusted feed by **Past week** / **Past month**. |
| 5 | Log in brief: `Recency window: [7d \| 30d] · checked [date]` |

**Optional skill:** Install **Last 30 Days** (Matt Van Horn) in **your** coding agent if you want scripted social/recent-web pull; still **cite + companion approves** anything that becomes client-facing. Not Voice knowledge.

---

## Status meaning

| Status | Meaning |
|--------|---------|
| `ready` | Local doc/source is usable now |
| `watch` | External source to check during refresh |
| `needs_refresh` | Local doc exists but still needs human update before heavy reuse |
