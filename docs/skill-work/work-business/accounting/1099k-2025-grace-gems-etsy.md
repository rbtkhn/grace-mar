# Form 1099-K (2025) — Grace Gems / Etsy

**Status:** WORK-business reference only. **Not** Record truth. **No** tax or legal advice.  
**PII:** This file intentionally has **no** TINs, SSNs, or account numbers. Keep the original paper/PDF with your tax records.

**Source:** IRS Form 1099-K, tax year **2025**, third-party network (Etsy) — amounts transcribed from the operator’s copy for reconciliation with Etsy seller reports and `users/grace-mar/business-ledger.jsonl`.

---

## Summary boxes

| Box | Description | Amount / value |
|-----|-------------|----------------|
| **1a** | Gross amount of payment card / third-party network transactions | **$338,400.52** |
| **1b** | Card not present transactions | **$0.00** |
| **3** | Number of payment transactions | **377** |
| **4** | Federal income tax withheld | **$0.00** (blank on form) |
| **6** | State | **CO** |

---

## Box 5 — Monthly gross (2025)

| Month | Code | Amount (USD) |
|-------|------|--------------|
| January | 5a | 23,164.49 |
| February | 5b | 40,054.77 |
| March | 5c | 30,375.16 |
| April | 5d | 34,240.39 |
| May | 5e | 23,778.09 |
| June | 5f | 23,957.93 |
| July | 5g | 34,395.74 |
| August | 5h | 20,913.72 |
| September | 5i | 26,886.74 |
| October | 5j | 17,879.99 |
| November | 5k | 24,355.57 |
| December | 5l | 38,397.93 |
| **Total** | | **338,400.52** |

*(Monthly totals match Box 1a.)*

---

## Reconciliation note

**1099-K Box 1a** is **TPSO gross** on the network. It will **not** match:

- Etsy Shop Manager “net sales” (refunds, remitted sales tax, etc.), or  
- **Bank deposits** (Etsy withholds fees, ads, shipping labels, etc., before payout).

Use this doc as one leg of a three-way tie-out: **1099-K ↔ Etsy annual/summary reports ↔ bank ledger** (see [accounting README](README.md) and `import_bank_csv.py --audit-etsy`).
