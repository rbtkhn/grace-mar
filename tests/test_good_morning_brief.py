"""Tests for scripts/good-morning-brief.py (importlib load — hyphenated filename)."""

import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_gmb():
    path = REPO_ROOT / "scripts" / "good-morning-brief.py"
    spec = importlib.util.spec_from_file_location("good_morning_brief_mod", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["good_morning_brief_mod"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_user_profile_dir():
    mod = _load_gmb()
    r = Path("/tmp/r")
    assert mod.user_profile_dir(r, "x") == r / "users" / "x"


def test_detect_tone_from_memory():
    mod = _load_gmb()
    assert mod._detect_tone_from_memory("Preferred warm-direct tone") == "warm-direct"
    assert mod._detect_tone_from_memory("nothing") == "analytical-crisp"


def test_save_daily_intention(tmp_path):
    mod = _load_gmb()
    repo = tmp_path / "repo"
    prof = mod.user_profile_dir(repo, "u1")
    prof.mkdir(parents=True)
    d = date(2026, 3, 10)
    out = mod.save_daily_intention(prof, d, "Ship the brief")
    assert out.name == "DAILY-INTENTION-2026-03-10.md"
    body = out.read_text(encoding="utf-8")
    assert "Ship the brief" in body
    assert "not part of the record" in body.lower()


def test_yesterday_intention_found(tmp_path):
    mod = _load_gmb()
    repo = tmp_path / "repo"
    prof = mod.user_profile_dir(repo, "u1")
    (prof / "reflection-proposals").mkdir(parents=True)
    today = date(2026, 3, 15)
    y = today - timedelta(days=1)
    (prof / "reflection-proposals" / f"DAILY-INTENTION-{y.isoformat()}.md").write_text(
        "# Daily\n\nYesterday focus text here.",
        encoding="utf-8",
    )
    got = mod._yesterday_intention(prof, today)
    assert got and "Yesterday focus" in got


def test_yesterday_intention_missing(tmp_path):
    mod = _load_gmb()
    prof = tmp_path / "repo" / "users" / "u1"
    prof.mkdir(parents=True)
    assert mod._yesterday_intention(prof, date(2026, 1, 5)) is None


def test_run_brief_minimal_no_crash(tmp_path, monkeypatch):
    mod = _load_gmb()
    repo = tmp_path / "repo"
    prof = mod.user_profile_dir(repo, "u1")
    (prof / "seed").mkdir(parents=True)
    (prof / "seed" / "minimal-core.json").write_text(
        '{"instanceName": "u1", "coreFacts": ["alpha"]}',
        encoding="utf-8",
    )
    # intention empty; ask() for format uses default "1"
    monkeypatch.setattr("builtins.input", lambda _="": "")
    mod.run_brief(repo_root=repo, user_id="u1", skip_warmup_prompt=True)
