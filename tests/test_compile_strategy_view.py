"""Tests for scripts/compile_strategy_view.py."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from compile_strategy_view import (
    RECIPE_ID,
    build_bundle,
    extract_machine_layer,
    expert_id_from_thread_path,
)

FIXTURE_NOTEBOOK = (
    Path(__file__).resolve().parent / "fixtures" / "compile_strategy_view" / "notebook"
)


def test_extract_machine_layer() -> None:
    text = "pre\n<!-- strategy-expert-thread:start -->\ninner\n<!-- strategy-expert-thread:end -->\n"
    assert extract_machine_layer(text) == "inner"


def test_expert_id_from_thread_path() -> None:
    nb = FIXTURE_NOTEBOOK
    p = nb / "experts" / "demo" / "thread.md"
    assert expert_id_from_thread_path(p, nb) == "demo"


def test_build_bundle_fixture(tmp_path: Path) -> None:
    out = tmp_path / "bundle.md"
    md = build_bundle(
        FIXTURE_NOTEBOOK,
        date(2026, 4, 1),
        expert_filter=None,
        inbox_tail_lines=20,
        max_journal_chars=8000,
        max_machine_chars=12000,
    )
    out.write_text(md, encoding="utf-8")
    assert RECIPE_ID in md
    assert "Derived artifact" in md
    assert "Fixture machine layer" in md
    assert "fixture-page" in md
    assert "Symphony Snapshot — 2026-04-01" in md
    assert "### `demo`" in md


def test_build_bundle_expert_filter_excludes() -> None:
    md = build_bundle(
        FIXTURE_NOTEBOOK,
        date(2026, 4, 1),
        expert_filter=frozenset({"other"}),
        inbox_tail_lines=5,
        max_journal_chars=1000,
        max_machine_chars=1000,
    )
    assert "### `demo`" not in md
    assert "Expert / voice threads (0 files)" in md
