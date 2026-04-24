"""Tests for strategy-notebook workbench visualizer fixture generator (WORK)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts/work_strategy" / "generate_strategy_notebook_visualizer_fixture.py"


def _load_generator():
    spec = importlib.util.spec_from_file_location(
        "generate_strategy_notebook_visualizer_fixture", SCRIPT
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def _run_script(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    r = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if check and r.returncode != 0:
        msg = f"exit {r.returncode}\nstdout: {r.stdout!r}\nstderr: {r.stderr!r}"
        raise AssertionError(msg)
    return r


def test_build_fixture_top_level_and_node_shape() -> None:
    mod = _load_generator()
    doc, warnings = mod._build_fixture(
        repo_root=REPO_ROOT,
        notebook_rel=mod.DEFAULT_NOTEBOOK,
    )
    for key in (
        "schemaVersion",
        "generatedAt",
        "sourceRoot",
        "recordAuthority",
        "gateEffect",
        "truthScope",
        "nodes",
        "edges",
    ):
        assert key in doc, f"missing {key!r}"
    assert doc["schemaVersion"] == mod.SCHEMA_VERSION
    assert doc["recordAuthority"] == "none"
    assert doc["gateEffect"] == "none"
    assert doc["sourceRoot"] == mod.DEFAULT_NOTEBOOK
    assert isinstance(warnings, list)
    for n in doc["nodes"]:
        assert "id" in n and "label" in n and "kind" in n and "path" in n
        assert n.get("authority") == "work-only"
    for e in doc["edges"]:
        assert "source" in e and "target" in e and "relation" in e
    ids = {n["id"] for n in doc["nodes"]}
    assert "strategy-notebook" in ids
    assert "knot-index" in ids


def test_check_passes_after_write_to_tmp(tmp_path: Path) -> None:
    out = tmp_path / "fixture.json"
    _run_script(["-o", str(out)])
    r = _run_script(["-o", str(out), "--check"], check=False)
    assert r.returncode == 0, r.stderr
    assert "ok" in (r.stdout + r.stderr).lower() or "up to date" in (r.stdout + r.stderr)


def test_check_fails_when_file_missing(tmp_path: Path) -> None:
    out = tmp_path / "nope.json"
    r = _run_script(["-o", str(out), "--check"], check=False)
    assert r.returncode == 1


def test_normalize_json_stability() -> None:
    mod = _load_generator()
    a = mod._normalize_json({"b": 1, "a": 2})
    b = mod._normalize_json({"a": 2, "b": 1})
    assert a == b


def test_default_fixture_path_exists_and_is_valid_json() -> None:
    mod = _load_generator()
    p = REPO_ROOT / mod.DEFAULT_OUT
    assert p.is_file()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert "nodes" in data and "edges" in data


def test_check_default_output_matches_repo_fixture() -> None:
    r = _run_script(["--check"], check=False)
    assert r.returncode == 0, r.stdout + r.stderr
