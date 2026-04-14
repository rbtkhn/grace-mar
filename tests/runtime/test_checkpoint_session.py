"""Tests for scripts/runtime/checkpoint_session.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "runtime" / "checkpoint_session.py"


def test_checkpoint_session_subprocess(tmp_path: Path) -> None:
    out = tmp_path / "artifacts" / "handoffs" / "checkpoints"
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(tmp_path),
            "--lane",
            "work-strategy",
            "--title",
            "Test checkpoint",
            "--gate-relevance",
            "maybe later",
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    files = list(out.glob("*.md"))
    assert len(files) == 1
    text = files[0].read_text(encoding="utf-8")
    assert "# Session Checkpoint" in text
    assert "Lane: work-strategy" in text
    assert "Title: Test checkpoint" in text
    assert "## Gate relevance" in text
    assert "maybe later" in text
    assert "Policy mode: operator_only" in text
    assert "Boundary reminder" in text


def test_checkpoint_from_memory_brief(tmp_path: Path) -> None:
    mb = tmp_path / "brief.md"
    mb.write_text(
        "\n".join(
            [
                "# Memory Brief",
                "",
                "Lane: work-strategy",
                "Query: iran test",
                "",
                "## Best Matches",
                "- obs1 | title one",
                "",
                "## Expanded Takeaways",
                "- takeaway a [obs1]",
                "",
            ]
        ),
        encoding="utf-8",
    )
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(tmp_path),
            "--lane",
            "work-strategy",
            "--title",
            "Seeded",
            "--from-memory-brief",
            str(mb),
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    cp = next((tmp_path / "artifacts" / "handoffs" / "checkpoints").glob("*.md"))
    body = cp.read_text(encoding="utf-8")
    assert "iran test" in body
    assert "title one" in body or "takeaway a" in body
