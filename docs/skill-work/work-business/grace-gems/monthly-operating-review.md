# Grace Gems - monthly operating review

**Status:** WORK-only operator checklist. Not accounting, tax, legal, or Record truth.
**Cadence:** Once per month, preferably near month close or before a seasonal peak.
**Purpose:** Keep Grace Gems legible as a business without turning every shop task into a crisis.

## Karajan arc

Read the month in four balanced movements:

1. **Books** - Are transactions, payouts, expenses, layaway, and receipts captured enough for the ledger to be useful?
2. **Shop health** - Are Etsy account health, messages, reviews, listings, and inventory stable?
3. **Marketing** - Are traffic, ads, seasonal timing, and social presence aligned with the next month?
4. **Tax / compliance readiness** - Are records and reminders clean enough that quarterly or annual obligations will not surprise the operator?

The review is complete when each movement has either an update, a parked note, or an explicit "no material change."

## Inputs

- [workflow-reminders.md](workflow-reminders.md)
- [marketing-plan.md](marketing-plan.md)
- [roadmap.md](roadmap.md)
- [../accounting/README.md](../accounting/README.md)
- [../accounting/chart-of-accounts.md](../accounting/chart-of-accounts.md)
- `users/grace-mar/business-ledger.jsonl`
- Etsy shop dashboard / stats / conversations / listings
- Receipts, payout records, ad spend, supply purchases, layaway notes

## Review checklist

### 1. Books

- [ ] Run or prepare a venture summary for `grace-gems`.
- [ ] Confirm recent Etsy payouts are represented or explicitly parked.
- [ ] Confirm expenses are categorized enough for useful P&L review.
- [ ] Check whether the ledger has gone more than 30 days without a transaction.
- [ ] Note missing receipts, layaway balances, refunds, or custom-order payments.

Suggested command:

```bash
python3 scripts/business_ledger_summary.py --venture grace-gems --by category
```

### 2. Shop health

- [ ] Check Etsy messages and response-rate risk.
- [ ] Check Star Seller / account health indicators.
- [ ] Check review count, review score, and unresolved customer issues.
- [ ] Identify listings that need title, tag, photo, price, or policy refresh.
- [ ] Identify inventory or material constraints before the next seasonal window.

### 3. Marketing

- [ ] Review Etsy views / visits and conversion signal.
- [ ] Review ad spend and ROAS if ads ran.
- [ ] Confirm no low-margin listings are being advertised.
- [ ] Check whether seasonal prep is due in the next 30-60 days.
- [ ] Choose one small marketing action for the next month, or explicitly choose none.

### 4. Tax / compliance readiness

- [ ] Check quarterly estimated-tax timing if applicable.
- [ ] Check sales-tax or nexus-related reminders if applicable.
- [ ] Confirm Colorado SOS / business license reminders are not approaching.
- [ ] Confirm records are clean enough for year-end tax prep.
- [ ] Mark any accountant-only question as accountant territory, not agent advice.

## Monthly review note template

Review instances may live under [monthly-reviews/](monthly-reviews/) when the operator wants a durable month file. The first blank instance is [monthly-reviews/2026-04.md](monthly-reviews/2026-04.md).

Append a short note to [../work-business-history.md](../work-business-history.md) only when the review produces a material update, blocker, or decision.

```markdown
### YYYY-MM-DD

- **Grace Gems monthly operating review:** Books: <ok / missing / parked>. Shop health: <ok / issue>. Marketing: <next action / none>. Tax/compliance: <ok / reminder>. Follow-up: <one concrete next action>.
```

## Non-goals

- Do not infer revenue, taxes, inventory, or account status without evidence.
- Do not stage Record candidates unless the companion explicitly wants a business milestone captured.
- Do not treat this checklist as tax or legal advice.
- Do not optimize every surface every month; one real follow-up is enough if the business is quiet.
