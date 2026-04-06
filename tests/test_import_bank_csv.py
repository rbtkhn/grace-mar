#!/usr/bin/env python3
"""Tests for bank CSV Etsy descriptor matching and classification."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location("import_bank_csv", ROOT / "scripts" / "import_bank_csv.py")
assert _SPEC and _SPEC.loader
_ibc = importlib.util.module_from_spec(_SPEC)
sys.modules["import_bank_csv"] = _ibc
_SPEC.loader.exec_module(_ibc)


class TestIsEtsyBankDescriptor:
    @pytest.mark.parametrize(
        ("name", "memo", "expected"),
        [
            ("ELECTRONIC DEPOSIT ETSY INC.", "", True),
            ("DEBIT PURCHASE -VISA ETSY INC. 718-8557955 NY", "", True),
            ("RECURRING DEBIT PURCHASE Etsy.com*US 718-8557955 NY", "", True),
            ("ACH CREDIT", "ETSY PAYMENTS PAYOUT", True),
            ("ACH CREDIT", "MONTHLY ETSY PAYOUT REFERENCE", True),
            ("Some Corp", "ETSY DEPOSIT", True),
            ("ACH CREDIT", "ETSYINC SETTLEMENT", True),
            ("PERSONAL PAYMENT BETSY SMITH", "", False),
            ("ZELLE FROM JANE", "", False),
        ],
    )
    def test_patterns(self, name: str, memo: str, expected: bool) -> None:
        assert _ibc.is_etsy_bank_descriptor(name, memo) is expected


class TestClassifyMemo:
    def test_credit_memo_only_etsy_payments(self) -> None:
        cls = _ibc._classify("CREDIT", "ACH CREDIT", 100.0, "ETSY PAYMENTS WEEKLY")
        assert cls["account"] == "etsy_payments"
        assert cls["category"] == "revenue"

    def test_debit_memo_etsy_deposit_false_but_card_name(self) -> None:
        cls = _ibc._classify("DEBIT", "Etsy.com*US 718-8557955 NY", 10.0, "")
        assert cls["category"] == "platform_fees"
        assert cls["account"] == "credit_card"
