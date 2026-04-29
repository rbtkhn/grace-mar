"""Tests for scripts/build_external_codex_neighborhood.py."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_external_codex_neighborhood as becn  # noqa: E402

FIXED_TS = datetime(2026, 4, 27, 12, 0, 0, tzinfo=timezone.utc)


def test_resolve_rejects_traversal(tmp_path: Path) -> None:
    ck = tmp_path / "checkout"
    ck.mkdir()
    (ck / "a.txt").write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="traversal"):
        becn.resolve_subject_under_checkout(ck, "..")


def test_resolve_rejects_escape(tmp_path: Path) -> None:
    ck = tmp_path / "checkout"
    ck.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("x", encoding="utf-8")
    try:
        (ck / "link_out").symlink_to(outside)
    except OSError:
        pytest.skip("symlink not supported")
    with pytest.raises(ValueError, match="escapes"):
        becn.resolve_subject_under_checkout(ck, "link_out")


def test_neighbors_file_subject(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    ck_rel = "fake-checkout"
    ck = repo / ck_rel
    subdir = ck / "w" / "x"
    subdir.mkdir(parents=True)
    (subdir / "target.md").write_text("t", encoding="utf-8")
    (subdir / "sibling.md").write_text("s", encoding="utf-8")
    par = ck / "w"
    (par / "cousin.md").write_text("c", encoding="utf-8")

    report = becn.build_report(
        repo,
        ck_rel,
        "w/x/target.md",
        generated_at=FIXED_TS,
        include_checkout_absolute=False,
        neighbor_limit=50,
    )
    assert report["subject_kind"] == "file"
    assert report["truncated"] is False
    assert "likely_family" in report
    assert "suggested_next_inspection" in report
    by_path = {n["path_relative"]: n for n in report["neighbors"]}
    assert by_path["w/x/sibling.md"]["edge"] == "same_directory"
    assert by_path["w/cousin.md"]["edge"] == "parent_directory"
    assert "reason" in by_path["w/x/sibling.md"]
    assert "section" in by_path["w/x/sibling.md"]


def test_neighbors_directory_subject(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    ck_rel = "fake-checkout"
    ck = repo / ck_rel
    d = ck / "a" / "b"
    d.mkdir(parents=True)
    (d / "child.md").write_text("c", encoding="utf-8")
    (d.parent / "other.txt").write_text("o", encoding="utf-8")

    report = becn.build_report(
        repo,
        ck_rel,
        "a/b",
        generated_at=FIXED_TS,
        include_checkout_absolute=False,
        neighbor_limit=50,
    )
    assert report["subject_kind"] == "directory"
    paths = [n["path_relative"] for n in report["neighbors"]]
    assert "a/b/child.md" in paths


def test_truncation(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    ck_rel = "fc"
    ck = repo / ck_rel / "d"
    ck.mkdir(parents=True)
    for i in range(30):
        (ck / f"f{i}.txt").write_text("x", encoding="utf-8")
    (ck / "subj.txt").write_text("s", encoding="utf-8")

    report = becn.build_report(
        repo,
        ck_rel,
        "d/subj.txt",
        generated_at=FIXED_TS,
        include_checkout_absolute=False,
        neighbor_limit=5,
    )
    assert report["truncated"] is True
    assert len(report["neighbors"]) == 5


def test_main_writes_json(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    ck_rel = "fc"
    f = repo / ck_rel / "hello.txt"
    f.parent.mkdir(parents=True)
    f.write_text("hi", encoding="utf-8")
    out_dir = repo / "out"
    rc = becn.main(
        [
            "--repo-root",
            str(repo),
            "--checkout",
            ck_rel,
            "--subject",
            "hello.txt",
            "--out-dir",
            str(out_dir),
        ]
    )
    assert rc == 0
    jp = out_dir / "hello.txt.json"
    assert jp.is_file()
    data = json.loads(jp.read_text(encoding="utf-8"))
    assert data["report_type"] == "external_codex_neighborhood_report"
    assert data["schema_version"] == "v1"
    assert "likely_family" in data


def test_render_companion_markdown_stable_headings(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    ck_rel = "fc"
    ck = repo / ck_rel / "content" / "civilizations" / "X"
    ck.mkdir(parents=True)
    subj = ck / "CIV--STATE--X.md"
    subj.write_text("# Title One\n\nbody\n", encoding="utf-8")
    (ck / "MEM--X.md").write_text("x", encoding="utf-8")

    report = becn.build_report(
        repo,
        ck_rel,
        "content/civilizations/X/CIV--STATE--X.md",
        generated_at=FIXED_TS,
        include_checkout_absolute=False,
        neighbor_limit=50,
    )
    md = becn.render_companion_markdown(report)
    assert md.startswith("# External Codex Neighborhood Report\n")
    assert "## Subject\n" in md
    assert "## Likely family\n" in md
    assert "## Structural neighbors\n" in md
    assert "### Same civilization\n" in md
    assert "## Suggested next inspection targets\n" in md
    assert "## Notes\n" in md
    assert report["subject_title"] == "Title One"
    sug = report["suggested_next_inspection"]
    assert isinstance(sug, list) and len(sug) >= 1
    assert sug[0]["path_relative"] == "content/civilizations/X/MEM--X.md"


def test_render_empty_neighborhood(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    ck_rel = "fc"
    ck = repo / ck_rel
    ck.mkdir(parents=True)
    (ck / "only.txt").write_text("x", encoding="utf-8")

    report = becn.build_report(
        repo,
        ck_rel,
        "only.txt",
        generated_at=FIXED_TS,
        include_checkout_absolute=False,
        neighbor_limit=50,
    )
    assert report["neighbors"] == []
    md = becn.render_companion_markdown(report)
    assert "*No neighbors in this bucket.*" in md
    assert '*No suggestions (empty neighborhood).*' in md


def test_main_write_md_custom_paths(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    ck_rel = "fc"
    f = repo / ck_rel / "a.txt"
    f.parent.mkdir(parents=True)
    f.write_text("x", encoding="utf-8")
    jp = repo / "custom.json"
    mp = repo / "custom.md"
    rc = becn.main(
        [
            "--repo-root",
            str(repo),
            "--checkout",
            ck_rel,
            "--subject",
            "a.txt",
            "--write-md",
            "--output-json",
            str(jp),
            "--output-md",
            str(mp),
        ]
    )
    assert rc == 0
    assert jp.is_file()
    assert mp.is_file()
    assert "# External Codex Neighborhood Report" in mp.read_text(encoding="utf-8")


def test_main_output_md_without_write_md_errors(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    ck_rel = "fc"
    (repo / ck_rel / "a.txt").parent.mkdir(parents=True)
    (repo / ck_rel / "a.txt").write_text("x", encoding="utf-8")
    rc = becn.main(
        [
            "--repo-root",
            str(repo),
            "--checkout",
            ck_rel,
            "--subject",
            "a.txt",
            "--output-md",
            str(repo / "o.md"),
        ]
    )
    assert rc == 1
