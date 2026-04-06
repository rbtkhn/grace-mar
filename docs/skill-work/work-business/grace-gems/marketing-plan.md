# Grace Gems — Marketing Plan

**Venture:** [Grace Gems on Etsy](https://www.etsy.com/market/grace_gems) — custom fine jewelry with natural gemstones; solid 14k/18k gold; handmade in Denver. Star Seller.

**Differentiators:** Natural untreated gemstones, handmade (not mass-produced), solid gold (not plated), custom design available, free worldwide shipping, 30-day returns, 1-year repair warranty, layaway.

---

## 1. Etsy SEO

**Goal:** Improve organic search visibility within Etsy's marketplace.

| Action | Frequency | Notes |
|--------|-----------|-------|
| Title optimization | Per listing | Front-load primary search terms (stone type + jewelry type + metal); 140 char max |
| Tags | Per listing | Use all 13 tags; mix broad ("emerald ring") and long-tail ("natural emerald engagement ring 14k gold") |
| Category accuracy | Per listing | Correct primary + secondary category; affects search placement |
| Photo quality | Per listing | First photo is search thumbnail; clean white background or lifestyle; minimum 5 photos |
| Listing renewal timing | Monthly | Renew top performers before seasonal peaks |
| Competitor keyword audit | Quarterly | Check top sellers in natural gemstone jewelry for tag patterns |

---

## 2. Etsy Ads

**Goal:** Profitable paid visibility for high-margin listings.

| Metric | Target |
|--------|--------|
| Daily budget | Start $1–5/day; scale based on ROAS |
| ROAS target | > 4:1 (revenue / ad spend) |
| Focus listings | Custom engagement rings, high-value pieces (>$200) |

**Rules:** Pause ads on listings with < 3:1 ROAS after 30 days. Do not advertise low-margin items (under $50). Track spend via ledger: `--category advertising --tax-category business_expense`.

---

## 3. Social media

**Channels:** Instagram (primary), Pinterest (secondary).

| Content type | Frequency | Purpose |
|-------------|-----------|---------|
| Product photos | 2–3/week | Showcase new and featured pieces |
| Process / behind-the-scenes | 1/week | Show handmade craft, gemstone selection |
| Customer stories (with permission) | As available | Social proof, engagement |
| Educational (gemstone facts, care tips) | 1–2/month | Authority, SEO backlinks |

**Not:** Political content, campaign material, or work-politics crossover. Grace Gems social is brand-only.

---

## 4. Seasonal calendar

| Window | Prep start | Peak | Key products |
|--------|-----------|------|-------------|
| Valentine's Day | Jan 1 | Feb 1–14 | Engagement rings, heart pendants, couples sets |
| Mother's Day | Mar 15 | Apr 25–May 10 | Birthstone jewelry, family sets, custom pieces |
| Wedding season | Mar 1 | May–Sep | Engagement rings, bridal sets, wedding bands |
| Holiday / Christmas | Oct 1 | Nov 15–Dec 20 | Gift sets, statement pieces, custom orders (early cutoff) |

**Custom order cutoff:** Communicate 3–4 week lead time for custom pieces before each peak.

---

## 5. Customer retention

| Action | Trigger |
|--------|---------|
| Thank-you card with care instructions | Every order |
| Follow-up message (30 days post-delivery) | Orders > $100 |
| Repeat buyer discount | 2nd+ order (optional coupon in packaging) |
| Review request | After delivery confirmation |

---

## 6. Budget tracking

All marketing spend tracked via the business ledger:

```bash
python3 scripts/emit_business_transaction.py \
  --venture grace-gems --type expense --amount 45.00 \
  --category advertising --description "Etsy Ads — March 2026" \
  --tax-category business_expense
```

Monthly review: `python3 scripts/business_ledger_summary.py --venture grace-gems --by category`

---

## 7. Metrics to track

| Metric | Source | Frequency |
|--------|--------|-----------|
| Etsy views / visits | Etsy Stats | Weekly |
| Conversion rate | Etsy Stats | Weekly |
| Revenue | Ledger + Etsy | Monthly |
| Ad spend / ROAS | Ledger + Etsy Ads | Monthly |
| Favorites / saves | Etsy Stats | Monthly |
| Review count / rating | Etsy | Monthly |
| Social followers / engagement | Platform analytics | Monthly |
