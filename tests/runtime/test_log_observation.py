"""Tests for scripts/runtime/log_observation.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "runtime" / "log_observation.py"
SCHEMA_PATH = REPO_ROOT / "schema-registry" / "runtime-observation.v1.json"


@pytest.fixture
def jsonschema_mod():
    return pytest.importorskip("jsonschema")


def _run_log_observation(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def _schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def test_validate_only_does_not_create_ledger(tmp_path: Path, jsonschema_mod) -> None:
    obs_dir = tmp_path / "runtime" / "observations"
    assert not obs_dir.exists()
    proc = _run_log_observation(
        tmp_path,
        "--lane",
        "work-strategy",
        "--source-kind",
        "manual_note",
        "--title",
        "T",
        "--summary",
        "S",
        "--validate-only",
    )
    assert proc.returncode == 0, proc.stderr
    assert not obs_dir.exists()


def test_appends_valid_jsonl_line(tmp_path: Path, jsonschema_mod) -> None:
    proc = _run_log_observation(
        tmp_path,
        "--lane",
        "work-strategy",
        "--source-kind",
        "notebook_entry",
        "--title",
        "Title here",
        "--summary",
        "Summary body for the observation.",
    )
    assert proc.returncode == 0, proc.stderr
    ledger = tmp_path / "runtime" / "observations" / "index.jsonl"
    assert ledger.is_file()
    line = ledger.read_text(encoding="utf-8").strip().splitlines()[0]
    doc = json.loads(line)
    from jsonschema import Draft202012Validator

    Draft202012Validator(_schema()).validate(doc)
    assert doc["lane"] == "work-strategy"
    assert doc["source_kind"] == "notebook_entry"
    assert doc["record_mutation_candidate"] is False


def test_rejects_invalid_source_kind(tmp_path: Path) -> None:
    proc = _run_log_observation(
        tmp_path,
        "--lane",
        "x",
        "--source-kind",
        "not_a_kind",
        "--title",
        "T",
        "--summary",
        "S",
        "--validate-only",
    )
    assert proc.returncode != 0


def test_rejects_bad_confidence(tmp_path: Path) -> None:
    proc = _run_log_observation(
        tmp_path,
        "--lane",
        "x",
        "--source-kind",
        "manual_note",
        "--title",
        "T",
        "--summary",
        "S",
        "--confidence",
        "2",
        "--validate-only",
    )
    assert proc.returncode != 0


def test_record_mutation_candidate_flag(tmp_path: Path, jsonschema_mod) -> None:
    proc = _run_log_observation(
        tmp_path,
        "--lane",
        "work-dev",
        "--source-kind",
        "candidate_derivation",
        "--title",
        "T",
        "--summary",
        "S",
        "--record-mutation-candidate",
    )
    assert proc.returncode == 0, proc.stderr
    line = (tmp_path / "runtime" / "observations" / "index.jsonl").read_text(encoding="utf-8")
    assert json.loads(line.strip())["record_mutation_candidate"] is True


def test_only_observations_tree_written(tmp_path: Path, jsonschema_mod) -> None:
    proc = _run_log_observation(
        tmp_path,
        "--lane",
        "a",
        "--source-kind",
        "manual_note",
        "--title",
        "T",
        "--summary",
        "S",
    )
    assert proc.returncode == 0
    all_files = [p.relative_to(tmp_path) for p in tmp_path.rglob("*") if p.is_file()]
    assert all(str(p).startswith("runtime/observations/") for p in all_files)


def test_tags_and_source_refs(tmp_path: Path, jsonschema_mod) -> None:
    proc = _run_log_observation(
        tmp_path,
        "--lane",
        "history-notebook",
        "--source-kind",
        "notebook_entry",
        "--title",
        "Roman note",
        "--summary",
        "Corridor framing.",
        "--source-path",
        "docs/foo.md",
        "--source-ref",
        "turn_018",
        "--tag",
        "rome",
        "--tag",
        "corridor",
    )
    assert proc.returncode == 0, proc.stderr
    doc = json.loads(
        (tmp_path / "runtime" / "observations" / "index.jsonl").read_text(encoding="utf-8").strip()
    )
    assert doc["source_path"] == "docs/foo.md"
    assert doc["source_refs"] == ["turn_018"]
    assert set(doc["tags"]) == {"corridor", "rome"}
