"""Tests for lane scope checker and path inference."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from check_lane_scope import (  # noqa: E402
    check_any_lane,
    check_lane,
    load_lanes,
    path_matches_glob,
)
from infer_lane_from_paths import infer_dominant  # noqa: E402


def test_path_matches_glob_starstar() -> None:
    assert path_matches_glob("docs/skill-work/work-dev/README.md", "docs/skill-work/work-dev/**")
    assert path_matches_glob("docs/skill-work/work-dev/a/b.md", "docs/skill-work/work-dev/**")
    assert not path_matches_glob("docs/skill-work/work-jiang/x.md", "docs/skill-work/work-dev/**")
    assert path_matches_glob("tests/test_work_jiang_foo.py", "tests/test_work_jiang*.py")


def test_check_lane_work_dev_clean() -> None:
    doc = load_lanes(REPO_ROOT / "lanes.yaml")
    code, msgs = check_lane(
        "work-dev",
        ["docs/skill-work/work-dev/README.md", "scripts/work_dev/foo.py"],
        doc,
        allow_cross_lane=False,
        justification="",
    )
    assert code == 0
    assert any("OK" in m for m in msgs)


def test_check_lane_forbidden_work_jiang() -> None:
    doc = load_lanes(REPO_ROOT / "lanes.yaml")
    code, msgs = check_lane(
        "work-dev",
        ["research/external/work-jiang/metadata/sources.yaml"],
        doc,
        allow_cross_lane=False,
        justification="",
    )
    assert code == 1
    assert any("FORBIDDEN" in m for m in msgs)


def test_shared_allowlisted() -> None:
    doc = load_lanes(REPO_ROOT / "lanes.yaml")
    code, _ = check_lane(
        "work-dev",
        ["README.md"],
        doc,
        allow_cross_lane=False,
        justification="",
    )
    assert code == 0


def test_mixed_fails_without_override() -> None:
    doc = load_lanes(REPO_ROOT / "lanes.yaml")
    code, msgs = check_lane(
        "work-dev",
        ["docs/skill-work/work-politics/README.md"],
        doc,
        allow_cross_lane=False,
        justification="",
    )
    assert code == 1
    assert any("OUT_OF_SCOPE" in m for m in msgs)


def test_allow_cross_lane_requires_justification() -> None:
    doc = load_lanes(REPO_ROOT / "lanes.yaml")
    code, msgs = check_lane(
        "work-dev",
        ["docs/skill-work/work-politics/README.md"],
        doc,
        allow_cross_lane=True,
        justification="",
    )
    assert code == 1
    assert any("justification" in m.lower() for m in msgs)


def test_allow_cross_lane_with_justification() -> None:
    doc = load_lanes(REPO_ROOT / "lanes.yaml")
    code, msgs = check_lane(
        "work-dev",
        ["docs/skill-work/work-politics/README.md"],
        doc,
        allow_cross_lane=True,
        justification="cross-lane doc sync",
    )
    assert code == 0


def test_infer_dominant_single_lane() -> None:
    doc = load_lanes(REPO_ROOT / "lanes.yaml")
    assert infer_dominant(["docs/skill-work/work-dev/README.md"], doc) == "work-dev"


def test_infer_mixed_two_lanes() -> None:
    doc = load_lanes(REPO_ROOT / "lanes.yaml")
    assert (
        infer_dominant(
            [
                "docs/skill-work/work-dev/README.md",
                "research/external/work-jiang/README.md",
            ],
            doc,
        )
        == "mixed"
    )


def test_infer_work_strategy_lane() -> None:
    doc = load_lanes(REPO_ROOT / "lanes.yaml")
    assert (
        infer_dominant(
            [
                "docs/skill-work/work-strategy/README.md",
                "research/prototypes/mind-synthesis.py",
            ],
            doc,
        )
        == "work-strategy"
    )


def test_infer_unclassified() -> None:
    doc = {"lanes": {"a": {"owned_paths": ["only-a/**"]}}}
    assert infer_dominant([], doc) == "unclassified"
    assert infer_dominant(["zzz/unknown.txt"], doc) == "unclassified"


def test_check_any_lane_matches_work_jiang() -> None:
    doc = load_lanes(REPO_ROOT / "lanes.yaml")
    code, msgs, _matched = check_any_lane(
        ["research/external/work-jiang/metadata/sources.yaml"],
        doc,
    )
    assert code == 0
    assert any("work-jiang" in m or "matched" in m for m in msgs)


def test_check_any_lane_mixed_fails() -> None:
    doc = load_lanes(REPO_ROOT / "lanes.yaml")
    code, _, _matched = check_any_lane(
        [
            "docs/skill-work/work-dev/README.md",
            "research/external/work-jiang/README.md",
        ],
        doc,
    )
    assert code == 1


def test_infer_multi_owner_path_is_mixed() -> None:
    doc = {
        "lanes": {
            "x": {"owned_paths": ["shared/**"]},
            "y": {"owned_paths": ["shared/**"]},
        }
    }
    assert infer_dominant(["shared/file.txt"], doc) == "mixed"


@pytest.fixture
def tmp_lanes(tmp_path: Path) -> Path:
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
    p = tmp_path / "lanes.yaml"
    p.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return p


def test_check_lane_uses_custom_yaml(tmp_lanes: Path) -> None:
    doc = load_lanes(tmp_lanes)
    code, _ = check_lane(
        "work-dev",
        ["docs/work-dev/x.md"],
        doc,
        allow_cross_lane=False,
        justification="",
    )
    assert code == 0
    code2, _ = check_lane(
        "work-dev",
        ["bad/x.md"],
        doc,
        allow_cross_lane=False,
        justification="",
    )
    assert code2 == 1


@pytest.mark.skipif(
    subprocess.run(["git", "version"], capture_output=True).returncode != 0,
    reason="git not available",
)
def test_cli_check_lane_scope(tmp_path: Path, tmp_lanes: Path) -> None:
    import shutil

    repo = tmp_path / "repo"
    (repo / "docs" / "work-dev").mkdir(parents=True)
    (repo / "docs" / "work-dev" / "a.md").write_text("x", encoding="utf-8")
    init = subprocess.run(["git", "init"], cwd=repo, capture_output=True, text=True)
    if init.returncode != 0:
        pytest.skip(f"git init failed: {init.stderr}")
    subprocess.run(["git", "config", "user.email", "t@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True, capture_output=True)
    (repo / "lanes.yaml").write_text(tmp_lanes.read_text(encoding="utf-8"), encoding="utf-8")
    (repo / "scripts").mkdir()
    shutil.copy(SCRIPTS / "check_lane_scope.py", repo / "scripts" / "check_lane_scope.py")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)
    rc = subprocess.run(
        [
            sys.executable,
            str(repo / "scripts" / "check_lane_scope.py"),
            "--lane",
            "work-dev",
            "--lanes-yaml",
            str(repo / "lanes.yaml"),
            "--repo-root",
            str(repo),
            "--files",
            "docs/work-dev/a.md",
        ],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert rc.returncode == 0, rc.stderr
