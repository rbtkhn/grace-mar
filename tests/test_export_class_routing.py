"""Tests for export-class routing in scripts/export.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
EXPORT_PY = SCRIPTS / "export.py"

sys.path.insert(0, str(SCRIPTS))
from export import EXPORT_CLASS_ROUTES, EXPORT_CLASS_UNSUPPORTED, ALL_EXPORT_CLASSES  # noqa: E402


def test_supported_classes_present():
    assert "tool_bootstrap" in EXPORT_CLASS_ROUTES
    assert "full" in EXPORT_CLASS_ROUTES
    assert "task_limited" in EXPORT_CLASS_ROUTES
    assert "emulation" in EXPORT_CLASS_ROUTES


def test_tool_bootstrap_routes_to_prp():
    script, _args = EXPORT_CLASS_ROUTES["tool_bootstrap"]
    assert script == "export_prp.py"


def test_full_routes_to_runtime_bundle():
    script, args = EXPORT_CLASS_ROUTES["full"]
    assert script == "export_runtime_bundle.py"
    assert "--mode" in args
    assert "portable_bundle_only" in args


def test_task_limited_routes_to_fork():
    script, args = EXPORT_CLASS_ROUTES["task_limited"]
    assert script == "export_fork.py"
    assert "--format" in args
    assert "coach-handoff" in args


def test_capability_routes_to_export_capability():
    script, _args = EXPORT_CLASS_ROUTES["capability"]
    assert script == "export_capability.py"


def test_emulation_routes_to_export_emulation_bundle():
    script, args = EXPORT_CLASS_ROUTES["emulation"]
    assert script == "export_emulation_bundle.py"
    assert "--mode" in args
    assert "portable_bundle_only" in args


def test_unsupported_classes_defined():
    assert "internal" in EXPORT_CLASS_UNSUPPORTED


def test_unsupported_classes_not_in_routes():
    for cls in EXPORT_CLASS_UNSUPPORTED:
        assert cls not in EXPORT_CLASS_ROUTES


def test_all_classes_enumerated():
    assert set(ALL_EXPORT_CLASSES) == {
        "tool_bootstrap",
        "full",
        "task_limited",
        "capability",
        "emulation",
        "internal",
    }


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(EXPORT_PY)] + args,
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=False,
    )


def test_tool_bootstrap_smoke():
    """tool_bootstrap should run successfully (PRP export to stdout)."""
    r = _run(["--export-class", "tool_bootstrap"])
    assert r.returncode == 0, f"stderr: {r.stderr}"
    assert len(r.stdout) > 100, "PRP output should be non-trivial"


def test_capability_exports_successfully():
    r = _run(["--export-class", "capability"])
    assert r.returncode == 0, f"stderr: {r.stderr}"
    assert "grace-mar-capability-export" in r.stdout


def test_internal_rejects_clearly():
    r = _run(["--export-class", "internal"])
    assert r.returncode == 2
    assert "not exportable" in r.stderr


def test_unknown_class_rejects():
    r = _run(["--export-class", "nonexistent"])
    assert r.returncode == 2
    assert "unknown export class" in r.stderr.lower()


def test_backward_compat_subcommand_still_works():
    """Existing subcommand invocations must still work."""
    r = _run(["prp"])
    assert r.returncode == 0, f"stderr: {r.stderr}"
    assert len(r.stdout) > 100
