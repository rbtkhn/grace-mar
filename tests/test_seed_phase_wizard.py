"""Tests for scripts/seed-phase-wizard.py (importlib load — hyphenated filename)."""

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from repo_io import CANONICAL_RECORD_FILES_REQUIRED


def _load_seed_wizard():
    path = REPO_ROOT / "scripts" / "seed-phase-wizard.py"
    spec = importlib.util.spec_from_file_location("seed_phase_wizard_mod", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["seed_phase_wizard_mod"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_user_profile_dir():
    mod = _load_seed_wizard()
    r = Path("/tmp/fake-repo")
    assert mod.user_profile_dir(r, "ab") == r / "users" / "ab"


def test_canonical_record_ready_false_when_empty(tmp_path):
    mod = _load_seed_wizard()
    repo = tmp_path / "repo"
    (repo / "users" / "u1").mkdir(parents=True)
    assert mod.canonical_record_ready(repo, "u1") is False


def test_canonical_record_ready_true_when_all_present(tmp_path):
    mod = _load_seed_wizard()
    repo = tmp_path / "repo"
    prof = repo / "users" / "u1"
    prof.mkdir(parents=True)
    for name in CANONICAL_RECORD_FILES_REQUIRED:
        (prof / name).write_text("# stub\n", encoding="utf-8")
    assert mod.canonical_record_ready(repo, "u1") is True


def test_append_good_morning_creates_memory(tmp_path):
    mod = _load_seed_wizard()
    repo = tmp_path / "repo"
    prof = mod.user_profile_dir(repo, "u1")
    prof.mkdir(parents=True)
    mod.append_good_morning_tone_memory(
        prof, "warm-direct", when="2026-01-01T00:00:00Z", repo_root=repo
    )
    mem = (prof / "self-memory.md").read_text(encoding="utf-8")
    assert "warm-direct" in mem
    assert "Seed wizard" in mem


def test_append_good_morning_appends_existing(tmp_path):
    mod = _load_seed_wizard()
    repo = tmp_path / "repo"
    prof = mod.user_profile_dir(repo, "u1")
    prof.mkdir(parents=True)
    (prof / "self-memory.md").write_text("# MEMORY\n\n## Long-term\n\n- x\n", encoding="utf-8")
    mod.append_good_morning_tone_memory(
        prof, "curious-playful", when="2026-02-01T00:00:00Z", repo_root=repo
    )
    text = (prof / "self-memory.md").read_text(encoding="utf-8")
    assert "curious-playful" in text
    assert "- x" in text


def test_save_file_writes_relative_message(tmp_path, capsys):
    mod = _load_seed_wizard()
    repo = tmp_path / "repo"
    target = repo / "users" / "u1" / "reflection-proposals" / "x.md"
    mod.save_file(target, "body\n", repo_root=repo)
    assert target.read_text(encoding="utf-8") == "body\n"
    out = capsys.readouterr().out
    assert "users/u1/reflection-proposals/x.md" in out.replace("\\", "/")
