"""Tests for scripts/prepared_context/build_context_from_observations.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "prepared_context" / "build_context_from_observations.py"


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


def _base_row(oid: str, lane: str, summary: str, conf: float | None = None) -> dict:
    return {
        "obs_id": oid,
        "timestamp": "2026-01-01T12:00:00Z",
        "lane": lane,
        "source_kind": "manual_note",
        "title": "T",
        "summary": summary,
        "record_mutation_candidate": False,
        "source_path": None,
        "source_refs": [],
        "tags": [],
        "confidence": conf,
        "contradiction_refs": [],
        "notes": None,
    }


def test_lane_match_enforced(tmp_path: Path) -> None:
    a = _base_row("obs_20260101T120000Z_aaaaaaaa", "work-strategy", "one")
    b = _base_row("obs_20260101T130000Z_bbbbbbbb", "other-lane", "two")
    _write_ledger(tmp_path, a, b)
    proc = _run(
        tmp_path,
        "--lane",
        "work-strategy",
        "--id",
        a["obs_id"],
        "--id",
        b["obs_id"],
        "-o",
        str(tmp_path / "out.md"),
    )
    assert proc.returncode == 2
    assert "outside lane" in proc.stderr or "expected" in proc.stderr


def test_mixed_lane_allows(tmp_path: Path) -> None:
    a = _base_row("obs_20260101T120000Z_aaaaaaaa", "a", "one")
    b = _base_row("obs_20260101T130000Z_bbbbbbbb", "b", "two")
    _write_ledger(tmp_path, a, b)
    out = tmp_path / "ctx.md"
    proc = _run(
        tmp_path,
        "--mixed-lane",
        "--id",
        a["obs_id"],
        "--id",
        b["obs_id"],
        "-o",
        str(out),
    )
    assert proc.returncode == 0, proc.stderr
    text = out.read_text(encoding="utf-8")
    assert "Runtime-only" in text
    assert "(mixed lanes)" in text
    assert a["obs_id"] in text


def test_boundary_notice_and_ids(tmp_path: Path) -> None:
    a = _base_row("obs_20260101T120000Z_aaaaaaaa", "work-strategy", "one")
    _write_ledger(tmp_path, a)
    out = tmp_path / "ctx.md"
    proc = _run(
        tmp_path,
        "--lane",
        "work-strategy",
        "--id",
        a["obs_id"],
        "-o",
        str(out),
    )
    assert proc.returncode == 0, proc.stderr
    text = out.read_text(encoding="utf-8")
    assert "not canonical Record truth" in text
    assert "recursion-gate.md" in text
    assert a["obs_id"] in text


def test_does_not_write_canonical_record_paths(tmp_path: Path) -> None:
    a = _base_row("obs_20260101T120000Z_aaaaaaaa", "work-strategy", "one")
    _write_ledger(tmp_path, a)
    out = tmp_path / "safe" / "ctx.md"
    proc = _run(
        tmp_path,
        "--lane",
        "work-strategy",
        "--id",
        a["obs_id"],
        "-o",
        str(out),
    )
    assert proc.returncode == 0
    assert not (tmp_path / "users").exists()


def test_max_ids(tmp_path: Path) -> None:
    rows = [
        _base_row(f"obs_2026010{i}T120000Z_{i:08x}", "work-strategy", f"s{i}")
        for i in range(10)
    ]
    _write_ledger(tmp_path, *rows)
    ids = [r["obs_id"] for r in rows]
    argv = ["--lane", "work-strategy", "-o", str(tmp_path / "o.md")]
    for oid in ids:
        argv.extend(["--id", oid])
    proc = _run(tmp_path, *argv)
    assert proc.returncode == 2
    assert "at most" in proc.stderr.lower()
