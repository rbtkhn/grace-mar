# Chart of Accounts — work-business

Categories for the business ledger. Use the **slug** column when recording transactions via `emit_business_transaction.py --category <slug>`.

---

## Revenue

| Slug | Description | Tax category |
|------|-------------|-------------|
| `revenue` | Product sales (Etsy, direct) | `sales_revenue` |
| `shipping_revenue` | Shipping charges collected from buyers | `sales_revenue` |
| `custom_fee` | Custom design / rush fees | `sales_revenue` |
| `other_income` | Miscellaneous income | `other_income` |

## Cost of Goods Sold (COGS)

| Slug | Description | Tax category |
|------|-------------|-------------|
| `materials` | Gemstones, gold, silver, findings, settings | `cogs` |
| `shipping_supplies` | Boxes, bubble wrap, labels, tape | `cogs` |
| `postage` | Actual shipping / postage costs | `cogs` |
| `production_labor` | Subcontracted labor (if applicable) | `cogs` |

## Operating Expenses

| Slug | Description | Tax category |
|------|-------------|-------------|
| `platform_fees` | Etsy listing fees, transaction fees, payment processing | `business_expense` |
| `advertising` | Etsy ads, social media ads, promoted listings | `business_expense` |
| `marketing` | Photography, styling, brand materials | `business_expense` |
| `tools_equipment` | Tools, equipment, repair supplies | `business_expense` |
| `office` | Office supplies, software subscriptions | `business_expense` |
| `insurance` | Business insurance (if applicable) | `business_expense` |
| `professional_services` | Accounting, legal, consulting | `business_expense` |
| `education` | Courses, certifications, trade shows | `business_expense` |
| `travel` | Business travel, trade show expenses | `business_expense` |
| `bank_fees` | Bank charges, wire transfer fees | `business_expense` |

## Non-operating

| Slug | Description | Tax category |
|------|-------------|-------------|
| `refund_issued` | Customer refunds | `refund` |
| `sales_tax` | Sales tax collected / remitted | `sales_tax` |
| `personal_draw` | Owner draw (not deductible) | `non_deductible` |
| `transfer` | Internal transfers between accounts | `non_deductible` |

---

## Accounts (payment methods)

Use `--account <slug>` to track where money flows.

| Slug | Description |
|------|-------------|
| `etsy_payments` | Etsy Payments deposit account |
| `paypal` | PayPal business |
| `bank_checking` | Business checking account |
| `cash` | Cash transactions |
| `credit_card` | Business credit card |

---

## Adding categories

Append new rows to the relevant table above. Keep slugs lowercase with underscores. Update this file before using a new slug in the ledger so summaries group correctly.
