"""Tests for scripts/build_external_codex_family_report.py."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_external_codex_family_report as becf  # noqa: E402

FIXED_TS = datetime(2026, 4, 27, 12, 0, 0, tzinfo=timezone.utc)


def test_civilization_selector_two_siblings_connection(tmp_path: Path) -> None:
    ck = tmp_path / "checkout"
    base = ck / "content" / "civilizations" / "ROME"
    base.mkdir(parents=True)
    (base / "a.md").write_text("# A\n", encoding="utf-8")
    (base / "b.md").write_text("# B\n", encoding="utf-8")

    r = becf.build_family_report(
        tmp_path,
        ck,
        "civilization",
        "ROME",
        generated_at=FIXED_TS,
    )
    assert r["member_count"] == 2
    assert r["truncated"] is False
    by_path = {str(m["path"]): m["connection_count"] for m in r["members"]}
    assert by_path["content/civilizations/ROME/a.md"] == 1
    assert by_path["content/civilizations/ROME/b.md"] == 1


def test_file_class_selector(tmp_path: Path) -> None:
    ck = tmp_path / "co"
    d1 = ck / "content" / "civilizations" / "PARIS"
    d1.mkdir(parents=True)
    (d1 / "MEM--STATE.md").write_text("# State\n", encoding="utf-8")
    nested = d1 / "inner"
    nested.mkdir()
    (nested / "MEM--OTHER.md").write_text("# Other\n", encoding="utf-8")

    r = becf.build_family_report(
        tmp_path,
        ck,
        "file_class",
        "memory_spine",
        generated_at=FIXED_TS,
    )
    assert r["member_count"] == 2
    assert all(m["file_class"] == "memory_spine" for m in r["members"])


def test_suggested_entry_points_tie_break_lex(tmp_path: Path) -> None:
    """Three spine files in one folder: equal connection counts; paths sort lexically."""
    ck = tmp_path / "flat"
    base = ck / "content" / "civilizations" / "FLAT"
    base.mkdir(parents=True)
    (base / "MEM--c.md").write_text("# C\n", encoding="utf-8")
    (base / "MEM--a.md").write_text("# A\n", encoding="utf-8")
    (base / "MEM--b.md").write_text("# B\n", encoding="utf-8")

    r = becf.build_family_report(
        tmp_path,
        ck,
        "file_class",
        "memory_spine",
        generated_at=FIXED_TS,
    )
    assert r["member_count"] == 3
    for m in r["members"]:
        assert m["connection_count"] == 2
    sug_paths = [str(x["path"]) for x in r["suggested_entry_points"]]
    assert sug_paths[0] == "content/civilizations/FLAT/MEM--a.md"


def test_empty_cluster(tmp_path: Path) -> None:
    ck = tmp_path / "empty_co"
    ck.mkdir()
    (ck / "readme.txt").write_text("x", encoding="utf-8")

    r = becf.build_family_report(
        tmp_path,
        ck,
        "civilization",
        "NOMATCH",
        generated_at=FIXED_TS,
    )
    assert r["member_count"] == 0
    assert r["members"] == []
    assert r["suggested_entry_points"] == []
    md = becf.render_family_markdown(r)
    assert "# External Codex Family Report" in md
    assert "Empty cluster" in md or "empty cluster" in md.lower()


def test_report_id_stable(tmp_path: Path) -> None:
    ck = tmp_path / "ck"
    xd = ck / "content" / "civilizations" / "X"
    xd.mkdir(parents=True)
    (xd / "f.md").write_text("# F\n", encoding="utf-8")

    a = becf.build_family_report(tmp_path, ck, "civilization", "X", generated_at=FIXED_TS)
    b = becf.build_family_report(tmp_path, ck, "civilization", "X", generated_at=FIXED_TS)
    assert a["report_id"] == b["report_id"]


def test_markdown_stable_headings(tmp_path: Path) -> None:
    ck = tmp_path / "c2"
    ck.mkdir()
    r = becf.build_family_report(tmp_path, ck, "file_class", "other", generated_at=FIXED_TS)
    md = becf.render_family_markdown(r)
    assert md.startswith("# External Codex Family Report\n")
    assert "## Selector" in md
    assert "## Summary" in md
    assert "## Suggested entry points" in md
    assert "## Most connected members" in md
    assert "## Members" in md
    assert "## Notes" in md


def test_passes_selector_rejects_unknown_type() -> None:
    with pytest.raises(ValueError, match="unsupported"):
        becf.passes_selector("p/a", "f", "bad_type", "x")


def test_example_fixture_matches_schema(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parent.parent
    example = repo_root / "artifacts" / "external-codex" / "examples" / "family-fixture.v1.json"
    if not example.is_file():
        pytest.skip("family-fixture.v1.json not committed")
    data = json.loads(example.read_text(encoding="utf-8"))
    assert data["report_type"] == "external_codex_family_report"
    assert data["schema_version"] == "v1"
