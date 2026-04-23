"""Tests for scripts/build_strategy_notebook_graph.py (WORK only)."""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def minimal_notebook(tmp_path: Path) -> Path:
    """Notebook with one canonical expert and a strategy-page block."""
    nb = tmp_path / "nb"
    eid = "davis"
    d = nb / "experts" / eid
    d.mkdir(parents=True)
    thread_content = textwrap.dedent(f"""\
        # Expert thread — `{eid}`

        ## 2026-04

        <!-- strategy-page:start id="test-page-one" date="2026-04-16" watch="testwatch" -->
        ### Page: test-page-one
        body
        <!-- strategy-page:end -->

        <!-- strategy-expert-thread:start -->
        machine
        <!-- strategy-expert-thread:end -->
    """)
    (d / "thread.md").write_text(thread_content, encoding="utf-8")
    return nb


def test_build_graph_has_page_expert_and_watch(
    minimal_notebook: Path, tmp_path: Path
) -> None:
    out = tmp_path / "graph.json"
    vdir = tmp_path / "views"
    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "build_strategy_notebook_graph.py"),
            "--notebook-dir",
            str(minimal_notebook),
            "--out",
            str(out),
            "--views-dir",
            str(vdir),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data.get("schema_version", "").startswith("1.0.0")
    types = {n["type"] for n in data["nodes"]}
    assert "page" in types and "expert" in types and "watch" in types
    edge_types = {e["type"] for e in data["edges"]}
    assert "belongs_to_expert" in edge_types
    assert "belongs_to_watch" in edge_types
    w = json.loads((vdir / "watch-clusters.json").read_text(encoding="utf-8"))
    assert "testwatch" in w
    assert "test-page-one" in w["testwatch"]
