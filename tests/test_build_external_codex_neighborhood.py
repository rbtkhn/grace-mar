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
    edges = {n["path_relative"]: n["edge"] for n in report["neighbors"]}
    assert edges["w/x/sibling.md"] == "same_directory"
    assert edges["w/cousin.md"] == "parent_directory"


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
