"""Tests for scripts/runtime/lane_timeline.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "runtime" / "lane_timeline.py"


def _write_ledger(tmp_path: Path, rows: list[dict]) -> None:
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    path = obs_dir / "index.jsonl"
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


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


def _obs(
    oid: str,
    ts: str,
    lane: str,
    *,
    title: str,
    summary: str,
    source_kind: str = "manual_note",
) -> dict:
    return {
        "obs_id": oid,
        "timestamp": ts,
        "lane": lane,
        "source_kind": source_kind,
        "title": title,
        "summary": summary,
        "record_mutation_candidate": False,
        "tags": [],
        "notes": "TIMELINE_NOTES_SHOULD_NOT_LEAK",
    }


def test_anchor_centered_window(tmp_path: Path) -> None:
    rows = [
        _obs("obs_20200101T080000Z_aaaabbbb", "2020-01-01T08:00:00Z", "work-strategy", title="a", summary="1"),
        _obs("obs_20200101T090000Z_ccccdddd", "2020-01-01T09:00:00Z", "work-strategy", title="b", summary="2"),
        _obs("obs_20200101T100000Z_eeeeffff", "2020-01-01T10:00:00Z", "work-strategy", title="c", summary="3"),
        _obs("obs_20200101T110000Z_11112222", "2020-01-01T11:00:00Z", "work-strategy", title="d", summary="4"),
        _obs("obs_20200101T120000Z_33334444", "2020-01-01T12:00:00Z", "work-strategy", title="e", summary="5"),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(
        tmp_path,
        "--anchor",
        "obs_20200101T100000Z_eeeeffff",
        "--before",
        "1",
        "--after",
        "1",
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.count("obs_") == 3
    assert "obs_20200101T090000Z_ccccdddd" in proc.stdout
    assert "obs_20200101T100000Z_eeeeffff" in proc.stdout
    assert "obs_20200101T110000Z_11112222" in proc.stdout
    assert "TIMELINE_NOTES" not in proc.stdout


def test_defaults_to_same_lane_only(tmp_path: Path) -> None:
    rows = [
        _obs("obs_20200101T090000Z_bbbbbbbb", "2020-01-01T09:00:00Z", "work-strategy", title="in lane", summary="x"),
        _obs("obs_20200101T100000Z_cccccccc", "2020-01-01T10:00:00Z", "work-strategy", title="anchor", summary="y"),
        _obs("obs_20200101T095000Z_otherabcd", "2020-01-01T09:50:00Z", "other-lane", title="not shown", summary="z"),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(
        tmp_path,
        "--anchor",
        "obs_20200101T100000Z_cccccccc",
        "--before",
        "5",
        "--after",
        "5",
    )
    assert proc.returncode == 0, proc.stderr
    assert "other-lane" not in proc.stdout
    assert "not shown" not in proc.stdout


def test_cross_lane_includes_other_lane(tmp_path: Path) -> None:
    rows = [
        _obs("obs_20200101T090000Z_bbbbbbbb", "2020-01-01T09:00:00Z", "work-strategy", title="a", summary="1"),
        _obs("obs_20200101T095000Z_otherabcd", "2020-01-01T09:50:00Z", "other-lane", title="between", summary="2"),
        _obs("obs_20200101T100000Z_cccccccc", "2020-01-01T10:00:00Z", "work-strategy", title="anchor", summary="3"),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(
        tmp_path,
        "--anchor",
        "obs_20200101T100000Z_cccccccc",
        "--before",
        "5",
        "--after",
        "0",
        "--cross-lane",
    )
    assert proc.returncode == 0, proc.stderr
    assert "other-lane" in proc.stdout
    assert "between" in proc.stdout


def test_respects_before_after(tmp_path: Path) -> None:
    suffixes = ["10101010", "20202020", "30303030", "40404040", "50505050"]
    rows = [
        _obs(
            f"obs_20200101T{i:02d}0000Z_{suffixes[i - 8]}",
            f"2020-01-01T{i:02d}:00:00Z",
            "work-strategy",
            title=f"t{i}",
            summary="s",
        )
        for i in range(8, 13)
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(
        tmp_path,
        "--anchor",
        "obs_20200101T100000Z_30303030",
        "--before",
        "0",
        "--after",
        "0",
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.count("obs_") == 1


def test_missing_anchor_errors(tmp_path: Path) -> None:
    _write_ledger(tmp_path, [])
    proc = _run(tmp_path, "--anchor", "obs_20200101T100000Z_aaaaaaaa", "--before", "1", "--after", "1")
    assert proc.returncode == 2
    assert "not found" in proc.stderr.lower()


def test_chronological_order(tmp_path: Path) -> None:
    rows = [
        _obs("obs_20200101T120000Z_eeeeeeee", "2020-01-01T12:00:00Z", "work-strategy", title="late", summary="3"),
        _obs("obs_20200101T100000Z_cccccccc", "2020-01-01T10:00:00Z", "work-strategy", title="mid", summary="2"),
        _obs("obs_20200101T080000Z_aaaaaaaa", "2020-01-01T08:00:00Z", "work-strategy", title="early", summary="1"),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(tmp_path, "--anchor", "obs_20200101T100000Z_cccccccc", "--before", "2", "--after", "2")
    assert proc.returncode == 0, proc.stderr
    early_i = proc.stdout.find("early")
    mid_i = proc.stdout.find("mid")
    late_i = proc.stdout.find("late")
    assert early_i < mid_i < late_i


def test_query_resolves_anchor(tmp_path: Path) -> None:
    rows = [
        _obs("obs_20200101T100000Z_aaaaaaaa", "2020-01-01T10:00:00Z", "work-strategy", title="noise", summary="other"),
        _obs("obs_20200101T110000Z_bbbbbbbb", "2020-01-01T11:00:00Z", "work-strategy", title="uniquequerytoken", summary="hit"),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(
        tmp_path,
        "--lane",
        "work-strategy",
        "--query",
        "uniquequerytoken",
        "--before",
        "1",
        "--after",
        "0",
    )
    assert proc.returncode == 0, proc.stderr
    assert "uniquequerytoken" in proc.stdout
    assert "noise" in proc.stdout


def test_json_compact_no_notes(tmp_path: Path) -> None:
    rows = [
        _obs("obs_20200101T100000Z_cccccccc", "2020-01-01T10:00:00Z", "work-strategy", title="x", summary="y"),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(tmp_path, "--anchor", "obs_20200101T100000Z_cccccccc", "--before", "0", "--after", "0", "--json")
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert isinstance(data, list)
    assert "notes" not in data[0]
