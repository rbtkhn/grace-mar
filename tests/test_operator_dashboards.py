"""Tests for operator dashboard generators (derived artifacts)."""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_review_dashboard import _pending_structs, _processed_structs  # noqa: E402
from operator_dashboard_common import extract_yaml_scalar, load_self_library_entries  # noqa: E402


def test_extract_yaml_scalar() -> None:
    blob = 'status: pending\nsummary: "Hello | world"\n'
    assert extract_yaml_scalar(blob, "status") == "pending"
    assert "Hello" in (extract_yaml_scalar(blob, "summary") or "")


def test_pending_structs_finds_pending_anywhere() -> None:
    gate = textwrap.dedent(
        """
        ## Processed
        ### CANDIDATE-0001 (t)
        ```yaml
        status: pending
        mind_category: knowledge
        summary: x
        ```
        """
    )
    p = _pending_structs(gate)
    assert len(p) == 1
    assert p[0]["id"] == "CANDIDATE-0001"


def test_processed_structs() -> None:
    tail = textwrap.dedent(
        """
        ### CANDIDATE-0002 (t)
        ```yaml
        status: approved
        summary: done
        ```
        """
    )
    pr = _processed_structs(tail)
    assert len(pr) == 1
    assert pr[0]["status"] == "approved"


def test_load_self_library_entries_minimal(tmp_path: Path) -> None:
    user = "u1"
    (tmp_path / "users" / user).mkdir(parents=True)
    (tmp_path / "users" / user / "self-library.md").write_text(
        textwrap.dedent(
            """
            # L
            ## Entries

            ```yaml
            entries:
              - id: LIB-0001
                title: "T"
                lane: reference
                type: book
                status: active
                engagement_status: planned
                source: manual
                added_at: 2026-01-01
            ```
            """
        ),
        encoding="utf-8",
    )
    rows = load_self_library_entries(tmp_path, user)
    assert len(rows) == 1
    assert rows[0]["id"] == "LIB-0001"
