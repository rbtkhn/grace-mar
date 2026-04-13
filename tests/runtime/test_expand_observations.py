"""Tests for scripts/runtime/expand_observations.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "runtime" / "expand_observations.py"


def _write_ledger(tmp_path: Path, *rows: dict) -> None:
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    lines = [json.dumps(r, ensure_ascii=False) + "\n" for r in rows]
    (obs_dir / "index.jsonl").write_text("".join(lines), encoding="utf-8")


def _run(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_expand_selected_ids_json_array(tmp_path: Path) -> None:
    a = {
        "obs_id": "obs_20260101T120000Z_aaaaaaaa",
        "timestamp": "2026-01-01T12:00:00Z",
        "lane": "work-strategy",
        "source_kind": "manual_note",
        "title": "A",
        "summary": "First",
        "record_mutation_candidate": False,
        "source_path": None,
        "source_refs": [],
        "tags": [],
        "confidence": None,
        "contradiction_refs": [],
        "notes": None,
    }
    b = {
        "obs_id": "obs_20260102T120000Z_bbbbbbbb",
        "timestamp": "2026-01-02T12:00:00Z",
        "lane": "work-strategy",
        "source_kind": "manual_note",
        "title": "B",
        "summary": "Second",
        "record_mutation_candidate": False,
        "source_path": None,
        "source_refs": [],
        "tags": [],
        "confidence": None,
        "contradiction_refs": [],
        "notes": "secret notes",
    }
    _write_ledger(tmp_path, b, a)  # file order ≠ chrono
    proc = _run(
        tmp_path,
        "--id",
        "obs_20260101T120000Z_aaaaaaaa",
        "--id",
        "obs_20260102T120000Z_bbbbbbbb",
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert isinstance(data, list)
    assert [x["obs_id"] for x in data] == [
        "obs_20260101T120000Z_aaaaaaaa",
        "obs_20260102T120000Z_bbbbbbbb",
    ]
    assert "record_mutation_candidate" not in data[0]


def test_expand_errors_on_missing_id(tmp_path: Path) -> None:
    _write_ledger(tmp_path)
    proc = _run(tmp_path, "--id", "obs_missing_id_xxxxxxxx")
    assert proc.returncode == 2
    assert "missing" in proc.stderr.lower()


def test_expand_markdown_output(tmp_path: Path) -> None:
    row = {
        "obs_id": "obs_20260101T120000Z_aaaaaaaa",
        "timestamp": "2026-01-01T12:00:00Z",
        "lane": "work-strategy",
        "source_kind": "manual_note",
        "title": "T",
        "summary": "S",
        "record_mutation_candidate": False,
        "source_path": "docs/x.md",
        "source_refs": ["r1"],
        "tags": ["t"],
        "confidence": 0.9,
        "contradiction_refs": [],
        "notes": None,
    }
    _write_ledger(tmp_path, row)
    proc = _run(tmp_path, "--id", row["obs_id"], "--markdown")
    assert proc.returncode == 0
    assert "# Expanded runtime observations" in proc.stdout
    assert row["obs_id"] in proc.stdout
    assert "docs/x.md" in proc.stdout


def test_expand_writes_output_file_only(tmp_path: Path) -> None:
    row = {
        "obs_id": "obs_20260101T120000Z_aaaaaaaa",
        "timestamp": "2026-01-01T12:00:00Z",
        "lane": "x",
        "source_kind": "manual_note",
        "title": "T",
        "summary": "S",
        "record_mutation_candidate": False,
        "source_path": None,
        "source_refs": [],
        "tags": [],
        "confidence": None,
        "contradiction_refs": [],
        "notes": None,
    }
    _write_ledger(tmp_path, row)
    out = tmp_path / "out.json"
    proc = _run(tmp_path, "--id", row["obs_id"], "-o", str(out))
    assert proc.returncode == 0
    assert out.is_file()
    assert proc.stdout == ""


def test_expand_does_not_mutate_ledger(tmp_path: Path) -> None:
    row = {
        "obs_id": "obs_20260101T120000Z_aaaaaaaa",
        "timestamp": "2026-01-01T12:00:00Z",
        "lane": "x",
        "source_kind": "manual_note",
        "title": "T",
        "summary": "S",
        "record_mutation_candidate": False,
        "source_path": None,
        "source_refs": [],
        "tags": [],
        "confidence": None,
        "contradiction_refs": [],
        "notes": None,
    }
    _write_ledger(tmp_path, row)
    path = tmp_path / "runtime" / "observations" / "index.jsonl"
    before = path.read_text(encoding="utf-8")
    proc = _run(tmp_path, "--id", row["obs_id"])
    assert proc.returncode == 0
    assert path.read_text(encoding="utf-8") == before
