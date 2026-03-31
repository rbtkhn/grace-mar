"""Tests for scripts/generate-seed-dossier.py (importlib load — hyphenated filename)."""

import importlib.util
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_generate_seed_dossier():
    path = REPO_ROOT / "scripts" / "generate-seed-dossier.py"
    spec = importlib.util.spec_from_file_location("generate_seed_dossier_mod", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["generate_seed_dossier_mod"] = mod
    spec.loader.exec_module(mod)
    return mod


def _run_generator(mod, directory: Path) -> str:
    old_argv = sys.argv[:]
    try:
        sys.argv = ["generate-seed-dossier.py", str(directory)]
        mod.main()
    finally:
        sys.argv = old_argv
    return (directory / "seed_dossier.md").read_text(encoding="utf-8")


def test_generate_seed_dossier_includes_cadence_ritual(tmp_path):
    mod = _load_generate_seed_dossier()
    target = tmp_path / "seed-phase"
    shutil.copytree(REPO_ROOT / "users" / "demo" / "seed-phase", target)

    text = _run_generator(mod, target)

    assert "## Cadence Ritual" in text
    assert "Default **coffee**; active **coffee**; source **default**." in text
    assert "Offer threshold: 3 successful uses; 2 distinct days; 2 successful follow-through uses." in text


def test_generate_seed_dossier_omits_cadence_ritual_when_absent(tmp_path):
    mod = _load_generate_seed_dossier()
    target = tmp_path / "seed-phase"
    shutil.copytree(REPO_ROOT / "users" / "demo" / "seed-phase", target)

    intake_path = target / "seed_intake.json"
    intake = json.loads(intake_path.read_text(encoding="utf-8"))
    intake.pop("cadence_preference", None)
    intake_path.write_text(json.dumps(intake, indent=2) + "\n", encoding="utf-8")

    text = _run_generator(mod, target)

    assert "## Cadence Ritual" not in text
