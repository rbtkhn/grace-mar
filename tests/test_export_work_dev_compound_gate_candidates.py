"""Unit tests for export_work_dev_compound_gate_candidates build_markdown."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def build_markdown_mod():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import export_work_dev_compound_gate_candidates as m

    return m


def test_build_markdown_includes_h2_in_blocks(build_markdown_mod) -> None:
    bm = build_markdown_mod.build_markdown
    rec: dict[str, Any] = {
        "title": "One",
        "name": "one.md",
        "path": "x/one.md",
        "date": "2025-06-01",
        "source_pr": "",
        "source_commit": "",
        "affected_files": ["a/b.py"],
        "problem_type": "p",
        "reusable_pattern": "pat",
        "self_catching_test": "yes",
        "gate_candidate": True,
        "body": """## Reusable lesson

The lesson

## Gate recommendation

Ship it
""",
        "meta": {"reusable_pattern": "pat", "gate_candidate": True},
    }
    out = bm([rec], include_all=False, empty_reason=None)
    assert "recordAuthority: none" in out
    assert "artifact_kind: work_dev_compound_gate_export" in out
    assert "**Candidate:** One" in out
    assert "The lesson" in out
    assert "Ship it" in out
    assert "`a/b.py`" in out


def test_build_markdown_no_gate_candidates_status(build_markdown_mod) -> None:
    bm = build_markdown_mod.build_markdown
    rec: dict[str, Any] = {
        "title": "No gate",
        "path": "n.md",
        "date": "2025-01-01",
        "source_pr": "",
        "source_commit": "",
        "affected_files": [],
        "problem_type": "",
        "reusable_pattern": "",
        "self_catching_test": "unknown",
        "gate_candidate": False,
        "body": "",
        "meta": {"gate_candidate": False},
    }
    out = bm([rec], include_all=False, empty_reason=None)
    assert "## Status" in out
    assert "No `gate_candidate`" in out
    assert out.count("**Candidate:**") == 0


def test_build_markdown_sorts_by_date_then_title(build_markdown_mod) -> None:
    bm = build_markdown_mod.build_markdown
    a: dict[str, Any] = {
        "title": "Later",
        "name": "l.md",
        "path": "l.md",
        "date": "2025-12-01",
        "source_pr": "",
        "source_commit": "",
        "affected_files": [],
        "problem_type": "",
        "reusable_pattern": "",
        "self_catching_test": "unknown",
        "gate_candidate": True,
        "body": "",
        "meta": {"gate_candidate": True},
    }
    b: dict[str, Any] = {
        "title": "Earlier",
        "name": "e.md",
        "path": "e.md",
        "date": "2020-01-01",
        "source_pr": "",
        "source_commit": "",
        "affected_files": [],
        "problem_type": "",
        "reusable_pattern": "",
        "self_catching_test": "unknown",
        "gate_candidate": True,
        "body": "",
        "meta": {"gate_candidate": True},
    }
    out = bm([a, b], include_all=False, empty_reason=None)
    pos_b = out.index("**Candidate:** Earlier")
    pos_a = out.index("**Candidate:** Later")
    assert pos_b < pos_a
