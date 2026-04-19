# Strategy expert predictions (ledger)

**Purpose:** Single **WORK** place to register **falsifiable** claims attributed to indexed **`thread:<expert_id>`** commentators, with **resolution** and **receipts**—notebook calibration, not a public ranking.

**Not:** Record truth, Voice truth, or a competitive **leaderboard** (see [gamification-metrics.md](gamification-metrics.md)). Prefer **sparse** high-quality rows over scoreboard theater; see guardrails in [strategy-commentator-threads.md](strategy-commentator-threads.md) § *Expert threads: predictive accuracy and opinion drift*.

**Related:** [forecast-watch-log.md](forecast-watch-log.md) (forecast **artifacts**, not per-expert rows) · [daily-brief-YYYY-MM-DD.md](../daily-brief-YYYY-MM-DD.md) **`strategy + verify`** · [`.cursor/skills/fact-check/SKILL.md`](../../../.cursor/skills/fact-check/SKILL.md) for tiered verdicts.

---

## Operator calibration (how this file is maintained)

- **Primary surfaces (equal weight):** append **`pred_id` rows** in the prediction table *and* keep the **`topic_slug` registry** accurate as themes evolve (new rows or notes when a bucket becomes load-bearing).
- **Ingest:** capturing claims in [daily-strategy-inbox.md](daily-strategy-inbox.md) first is **recommended** for traceability; **direct edits to this file are allowed** when you already have cite-grade material.
- **Resolution:** when a row moves past `open`, record **`resolution_confidence`** (evidence tier for the closing receipt), not only status text.
- **Automation:** `scripts/validate_expert_predictions.py` checks roster **`expert_id`**s and registry **`topic_slug`**s; CI runs it with other strategy-notebook validators.

---

## Guardrails

- Only claims that are **checkable** against **primaries or twin wires** (not vibes).
- **Conditional** forecasts (`if X then Y`) need **both** legs scored or deferred.
- Distinguish **Bayesian update** from **flip**; new facts may justify revised judgment.
- **Ingest flow:** inbox first when practical; this file holds **canonical adjudication rows** + optional pointers from [`chapters/YYYY-MM/days.md`](chapters/2026-04/days.md) **`### Open`**. **Direct rows here are OK** without a prior inbox line when attribution is already solid.

---

## Status vocabulary

Use one of: `open` · `resolved-supported` · `resolved-contradicted` · `resolved-partial` · `deferred-horizon` · `deferred-ambiguous` · `withdrawn` (expert explicitly walks back).

---

## Row template

| Field | Description |
|--------|-------------|
| `pred_id` | Stable slug, grep-friendly, e.g. `pred-2026-04-19-example` |
| `expert_id` | Roster slug from [strategy-commentator-threads.md](strategy-commentator-threads.md) |
| `topic_slug` | One of the **2026 prediction-topic registry** slugs below |
| `stated_claim` | One tight sentence (quote or tight paraphrase + attribution) |
| `source` | URL + optional timestamp; inbox line or `days.md` anchor |
| `date_stated` | ISO date |
| `review_by` / `horizon` | Optional |
| `falsifier` | One sentence: what would make the call wrong |
| `resolution_confidence` | Evidence tier for the **closing** receipt (when not `open`): `wire` · `primary` · `expert-echo` · `unclear` — or `—` while still open |
| `resolution` | Status + date + receipt link(s) when closed |
| `notes` | Seams to other experts, `batch-analysis` keys |

---

## 2026 prediction-topic registry (frequency-informed)

**Method:** Keyword / document-frequency scan across [daily-strategy-inbox.md](daily-strategy-inbox.md), [experts/\*/thread.md](experts/mercouris/thread.md), [chapters/2026-04/days.md](chapters/2026-04/days.md), [chapters/2026-04/knots/](chapters/2026-04/knots/), and [meta.md April arc](chapters/2026-04/meta.md). Counts are **indicative** (keyword overlap, not a statistical model). Dense **2026** expert activity in-repo is currently strongest in **2026-04**; extend this registry when other months accumulate comparable ingest volume.

| Order | `topic_slug` | Bucket | Typical falsifiable shape | Often-involved `expert_id` lanes |
|-------|----------------|--------|---------------------------|----------------------------------|
| 1 | `hormuz-strait` | Strait of Hormuz status, transit, closure/reopen, chokepoint leverage | Named strait / blockade / toll / flag-state receipts vs headline | `ritter`, `davis`, `jermy`, `pape`, `johnson`, `marandi`, `mercouris` |
| 2 | `islamabad-us-iran-talks` | Islamabad (or successor venue) negotiation track, MOU, delegation rounds | Scheduled talks / readouts / walk-away vs continuation | `davis`, `freeman`, `parsi`, `mercouris`, `pape`, `marandi` |
| 3 | `ceasefire-pause-resumption` | Ceasefire clock, pause vs resumed strikes, “deal” vs extension | Date-bound ceasefire state + kinetic receipts | `pape`, `davis`, `johnson`, `mercouris`, `marandi` |
| 4 | `naval-blockade-interdiction` | Blockade credibility, interdiction, ORBAT, “porous” vs enforced | AIS / hull / interdiction throughput vs rhetoric | `ritter`, `davis`, `jermy`, `johnson` |
| 5 | `escalation-trap-coercion` | Escalation trap, commitment ratchet, ultimatum geometry | Stated demand sequence + branch outcomes | `pape`, `davis`, `mearsheimer` |
| 6 | `lebanon-vs-nuclear-scope` | Lebanon theater vs nuclear file / EU accountability language | Which fork official rhetoric prioritizes; field vs diplomacy lag | `parsi`, `mercouris`, `mearsheimer`, `blumenthal`, `marandi` |
| 7 | `sanctions-energy-oil` | Sanctions waivers, oil price, SPR, energy macro under war | Policy instrument + market / inventory receipts | `jermy`, `johnson`, `diesen`, `sachs`, `mercouris` |
| 8 | `nato-alliance-europe` | NATO / Article 5 / European theater spillover | Alliance posture statements vs ORBAT / readiness | `johnson`, `ritter`, `mearsheimer`, `macgregor`, `baud` |
| 9 | `war-powers-congress` | U.S. domestic: war powers, authorization, executive vs legislature | Vote / resolution / WH readout chain | `parsi`, `davis`, `barnes` |
| 10 | `multipolar-institutions-dc-process` | Multipolar framing, institutional decay, ExCom vs Truth Social process | Institutional artifact vs personality-driven announcements | `diesen`, `sachs`, `jiang` (PH overlay), `freeman` |

**Optional adjacent slug (not in top-10 density):** `rome-legitimacy` — Rome / papacy / ecumenical seams per [NOTEBOOK-PREFERENCES.md](NOTEBOOK-PREFERENCES.md) grep tags; use when that plane is load-bearing without collapsing into Hormuz/Lebanon mechanics.

### Adding a `topic_slug`

When a recurring falsifiable theme does not fit the table, **append** a new numbered row (next `Order` index), **kebab-case** slug, short **Bucket**, **Typical falsifiable shape**, and **Often-involved** lanes. Then run `python3 scripts/validate_expert_predictions.py` (or rely on CI) so the slug is recognized. **Extended** slugs not in the numbered table must be listed in `EXTENDED_TOPIC_SLUGS` inside `scripts/validate_expert_predictions.py` until promoted into the registry.

---

## Prediction rows (append below)

### Logged rows

| pred_id | expert_id | topic_slug | stated_claim | source | date_stated | falsifier | resolution_confidence | resolution | notes |
|---------|-----------|------------|--------------|--------|-------------|-----------|----------------------|------------|-------|
| `pred-2026-04-17-davis-hormuz-commercial-ceasefire-route` | `davis` | `ceasefire-pause-resumption` | **Davis** (X, same calendar day) **packages** **IRI FM @araghchi** (~06:45): Hormuz passage **open** for **all commercial vessels** for **remaining ceasefire period** on **PMO coordinated route** (Ports & Maritime Organisation framing). | [daily-strategy-inbox.md](daily-strategy-inbox.md) (`thread:davis` + `IRI+TEHRAN` **2026-04-17**); [days.md §2026-04-17](chapters/2026-04/days.md#2026-04-17) **IRI FM primary** + expert continuity | 2026-04-17 | Dated primary or wire that commercial passage on the PMO coordinated route **does not** hold for the billed ceasefire remainder in the sense Davis’s packaging asserts. | — | `open` | Same-day **tension** with `thread:marandi` three-condition Hormuz gloss (commercial-only / Iran route control); **seam**, not merge. |

_Append further rows above this line; keep one primary `expert_id` per row per [strategy-commentator-threads.md](strategy-commentator-threads.md) pairing rules._
