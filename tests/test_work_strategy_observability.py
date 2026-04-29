"""Tests for work-strategy carry-stack observability summarizer."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WS_SCRIPTS = REPO_ROOT / "scripts" / "work_strategy"
EX_OBS = REPO_ROOT / "examples" / "work-strategy" / "observability"


def _summarize_mod():
    import importlib.util

    ws = str(WS_SCRIPTS)
    if ws not in sys.path:
        sys.path.insert(0, ws)
    path = WS_SCRIPTS / "summarize_carry_receipts.py"
    spec = importlib.util.spec_from_file_location("summarize_carry_receipts", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["summarize_carry_receipts"] = mod
    spec.loader.exec_module(mod)
    return mod


mod = _summarize_mod()


def _seed_runtime(tmp: Path) -> Path:
    rt = tmp / "runtime" / "work-strategy"
    for sub in ("carry-receipts", "validation-reports", "task-shape-reports", "review-packets"):
        (rt / sub).mkdir(parents=True)
    shutil.copy(EX_OBS / "carry-pass.json", rt / "carry-receipts" / "carry-pass.json")
    shutil.copy(EX_OBS / "carry-needs-review.json", rt / "carry-receipts" / "carry-needs-review.json")
    shutil.copy(EX_OBS / "validation-sample.json", rt / "validation-reports" / "validation-sample.json")
    shutil.copy(EX_OBS / "task-shape-sample.json", rt / "task-shape-reports" / "task-shape-sample.json")
    shutil.copy(EX_OBS / "review-packet-sample.json", rt / "review-packets" / "review-packet-sample.json")
    shutil.copy(EX_OBS / "malformed.json", rt / "carry-receipts" / "malformed.json")
    return rt


def test_build_report_aggregates(tmp_path: Path) -> None:
    rt = _seed_runtime(tmp_path)
    report = mod.build_report(
        repo_root=tmp_path,
        runtime_root=rt,
        receipts_dir=None,
        validation_dir=None,
        task_shape_dir=None,
        review_packet_dir=None,
        window_mode="all",
        last_n=None,
        since=None,
    )
    assert report["counts"]["carry_receipts_total"] == 2
    assert report["counts"]["pass_total"] == 1
    assert report["counts"]["needs_review_total"] == 1
    assert report["counts"]["validation_reports_total"] == 1
    assert report["counts"]["validation_report_fail"] == 1
    assert report["task_shapes"]["watch_update"] == 1
    ids_fail = [x["id"] for x in report["validation"]["top_failed_checks"]]
    assert "artifact_substance" in ids_fail
    assert report["review_packets"]["with_validation_count"] == 1
    assert report["review_packets"]["with_task_shape_count"] == 1
    assert report["files_scanned"]["malformed_skipped"] >= 1
    assert any("malformed JSON" in n for n in report["notes"])


def test_last_n_filters(tmp_path: Path) -> None:
    rt = _seed_runtime(tmp_path)
    report = mod.build_report(
        repo_root=tmp_path,
        runtime_root=rt,
        receipts_dir=None,
        validation_dir=None,
        task_shape_dir=None,
        review_packet_dir=None,
        window_mode="last_n",
        last_n=1,
        since=None,
    )
    assert report["counts"]["carry_receipts_total"] == 1


def test_forbidden_out_users() -> None:
    cmd = [
        sys.executable,
        str(WS_SCRIPTS / "summarize_carry_receipts.py"),
        "--repo-root",
        str(REPO_ROOT),
        "--runtime-root",
        "runtime/work-strategy",
        "--out",
        "users/grace-mar/__obs_test__.json",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 2
    assert not (REPO_ROOT / "users/grace-mar/__obs_test__.json").exists()


def test_json_stdout_valid(tmp_path: Path) -> None:
    rt = _seed_runtime(tmp_path)
    cmd = [
        sys.executable,
        str(WS_SCRIPTS / "summarize_carry_receipts.py"),
        "--repo-root",
        str(tmp_path),
        "--runtime-root",
        "runtime/work-strategy",
        "--json",
        "--out",
        "obs.json",
    ]
    r = subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    json.loads(r.stdout)
    assert (tmp_path / "obs.json").is_file()


def test_markdown_sections(tmp_path: Path) -> None:
    rt = _seed_runtime(tmp_path)
    report = mod.build_report(
        repo_root=tmp_path,
        runtime_root=rt,
        receipts_dir=None,
        validation_dir=None,
        task_shape_dir=None,
        review_packet_dir=None,
        window_mode="all",
        last_n=None,
        since=None,
    )
    md = mod.render_observability_markdown(report)
    for label in (
        "## Window",
        "## Totals",
        "## Carry receipt results",
        "## Task-shape distribution",
        "## Common validator checks",
        "## Review packet coverage",
        "## Gate prep coverage",
        "## Files scanned",
        "## Notes",
    ):
        assert label in md


def test_load_json_files_skips_malformed(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    ok = tmp_path / "ok.json"
    ok.write_text(json.dumps({"created_at": "2026-01-01T00:00:00+00:00", "x": 1}), encoding="utf-8")
    good, notes = mod.load_json_files([bad, ok])
    assert len(good) == 1
    assert len(notes) >= 1
