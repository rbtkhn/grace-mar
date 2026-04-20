"""Runtime worker: dry-run only, no canonical writes, trace line validates."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "runtime" / "grace_mar_runtime_worker.py"
TRACE_SCHEMA = REPO_ROOT / "schema-registry" / "runtime-worker-trace.v1.json"

CANONICAL_TOUCH_PATHS = (
    REPO_ROOT / "users" / "grace-mar" / "self.md",
    REPO_ROOT / "users" / "grace-mar" / "recursion-gate.md",
    REPO_ROOT / "bot" / "prompt.py",
)


def _validator():
    try:
        import jsonschema
    except ImportError:
        return None
    schema = json.loads(TRACE_SCHEMA.read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


@pytest.fixture
def worker_env(tmp_path: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
    env["GRACE_MAR_RUNTIME_WORKER_HOME"] = str(tmp_path / "runtime-worker")
    return env


def test_inspect_work_area_dry_run_writes_only_worker_home(
    tmp_path: Path, worker_env: dict[str, str]
) -> None:
    before = {p: (p.stat().st_mtime_ns if p.exists() else None) for p in CANONICAL_TOUCH_PATHS}

    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--task",
            "inspect_work_area",
            "--dry-run",
            "--repo-root",
            str(REPO_ROOT),
            "--scope",
            "docs/skill-work/work-strategy/strategy-notebook",
            "--max-files",
            "8",
            "--max-chars",
            "12000",
        ],
        cwd=str(REPO_ROOT),
        env=worker_env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout

    for p, t in before.items():
        if t is not None and p.exists():
            assert p.stat().st_mtime_ns == t

    wh = Path(worker_env["GRACE_MAR_RUNTIME_WORKER_HOME"])
    proposals = list((wh / "proposals").glob("rw_*.md"))
    assert len(proposals) == 1
    text = proposals[0].read_text(encoding="utf-8")
    assert "NON-CANONICAL" in text
    assert "inspect_work_area" in text

    trace_path = wh / "traces" / "index.jsonl"
    assert trace_path.exists()
    line = trace_path.read_text(encoding="utf-8").strip().splitlines()[-1]
    obj = json.loads(line)
    assert obj["task_mode"] == "inspect_work_area"
    assert obj["status"] in ("ok", "partial", "error")
    assert "dry_run" in obj["tools_used"]

    v = _validator()
    if v is not None:
        v.validate(obj)


def test_overlay_strategy_applies_scope_and_task_type_and_runtime_receipt(
    tmp_path: Path, worker_env: dict[str, str]
) -> None:
    before = {p: (p.stat().st_mtime_ns if p.exists() else None) for p in CANONICAL_TOUCH_PATHS}

    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--task",
            "inspect_work_area",
            "--overlay",
            "strategy",
            "--dry-run",
            "--repo-root",
            str(REPO_ROOT),
            "--max-files",
            "5",
            "--max-chars",
            "5000",
        ],
        cwd=str(REPO_ROOT),
        env=worker_env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout

    for p, t in before.items():
        if t is not None and p.exists():
            assert p.stat().st_mtime_ns == t

    wh = Path(worker_env["GRACE_MAR_RUNTIME_WORKER_HOME"])
    trace_path = wh / "traces" / "index.jsonl"
    line = trace_path.read_text(encoding="utf-8").strip().splitlines()[-1]
    obj = json.loads(line)
    assert obj["scope"] == "docs/skill-work/work-strategy/strategy-notebook"
    prov = obj["provenance"]
    assert prov.get("overlay") == "strategy"
    assert "scope" in prov.get("overlay_defaults_applied", [])
    assert "task_type" in prov.get("overlay_defaults_applied", [])
    rr = prov.get("runtime_receipt")
    assert isinstance(rr, dict)
    assert rr.get("non_canonical") is True
    assert rr.get("overlay") == "strategy"
    assert rr.get("task_type") == "strategy"
    assert rr.get("routed_worker") == "strategy_worker"
    assert "provenance_checker" in rr.get("shared_workers", [])
    assert "emphasize_anchor" in (rr.get("emphasis") or {})

    v = _validator()
    if v is not None:
        v.validate(obj)


def test_overlay_research_explicit_task_type_overrides_default(
    tmp_path: Path, worker_env: dict[str, str]
) -> None:
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--overlay",
            "research",
            "--task-type",
            "contradiction",
            "--dry-run",
            "--repo-root",
            str(REPO_ROOT),
            "--scope",
            "research",
            "--max-files",
            "8",
            "--max-chars",
            "12000",
        ],
        cwd=str(REPO_ROOT),
        env=worker_env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    wh = Path(worker_env["GRACE_MAR_RUNTIME_WORKER_HOME"])
    line = (wh / "traces" / "index.jsonl").read_text(encoding="utf-8").strip().splitlines()[-1]
    obj = json.loads(line)
    rr = obj["provenance"]["runtime_receipt"]
    assert rr["overlay"] == "research"
    assert rr["task_type"] == "contradiction"
    assert rr["routed_worker"] == "contradiction_worker"


def test_task_type_strategy_records_worker_routing_in_trace(
    tmp_path: Path, worker_env: dict[str, str]
) -> None:
    before = {p: (p.stat().st_mtime_ns if p.exists() else None) for p in CANONICAL_TOUCH_PATHS}

    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--task",
            "inspect_work_area",
            "--task-type",
            "strategy",
            "--dry-run",
            "--repo-root",
            str(REPO_ROOT),
            "--scope",
            "docs/skill-work/work-strategy/strategy-notebook",
            "--max-files",
            "8",
            "--max-chars",
            "12000",
        ],
        cwd=str(REPO_ROOT),
        env=worker_env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout

    for p, t in before.items():
        if t is not None and p.exists():
            assert p.stat().st_mtime_ns == t

    wh = Path(worker_env["GRACE_MAR_RUNTIME_WORKER_HOME"])
    trace_path = wh / "traces" / "index.jsonl"
    line = trace_path.read_text(encoding="utf-8").strip().splitlines()[-1]
    obj = json.loads(line)
    wr = obj["provenance"].get("worker_routing")
    assert isinstance(wr, dict)
    assert wr.get("non_canonical") is True
    assert wr.get("task_type") == "strategy"
    assert wr.get("routed_worker") == "strategy_worker"
    assert "provenance_checker" in wr.get("shared_workers", [])
    assert wr["entrypoints"]["strategy_worker"].endswith("review_orchestrator.py")

    v = _validator()
    if v is not None:
        v.validate(obj)


def test_lens_quick_scan_sets_caps_and_trace_lens(
    tmp_path: Path, worker_env: dict[str, str]
) -> None:
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--lens",
            "quick-scan",
            "--dry-run",
            "--repo-root",
            str(REPO_ROOT),
        ],
        cwd=str(REPO_ROOT),
        env=worker_env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    wh = Path(worker_env["GRACE_MAR_RUNTIME_WORKER_HOME"])
    trace_path = wh / "traces" / "index.jsonl"
    line = trace_path.read_text(encoding="utf-8").strip().splitlines()[-1]
    obj = json.loads(line)
    assert obj["provenance"].get("lens") == "quick-scan"
    prop = (wh / "proposals").glob("rw_*.md")
    text = next(prop).read_text(encoding="utf-8")
    assert "**lens:** `quick-scan`" in text
    assert "(cap 25)" in text


def test_compose_with_allowlist_only() -> None:
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--dry-run",
            "--compose-with",
            "scripts/evil.py",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode != 0
    assert "allowlist" in r.stderr.lower() or "allowlist" in r.stdout.lower()
