#!/usr/bin/env python3
"""
Import a US Bank checking CSV into business-ledger.jsonl.

Instance-specific (grace-mar). Not template-portable.

Usage:
  python3 scripts/import_bank_csv.py \
    --csv "/path/to/Checking - 0889_01-01-2025_12-31-2025.csv" \
    --venture grace-gems

  python3 scripts/import_bank_csv.py --csv /path/to.csv --venture grace-gems --dry-run

  python3 scripts/import_bank_csv.py -u grace-mar --audit-etsy --venture grace-gems --year 2025
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


def _bank_text_blob(name: str, memo: str = "") -> str:
    """Normalize name + memo for pattern matching (whitespace-collapsed, upper)."""
    parts = [name or "", memo or ""]
    return " ".join(" ".join(parts).upper().split())


def is_etsy_bank_descriptor(name: str, memo: str = "") -> bool:
    """
    True if bank Name/Memo text indicates Etsy payouts or Etsy card charges.

    Covers common US Bank / Visa strings and variants where only part of the
    descriptor mentions Etsy (memo-only hits, ETSY.COM*, ETSY PAYMENTS, etc.).
    """
    u = _bank_text_blob(name, memo)
    if "ETSY" not in u:
        return False
    if re.search(r"ETSY\s*INC\.?", u):
        return True
    if "ETSY.COM" in u:
        return True
    if "ETSY PAYMENTS" in u or "ETSY PAYOUT" in u or "ETSY DEPOSIT" in u:
        return True
    if re.search(r"ETSY\s*\*", u):
        return True
    if re.search(r"(?<![A-Z0-9])ETSYINC(?![A-Z0-9])", u):
        return True
    return False


def _classify(tx_type: str, name: str, amount: float, memo: str = "") -> dict[str, str]:
    """Return category, tax_category, and account based on transaction name + memo patterns."""
    name_upper = name.upper()

    if tx_type == "CREDIT":
        if is_etsy_bank_descriptor(name, memo):
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
    if is_etsy_bank_descriptor(name, memo):
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


def _extract_counterparty(name: str, memo: str = "") -> str | None:
    """Try to extract a meaningful counterparty name."""
    if is_etsy_bank_descriptor(name, memo):
        return "Etsy Inc."
    name_upper = name.upper()
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

            cls = _classify(tx_type, name, amount, memo)

            ledger_type = "income" if tx_type == "CREDIT" else "expense"
            if cls["category"] == "transfer":
                ledger_type = "transfer"

            counterparty = _extract_counterparty(name, memo)

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


def _ledger_tagged_as_etsy(row: dict[str, Any]) -> bool:
    """How existing rows mark Etsy (importer output or consistent manual rows)."""
    if row.get("vendor_or_customer") == "Etsy Inc.":
        return True
    if row.get("account") == "etsy_payments":
        return True
    desc_u = (row.get("description") or "").upper()
    if row.get("type") == "expense" and row.get("category") == "platform_fees" and "ETSY" in desc_u:
        return True
    return False


def run_etsy_audit(
    ledger_path: Path,
    *,
    venture: str | None,
    year: int | None,
) -> int:
    """Print Etsy detector vs ledger tags; return 0."""
    if not ledger_path.is_file():
        print(f"Ledger not found: {ledger_path}", file=sys.stderr)
        return 1

    rows: list[dict[str, Any]] = []
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))

    filt: list[dict[str, Any]] = []
    for r in rows:
        if venture and r.get("venture") != venture:
            continue
        d = r.get("date") or ""
        if year is not None and not d.startswith(f"{year}-"):
            continue
        filt.append(r)

    det_inc = det_exp = 0.0
    tag_inc = tag_exp = 0.0
    detected_not_tagged: list[dict[str, Any]] = []
    tagged_not_detected: list[dict[str, Any]] = []

    for r in filt:
        desc = r.get("description") or ""
        note = r.get("notes") or ""
        detected = is_etsy_bank_descriptor(desc, note)
        tagged = _ledger_tagged_as_etsy(r)
        amt = float(r["amount_usd"])
        t = r.get("type")
        if detected:
            if t == "income":
                det_inc += amt
            elif t == "expense":
                det_exp += amt
        if tagged:
            if t == "income":
                tag_inc += amt
            elif t == "expense":
                tag_exp += amt
        if detected and not tagged:
            detected_not_tagged.append(r)
        if tagged and not detected:
            tagged_not_detected.append(r)

    print("Etsy audit (descriptor vs ledger tags)")
    print(f"  Ledger: {ledger_path}")
    print(f"  Filter: venture={venture!r} year={year}")
    print(f"  Rows in filter: {len(filt)}")
    print()
    print("  Detector (name+notes) — income sum / expense sum / net:")
    print(f"    ${det_inc:,.2f}  /  ${det_exp:,.2f}  /  ${det_inc - det_exp:,.2f}")
    print("  Ledger tags (vendor Etsy, account etsy_payments, or platform_fees+ETSY in desc):")
    print(f"    ${tag_inc:,.2f}  /  ${tag_exp:,.2f}  /  ${tag_inc - tag_exp:,.2f}")
    print()
    if detected_not_tagged:
        print(f"  Detected but not tagged as Etsy ({len(detected_not_tagged)}) — review for backfill:")
        for r in detected_not_tagged[:25]:
            print(
                f"    {r.get('date')}  {r.get('type'):<8} ${r.get('amount_usd'):>10,.2f}  "
                f"{(r.get('description') or '')[:70]}"
            )
        if len(detected_not_tagged) > 25:
            print(f"    ... and {len(detected_not_tagged) - 25} more")
        print()
    else:
        print("  Detected but not tagged: 0")
        print()
    if tagged_not_detected:
        print(f"  Tagged but not detected ({len(tagged_not_detected)}) — legacy wording?")
        for r in tagged_not_detected[:15]:
            print(
                f"    {r.get('date')}  {r.get('type'):<8} ${r.get('amount_usd'):>10,.2f}  "
                f"{(r.get('description') or '')[:70]}"
            )
        print()
    # Etsy Payments CSV / seller hub "residual" check (deposits ≈ net sales − fees − marketing − shipping)
    print(
        "  Cross-check: Etsy annual summary net sales minus fees, marketing, and shipping "
        "should approximate bank deposits (timing and credits widen the gap)."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Import bank CSV into business ledger.")
    parser.add_argument("--csv", help="Path to the bank CSV file")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--venture", help="Venture slug (e.g. grace-gems); required for import")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument(
        "--audit-etsy",
        action="store_true",
        help="Scan business-ledger.jsonl: Etsy descriptor vs tags (use --venture / --year)",
    )
    parser.add_argument("--year", type=int, help="Limit audit to YYYY (transaction date prefix)")
    args = parser.parse_args()

    ledger_path = REPO_ROOT / "users" / args.user / "business-ledger.jsonl"

    if args.audit_etsy:
        return run_etsy_audit(ledger_path, venture=args.venture, year=args.year)

    if not args.csv:
        print("Import requires --csv (or use --audit-etsy).", file=sys.stderr)
        return 1
    if not args.venture:
        print("Import requires --venture.", file=sys.stderr)
        return 1

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

        ev = [r for r in rows if r.get("vendor_or_customer") == "Etsy Inc."]
        ei = sum(r["amount_usd"] for r in ev if r["type"] == "income")
        ee = sum(r["amount_usd"] for r in ev if r["type"] == "expense")
        print(f"  Etsy (vendor_or_customer=Etsy Inc.): income ${ei:>12,.2f}  expense ${ee:>12,.2f}  net ${ei - ee:>12,.2f}")
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
