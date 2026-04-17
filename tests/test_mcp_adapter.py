"""Tests for integrations/mcp_adapter.py — core retrieval functions (layer 1).

These tests exercise the plain-Python retrieval API directly.
The ``mcp`` package is NOT required.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "integrations"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from mcp_adapter import (  # noqa: E402
    SUPPORTED_CLASSES,
    UNSUPPORTED_CLASSES,
    health,
    list_export_classes,
    retrieve_export,
)


# ── health ──────────────────────────────────────────────────────────────

def test_health_returns_ok():
    result = health()
    assert result["status"] == "ok"
    assert result["adapter"] == "grace-mar-mcp"
    assert result["read_only"] is True


def test_health_lists_supported_classes():
    result = health()
    for cls in SUPPORTED_CLASSES:
        assert cls in result["supported_classes"]


# ── list_export_classes ─────────────────────────────────────────────────

def test_list_classes_includes_supported():
    result = list_export_classes()
    for cls in ("tool_bootstrap", "full", "task_limited"):
        assert cls in result["supported"]
        assert result["supported"][cls]["operational"] is True


def test_list_classes_includes_capability_as_supported():
    result = list_export_classes()
    assert "capability" in result["supported"]
    assert result["supported"]["capability"]["operational"] is True


def test_list_classes_includes_unsupported():
    result = list_export_classes()
    assert "internal" in result["unsupported"]
    assert result["unsupported"]["internal"]["operational"] is False
    assert result["unsupported"]["internal"]["description"]


# ── retrieve_export — successful paths ──────────────────────────────────

def test_retrieve_tool_bootstrap():
    result = retrieve_export(user_id="grace-mar", export_class="tool_bootstrap")
    assert "error" not in result
    assert result["export_class"] == "tool_bootstrap"
    assert result["content_type"] == "text/plain"
    assert isinstance(result["content"], str)
    assert len(result["content"]) > 0
    assert result["generated_via"] == "export_prp"


def test_retrieve_full():
    result = retrieve_export(user_id="grace-mar", export_class="full")
    assert "error" not in result
    assert result["export_class"] == "full"
    assert result["content_type"] == "application/json"
    content = result["content"]
    assert "metadata" in content
    assert "primary_artifact" in content
    assert isinstance(content["primary_artifact"], str)
    assert "bundle_files" in content
    assert isinstance(content["bundle_files"], list)
    assert result["generated_via"] == "export_runtime_bundle"


def test_retrieve_task_limited():
    result = retrieve_export(user_id="grace-mar", export_class="task_limited")
    assert "error" not in result
    assert result["export_class"] == "task_limited"
    assert result["content_type"] == "application/json"
    assert isinstance(result["content"], dict)
    assert result["generated_via"] == "export_fork"


# ── retrieve_export — rejection paths ───────────────────────────────────

def test_retrieve_capability():
    result = retrieve_export(user_id="grace-mar", export_class="capability")
    assert "error" not in result
    assert result["export_class"] == "capability"
    assert result["content_type"] == "application/json"
    assert isinstance(result["content"], dict)
    assert result["generated_via"] == "export_capability"


def test_internal_class_not_exposed():
    result = retrieve_export(user_id="grace-mar", export_class="internal")
    assert "error" in result
    assert "not exportable" in result["error"]
    assert "supported_classes" in result


def test_unknown_class_rejects():
    result = retrieve_export(user_id="grace-mar", export_class="nonexistent_class")
    assert "error" in result
    assert "unknown" in result["error"]
    assert "supported_classes" in result


# ── response shape invariants ───────────────────────────────────────────

@pytest.mark.parametrize("cls", list(SUPPORTED_CLASSES))
def test_successful_response_has_required_fields(cls: str):
    result = retrieve_export(user_id="grace-mar", export_class=cls)
    for field in ("user", "export_class", "content_type", "content", "generated_via", "warnings"):
        assert field in result, f"missing field {field!r} in {cls} response"
