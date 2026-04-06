# Accounting — work-business

**Purpose:** Real bookkeeping for operator-owned ventures. Revenue, expenses, P&L, tax prep support via a JSONL ledger and summary scripts.

**Instance-specific:** This accounting surface and all scripts/data are grace-mar only. Nothing syncs to companion-self. The template provides the *shape* (seed survey, `work-business.md` stub); this fills it with specific financial data.

---

## How it works

```
operator ──emit──▶ business-ledger.jsonl ──summary──▶ P&L / category / tax reports
```

1. **Record a transaction** — use the CLI or import the function:

```bash
python3 scripts/emit_business_transaction.py \
  --venture grace-gems --type expense --amount 12.50 \
  --category materials --description "Emerald cabochon 3ct" \
  --tax-category cogs
```

2. **View summaries** — P&L, category breakdown, per-venture rollup:

```bash
python3 scripts/business_ledger_summary.py --pnl
python3 scripts/business_ledger_summary.py --by category
python3 scripts/business_ledger_summary.py --venture grace-gems --since 2026-01-01
python3 scripts/business_ledger_summary.py --by tax_category --json
```

3. **Tax prep** — filter by tax_category and date range for Schedule C line items:

```bash
python3 scripts/business_ledger_summary.py --by tax_category --since 2026-01-01 --until 2026-12-31
```

4. **Bank CSV import** — US Bank checking export → `business-ledger.jsonl`:

```bash
python3 scripts/import_bank_csv.py --csv "/path/to/export.csv" --venture grace-gems
python3 scripts/import_bank_csv.py --csv "/path/to/export.csv" --venture grace-gems --dry-run
```

**Etsy matching:** The importer classifies Etsy payouts and Etsy card charges using both the **Name** and **Memo** columns (`is_etsy_bank_descriptor` in `scripts/import_bank_csv.py`) — e.g. `ETSY INC`, `ETSY.COM*`, `ETSY PAYMENTS` / `PAYOUT` / `DEPOSIT` in memo, and compact `ETSYINC`. Reconcile the ledger against Etsy’s seller annual summary (net sales minus fees, marketing, and shipping ≈ deposits, modulo timing).

```bash
python3 scripts/import_bank_csv.py -u grace-mar --audit-etsy --venture grace-gems --year 2025
```

---

## Files

| File | Purpose |
|------|---------|
| `schema-registry/business-transaction.v1.json` | Transaction schema (instance-specific) |
| `scripts/emit_business_transaction.py` | Append one transaction row |
| `scripts/import_bank_csv.py` | Import bank CSV; Etsy descriptor rules; `--audit-etsy` |
| `scripts/business_ledger_summary.py` | P&L, grouping, tax summaries |
| `users/grace-mar/business-ledger.jsonl` | Append-only transaction log |
| **This README** | How to use the accounting surface |
| [chart-of-accounts.md](chart-of-accounts.md) | Account categories with tax mapping |

---

## Conventions

- **Amounts are always positive.** The `type` field (income/expense/refund/transfer) determines the sign.
- **Dates use YYYY-MM-DD.** The `date` field is the transaction date; `ts` is the append timestamp.
- **Categories match chart-of-accounts.** Use the slugs from [chart-of-accounts.md](chart-of-accounts.md) for consistency.
- **One row per transaction.** Split multi-item orders into separate rows if categories differ.
- **Receipt references are optional but recommended** for any transaction over $25 or for tax-deductible items.

---

## Tax prep workflow

1. Run `--by tax_category` for the tax year to get Schedule C line totals
2. Cross-reference with Etsy annual tax summary (1099-K if applicable)
3. Verify COGS total against materials + shipping supply receipts
4. Export JSON for accountant if needed: `--by tax_category --json > tax-2026.json`
