"""Session brief Context Efficiency Layer (recovery links, compact mode)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_context_surfaces_json_schema() -> None:
    path = REPO / "config" / "context_surfaces.json"
    assert path.is_file()
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw.get("schemaVersion")
    assert isinstance(raw.get("operator_runtime_tiers"), dict)
    assert len(raw["operator_runtime_tiers"]) >= 1


def test_session_brief_json_loads() -> None:
    path = REPO / "config" / "context_budgets" / "session_brief.json"
    assert path.is_file()
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert "max_pending_ids_listed" in raw


def test_session_brief_minimal_stdout_includes_recovery() -> None:
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "session_brief.py"), "-u", "grace-mar", "--minimal"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    assert "Recovery links" in proc.stdout
    assert "recursion-gate.md" in proc.stdout


def test_session_brief_compact_stdout_includes_tiers() -> None:
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "session_brief.py"), "-u", "grace-mar", "--compact"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    assert "Session brief (compact)" in proc.stdout
    assert "Operator-runtime tiers" in proc.stdout
    assert "recursion_gate" in proc.stdout
