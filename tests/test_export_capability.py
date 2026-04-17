"""Tests for scripts/export_capability.py — demonstrated-capability exporter."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from export_capability import (  # noqa: E402
    export_capability,
    _load_rationales,
    _parse_identity_context,
    _extract_evidence,
    RATIONALE_REQUIRED_FIELDS,
)


# ── top-level shape ────────────────────────────────────────────────────

def test_export_returns_required_keys():
    result = export_capability(user_id="grace-mar")
    for key in ("version", "format", "generated_at", "user_id",
                "identity_context", "skills", "evidence", "rationales", "counts"):
        assert key in result, f"missing top-level key {key!r}"
    assert result["format"] == "grace-mar-capability-export"
    assert result["user_id"] == "grace-mar"


def test_counts_are_consistent():
    result = export_capability(user_id="grace-mar")
    counts = result["counts"]
    evidence = result["evidence"]
    total = sum(len(v) for v in evidence.values())
    assert counts["evidence_total"] == total
    assert counts["rationale_total"] == len(result["rationales"])


# ── identity context ───────────────────────────────────────────────────

def test_identity_context_minimal():
    result = export_capability(user_id="grace-mar")
    ctx = result["identity_context"]
    assert "name" in ctx
    assert "age" in ctx
    assert "lexile_output" in ctx
    assert len(ctx) == 3, "identity_context should contain only name, age, lexile_output"


def test_identity_context_no_full_self():
    result = export_capability(user_id="grace-mar")
    assert "self" not in result or "raw" not in result.get("self", {})


# ── evidence filtering ─────────────────────────────────────────────────

def test_evidence_has_production_categories():
    result = export_capability(user_id="grace-mar")
    ev = result["evidence"]
    assert "write" in ev
    assert "create" in ev
    assert "act" in ev


def test_evidence_excludes_read_and_media():
    result = export_capability(user_id="grace-mar")
    ev = result["evidence"]
    assert "read" not in ev
    assert "media" not in ev


def test_evidence_entries_have_ids():
    result = export_capability(user_id="grace-mar")
    for category in ("write", "create", "act"):
        for entry in result["evidence"][category]:
            assert "id" in entry
            assert entry["id"].startswith(category.upper() + "-")


# ── rationale loading ──────────────────────────────────────────────────

def test_rationale_attachment():
    result = export_capability(user_id="grace-mar")
    rationales = result["rationales"]
    assert isinstance(rationales, list)
    for r in rationales:
        for field in RATIONALE_REQUIRED_FIELDS:
            assert field in r, f"rationale missing required field {field!r}"


def test_rationale_export_class_is_capability():
    result = export_capability(user_id="grace-mar")
    for r in result["rationales"]:
        if "export_class" in r:
            assert r["export_class"] == "capability"


def test_empty_rationales_ok(tmp_path):
    rationales = _load_rationales(tmp_path)
    assert rationales == []


def test_invalid_rationale_skipped(tmp_path):
    (tmp_path / "bad.json").write_text('{"artifact_name": "X"}', encoding="utf-8")
    rationales = _load_rationales(tmp_path)
    assert len(rationales) == 0


# ── skills section ─────────────────────────────────────────────────────

def test_skills_structure():
    result = export_capability(user_id="grace-mar")
    skills = result["skills"]
    assert "claims" in skills
    assert "gaps" in skills
    assert "milestones" in skills
    assert isinstance(skills["claims"], list)


# ── CLI smoke test ─────────────────────────────────────────────────────

def test_cli_smoke():
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "export_capability.py"),
         "-u", "grace-mar"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data["format"] == "grace-mar-capability-export"


# ── JSON serialization ─────────────────────────────────────────────────

def test_output_is_json_serializable():
    result = export_capability(user_id="grace-mar")
    text = json.dumps(result, default=str, ensure_ascii=False)
    assert len(text) > 100
