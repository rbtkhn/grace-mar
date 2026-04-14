"""Tests for scripts/prepared_context/build_budgeted_context.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "prepared_context" / "build_budgeted_context.py"


def _minimal_obs(oid: str, lane: str, title: str, summary: str) -> dict:
    return {
        "obs_id": oid,
        "timestamp": "2026-04-01T12:00:00Z",
        "lane": lane,
        "source_kind": "test",
        "title": title,
        "summary": summary,
        "record_mutation_candidate": False,
        "source_path": None,
        "source_refs": [],
        "tags": [],
        "confidence": 0.9,
        "contradiction_refs": [],
        "notes": None,
    }


def test_build_budgeted_context_subprocess(tmp_path: Path) -> None:
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    a = _minimal_obs("obs_test_001", "lane-x", "T1", "summary one about iran")
    b = _minimal_obs("obs_test_002", "lane-x", "T2", "summary two")
    b["timestamp"] = "2026-04-02T12:00:00Z"
    (obs_dir / "index.jsonl").write_text(
        json.dumps(a) + "\n" + json.dumps(b) + "\n", encoding="utf-8"
    )
    out = tmp_path / "prepared-context" / "out.md"
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(tmp_path),
            "--lane",
            "lane-x",
            "--mode",
            "compact",
            "--query",
            "iran",
            "-o",
            str(out),
            "--budgets-file",
            str(REPO_ROOT / "config" / "context_budgets" / "lane-defaults.json"),
        ],
        env=env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    text = out.read_text(encoding="utf-8")
    assert "# Budgeted Context" in text
    assert "## Included" in text
    assert "## Excluded" in text
    assert "## Context Block" in text
    assert "Budget Notes" in text
    receipt = tmp_path / "prepared-context" / "last-budget-builds.json"
    assert receipt.is_file()
    data = json.loads(receipt.read_text(encoding="utf-8"))
    assert data["lanes"]["lane-x"]["mode"] == "compact"
    assert "exclusions" in data["lanes"]["lane-x"]
