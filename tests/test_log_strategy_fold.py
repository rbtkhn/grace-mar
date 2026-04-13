"""Tests for scripts/log_strategy_fold.py and report_strategy_fold_learning.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PY = sys.executable
LOG = REPO / "scripts" / "log_strategy_fold.py"
REPORT = REPO / "scripts" / "report_strategy_fold_learning.py"


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PY, str(args[0])] + args[1:],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=False,
    )


def test_log_strategy_fold_appends_jsonl(tmp_path: Path):
    ledger = tmp_path / "strategy-fold-events.jsonl"
    r = _run(
        [
            LOG,
            "-u",
            "grace-mar",
            "--jsonl",
            str(ledger),
            "--notebook-date",
            "2026-04-01",
            "--fold-kind",
            "manual",
            "--inbox-chars",
            "1000",
            "--days-delta-chars",
            "200",
            "--note",
            "first",
        ]
    )
    assert r.returncode == 0, r.stderr
    r2 = _run(
        [
            LOG,
            "-u",
            "grace-mar",
            "--jsonl",
            str(ledger),
            "--notebook-date",
            "2026-04-02",
            "--fold-kind",
            "dream",
            "--inbox-chars",
            "500",
            "--days-delta-chars",
            "2500",
        ]
    )
    assert r2.returncode == 0, r2.stderr
    lines = ledger.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 2
    a = json.loads(lines[0])
    b = json.loads(lines[1])
    assert a["notebook_date"] == "2026-04-01"
    assert a["fold_kind"] == "manual"
    assert a["inbox_chars"] == 1000
    assert a["days_delta_chars"] == 200
    assert a["note"] == "first"
    assert b["notebook_date"] == "2026-04-02"
    assert b["fold_kind"] == "dream"


def test_report_strategy_fold_learning_stdout(tmp_path: Path):
    ledger = tmp_path / "e.jsonl"
    events = [
        {
            "ts": "2099-01-15T12:00:00Z",
            "notebook_date": "2099-01-15",
            "fold_kind": "manual",
            "inbox_chars": 1000,
            "days_delta_chars": 100,
            "note": "tight",
        },
        {
            "ts": "2099-01-16T12:00:00Z",
            "notebook_date": "2099-01-16",
            "fold_kind": "dream",
            "inbox_chars": 100,
            "days_delta_chars": 5000,
            "note": "loose",
        },
    ]
    with open(ledger, "w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")

    r = _run(
        [
            REPORT,
            "-u",
            "grace-mar",
            "--jsonl",
            str(ledger),
            "--days",
            "365",
        ]
    )
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "2099-01-15" in out
    assert "2099-01-16" in out
    assert "Tightest" in out
    assert "Loosest" in out
    assert "tight" in out or "loose" in out


def test_log_invalid_date_exits_nonzero(tmp_path: Path):
    ledger = tmp_path / "bad.jsonl"
    r = _run(
        [
            LOG,
            "-u",
            "grace-mar",
            "--notebook-date",
            "not-a-date",
            "--fold-kind",
            "manual",
            "--jsonl",
            str(ledger),
        ]
    )
    assert r.returncode == 2
    assert not ledger.exists() or ledger.read_text() == ""
