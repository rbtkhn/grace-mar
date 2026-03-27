# Polling and prediction markets — KY-4 (operator)

**Purpose:** Standard **good morning** intel for the Massie shadow / work-politics lane: **horserace polling** (when it exists) and **prediction-market prices** (Polymarket). This is **operator WORK product**, not Record truth and not Voice knowledge.

**Last checked:** 2026-03-27

---

## Canonical surfaces (bookmark)

| Surface | URL | What it measures |
|--------|-----|-------------------|
| **Polymarket — GOP primary winner** | [polymarket.com/event/ky-04-republican-primary-winner](https://polymarket.com/event/ky-04-republican-primary-winner) | Implied probability per candidate (Massie, Gallrein, others); check **volume** on each outcome and total. |
| **Polymarket — general election (party)** | [polymarket.com/event/ky-04-house-election-winner](https://polymarket.com/event/ky-04-house-election-winner) | Republican vs Democratic **party** to win the seat (not candidate-specific); often **low volume** early — treat price as weak if vol ≈ 0. |

**In-repo race context (static):** [principal-profile.md](principal-profile.md), [opposition-brief.md](opposition-brief.md), [brief-source-registry.md](brief-source-registry.md).

---

## Good morning routine (agent)

Run **after** `operator_daily_warmup.py` / `harness_warmup.py` and **with** the [daily-warmup skill](../../../.cursor/skills/daily-warmup/SKILL.md) “good morning” flow.

1. **Fetch** the two Polymarket URLs above (or equivalent fetch). Report **implied %** and **volume** from the **price row / order book**, not from Polymarket’s **AI “Market Context”** blurb (blurbs can be wrong on names, dates, and poll citations).
2. **Search** the public web for **independent** KY-4 primary polling: e.g. named pollsters, university polls, or major outlets reporting **toplines + methodology**. If none in the last ~30 days, say so plainly.
3. **Separate** (a) **campaign / internal** polls and **media repeating internals** vs (b) **public** polls with disclosed methodology. Never treat internals as equivalent to public surveys.
4. **Caveat block** in the reply: markets ≠ polls; liquidity matters; U.S. regulatory/access context for traders ≠ electorate.

---

## Weekly brief and registry

- Log notable shifts (big volume move, first public poll, etc.) in the weekly brief or session notes as needed.
- Registry row: [brief-source-registry.md](brief-source-registry.md) lists these surfaces under **watch** — update **Last checked** when you touch them.

---

## Guardrails

- **Cite** Polymarket and outlet URLs before any **client-facing** or **posted** use.
- Do not merge polling or market numbers into **SELF**, **EVIDENCE**, or **prompt** without the gated pipeline.
- Prediction markets can be **thin** or **manipulated** at small size; say so when volume is low.
