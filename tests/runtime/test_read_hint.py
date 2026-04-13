"""Tests for scripts/runtime/read_hint.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "runtime" / "read_hint.py"


def _obs(oid: str, *, lane: str, title: str, summary: str, source_path: str | None = None, **extra) -> dict:
    base = {
        "obs_id": oid,
        "timestamp": "2020-01-01T12:00:00Z",
        "lane": lane,
        "source_kind": "manual_note",
        "title": title,
        "summary": summary,
        "record_mutation_candidate": False,
        "tags": [],
        "source_refs": [],
        "confidence": None,
    }
    base.update(extra)
    if source_path is not None:
        base["source_path"] = source_path
    return base


def _write_ledger(tmp_path: Path, rows: list[dict]) -> None:
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    p = obs_dir / "index.jsonl"
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def _run(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_finds_by_path(tmp_path: Path) -> None:
    rows = [
        _obs(
            "obs_20200101T100000Z_aaaaaaaa",
            lane="work-strategy",
            title="Note",
            summary="About docs/strategy-notebook.md",
            source_path="docs/strategy-notebook.md",
        ),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(tmp_path, "--path", "docs/strategy-notebook.md", "--lane", "work-strategy")
    assert proc.returncode == 0, proc.stderr
    assert "relevant runtime observation" in proc.stdout.lower() or "observation" in proc.stdout.lower()
    assert "obs_20200101T100000Z_aaaaaaaa" in proc.stdout
    assert "lane_timeline.py" in proc.stdout
    assert "still read" in proc.stdout.lower() or "directly" in proc.stdout.lower()


def test_finds_by_query(tmp_path: Path) -> None:
    rows = [
        _obs(
            "obs_20200101T100000Z_aaaaaaaa",
            lane="history-notebook",
            title="Corridor connectivity Rome",
            summary="Corridor connectivity and trade routes.",
        ),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(tmp_path, "--lane", "history-notebook", "--query", "corridor connectivity")
    assert proc.returncode == 0, proc.stderr
    assert "obs_20200101T100000Z_aaaaaaaa" in proc.stdout
    assert "memory_brief.py" in proc.stdout


def test_respects_lane_filter(tmp_path: Path) -> None:
    rows = [
        _obs("obs_20200101T100000Z_aaaaaaaa", lane="work-strategy", title="A", summary="alpha token"),
        _obs("obs_20200101T110000Z_bbbbbbbb", lane="other-lane", title="B", summary="alpha token"),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(tmp_path, "--lane", "work-strategy", "--query", "alpha")
    assert proc.returncode == 0, proc.stderr
    assert "aaaaaaaa" in proc.stdout
    assert "bbbbbbbb" not in proc.stdout


def test_no_writes(tmp_path: Path) -> None:
    rows = [_obs("obs_20200101T100000Z_aaaaaaaa", lane="x", title="t", summary="hello world")]
    _write_ledger(tmp_path, rows)
    extra = tmp_path / "extra.md"
    extra.write_text("keep", encoding="utf-8")
    proc = _run(tmp_path, "--lane", "x", "--query", "hello")
    assert proc.returncode == 0
    assert extra.read_text() == "keep"


def test_requires_path_or_query(tmp_path: Path) -> None:
    _write_ledger(tmp_path, [])
    proc = _run(tmp_path)
    assert proc.returncode == 2
