"""PR lane resolution from simulated GitHub event payload."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def rpl():
    import sys

    sdir = str(REPO_ROOT / "scripts")
    if sdir not in sys.path:
        sys.path.insert(0, sdir)
    import resolve_pr_lane as mod

    return mod


def test_resolve_single_lane_label(rpl) -> None:
    out = rpl.resolve({"body": "", "labels": [{"name": "lane/work-dev"}]})
    assert out[0] == "work-dev"
    assert out[1] is False
    assert out[2] == ""


def test_resolve_cross_lane_requires_justification(rpl) -> None:
    pr = {
        "body": "### Cross-lane justification\n\n```text\nwire bot + work-dev\n```",
        "labels": [{"name": "lane/cross"}, {"name": "lane/work-dev"}],
    }
    out = rpl.resolve(pr)
    assert out[0] == "work-dev"
    assert out[1] is True
    assert "wire bot" in out[2]


def test_resolve_missing_label_errors(rpl) -> None:
    out = rpl.resolve({"body": "", "labels": []})
    assert out[0] is None


def test_main_writes_github_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, rpl) -> None:
    event = {
        "pull_request": {
            "body": "",
            "labels": [{"name": "lane/companion-record"}],
        }
    }
    ev = tmp_path / "event.json"
    ev.write_text(json.dumps(event), encoding="utf-8")
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(ev))
    out_env = tmp_path / "env"
    monkeypatch.setenv("GITHUB_ENV", str(out_env))

    assert rpl.main() == 0
    text = out_env.read_text(encoding="utf-8")
    assert "PR_LANE=companion-record" in text
    assert "ALLOW_CROSS_LANE=false" in text
