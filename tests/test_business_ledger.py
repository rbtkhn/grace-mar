#!/usr/bin/env python3
"""
Tests for business ledger: schema, emit, summary, P&L, CLI.

Instance-specific (grace-mar). Not template-portable.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------

class TestSchema:
    @pytest.fixture
    def schema(self):
        return json.loads((ROOT / "schema-registry" / "business-transaction.v1.json").read_text())

    def test_required_fields(self, schema):
        expected = {"ts", "date", "description", "amount_usd", "type", "category", "venture"}
        assert expected == set(schema["required"])

    def test_type_enum(self, schema):
        assert set(schema["properties"]["type"]["enum"]) == {"income", "expense", "refund", "transfer"}

    def test_amount_is_number(self, schema):
        assert schema["properties"]["amount_usd"]["type"] == "number"

    def test_optional_fields_exist(self, schema):
        for field in ("account", "tax_category", "vendor_or_customer", "receipt_ref", "notes"):
            assert field in schema["properties"]


# ---------------------------------------------------------------------------
# Emit tests
# ---------------------------------------------------------------------------

class TestEmit:
    @pytest.fixture
    def ledger_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr("emit_business_transaction.REPO_ROOT", tmp_path)
        user_dir = tmp_path / "users" / "test-user"
        user_dir.mkdir(parents=True)
        return user_dir / "business-ledger.jsonl"

    def test_append_transaction_creates_file(self, ledger_file, monkeypatch):
        from emit_business_transaction import append_transaction
        monkeypatch.setattr("emit_business_transaction.REPO_ROOT", ledger_file.parent.parent.parent)

        row = append_transaction(
            "test-user",
            description="Test emerald",
            amount_usd=100.00,
            tx_type="income",
            category="revenue",
            venture="grace-gems",
        )
        assert ledger_file.exists()
        assert row["amount_usd"] == 100.00
        assert row["type"] == "income"
        assert row["venture"] == "grace-gems"

        lines = ledger_file.read_text().strip().splitlines()
        assert len(lines) == 1
        parsed = json.loads(lines[0])
        assert parsed["description"] == "Test emerald"

    def test_append_with_optional_fields(self, ledger_file, monkeypatch):
        from emit_business_transaction import append_transaction
        monkeypatch.setattr("emit_business_transaction.REPO_ROOT", ledger_file.parent.parent.parent)

        row = append_transaction(
            "test-user",
            transaction_date="2026-03-15",
            description="Gold findings",
            amount_usd=45.50,
            tx_type="expense",
            category="materials",
            venture="grace-gems",
            account="bank_checking",
            tax_category="cogs",
            vendor_or_customer="Rio Grande",
            receipt_ref="inv-2026-0042",
            notes="14k yellow gold jump rings",
        )
        assert row["date"] == "2026-03-15"
        assert row["account"] == "bank_checking"
        assert row["tax_category"] == "cogs"
        assert row["vendor_or_customer"] == "Rio Grande"
        assert row["receipt_ref"] == "inv-2026-0042"
        assert row["notes"] == "14k yellow gold jump rings"

    def test_multiple_appends(self, ledger_file, monkeypatch):
        from emit_business_transaction import append_transaction
        monkeypatch.setattr("emit_business_transaction.REPO_ROOT", ledger_file.parent.parent.parent)

        for i in range(3):
            append_transaction(
                "test-user",
                description=f"Transaction {i}",
                amount_usd=10.0 * (i + 1),
                tx_type="expense",
                category="materials",
                venture="grace-gems",
            )
        lines = ledger_file.read_text().strip().splitlines()
        assert len(lines) == 3

    def test_invalid_type_raises(self, ledger_file, monkeypatch):
        from emit_business_transaction import append_transaction
        monkeypatch.setattr("emit_business_transaction.REPO_ROOT", ledger_file.parent.parent.parent)

        with pytest.raises(ValueError, match="Invalid type"):
            append_transaction(
                "test-user",
                description="Bad",
                amount_usd=10.0,
                tx_type="invalid",
                category="revenue",
                venture="test",
            )

    def test_negative_amount_raises(self, ledger_file, monkeypatch):
        from emit_business_transaction import append_transaction
        monkeypatch.setattr("emit_business_transaction.REPO_ROOT", ledger_file.parent.parent.parent)

        with pytest.raises(ValueError, match="non-negative"):
            append_transaction(
                "test-user",
                description="Bad",
                amount_usd=-5.0,
                tx_type="expense",
                category="materials",
                venture="test",
            )

    def test_amount_rounded(self, ledger_file, monkeypatch):
        from emit_business_transaction import append_transaction
        monkeypatch.setattr("emit_business_transaction.REPO_ROOT", ledger_file.parent.parent.parent)

        row = append_transaction(
            "test-user",
            description="Rounding test",
            amount_usd=12.345,
            tx_type="expense",
            category="materials",
            venture="grace-gems",
        )
        assert row["amount_usd"] == 12.35


# ---------------------------------------------------------------------------
# Summary tests
# ---------------------------------------------------------------------------

class TestSummary:
    @pytest.fixture
    def populated_ledger(self, tmp_path, monkeypatch):
        monkeypatch.setattr("business_ledger_summary.REPO_ROOT", tmp_path)
        user_dir = tmp_path / "users" / "test-user"
        user_dir.mkdir(parents=True)
        ledger = user_dir / "business-ledger.jsonl"

        rows = [
            {"ts": "2026-01-15T10:00:00Z", "date": "2026-01-15", "description": "Ring sale",
             "amount_usd": 300.0, "type": "income", "category": "revenue", "venture": "grace-gems",
             "tax_category": "sales_revenue"},
            {"ts": "2026-01-20T10:00:00Z", "date": "2026-01-20", "description": "Emerald purchase",
             "amount_usd": 80.0, "type": "expense", "category": "materials", "venture": "grace-gems",
             "tax_category": "cogs"},
            {"ts": "2026-02-01T10:00:00Z", "date": "2026-02-01", "description": "Etsy fees",
             "amount_usd": 25.0, "type": "expense", "category": "platform_fees", "venture": "grace-gems",
             "tax_category": "business_expense"},
            {"ts": "2026-02-10T10:00:00Z", "date": "2026-02-10", "description": "Pendant sale",
             "amount_usd": 150.0, "type": "income", "category": "revenue", "venture": "grace-gems",
             "tax_category": "sales_revenue"},
            {"ts": "2026-02-15T10:00:00Z", "date": "2026-02-15", "description": "Customer refund",
             "amount_usd": 50.0, "type": "refund", "category": "refund_issued", "venture": "grace-gems",
             "tax_category": "refund"},
        ]
        with ledger.open("w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        return ledger

    def test_pnl(self, populated_ledger):
        from business_ledger_summary import _load_rows, _pnl
        rows = _load_rows("test-user")
        pnl = _pnl(rows)
        assert pnl["total_income"] == 450.0
        assert pnl["total_expense"] == 105.0
        assert pnl["total_refund"] == 50.0
        assert pnl["gross_profit"] == 295.0
        assert pnl["transaction_count"] == 5

    def test_group_by_category(self, populated_ledger):
        from business_ledger_summary import _load_rows, _group_by
        rows = _load_rows("test-user")
        groups = _group_by(rows, "category")
        assert "revenue" in groups
        assert groups["revenue"]["income"] == 450.0
        assert "materials" in groups
        assert groups["materials"]["expense"] == 80.0
        assert "platform_fees" in groups

    def test_group_by_tax_category(self, populated_ledger):
        from business_ledger_summary import _load_rows, _group_by
        rows = _load_rows("test-user")
        groups = _group_by(rows, "tax_category")
        assert "sales_revenue" in groups
        assert groups["sales_revenue"]["income"] == 450.0
        assert "cogs" in groups
        assert groups["cogs"]["expense"] == 80.0

    def test_filter_by_date(self, populated_ledger):
        from business_ledger_summary import _load_rows, _filter_rows, _pnl
        rows = _load_rows("test-user")
        filtered = _filter_rows(rows, since="2026-02-01")
        pnl = _pnl(filtered)
        assert pnl["total_income"] == 150.0
        assert pnl["total_expense"] == 25.0
        assert pnl["transaction_count"] == 3

    def test_filter_by_venture(self, populated_ledger):
        from business_ledger_summary import _load_rows, _filter_rows
        rows = _load_rows("test-user")
        filtered = _filter_rows(rows, venture="grace-gems")
        assert len(filtered) == 5
        filtered_other = _filter_rows(rows, venture="nonexistent")
        assert len(filtered_other) == 0

    def test_empty_ledger(self, tmp_path, monkeypatch):
        monkeypatch.setattr("business_ledger_summary.REPO_ROOT", tmp_path)
        from business_ledger_summary import _load_rows
        rows = _load_rows("nobody")
        assert rows == []


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------

class TestCLI:
    def test_emit_cli(self, tmp_path):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "emit_business_transaction.py"),
             "-u", "cli-test",
             "--venture", "test-venture",
             "--type", "expense",
             "--amount", "19.99",
             "--category", "materials",
             "--description", "Test CLI transaction",
             "--json"],
            capture_output=True, text=True,
            cwd=str(ROOT),
        )
        assert result.returncode == 0
        row = json.loads(result.stdout)
        assert row["amount_usd"] == 19.99
        assert row["venture"] == "test-venture"

    def test_summary_cli_no_data(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "business_ledger_summary.py"),
             "-u", "nonexistent-user", "--pnl"],
            capture_output=True, text=True,
            cwd=str(ROOT),
        )
        assert result.returncode == 0
        assert "No transactions" in result.stderr

    def test_emit_missing_required_args(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "emit_business_transaction.py")],
            capture_output=True, text=True,
            cwd=str(ROOT),
        )
        assert result.returncode != 0
