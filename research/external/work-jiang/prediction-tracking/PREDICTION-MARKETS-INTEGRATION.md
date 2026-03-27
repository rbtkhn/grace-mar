# Optional prediction-market crosswalk (work-jiang)

**Purpose:** When analyzing transcripts, the lane may **extract** Jiang’s forecast-like claims first, then **optionally** link each structured prediction to a **real** prediction market (e.g. Polymarket) whose resolution is **close enough** to compare **implied probability + volume** over time — for operator research, not Record truth.

**Status:** Design contract + safeguards. Implementation (matcher, CLI, schema fields) can follow incrementally.

---

## Order of operations (non-negotiable)

1. **Extract** what Jiang asserted from the transcript (scope, conditions, timeframe).
2. **Normalize** into the [prediction registry](README.md) shape (`claim_type`, `evaluation_window`, excerpt, etc.).
3. **Optionally** attempt a **market crosswalk** — only if the operator or automation enables this step for that run.

Never start from “find a Polymarket” and **retrofit** the quote to fit. Market linkage is **enrichment**, not the definition of the prediction.

---

## When to set a crosswalk

| Situation | Action |
|-----------|--------|
| Resolution text aligns with the claim after careful read | Allow `market_match_confidence: high` and store URL + snapshot fields |
| Only a **related** market exists (different geography, narrower event) | Allow with `market_match_confidence: low` and **equivalence_notes** explaining the gap |
| No market, or only **illiquid** / wrong horizon | **Omit** crosswalk; leave `prediction_market` null — **normal** |
| Temptation to stretch wording to force a fit | **Do not** link; log “unmapped” |

---

## Safeguards

1. **No forced fit** — If equivalence is debatable, skip the link or mark **low** confidence with explicit **equivalence_notes** (how market resolution differs from Jiang’s words).
2. **Market rules ≠ lecture intent** — Polymarket resolves on **its** official criteria (often binary, crisp). Jiang may use hedges or broader narrative. Document **assumptions** when you still compare.
3. **Liquidity** — Prefer **volume** on the outcome; treat thin markets as **weak** signals. Say so in notes.
4. **Prices, not AI blurbs** — For snapshots, use the **order book / price row** on the market page, not the site’s generated “Market Context” summary (can be wrong on dates, names, polls).
5. **Coverage** — Many Jiang predictions will have **no** corresponding market. Expect a **high unmapped rate**; that is not pipeline failure.
6. **Optional by run** — Transcript analysis pipelines may default to **extraction + registry only**; market crosswalk is an **opt-in** step or flag.

---

## Suggested optional fields (registry / analysis JSON)

When implementation lands, optional fields on a prediction row (or sidecar) might include:

- `prediction_market` — `{ "url": "...", "platform": "polymarket", "outcome_label": "..." }` or `null`
- `market_match_confidence` — `high` | `medium` | `low` | omitted
- `equivalence_notes` — string; required when confidence is not `high`
- `market_snapshots` — append-only list of `{ "observed_at_utc", "implied_probability", "volume_usd_or_note", "source" }` (operator or script)

Until schema is wired, operators can keep crosswalks in **analysis memos** and link from `outcome_notes`.

---

## Relation to other surfaces

- **[README.md](README.md)** — Core prediction discipline and JSONL shape.
- **work-politics Polymarket** — KY-04 / campaign markets live under [work-politics polling-and-markets.md](../../../../docs/skill-work/work-politics/polling-and-markets.md). work-jiang may reference **different** markets (geopolitics, macro); avoid duplicating Massie-specific URLs unless the same claim is genuinely in scope.

---

## Guardrail

Prediction markets aggregate **trader beliefs**, not ground truth. Use them as a **comparison instrument** alongside **dated world events** — not as a substitute for resolution against reality in the main registry.
