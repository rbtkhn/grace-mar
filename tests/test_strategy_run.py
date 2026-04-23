"""Tests for strategy run wrapper (WORK only)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
STRATEGY_RUN = REPO_ROOT / "scripts" / "strategy_run.py"
BUILD_REPORT = REPO_ROOT / "scripts" / "build_strategy_run_report.py"


def _env(root: Path) -> dict[str, str]:
    e = dict(os.environ)
    e["STRATEGY_RUN_ARTIFACT_ROOT"] = str(root)
    return e


def _nb(root: Path) -> Path:
    d = (
        root
        / "docs"
        / "skill-work"
        / "work-strategy"
        / "strategy-notebook"
    )
    d.mkdir(parents=True)
    (d / "daily-strategy-inbox.md").write_text("- capture\n", encoding="utf-8")
    ymd = "2026-04-16"
    ym = ymd[:7]
    (d / "chapters" / ym).mkdir(parents=True)
    (d / "chapters" / ym / "days.md").write_text(f"## {ymd}\n", encoding="utf-8")
    (d / "raw-input" / ymd).mkdir(parents=True)
    (d / "raw-input" / ymd / "note.md").write_text("x", encoding="utf-8")
    return d


def _run(
    args: list[str], *, root: Path, check: bool = True
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(STRATEGY_RUN), *args],
        cwd=str(REPO_ROOT),
        env=_env(root),
        capture_output=True,
        text=True,
        check=check,
    )


def test_start_creates_state_and_receipt_and_validates_schema(tmp_path: Path) -> None:
    jsonschema = pytest.importorskip("jsonschema")
    _nb(tmp_path)
    r = _run(
        [
            "start",
            "--date",
            "2026-04-16",
            "--notebook-dir",
            str(
                tmp_path
                / "docs"
                / "skill-work"
                / "work-strategy"
                / "strategy-notebook"
            ),
        ],
        root=tmp_path,
    )
    assert r.returncode == 0, r.stderr
    run_id = r.stdout.splitlines()[0].strip()
    sp = (
        tmp_path
        / "artifacts"
        / "strategy-runs"
        / run_id
        / "state.json"
    )
    assert sp.is_file()
    st = json.loads(sp.read_text(encoding="utf-8"))
    with (REPO_ROOT / "schema-registry" / "strategy-run-state.v1.json").open(
        encoding="utf-8"
    ) as f:
        schema = json.load(f)
    jsonschema.validate(st, schema=schema)
    assert st["status"] == "inputs_resolved"
    rec_path = (
        tmp_path
        / "artifacts"
        / "run-receipts"
        / f"{run_id}-start.json"
    )
    assert rec_path.is_file()
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    with (REPO_ROOT / "schema-registry" / "run-receipt.v1.json").open(
        encoding="utf-8"
    ) as f:
        rs = json.load(f)
    jsonschema.validate(rec, schema=rs)


def test_start_missing_inbox_is_started_status(tmp_path: Path) -> None:
    jsonschema = pytest.importorskip("jsonschema")
    nb = (
        tmp_path
        / "docs"
        / "skill-work"
        / "work-strategy"
        / "strategy-notebook"
    )
    nb.mkdir(parents=True)
    r = _run(
        [
            "start",
            "--date",
            "2026-04-16",
            "--notebook-dir",
            str(nb),
        ],
        root=tmp_path,
    )
    assert r.returncode == 0, r.stderr
    run_id = r.stdout.splitlines()[0].strip()
    st = json.loads(
        (tmp_path / "artifacts" / "strategy-runs" / run_id / "state.json").read_text(
            encoding="utf-8"
        )
    )
    assert st["status"] == "started"
    with (REPO_ROOT / "schema-registry" / "strategy-run-state.v1.json").open(
        encoding="utf-8"
    ) as f:
        jsonschema.validate(st, schema=json.load(f))


def test_inspect_resume_complete(tmp_path: Path) -> None:
    _nb(tmp_path)
    p = str(
        tmp_path
        / "docs"
        / "skill-work"
        / "work-strategy"
        / "strategy-notebook"
    )
    s = _run(["start", "--date", "2026-04-16", "--notebook-dir", p], root=tmp_path)
    run_id = s.stdout.splitlines()[0].strip()
    ins = _run(["inspect", "--run-id", run_id], root=tmp_path)
    assert ins.returncode == 0
    assert "inputs_resolved" in ins.stdout
    res = _run(["resume", "--run-id", run_id], root=tmp_path)
    assert res.returncode == 0
    com = _run(["complete", "--run-id", run_id], root=tmp_path)
    assert com.returncode == 0, com.stderr
    st = json.loads(
        (tmp_path / "artifacts" / "strategy-runs" / run_id / "state.json").read_text(
            encoding="utf-8"
        )
    )
    assert st["status"] == "completed"
    comp = (
        tmp_path
        / "artifacts"
        / "run-receipts"
        / f"{run_id}-complete.json"
    )
    assert comp.is_file()


def test_complete_refuses_failed_without_force(tmp_path: Path) -> None:
    _nb(tmp_path)
    p = str(
        tmp_path
        / "docs"
        / "skill-work"
        / "work-strategy"
        / "strategy-notebook"
    )
    s = _run(["start", "--date", "2026-04-16", "--notebook-dir", p], root=tmp_path)
    run_id = s.stdout.splitlines()[0].strip()
    sp = tmp_path / "artifacts" / "strategy-runs" / run_id / "state.json"
    st = json.loads(sp.read_text(encoding="utf-8"))
    st["status"] = "failed"
    sp.write_text(json.dumps(st), encoding="utf-8")
    bad = _run(["complete", "--run-id", run_id], root=tmp_path, check=False)
    assert bad.returncode == 1
    ok = _run(["complete", "--run-id", run_id, "--force"], root=tmp_path)
    assert ok.returncode == 0
    st2 = json.loads(sp.read_text(encoding="utf-8"))
    assert st2["status"] == "completed"


def test_inspect_invalid_run_id(tmp_path: Path) -> None:
    r = _run(
        ["inspect", "--run-id", "stratrun-99999999-nosuch"],
        root=tmp_path,
        check=False,
    )
    assert r.returncode == 1
    assert "no state" in r.stderr.lower() or "no state" in r.stdout.lower()


def test_proposal_schemas(tmp_path: Path) -> None:
    jsonschema = pytest.importorskip("jsonschema")
    day = {
        "run_id": "stratrun-20260416-deadbeef",
        "target_date": "2026-04-16",
        "thesis": "Test thesis line.",
        "mode": "days_only",
        "target_file": "docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04/days.md",
        "references": ["inbox:line1"],
        "approval_required": True,
    }
    with (REPO_ROOT / "schema-registry" / "strategy-day-proposal.v1.json").open(
        encoding="utf-8"
    ) as f:
        jsonschema.validate(day, schema=json.load(f))
    page = {
        "run_id": "stratrun-20260416-deadbeef",
        "page_id": "test-p",
        "operation": "new",
        "target_thread": "docs/skill-work/work-strategy/strategy-notebook/experts/mercouris/thread.md",
        "watch_ids": ["hormuz"],
        "experts": ["mercouris"],
        "thesis": "T",
        "references": [],
        "approval_required": True,
    }
    with (REPO_ROOT / "schema-registry" / "strategy-page-proposal.v1.json").open(
        encoding="utf-8"
    ) as f:
        jsonschema.validate(page, schema=json.load(f))


def test_build_report(tmp_path: Path) -> None:
    _nb(tmp_path)
    p = str(
        tmp_path
        / "docs"
        / "skill-work"
        / "work-strategy"
        / "strategy-notebook"
    )
    s = _run(["start", "--date", "2026-04-16", "--notebook-dir", p], root=tmp_path)
    run_id = s.stdout.splitlines()[0].strip()
    r = subprocess.run(
        [sys.executable, str(BUILD_REPORT), "--output", str(tmp_path / "r.md")],
        cwd=str(REPO_ROOT),
        env=_env(tmp_path),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    text = (tmp_path / "r.md").read_text(encoding="utf-8")
    assert run_id in text
    assert "inputs_resolved" in text
