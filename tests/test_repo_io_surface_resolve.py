"""resolve_surface_markdown_path: canonical vs legacy stems and self_evidence pointer."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _scripts_on_path() -> None:
    p = str(REPO_ROOT / "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)


def test_self_skills_prefers_canonical_when_both_exist(tmp_path: Path) -> None:
    from repo_io import resolve_surface_markdown_path

    (tmp_path / "self-skills.md").write_text("canonical\n", encoding="utf-8")
    (tmp_path / "skills.md").write_text("legacy\n", encoding="utf-8")
    p = resolve_surface_markdown_path(tmp_path, "self_skills")
    assert p.name == "self-skills.md"


def test_self_skills_legacy_only(tmp_path: Path) -> None:
    from repo_io import resolve_surface_markdown_path

    (tmp_path / "skills.md").write_text("legacy\n", encoding="utf-8")
    p = resolve_surface_markdown_path(tmp_path, "self_skills")
    assert p.name == "skills.md"


def test_self_skills_returns_canonical_target_when_missing(tmp_path: Path) -> None:
    from repo_io import resolve_surface_markdown_path

    p = resolve_surface_markdown_path(tmp_path, "self_skills")
    assert p == tmp_path / "self-skills.md"


def test_self_evidence_archive_then_pointer(tmp_path: Path) -> None:
    from repo_io import resolve_surface_markdown_path

    (tmp_path / "self-archive.md").write_text("log\n", encoding="utf-8")
    (tmp_path / "self-evidence.md").write_text("pointer\n", encoding="utf-8")
    p = resolve_surface_markdown_path(tmp_path, "self_evidence")
    assert p.name == "self-archive.md"


def test_self_evidence_pointer_only(tmp_path: Path) -> None:
    from repo_io import resolve_surface_markdown_path

    (tmp_path / "self-evidence.md").write_text("pointer\n", encoding="utf-8")
    p = resolve_surface_markdown_path(tmp_path, "self_evidence")
    assert p.name == "self-evidence.md"


def test_self_knowledge_raises(tmp_path: Path) -> None:
    from repo_io import resolve_surface_markdown_path

    with pytest.raises(ValueError, match="no on-disk"):
        resolve_surface_markdown_path(tmp_path, "self_knowledge")
