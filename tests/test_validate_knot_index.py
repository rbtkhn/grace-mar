"""Tests for scripts/validate_knot_index.py."""

from __future__ import annotations

from pathlib import Path

from scripts.validate_knot_index import REPO_ROOT, validate_knot_index_data


def test_empty_knots_ok() -> None:
    errs = validate_knot_index_data(
        {"schema_version": 3, "knots": []},
        repo_root=REPO_ROOT,
    )
    assert errs == []


def test_knot_label_kebab_invalid() -> None:
    errs = validate_knot_index_data(
        {
            "schema_version": 3,
            "knots": [
                {
                    "path": "docs/skill-work/work-strategy/strategy-notebook/knot-index.yaml",
                    "date": "2026-04-13",
                    "knot_label": "Bad_Case",
                }
            ],
        },
        repo_root=REPO_ROOT,
    )
    assert any("knot_label" in e for e in errs)


def test_knot_label_kebab_valid(tmp_path: Path) -> None:
    k = tmp_path / "strategy-notebook-knot-2026-04-13-test.md"
    k.write_text("# test\n", encoding="utf-8")
    rel = k.relative_to(tmp_path)
    errs = validate_knot_index_data(
        {
            "schema_version": 3,
            "knots": [
                {
                    "path": str(rel).replace("\\", "/"),
                    "date": "2026-04-13",
                    "knot_label": "tri-mind",
                }
            ],
        },
        repo_root=tmp_path,
    )
    assert errs == []


def test_duplicate_date_knot_label(tmp_path: Path) -> None:
    a = tmp_path / "strategy-notebook-knot-2026-04-13-a.md"
    b = tmp_path / "strategy-notebook-knot-2026-04-13-b.md"
    a.write_text("# a\n", encoding="utf-8")
    b.write_text("# b\n", encoding="utf-8")
    errs = validate_knot_index_data(
        {
            "schema_version": 3,
            "knots": [
                {
                    "path": "strategy-notebook-knot-2026-04-13-a.md",
                    "date": "2026-04-13",
                    "knot_label": "same",
                },
                {
                    "path": "strategy-notebook-knot-2026-04-13-b.md",
                    "date": "2026-04-13",
                    "knot_label": "same",
                },
            ],
        },
        repo_root=tmp_path,
    )
    assert any("duplicate (date, knot_label)" in e for e in errs)


def test_deprecated_weave_label_unknown_key(tmp_path: Path) -> None:
    k = tmp_path / "strategy-notebook-knot-2026-04-13-test.md"
    k.write_text("# test\n", encoding="utf-8")
    errs = validate_knot_index_data(
        {
            "schema_version": 3,
            "knots": [
                {
                    "path": "strategy-notebook-knot-2026-04-13-test.md",
                    "date": "2026-04-13",
                    "weave_label": "tri-mind",
                }
            ],
        },
        repo_root=tmp_path,
    )
    assert any("unknown keys" in e and "weave_label" in e for e in errs)


def test_basename_must_contain_knot(tmp_path: Path) -> None:
    p = tmp_path / "rope-2026-04-13.md"
    p.write_text("# x\n", encoding="utf-8")
    errs = validate_knot_index_data(
        {
            "schema_version": 3,
            "knots": [
                {"path": "rope-2026-04-13.md", "date": "2026-04-13"},
            ],
        },
        repo_root=tmp_path,
    )
    assert any("knot" in e.lower() for e in errs)
