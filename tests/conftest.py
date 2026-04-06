"""Pytest configuration and shared fixtures for Grace-Mar tests."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "seed-phase"
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def repo_python() -> str:
    return sys.executable


def run_cmd(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd or REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


@pytest.fixture
def tmp_seed_dir(tmp_path: Path) -> Path:
    d = tmp_path / "seed-phase"
    d.mkdir(parents=True, exist_ok=True)
    return d


def copy_fixture(name: str, target: Path) -> Path:
    src = FIXTURES_DIR / name
    if not src.is_dir():
        raise FileNotFoundError(src)
    shutil.copytree(src, target, dirs_exist_ok=True)
    return target
