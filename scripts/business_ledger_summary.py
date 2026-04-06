#!/usr/bin/env python3
"""
Summarize business-ledger.jsonl — P&L, category breakdown, per-venture rollup, tax summary.

Instance-specific (grace-mar). Not template-portable.

Usage:
  python3 scripts/business_ledger_summary.py -u grace-mar
  python3 scripts/business_ledger_summary.py --venture grace-gems --since 2026-01-01
  python3 scripts/business_ledger_summary.py --by category --json
  python3 scripts/business_ledger_summary.py --by tax_category
  python3 scripts/business_ledger_summary.py --pnl
  python3 scripts/business_ledger_summary.py --pnl --since 2026-01-01 --until 2026-03-31
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = "grace-mar"


def _load_rows(user_id: str) -> list[dict[str, Any]]:
    path = REPO_ROOT / "users" / user_id / "business-ledger.jsonl"
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _filter_rows(
    rows: list[dict[str, Any]],
    *,
    venture: str | None = None,
    since: str | None = None,
    until: str | None = None,
) -> list[dict[str, Any]]:
    filtered = rows
    if venture:
        filtered = [r for r in filtered if r.get("venture") == venture]
    if since:
        filtered = [r for r in filtered if r.get("date", "") >= since]
    if until:
        filtered = [r for r in filtered if r.get("date", "") <= until]
    return filtered


def _group_by(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, float]]:
    """Group rows by a field and sum income/expense."""
    groups: dict[str, dict[str, float]] = defaultdict(lambda: {"income": 0.0, "expense": 0.0, "refund": 0.0, "net": 0.0, "count": 0})
    for r in rows:
        group_key = r.get(key) or "(none)"
        amount = r.get("amount_usd", 0.0)
        tx_type = r.get("type", "expense")
        groups[group_key]["count"] += 1
        if tx_type == "income":
            groups[group_key]["income"] += amount
            groups[group_key]["net"] += amount
        elif tx_type == "expense":
            groups[group_key]["expense"] += amount
            groups[group_key]["net"] -= amount
        elif tx_type == "refund":
            groups[group_key]["refund"] += amount
            groups[group_key]["net"] -= amount
    return dict(groups)


def _pnl(rows: list[dict[str, Any]]) -> dict[str, float]:
    total_income = sum(r.get("amount_usd", 0) for r in rows if r.get("type") == "income")
    total_expense = sum(r.get("amount_usd", 0) for r in rows if r.get("type") == "expense")
    total_refund = sum(r.get("amount_usd", 0) for r in rows if r.get("type") == "refund")
    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "total_refund": round(total_refund, 2),
        "gross_profit": round(total_income - total_expense - total_refund, 2),
        "transaction_count": len(rows),
    }


_DEDUCTIBLE_TAX_CATS = {"cogs", "business_expense", "sales_revenue", "other_income", "refund", "sales_tax"}
_NON_DEDUCTIBLE_TAX_CATS = {"non_deductible"}


def _tax_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Schedule C-style tax summary: taxable income minus deductible expenses only."""
    taxable_income = 0.0
    cogs = 0.0
    business_expenses = 0.0
    non_deductible = 0.0

    line_items: dict[str, float] = defaultdict(float)

    for r in rows:
        amount = r.get("amount_usd", 0.0)
        tx_type = r.get("type", "expense")
        tax_cat = r.get("tax_category", "")

        if tx_type == "income":
            taxable_income += amount
            line_items[tax_cat or "income"] += amount
        elif tx_type in ("expense", "refund"):
            if tax_cat == "cogs":
                cogs += amount
                line_items["cogs"] -= amount
            elif tax_cat in _NON_DEDUCTIBLE_TAX_CATS or not tax_cat:
                non_deductible += amount
                line_items["non_deductible"] -= amount
            else:
                business_expenses += amount
                line_items[tax_cat or "business_expense"] -= amount
        elif tx_type == "transfer":
            non_deductible += amount
            line_items["non_deductible (transfers)"] -= amount

    taxable_profit = taxable_income - cogs - business_expenses
    return {
        "gross_receipts": round(taxable_income, 2),
        "cogs": round(cogs, 2),
        "gross_profit": round(taxable_income - cogs, 2),
        "business_expenses": round(business_expenses, 2),
        "net_profit_loss": round(taxable_profit, 2),
        "non_deductible": round(non_deductible, 2),
        "line_items": {k: round(v, 2) for k, v in sorted(line_items.items())},
    }


def _format_tax(tax: dict[str, Any], label: str = "") -> str:
    lines: list[str] = []
    if label:
        lines.append(f"  Schedule C — {label}")
    else:
        lines.append("  Schedule C Summary")
    lines.append("  " + "-" * 50)
    lines.append(f"  1.  Gross receipts:            ${tax['gross_receipts']:>12,.2f}")
    lines.append(f"  4.  Cost of goods sold:        ${tax['cogs']:>12,.2f}")
    lines.append(f"  7.  Gross profit:              ${tax['gross_profit']:>12,.2f}")
    lines.append(f"  28. Total business expenses:   ${tax['business_expenses']:>12,.2f}")
    lines.append(f"  31. Net profit (loss):         ${tax['net_profit_loss']:>12,.2f}")
    lines.append(f"      (Non-deductible excluded): ${tax['non_deductible']:>12,.2f}")
    lines.append("")
    lines.append("  Line items:")
    for k, v in sorted(tax["line_items"].items()):
        sign = "+" if v >= 0 else ""
        lines.append(f"    {k:<35} {sign}${v:>11,.2f}")
    return "\n".join(lines)


def _format_table(groups: dict[str, dict[str, float]], key_label: str) -> str:
    lines: list[str] = []
    header = f"{'':2}{key_label:<30} {'Income':>10} {'Expense':>10} {'Refund':>10} {'Net':>10} {'Count':>6}"
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))
    for key in sorted(groups.keys()):
        g = groups[key]
        lines.append(
            f"  {key:<30} {g['income']:>10.2f} {g['expense']:>10.2f} {g['refund']:>10.2f} {g['net']:>10.2f} {int(g['count']):>6}"
        )
    return "\n".join(lines)


def _format_pnl(pnl: dict[str, float], label: str = "") -> str:
    lines: list[str] = []
    if label:
        lines.append(f"  P&L — {label}")
    else:
        lines.append("  P&L Summary")
    lines.append("  " + "-" * 40)
    lines.append(f"  Total income:      ${pnl['total_income']:>10.2f}")
    lines.append(f"  Total expense:     ${pnl['total_expense']:>10.2f}")
    lines.append(f"  Total refund:      ${pnl['total_refund']:>10.2f}")
    lines.append(f"  Gross profit:      ${pnl['gross_profit']:>10.2f}")
    lines.append(f"  Transactions:       {pnl['transaction_count']:>10}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize the business ledger.")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID, help="User slug")
    parser.add_argument("--venture", help="Filter by venture slug")
    parser.add_argument("--since", help="Start date (YYYY-MM-DD, inclusive)")
    parser.add_argument("--until", help="End date (YYYY-MM-DD, inclusive)")
    parser.add_argument("--by", choices=["category", "venture", "tax_category", "account", "type", "date"],
                        help="Group by field")
    parser.add_argument("--pnl", action="store_true", help="Show P&L summary")
    parser.add_argument("--tax", action="store_true", help="Show Schedule C tax summary")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    rows = _load_rows(args.user)
    filtered = _filter_rows(rows, venture=args.venture, since=args.since, until=args.until)

    if not filtered:
        print("No transactions found.", file=sys.stderr)
        return 0

    label_parts = []
    if args.venture:
        label_parts.append(args.venture)
    if args.since or args.until:
        label_parts.append(f"{args.since or '...'} to {args.until or '...'}")
    label = " | ".join(label_parts) if label_parts else ""

    if args.tax:
        tax = _tax_summary(filtered)
        if args.json:
            print(json.dumps(tax, indent=2))
        else:
            print(_format_tax(tax, label))
        return 0

    if args.pnl:
        pnl = _pnl(filtered)
        if args.json:
            print(json.dumps(pnl, indent=2))
        else:
            print(_format_pnl(pnl, label))
        return 0

    if args.by:
        groups = _group_by(filtered, args.by)
        if args.json:
            print(json.dumps(groups, indent=2))
        else:
            print(_format_table(groups, args.by))
        return 0

    pnl = _pnl(filtered)
    if args.json:
        output = {
            "pnl": pnl,
            "by_category": _group_by(filtered, "category"),
            "by_venture": _group_by(filtered, "venture"),
        }
        print(json.dumps(output, indent=2))
    else:
        print(_format_pnl(pnl, label))
        print()
        print(_format_table(_group_by(filtered, "category"), "category"))
        if not args.venture:
            print()
            print(_format_table(_group_by(filtered, "venture"), "venture"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
