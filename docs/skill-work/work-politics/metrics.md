# Quantitative metrics — work-politics

Metrics to track across the territory: revenue, funnel, deliverables, territory health, and efficiency. Companion-led; use for reflection and tuning, not automated control.

---

## Current instrumentation status

| Surface | Status | Notes |
|--------|--------|-------|
| Revenue totals from `revenue-log.md` | Instrumented | Read by the WAP operator surface. |
| Key primary dates from `calendar-2026.md` | Instrumented | Read by the WAP operator surface. |
| WAP gate pending count | Instrumented | Derived from `RECURSION-GATE` with WAP territory filter. |
| Brief source readiness | Instrumented | Driven by `brief-source-registry.md`. |
| X/content queue state | Instrumented | Driven by `content-queue.md`. |
| Outreach funnel stages | Manual | Tracked in `outreach-funnel.md`. |
| Objection themes | Manual | Tracked in `objection-log.md`. |
| Fiverr conversion / X engagement / email response | Manual | Still requires human-entered analytics from external platforms. |

---

## Priority set (instrument first)

| Metric | Description | Source |
|--------|-------------|--------|
| **Total revenue** | Cumulative revenue (seed + Fiverr + direct BTC). | [revenue-log.md](revenue-log.md) |
| **Revenue by source** | Split: seed vs Fiverr vs direct BTC (0.1 BTC package). | revenue-log.md |
| **Paid deliverables** | Count of paid outputs (Fiverr orders, BTC package sales). | revenue-log.md; Fiverr orders. |
| **Fiverr conversion** | Orders / impressions (or orders / clicks) if visible; else orders per week. | Fiverr seller dashboard. |
| **Time to delivery** | Hours or days from order/commitment to delivered artifact. | Companion log or Fiverr delivery timestamp. |

---

## Revenue

| Metric | Description | Source |
|--------|-------------|--------|
| Total revenue | Sum of all revenue events. | revenue-log.md |
| Revenue by type | Seed; Fiverr ($100 microtask); direct BTC (0.1 BTC). | revenue-log.md |
| Revenue per principal | If multiple principals over time: revenue attributed to each. | revenue-log.md (note principal in row). |
| Revenue per cycle | Revenue in a defined window (e.g. primary cycle Mar–May 2026). | revenue-log.md + date filter. |

---

## Funnel / conversion

| Metric | Description | Source |
|--------|-------------|--------|
| Leads | Campaign emails sent; Fiverr gig views; X link clicks (if trackable). | Manual log; Fiverr analytics; X analytics. |
| Conversion (lead → paid) | Paid / leads (or paid / qualified leads). | revenue-log + lead log. |
| Average deal size | Total revenue / number of paid engagements. | revenue-log.md |
| Repeat rate | Buyers who pay more than once (Fiverr repeat; seed then BTC). | revenue-log.md |

---

## Outreach learning

| Metric | Description | Source |
|--------|-------------|--------|
| Leads identified | Prospects entered into the outreach working set. | [outreach-funnel.md](outreach-funnel.md) |
| Lane mix | Share of direct vs partner-led outreach entries. | outreach-funnel.md |
| Reply rate | Replies / contacted. | outreach-funnel.md |
| Positive reply rate | Positive replies / contacted. | outreach-funnel.md |
| Meeting rate | Meetings booked / contacted or / positive replies. | outreach-funnel.md |
| Offer response quality | Which offer gets the strongest curiosity or conversion by segment. | outreach-funnel.md |
| Objection frequency | Most common pushbacks by count. | [objection-log.md](objection-log.md) |
| Segment quality | Which segments produce the best conversations relative to volume. | target-registry.md + outreach-funnel.md |
| Partner quality | Which partner types produce credible intros or warmer conversations. | target-registry.md + outreach-funnel.md + objection-log.md |

---

## Deliverables / throughput

| Metric | Description | Source |
|--------|-------------|--------|
| Deliverables produced | Count: one-pagers, briefs, X drafts, research products (e.g. Iran brief). | Companion log or doc count. |
| Deliverables per paid engagement | e.g. Fiverr = 1 one-pager; 0.1 BTC = N briefs + research + X. | Scope per [fiverr-microtask-100.md](fiverr-microtask-100.md), [account-x.md](account-x.md). |
| Revisions requested | Per order: 0, 1, 2+. Quality / fit signal. | Fiverr messages; companion note. |
| On-time delivery % | Delivered within stated turnaround (e.g. 24–48h for Fiverr). | Fiverr delivery time vs order time. |

---

## Territory health

| Metric | Description | Source |
|--------|-------------|--------|
| Principal profile freshness | Date of last update to [principal-profile.md](principal-profile.md). | File mtime or changelog. |
| Calendar accuracy | Key dates (e.g. primary May 19) correct and not past. | [calendar-2026.md](calendar-2026.md). |
| Revenue log current | Last revenue or allocation entry date. | revenue-log.md |
| Allocation vs budget | Allocated / total seed (or / total revenue) — are we on plan? | revenue-log.md allocations vs [seed-allocation-plan.md](seed-allocation-plan.md). |
| Brief source readiness | Count of `ready` / `watch` / `needs_refresh` rows in [brief-source-registry.md](brief-source-registry.md). | brief-source-registry.md |
| Content queue flow | Count by status (`idea`, `draft`, `review`, `posted`) in [content-queue.md](content-queue.md). | content-queue.md |
| WAP gate rhythm | Pending WAP candidates and whether the territory has live gated continuity this week. | `users/grace-mar/recursion-gate.md` with WAP filter |

---

## Efficiency

| Metric | Description | Source |
|--------|-------------|--------|
| Revenue per deliverable | Total revenue / total deliverables (or per type). | revenue-log + deliverable count. |
| % revenue AI + BTC | Share of revenue that is (1) AI-produced and (2) paid in BTC. | revenue-log (note payment rail). |
| % revenue fiat (friendly persuasion) | Share of revenue where human paid in fiat (e.g. Fiverr) after being influenced. | revenue-log. |

---

## Optional (if scaling)

| Metric | Description | Source |
|--------|-------------|--------|
| X followers / engagement | @america_first_ky followers; likes, RTs, replies. | X analytics. |
| Email response rate | Campaign outreach: replies / sent. | Companion log. |
| Cost per acquisition | If running paid lead gen: spend / new paid client. | Ad spend + revenue-log. |

---

*Update metrics periodically; log source and date. Companion decides what to track and how to act on it.*
