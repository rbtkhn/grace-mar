"""Tests for grace_mar.replay loaders and bundle fallback."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from grace_mar.replay.loaders import (
    AuditPaths,
    load_pipeline_events,
    read_jsonl,
    resolve_jsonl_path,
)


def test_read_jsonl_skips_bad_lines(tmp_path: Path):
    p = tmp_path / "x.jsonl"
    p.write_text('{"a": 1}\nnot-json\n{"b": 2}\n', encoding="utf-8")
    rows = read_jsonl(p)
    assert len(rows) == 2
    assert rows[0]["a"] == 1


def test_resolve_jsonl_prefers_nonempty_primary(tmp_path: Path):
    primary = tmp_path / "p.jsonl"
    fb = tmp_path / "bundle" / "p.jsonl"
    fb.parent.mkdir(parents=True, exist_ok=True)
    primary.write_text('{"x": 1}\n', encoding="utf-8")
    fb.write_text('{"y": 2}\n', encoding="utf-8")
    assert resolve_jsonl_path(primary, fb) == primary


def test_resolve_jsonl_fallback_when_primary_missing(tmp_path: Path):
    primary = tmp_path / "missing.jsonl"
    fb = tmp_path / "bundle" / "audit" / "pipeline-events.jsonl"
    fb.parent.mkdir(parents=True, exist_ok=True)
    fb.write_text('{"event": "staged"}\n', encoding="utf-8")
    assert resolve_jsonl_path(primary, fb) == fb


def test_audit_paths_for_profile_resolves_bundle(tmp_path: Path):
    uid = tmp_path / "u1"
    (uid / "runtime-bundle" / "audit").mkdir(parents=True)
    pe = uid / "runtime-bundle" / "audit" / "pipeline-events.jsonl"
    pe.write_text('{"event": "applied", "candidate_id": "CANDIDATE-0001"}\n', encoding="utf-8")
    paths = AuditPaths.for_profile(uid)
    assert paths.pipeline_events == pe
    rows = load_pipeline_events(uid)
    assert len(rows) == 1


def test_load_pipeline_events_empty_when_no_files(tmp_path: Path):
    uid = tmp_path / "empty-user"
    uid.mkdir()
    assert load_pipeline_events(uid) == []
