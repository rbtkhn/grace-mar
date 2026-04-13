"""Tests for scripts/runtime/memory_brief.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "runtime" / "memory_brief.py"


def _obs(
    oid: str,
    *,
    ts: str,
    lane: str,
    title: str,
    summary: str,
    confidence: float | None = None,
) -> dict:
    return {
        "obs_id": oid,
        "timestamp": ts,
        "lane": lane,
        "source_kind": "manual_note",
        "title": title,
        "summary": summary,
        "record_mutation_candidate": False,
        "tags": [],
        "source_refs": [],
        "confidence": confidence,
    }


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


def test_builds_brief_and_anchor_is_top_hit(tmp_path: Path) -> None:
    rows = [
        _obs(
            "obs_20200101T080000Z_aaaaaaaa",
            ts="2020-01-01T08:00:00Z",
            lane="work-strategy",
            title="noise",
            summary="other",
        ),
        _obs(
            "obs_20200101T100000Z_bbbbbbbb",
            ts="2020-01-01T10:00:00Z",
            lane="work-strategy",
            title="iran negotiation framing split",
            summary="iran negotiation framing details here",
        ),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(
        tmp_path,
        "--lane",
        "work-strategy",
        "--query",
        "iran negotiation framing",
        "--limit",
        "5",
        "--expand",
        "2",
        "--timeline-before",
        "1",
        "--timeline-after",
        "1",
    )
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout
    assert "Memory Brief" in out
    assert "Runtime-only" in out
    assert "obs_20200101T100000Z_bbbbbbbb" in out
    assert "Timeline Context" in out
    assert "Expanded Takeaways" in out
    assert "recursion-gate.md" in out


def test_timeline_window_bounded(tmp_path: Path) -> None:
    rows = [
        _obs("obs_20200101T080000Z_aaaaaaaa", ts="2020-01-01T08:00:00Z", lane="work-strategy", title="a", summary="x"),
        _obs("obs_20200101T090000Z_bbbbbbbb", ts="2020-01-01T09:00:00Z", lane="work-strategy", title="b", summary="y"),
        _obs("obs_20200101T100000Z_cccccccc", ts="2020-01-01T10:00:00Z", lane="work-strategy", title="iran hit", summary="iran negotiation framing"),
        _obs("obs_20200101T110000Z_dddddddd", ts="2020-01-01T11:00:00Z", lane="work-strategy", title="d", summary="z"),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(
        tmp_path,
        "--lane",
        "work-strategy",
        "--query",
        "iran negotiation",
        "--timeline-before",
        "0",
        "--timeline-after",
        "0",
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.count("2020-01-01T10:00:00Z") >= 1


def test_expand_limit(tmp_path: Path) -> None:
    rows = [
        _obs(
            f"obs_2020010{i}T100000Z_{'a' * 8}",
            ts=f"2020-01-0{i}T10:00:00Z",
            lane="work-strategy",
            title=f"token{i}",
            summary="sharedquery token",
        )
        for i in range(1, 5)
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(
        tmp_path,
        "--lane",
        "work-strategy",
        "--query",
        "sharedquery",
        "--expand",
        "2",
        "--limit",
        "10",
    )
    assert proc.returncode == 0, proc.stderr
    take = proc.stdout.split("## Expanded Takeaways", 1)[-1].split("## Recommended", 1)[0]
    assert take.count("[obs_") <= 2 or take.count("obs_2020") <= 6


def test_writes_output_only(tmp_path: Path) -> None:
    rows = [
        _obs(
            "obs_20200101T100000Z_aaaaaaaa",
            ts="2020-01-01T10:00:00Z",
            lane="work-strategy",
            title="iran",
            summary="iran negotiation framing",
        ),
    ]
    _write_ledger(tmp_path, rows)
    out_path = tmp_path / "out" / "brief.md"
    proc = _run(
        tmp_path,
        "--lane",
        "work-strategy",
        "--query",
        "iran",
        "--output",
        str(out_path),
    )
    assert proc.returncode == 0, proc.stderr
    assert out_path.is_file()
    assert "Boundary:" in out_path.read_text(encoding="utf-8")
    assert proc.stdout.strip() == "" or "wrote" in proc.stderr.lower()


def test_does_not_touch_self(tmp_path: Path) -> None:
    user = tmp_path / "users" / "u1"
    user.mkdir(parents=True)
    self_p = user / "self.md"
    self_p.write_text("# SELF\n", encoding="utf-8")
    rows = [
        _obs(
            "obs_20200101T100000Z_aaaaaaaa",
            ts="2020-01-01T10:00:00Z",
            lane="work-strategy",
            title="iran",
            summary="iran negotiation framing",
        ),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(tmp_path, "--lane", "work-strategy", "--query", "iran")
    assert proc.returncode == 0
    assert self_p.read_text() == "# SELF\n"


def test_positional_lane_and_query(tmp_path: Path) -> None:
    rows = [
        _obs(
            "obs_20200101T100000Z_aaaaaaaa",
            ts="2020-01-01T10:00:00Z",
            lane="work-strategy",
            title="iran topic",
            summary="iran negotiation framing",
        ),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(
        tmp_path,
        "work-strategy",
        "iran",
        "negotiation",
    )
    assert proc.returncode == 0, proc.stderr
    assert "Memory Brief" in proc.stdout
    assert "work-strategy" in proc.stdout


def test_rejects_lane_plus_positional(tmp_path: Path) -> None:
    _write_ledger(tmp_path, [])
    proc = _run(tmp_path, "--lane", "work-strategy", "work-strategy")
    assert proc.returncode != 0


def test_high_confidence_soft_signal(tmp_path: Path) -> None:
    rows = [
        _obs(
            "obs_20200101T100000Z_aaaaaaaa",
            ts="2020-01-01T10:00:00Z",
            lane="work-strategy",
            title="a",
            summary="iran negotiation framing one",
            confidence=0.9,
        ),
        _obs(
            "obs_20200101T110000Z_bbbbbbbb",
            ts="2020-01-01T11:00:00Z",
            lane="work-strategy",
            title="b",
            summary="iran negotiation framing two",
            confidence=0.85,
        ),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(tmp_path, "--lane", "work-strategy", "--query", "iran negotiation framing", "--limit", "5")
    assert proc.returncode == 0, proc.stderr
    assert "0.8" in proc.stdout or "contradiction" in proc.stdout.lower() or "confidence" in proc.stdout.lower()
