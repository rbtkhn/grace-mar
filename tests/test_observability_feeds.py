"""Integration tests: lane_scope and continuity_blocks JSONL feeds (work-dev observability)."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def test_append_lane_violation_event_writes_jsonl(tmp_path: Path) -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_lane_scope import append_lane_violation_event

    append_lane_violation_event(
        tmp_path,
        lane="work-dev",
        files=["docs/x.md"],
        detail="declared_lane_failed",
    )
    p = tmp_path / "runtime" / "observability" / "lane_scope.jsonl"
    assert p.is_file()
    obj = json.loads(p.read_text(encoding="utf-8").strip().splitlines()[0])
    assert obj["event"] == "lane_violation"
    assert obj["lane"] == "work-dev"
    assert obj["files"] == ["docs/x.md"]
    assert obj["detail"] == "declared_lane_failed"
    assert "ts" in obj


def test_append_continuity_block_event_writes_jsonl(tmp_path: Path) -> None:
    sys.path.insert(0, str(SCRIPTS))
    from require_continuity_for_handback import append_continuity_block_event

    append_continuity_block_event(
        tmp_path,
        user_id="grace-mar",
        reason="no valid continuity receipt",
        source="test",
    )
    p = tmp_path / "runtime" / "observability" / "continuity_blocks.jsonl"
    assert p.is_file()
    obj = json.loads(p.read_text(encoding="utf-8").strip().splitlines()[0])
    assert obj["event"] == "continuity_block"
    assert obj["user_id"] == "grace-mar"
    assert obj["reason"] == "no valid continuity receipt"
    assert obj["source"] == "test"
    assert "ts" in obj


@pytest.fixture
def tmp_lane_repo(tmp_path: Path) -> Path:
    """Minimal git repo + lanes.yaml with forbidden path bad/**."""
    repo = tmp_path / "repo"
    (repo / "docs" / "work-dev").mkdir(parents=True)
    (repo / "bad").mkdir(parents=True)
    (repo / "docs" / "work-dev" / "ok.md").write_text("ok", encoding="utf-8")
    (repo / "bad" / "nope.md").write_text("x", encoding="utf-8")
    cfg = {
        "version": 1,
        "lanes": {
            "work-dev": {
                "owned_paths": ["docs/work-dev/**"],
                "allowed_shared_paths": ["README.md"],
                "forbidden_paths": ["bad/**"],
            }
        },
    }
    (repo / "lanes.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    (repo / "scripts").mkdir()
    shutil.copy(SCRIPTS / "check_lane_scope.py", repo / "scripts" / "check_lane_scope.py")
    init = subprocess.run(["git", "init"], cwd=repo, capture_output=True, text=True)
    if init.returncode != 0:
        pytest.skip(f"git init failed: {init.stderr}")
    subprocess.run(["git", "config", "user.email", "t@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)
    return repo


@pytest.mark.skipif(
    subprocess.run(["git", "version"], capture_output=True).returncode != 0,
    reason="git not available",
)
def test_cli_check_lane_scope_append_observability_on_failure(tmp_lane_repo: Path) -> None:
    rc = subprocess.run(
        [
            sys.executable,
            str(tmp_lane_repo / "scripts" / "check_lane_scope.py"),
            "--lane",
            "work-dev",
            "--lanes-yaml",
            str(tmp_lane_repo / "lanes.yaml"),
            "--repo-root",
            str(tmp_lane_repo),
            "--files",
            "bad/nope.md",
            "--append-observability",
        ],
        cwd=tmp_lane_repo,
        capture_output=True,
        text=True,
    )
    assert rc.returncode == 1, rc.stdout + rc.stderr
    obs = tmp_lane_repo / "runtime" / "observability" / "lane_scope.jsonl"
    assert obs.is_file(), "expected lane_scope.jsonl after failed check with --append-observability"
    obj = json.loads(obs.read_text(encoding="utf-8").strip().splitlines()[0])
    assert obj["event"] == "lane_violation"
    assert obj["lane"] == "work-dev"
    assert "bad/nope.md" in obj.get("files", [])
