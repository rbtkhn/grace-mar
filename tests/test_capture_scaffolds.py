"""Tests for capture scaffold scripts (non-canonical Markdown under artifacts/)."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def _mini_repo(tmp_path: Path) -> Path:
    root = tmp_path / "mini_repo"
    (root / "docs" / "templates").mkdir(parents=True)
    for name in (
        "work-note-template.md",
        "evidence-stub-template.md",
        "candidate-draft-template.md",
    ):
        shutil.copy2(REPO_ROOT / "docs" / "templates" / name, root / "docs" / "templates" / name)
    return root


def _run(script: str, *args: str, repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


def test_new_work_note_writes_under_output(tmp_path: Path) -> None:
    mini = _mini_repo(tmp_path)
    out = mini / "artifacts" / "work-notes"
    r = _run(
        "new_work_note.py",
        "--repo-root",
        str(mini),
        "--output",
        str(out),
        "--lane",
        "work-strategy",
        "--title",
        "Hello World Test",
        "--date",
        "2026-04-13",
        repo=mini,
    )
    assert r.returncode == 0, r.stderr
    written = Path(r.stdout.strip())
    assert written.exists()
    assert written.resolve().is_relative_to(mini.resolve())
    text = written.read_text(encoding="utf-8")
    assert "Date: 2026-04-13" in text
    assert "Lane: work-strategy" in text
    assert "Title: Hello World Test" in text


def test_new_evidence_stub_writes_under_output(tmp_path: Path) -> None:
    mini = _mini_repo(tmp_path)
    out = mini / "artifacts" / "evidence-stubs"
    r = _run(
        "new_evidence_stub.py",
        "--repo-root",
        str(mini),
        "--output",
        str(out),
        "--source",
        "session",
        "--type",
        "analysis",
        "--date",
        "2026-04-13",
        repo=mini,
    )
    assert r.returncode == 0, r.stderr
    written = Path(r.stdout.strip())
    assert written.exists()
    text = written.read_text(encoding="utf-8")
    assert "Date: 2026-04-13" in text
    assert "Source: session" in text
    assert "Type: analysis" in text


def test_new_candidate_draft_writes_under_output(tmp_path: Path) -> None:
    mini = _mini_repo(tmp_path)
    out = mini / "artifacts" / "candidate-drafts"
    r = _run(
        "new_candidate_draft.py",
        "--repo-root",
        str(mini),
        "--output",
        str(out),
        "--lane",
        "work-dev",
        "--target-surface",
        "SKILLS",
        "--title",
        "Add a skill stub",
        "--date",
        "2026-04-13",
        repo=mini,
    )
    assert r.returncode == 0, r.stderr
    written = Path(r.stdout.strip())
    assert written.exists()
    text = written.read_text(encoding="utf-8")
    assert "Date: 2026-04-13" in text
    assert "Lane: work-dev" in text
    assert "Target surface: SKILLS" in text
    assert "Title: Add a skill stub" in text


def test_rejects_output_outside_repo_root(tmp_path: Path) -> None:
    mini = _mini_repo(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    r = _run(
        "new_work_note.py",
        "--repo-root",
        str(mini),
        "--output",
        str(outside),
        "--lane",
        "x",
        "--title",
        "y",
        repo=mini,
    )
    assert r.returncode != 0
