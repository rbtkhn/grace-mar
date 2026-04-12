"""Parity: unified export.py vs legacy export_fork (normalized JSON)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
FIXTURE = REPO / "tests" / "fixtures" / "export_volatile_keys.json"


def _strip_volatile(obj: object) -> object:
    data = json.loads(json.dumps(obj))  # deep copy via json
    cfg = json.loads(FIXTURE.read_text(encoding="utf-8"))
    keys = set(cfg.get("strip_top_level_keys", []))
    suffixes = tuple(cfg.get("strip_suffixes", []))

    if not isinstance(data, dict):
        return data

    def strip_dict(d: dict) -> dict:
        out = {}
        for k, v in d.items():
            if k in keys:
                continue
            if any(k.endswith(s) for s in suffixes):
                continue
            if isinstance(v, dict):
                out[k] = strip_dict(v)
            elif isinstance(v, list):
                out[k] = [strip_dict(x) if isinstance(x, dict) else x for x in v]
            else:
                out[k] = v
        return out

    return strip_dict(data)


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=False,
    )


def test_export_fork_matches_unified_cli_json():
    """Legacy export_fork vs export.py fork (stdout JSON, volatile keys stripped)."""
    u = "grace-mar"
    a = [
        sys.executable,
        str(SCRIPTS / "export_fork.py"),
        "-u",
        u,
        "--no-raw",
    ]
    b = [
        sys.executable,
        str(SCRIPTS / "export.py"),
        "fork",
        "--",
        "-u",
        u,
        "--no-raw",
    ]
    ra = _run(a)
    rb = _run(b)
    assert ra.returncode == 0, ra.stderr
    assert rb.returncode == 0, rb.stderr
    ja = json.loads(ra.stdout)
    jb = json.loads(rb.stdout)
    assert _strip_volatile(ja) == _strip_volatile(jb)


def test_export_py_all_invokes_runtime_bundle():
    """G1: ``all`` uses same script as ``bundle`` (smoke: --help on child not available; check dispatch)."""
    text = (SCRIPTS / "export.py").read_text(encoding="utf-8")
    assert '"all": "export_runtime_bundle.py"' in text or "'all': 'export_runtime_bundle.py'" in text
    assert "export_runtime_bundle.py" in text
