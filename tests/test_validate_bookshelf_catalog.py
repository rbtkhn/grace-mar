"""Tests for scripts/validate_bookshelf_catalog.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "validate_bookshelf_catalog.py"
CATALOG = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "bookshelf-catalog.yaml"
)
HN_ARCH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "book-architecture.yaml"
)


def test_committed_catalog_validates() -> None:
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--catalog", str(CATALOG), "--architecture", str(HN_ARCH)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout


def test_unknown_hn_chapter_fails(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        """version: 1
items:
  - id: HNSRC-0999
    title: "X"
    author: "Y"
    era: ancient
    candidate_hn_chapters: [hn-i-v1-01, hn-i-v1-99-nonexistent]
""",
        encoding="utf-8",
    )
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--catalog", str(bad), "--architecture", str(HN_ARCH)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1
    assert "unknown hn chapter" in r.stderr.lower() or "hn-i-v1-99" in r.stderr


def test_eras_must_include_primary_era(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        """version: 1
items:
  - id: HNSRC-0998
    title: "X"
    author: "Y"
    era: medieval
    eras: [ancient]
    candidate_hn_chapters: []
""",
        encoding="utf-8",
    )
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--catalog", str(bad), "--architecture", str(HN_ARCH)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1
    assert "must be included in eras" in r.stderr


def test_redundant_single_eras_warns_in_strict(tmp_path: Path) -> None:
    bad = tmp_path / "warn.yaml"
    bad.write_text(
        """version: 1
items:
  - id: HNSRC-0997
    title: "X"
    author: "Y"
    era: ancient
    eras: [ancient]
    candidate_hn_chapters: []
""",
        encoding="utf-8",
    )
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--catalog",
            str(bad),
            "--architecture",
            str(HN_ARCH),
            "--strict",
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1
    assert "drop eras" in r.stderr.lower() or "eras" in r.stderr.lower()
