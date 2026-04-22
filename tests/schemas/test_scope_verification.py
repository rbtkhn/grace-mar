"""Unit tests for scope_verification helpers (runtime-only)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT / "scripts" / "runtime") not in sys.path:
    sys.path.insert(0, str(_ROOT / "scripts" / "runtime"))
from scope_verification import (  # noqa: E402
    build_scope_verification_block,
    compute_coverage_status,
    parse_stated_file_count_from_proposal,
)


def test_parse_files_listed_line() -> None:
    body = "x\n\n- **files listed:** 8 (cap 10)\n"
    n, src = parse_stated_file_count_from_proposal(body)
    assert n == 8
    assert src == "proposal_regex"


def test_parse_absent() -> None:
    n, src = parse_stated_file_count_from_proposal("no numbers here")
    assert n is None
    assert src == "absent"


def test_aligned() -> None:
    r, st, w = compute_coverage_status(
        files_opened=8, files_seen=8, files_claimed=8, stated_source="proposal_regex"
    )
    assert r == 1.0
    assert st == "aligned"
    assert w == []


def test_overclaim() -> None:
    r, st, w = compute_coverage_status(
        files_opened=3, files_seen=10, files_claimed=99, stated_source="proposal_regex"
    )
    assert st == "overclaim_suspected"
    assert r == round(3 / 99, 3)
    assert w


def test_build_block_smoke() -> None:
    body = "- **files listed:** 5 (cap)\n"
    out = build_scope_verification_block(
        files_seen=5,
        rel_paths=["a/b.md"],
        files_opened=5,
        chunks_read=5,
        proposal_body=body,
        base_warnings=[],
    )
    assert out["traversal"]["files_seen"] == 5
    assert out["stated_coverage"]["files_claimed"] == 5
    assert out["status"] == "aligned"
