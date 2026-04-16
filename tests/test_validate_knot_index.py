"""Tests for scripts/validate_knot_index.py."""

from __future__ import annotations

from pathlib import Path

from scripts.validate_knot_index import (
    REPO_ROOT,
    days_md_link_warnings,
    validate_knot_index_data,
)


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


def test_days_md_link_warning_when_basename_missing(tmp_path: Path) -> None:
    """Knot indexed but not mentioned in chapters/YYYY-MM/days.md."""
    nb = (
        tmp_path
        / "docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04"
    )
    knots_dir = nb / "knots"
    knots_dir.mkdir(parents=True)
    k = knots_dir / "strategy-notebook-knot-2026-04-13-absent-from-days.md"
    k.write_text("# k\n", encoding="utf-8")
    days = nb / "days.md"
    days.write_text("## 2026-04-13\n\nno knot link here\n", encoding="utf-8")
    rel = k.relative_to(tmp_path)
    data = {
        "schema_version": 3,
        "knots": [
            {
                "path": str(rel).replace("\\", "/"),
                "date": "2026-04-13",
                "knot_label": "absent-from-days",
            }
        ],
    }
    warns = days_md_link_warnings(data, repo_root=tmp_path)
    assert len(warns) == 1
    assert "not found" in warns[0]


def test_days_md_link_ok_when_basename_present(tmp_path: Path) -> None:
    nb = (
        tmp_path
        / "docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04"
    )
    knots_dir = nb / "knots"
    knots_dir.mkdir(parents=True)
    k = knots_dir / "strategy-notebook-knot-2026-04-13-linked.md"
    k.write_text("# k\n", encoding="utf-8")
    basename = k.name
    days = nb / "days.md"
    days.write_text(
        f"## 2026-04-13\n\n[{basename}](knots/{basename})\n",
        encoding="utf-8",
    )
    rel = k.relative_to(tmp_path)
    data = {
        "schema_version": 3,
        "knots": [
            {
                "path": str(rel).replace("\\", "/"),
                "date": "2026-04-13",
                "knot_label": "linked",
            }
        ],
    }
    warns = days_md_link_warnings(data, repo_root=tmp_path)
    assert warns == []


def test_weave_count_negative(tmp_path: Path) -> None:
    k = tmp_path / "strategy-notebook-knot-2026-04-13-test.md"
    k.write_text("# test\n", encoding="utf-8")
    errs = validate_knot_index_data(
        {
            "schema_version": 4,
            "knots": [
                {
                    "path": "strategy-notebook-knot-2026-04-13-test.md",
                    "date": "2026-04-13",
                    "weave_count": -1,
                }
            ],
        },
        repo_root=tmp_path,
    )
    assert any("weave_count" in e for e in errs)


def test_seam_integrity_out_of_range(tmp_path: Path) -> None:
    k = tmp_path / "strategy-notebook-knot-2026-04-13-test.md"
    k.write_text("# test\n", encoding="utf-8")
    errs = validate_knot_index_data(
        {
            "schema_version": 4,
            "knots": [
                {
                    "path": "strategy-notebook-knot-2026-04-13-test.md",
                    "date": "2026-04-13",
                    "seam_integrity": 1.5,
                }
            ],
        },
        repo_root=tmp_path,
    )
    assert any("seam_integrity" in e for e in errs)


def test_v4_optional_fields_ok(tmp_path: Path) -> None:
    k = tmp_path / "strategy-notebook-knot-2026-04-13-test.md"
    k.write_text("# test\n", encoding="utf-8")
    errs = validate_knot_index_data(
        {
            "schema_version": 4,
            "knots": [
                {
                    "path": "strategy-notebook-knot-2026-04-13-test.md",
                    "date": "2026-04-13",
                    "knot_label": "trial",
                    "weave_count": 2,
                    "seam_integrity": 0.75,
                    "qoi_check": True,
                    "kac_check": False,
                }
            ],
        },
        repo_root=tmp_path,
    )
    assert errs == []


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
