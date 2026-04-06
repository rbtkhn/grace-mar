#!/usr/bin/env python3
"""
Append one transaction row to users/<id>/business-ledger.jsonl.

Instance-specific (grace-mar). Not template-portable.

Usage:
  python3 scripts/emit_business_transaction.py \\
    --venture grace-gems --type expense --amount 12.50 \\
    --category materials --description "Emerald cabochon 3ct"

  python3 scripts/emit_business_transaction.py \\
    --venture grace-gems --type income --amount 285.00 \\
    --category revenue --description "Custom emerald ring" \\
    --customer "Etsy buyer" --receipt-ref "etsy-order-123456" \\
    --tax-category sales_revenue --account etsy_payments
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = "grace-mar"


def ledger_path(user_id: str = DEFAULT_USER_ID) -> Path:
    return REPO_ROOT / "users" / user_id / "business-ledger.jsonl"


def append_transaction(
    user_id: str = DEFAULT_USER_ID,
    *,
    transaction_date: str | None = None,
    description: str,
    amount_usd: float,
    tx_type: str,
    category: str,
    venture: str,
    account: str | None = None,
    tax_category: str | None = None,
    vendor_or_customer: str | None = None,
    receipt_ref: str | None = None,
    notes: str | None = None,
) -> dict[str, Any]:
    """Append one transaction row and return it."""
    if tx_type not in ("income", "expense", "refund", "transfer"):
        raise ValueError(f"Invalid type: {tx_type}")
    if amount_usd < 0:
        raise ValueError("amount_usd must be non-negative")

    row: dict[str, Any] = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "date": transaction_date or date.today().isoformat(),
        "description": description,
        "amount_usd": round(amount_usd, 2),
        "type": tx_type,
        "category": category,
        "venture": venture,
    }
    if account:
        row["account"] = account
    if tax_category:
        row["tax_category"] = tax_category
    if vendor_or_customer:
        row["vendor_or_customer"] = vendor_or_customer
    if receipt_ref:
        row["receipt_ref"] = receipt_ref
    if notes:
        row["notes"] = notes

    path = ledger_path(user_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")

    return row


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append a business transaction to the ledger."
    )
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID, help="User slug")
    parser.add_argument("--venture", required=True, help="Venture slug (e.g. grace-gems)")
    parser.add_argument("--type", dest="tx_type", required=True,
                        choices=["income", "expense", "refund", "transfer"])
    parser.add_argument("--amount", type=float, required=True, help="Amount in USD (positive)")
    parser.add_argument("--category", required=True, help="Account category (e.g. revenue, materials)")
    parser.add_argument("--description", required=True, help="Transaction description")
    parser.add_argument("--date", dest="tx_date", help="Transaction date YYYY-MM-DD (default: today)")
    parser.add_argument("--account", help="Payment method or sub-account")
    parser.add_argument("--tax-category", help="Tax classification")
    parser.add_argument("--customer", help="Customer name (for income)")
    parser.add_argument("--vendor", help="Vendor name (for expenses)")
    parser.add_argument("--receipt-ref", help="Receipt or order reference")
    parser.add_argument("--notes", help="Additional notes")
    parser.add_argument("--json", action="store_true", help="Print the appended row as JSON")
    args = parser.parse_args()

    counterparty = args.customer or args.vendor or None

    row = append_transaction(
        args.user,
        transaction_date=args.tx_date,
        description=args.description,
        amount_usd=args.amount,
        tx_type=args.tx_type,
        category=args.category,
        venture=args.venture,
        account=args.account,
        tax_category=args.tax_category,
        vendor_or_customer=counterparty,
        receipt_ref=args.receipt_ref,
        notes=args.notes,
    )

    if args.json:
        print(json.dumps(row, indent=2))
    else:
        sign = "+" if args.tx_type == "income" else "-"
        print(f"{sign}${row['amount_usd']:.2f}  {row['category']}  {row['description']}  [{row['venture']}]")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
