"""Tests for scripts/runtime/build_handoff_packet.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CP = REPO_ROOT / "scripts" / "runtime" / "checkpoint_session.py"
HO = REPO_ROOT / "scripts" / "runtime" / "build_handoff_packet.py"


def test_build_handoff_packet_subprocess(tmp_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(CP),
            "--repo-root",
            str(tmp_path),
            "--lane",
            "work-strategy",
            "--title",
            "One",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    out_path = tmp_path / "artifacts" / "handoffs" / "ws-handoff.md"
    r = subprocess.run(
        [
            sys.executable,
            str(HO),
            "--repo-root",
            str(tmp_path),
            "--lane",
            "work-strategy",
            "--latest",
            "2",
            "--output",
            str(out_path),
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    text = out_path.read_text(encoding="utf-8")
    assert "# Handoff Packet" in text
    assert "Lane: work-strategy" in text
    assert "## Recent checkpoints" in text
    assert "## Review / gate relevance" in text
    assert "Boundary reminder" in text
    assert "## Primary checkpoint (full)" in text
