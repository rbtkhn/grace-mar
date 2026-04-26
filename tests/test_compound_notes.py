"""Unit tests for scripts/work_dev/compound_notes.py (stdlib note parsing)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def cn():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from work_dev import compound_notes

    return compound_notes


def test_gate_candidate_truthy(cn) -> None:
    t = cn.gate_candidate_truthy
    assert t(True) is True
    assert t(False) is False
    assert t(None) is False
    assert t("") is False
    assert t("true") is True
    assert t("true ") is True
    assert t("yes") is True
    assert t("Y") is True
    assert t("y") is True
    assert t("1") is True
    assert t("no") is False
    assert t("false") is False


def test_parse_front_matter_minimal(cn) -> None:
    text = """---
date: 2026-01-15
title: "Hello"
gate_candidate: true
---
Body here.
"""
    m = cn.parse_front_matter(text)
    assert m.get("date") == "2026-01-15"
    assert m.get("title") == "Hello"
    assert m.get("gate_candidate") is True


def test_parse_front_matter_affected_files_list(cn) -> None:
    text = """---
title: t
affected_files:
  - foo/bar.py
  - baz.md
---
"""
    m = cn.parse_front_matter(text)
    assert m.get("affected_files") == ["foo/bar.py", "baz.md"]


def test_body_after_front_matter(cn) -> None:
    text = """---
k: v
---
First line
Second
"""
    assert cn.body_after_front_matter(text).rstrip("\n") == "First line\nSecond"


def test_extract_h2_section(cn) -> None:
    body = """# ignore

## Reusable lesson

Line one

## Next section

Gone
"""
    assert cn.extract_h2_section(body, "Reusable lesson") == "Line one"
    # Case-sensitive: no match
    assert cn.extract_h2_section(body, "reusable lesson") == ""


def test_load_note_file_path_and_source_path(tmp_path: Path, cn) -> None:
    p = tmp_path / "note.md"
    p.write_text(
        """---
title: T
date: 2026-01-01
gate_candidate: yes
---
## Reusable lesson

Hi
""",
        encoding="utf-8",
    )
    d = cn.load_note_file(p, repo_root=tmp_path)
    assert d["path"] == "note.md"
    assert d["source_path"] == "note.md"
    assert d["name"] == "note.md"
    assert d["meta"].get("title") == "T"
    assert "Hi" in d["body"]


def test_parse_note_for_export_flags_gate_candidate(tmp_path: Path, cn) -> None:
    p = tmp_path / "g.md"
    p.write_text(
        """---
title: "X"
date: 2020-01-01
gate_candidate: true
---
""",
        encoding="utf-8",
    )
    r = cn.parse_note_for_export(p, repo_root=tmp_path)
    assert r.get("path") == "g.md"
    assert r.get("gate_candidate") is True
    assert r.get("date") == "2020-01-01"
