"""Tests for scripts/runtime/lane_search.py (compact runtime index)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "runtime" / "lane_search.py"


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


def _base(
    obs_id: str,
    *,
    ts: str,
    lane: str,
    source_kind: str,
    title: str,
    summary: str,
    tags: list[str] | None = None,
) -> dict:
    return {
        "obs_id": obs_id,
        "timestamp": ts,
        "lane": lane,
        "source_kind": source_kind,
        "title": title,
        "summary": summary,
        "tags": tags or [],
        "record_mutation_candidate": False,
        "confidence": None,
        "notes": "SECRET_NOTES_BODY_SHOULD_NOT_APPEAR_IN_LANE_SEARCH_OUTPUT",
    }


def test_title_phrase_ranks(tmp_path: Path) -> None:
    rows = [
        _base(
            "obs_20200101T100000Z_aaaaaaaa",
            ts="2020-01-01T10:00:00Z",
            lane="work-strategy",
            source_kind="manual_note",
            title="Other topic",
            summary="iran negotiation framing appears only here",
        ),
        _base(
            "obs_20200101T110000Z_bbbbbbbb",
            ts="2020-01-01T11:00:00Z",
            lane="work-strategy",
            source_kind="manual_note",
            title="iran negotiation framing headline",
            summary="something else",
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
    )
    assert proc.returncode == 0, proc.stderr
    assert "iran negotiation framing headline" in proc.stdout
    lines = [ln for ln in proc.stdout.splitlines() if ln and not ln.startswith("  ")]
    assert lines[0].startswith("obs_20200101T110000Z_bbbbbbbb")


def test_summary_term_match(tmp_path: Path) -> None:
    rows = [
        _base(
            "obs_20200101T100000Z_aaaaaaaa",
            ts="2020-01-01T10:00:00Z",
            lane="work-strategy",
            source_kind="manual_note",
            title="Alpha",
            summary="contains zzyxxy keyword for test",
        ),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(tmp_path, "--lane", "work-strategy", "--query", "zzyxxy", "--limit", "3")
    assert proc.returncode == 0, proc.stderr
    assert "zzyxxy" in proc.stdout


def test_filters_by_lane(tmp_path: Path) -> None:
    rows = [
        _base(
            "obs_20200101T100000Z_aaaaaaaa",
            ts="2020-01-01T10:00:00Z",
            lane="work-strategy",
            source_kind="manual_note",
            title="shared token",
            summary="one",
        ),
        _base(
            "obs_20200101T110000Z_bbbbbbbb",
            ts="2020-01-01T11:00:00Z",
            lane="other-lane",
            source_kind="manual_note",
            title="shared token",
            summary="two",
        ),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(tmp_path, "--lane", "work-strategy", "--query", "shared", "--limit", "10")
    assert proc.returncode == 0, proc.stderr
    assert "other-lane" not in proc.stdout
    assert "work-strategy" in proc.stdout


def test_filters_by_source_kind(tmp_path: Path) -> None:
    rows = [
        _base(
            "obs_20200101T100000Z_aaaaaaaa",
            ts="2020-01-01T10:00:00Z",
            lane="work-strategy",
            source_kind="compression",
            title="pickme token",
            summary="x",
        ),
        _base(
            "obs_20200101T110000Z_bbbbbbbb",
            ts="2020-01-01T11:00:00Z",
            lane="work-strategy",
            source_kind="manual_note",
            title="pickme token",
            summary="y",
        ),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(
        tmp_path,
        "--lane",
        "work-strategy",
        "--query",
        "pickme",
        "--source-kind",
        "manual_note",
        "--limit",
        "5",
    )
    assert proc.returncode == 0, proc.stderr
    assert "compression" not in proc.stdout
    assert "manual_note" in proc.stdout


def test_respects_limit(tmp_path: Path) -> None:
    rows = [
        _base(
            f"obs_2020010{i}T100000Z_{'a' * 8}",
            ts=f"2020-01-0{i}T10:00:00Z",
            lane="work-strategy",
            source_kind="manual_note",
            title=f"limit token {i}",
            summary="s",
        )
        for i in range(1, 6)
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(tmp_path, "--lane", "work-strategy", "--query", "limit token", "--limit", "2")
    assert proc.returncode == 0, proc.stderr
    blocks = [b for b in proc.stdout.strip().split("\n\n") if b.strip()]
    assert len(blocks) == 2


def test_text_mode_is_compact_no_notes(tmp_path: Path) -> None:
    rows = [
        _base(
            "obs_20200101T100000Z_aaaaaaaa",
            ts="2020-01-01T10:00:00Z",
            lane="work-strategy",
            source_kind="manual_note",
            title="compact title",
            summary="compact summary line",
        ),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(tmp_path, "--lane", "work-strategy", "--query", "compact", "--limit", "3")
    assert proc.returncode == 0, proc.stderr
    assert "SECRET_NOTES_BODY" not in proc.stdout


def test_json_is_single_array_with_score(tmp_path: Path) -> None:
    rows = [
        _base(
            "obs_20200101T100000Z_aaaaaaaa",
            ts="2020-01-01T10:00:00Z",
            lane="work-strategy",
            source_kind="manual_note",
            title="json match",
            summary="summary text",
        ),
    ]
    _write_ledger(tmp_path, rows)
    proc = _run(tmp_path, "--lane", "work-strategy", "--query", "json", "--json", "--limit", "3")
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert isinstance(data, list)
    assert "score" in data[0]
    assert "notes" not in data[0]
