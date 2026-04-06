#!/usr/bin/env python3
"""
Import a US Bank checking CSV into business-ledger.jsonl.

Instance-specific (grace-mar). Not template-portable.

Usage:
  python3 scripts/import_bank_csv.py \
    --csv "/path/to/Checking - 0889_01-01-2025_12-31-2025.csv" \
    --venture grace-gems

  python3 scripts/import_bank_csv.py --csv /path/to.csv --venture grace-gems --dry-run
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = "grace-mar"


def _classify(tx_type: str, name: str, amount: float) -> dict[str, str]:
    """Return category, tax_category, and account based on transaction name patterns."""
    name_upper = name.upper()

    if tx_type == "CREDIT":
        if "ETSY INC" in name_upper:
            return {
                "category": "revenue",
                "tax_category": "sales_revenue",
                "account": "etsy_payments",
            }
        if "ZELLE" in name_upper:
            return {
                "category": "other_income",
                "tax_category": "other_income",
                "account": "bank_checking",
            }
        if "MOBILE CHECK" in name_upper:
            return {
                "category": "other_income",
                "tax_category": "other_income",
                "account": "bank_checking",
            }
        return {
            "category": "other_income",
            "tax_category": "other_income",
            "account": "bank_checking",
        }

    # DEBIT
    if "ETSY INC" in name_upper or "ETSY.COM" in name_upper:
        return {
            "category": "platform_fees",
            "tax_category": "business_expense",
            "account": "credit_card",
        }
    if "ANALYSIS SERVICE CHARGE" in name_upper:
        return {
            "category": "bank_fees",
            "tax_category": "business_expense",
            "account": "bank_checking",
        }
    if "WIRE TRANSFER" in name_upper:
        return {
            "category": "materials",
            "tax_category": "cogs",
            "account": "bank_checking",
        }
    if "ZELLE" in name_upper and "TO " in name_upper:
        return {
            "category": "materials",
            "tax_category": "cogs",
            "account": "bank_checking",
        }
    if "EXTERNAL TRANSFER" in name_upper:
        return {
            "category": "transfer",
            "tax_category": "non_deductible",
            "account": "bank_checking",
        }
    if "CUSTOMER WITHDRAWAL" in name_upper:
        return {
            "category": "personal_draw",
            "tax_category": "non_deductible",
            "account": "bank_checking",
        }
    return {
        "category": "other_income",
        "tax_category": "business_expense",
        "account": "bank_checking",
    }


def _extract_counterparty(name: str) -> str | None:
    """Try to extract a meaningful counterparty name."""
    name_upper = name.upper()
    if "ETSY INC" in name_upper:
        return "Etsy Inc."
    if "ZELLE" in name_upper:
        m = re.search(r"(?:FROM|TO)\s+(.+?)(?:\s{2,}|\s+CTI)", name)
        if m:
            return m.group(1).strip().title()
    return None


def parse_csv(csv_path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            date_str = r["Date"].strip().strip('"')
            tx_type = r["Transaction"].strip().strip('"')
            name = r["Name"].strip().strip('"')
            memo = r.get("Memo", "").strip().strip('"')
            amount_raw = float(r["Amount"].strip().strip('"'))
            amount = abs(amount_raw)

            cls = _classify(tx_type, name, amount)

            ledger_type = "income" if tx_type == "CREDIT" else "expense"
            if cls["category"] == "transfer":
                ledger_type = "transfer"

            counterparty = _extract_counterparty(name)

            row: dict[str, Any] = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "date": date_str,
                "description": name,
                "amount_usd": round(amount, 2),
                "type": ledger_type,
                "category": cls["category"],
                "venture": "",  # filled by caller
                "account": cls["account"],
                "tax_category": cls["tax_category"],
            }
            if counterparty:
                row["vendor_or_customer"] = counterparty

            rows.append(row)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Import bank CSV into business ledger.")
    parser.add_argument("--csv", required=True, help="Path to the bank CSV file")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--venture", required=True, help="Venture slug (e.g. grace-gems)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    csv_path = Path(args.csv).expanduser()
    if not csv_path.exists():
        print(f"CSV not found: {csv_path}", file=sys.stderr)
        return 1

    rows = parse_csv(csv_path)
    for r in rows:
        r["venture"] = args.venture

    if args.dry_run:
        income = sum(r["amount_usd"] for r in rows if r["type"] == "income")
        expense = sum(r["amount_usd"] for r in rows if r["type"] == "expense")
        transfer = sum(r["amount_usd"] for r in rows if r["type"] == "transfer")

        print(f"  Parsed {len(rows)} transactions from {csv_path.name}")
        print(f"  Date range: {rows[0]['date']} to {rows[-1]['date']}")
        print(f"  Total income:    ${income:>12,.2f}")
        print(f"  Total expense:   ${expense:>12,.2f}")
        print(f"  Total transfer:  ${transfer:>12,.2f}")
        print(f"  Net:             ${income - expense - transfer:>12,.2f}")
        print()

        # Category breakdown
        from collections import defaultdict
        cats: dict[str, float] = defaultdict(float)
        for r in rows:
            sign = 1 if r["type"] == "income" else -1
            cats[r["category"]] += r["amount_usd"] * sign
        print("  By category:")
        for cat in sorted(cats.keys()):
            print(f"    {cat:<25} ${cats[cat]:>12,.2f}")
        print()

        # Show a few sample rows
        print("  Sample rows:")
        for r in rows[:5]:
            sign = "+" if r["type"] == "income" else "-"
            print(f"    {r['date']}  {sign}${r['amount_usd']:>10,.2f}  {r['category']:<20}  {r['description'][:50]}")
        if len(rows) > 5:
            print(f"    ... and {len(rows) - 5} more")
        return 0

    # Write to ledger
    ledger_path = REPO_ROOT / "users" / args.user / "business-ledger.jsonl"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with open(ledger_path, "a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    print(f"Imported {len(rows)} transactions into {ledger_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
