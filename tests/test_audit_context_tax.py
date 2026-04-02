"""Smoke tests for audit_context_tax (approximate paste footprint)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import audit_context_tax as act  # noqa: E402


def test_build_context_tax_report_has_blocks() -> None:
    r = act.build_context_tax_report(user_id="grace-mar")
    assert r["user_id"] == "grace-mar"
    assert "total_chars" in r and int(r["total_chars"]) > 0
    labels = {b["label"] for b in r["blocks"]}
    assert "session_tail" in labels
    assert "velocity_oneliner" in labels
