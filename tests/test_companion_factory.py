"""Tests for scripts/companion_factory.py."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from tests.conftest import REPO_ROOT, repo_python, run_cmd


def test_companion_factory_new_minimal_template(tmp_path) -> None:
    tpl = tmp_path / "template-root"
    seed = tpl / "users" / "_template" / "seed-phase"
    seed.mkdir(parents=True)
    for name in (
        "seed-phase-manifest.json",
        "seed_intake.json",
        "seed_intent.json",
        "seed_identity.json",
        "seed_curiosity.json",
        "seed_pedagogy.json",
        "seed_expression.json",
        "seed_memory_contract.json",
        "memory_ops_contract.json",
        "seed_trial_report.json",
        "seed_readiness.json",
        "seed_confidence_map.json",
        "work_business_seed.json",
        "work_dev_seed.json",
        "seed_constitution.json",
    ):
        shutil.copy2(REPO_ROOT / "users" / "_template" / "seed-phase" / name, seed / name)
    shutil.copy2(REPO_ROOT / "users" / "_template" / "seed-phase" / "README.md", seed / "README.md")
    shutil.copy2(REPO_ROOT / "users" / "_template" / "seed-phase" / "seed_dossier.md", seed / "seed_dossier.md")
    (tpl / "template-manifest.json").write_text(
        json.dumps({"templateVersion": "9.9.9-test"}) + "\n", encoding="utf-8"
    )

    out_parent = tmp_path / "out"
    out_parent.mkdir()

    result = run_cmd(
        [
            repo_python(),
            "scripts/companion_factory.py",
            "new",
            "demo-factory-user",
            "--template",
            str(tpl),
            "--output-dir",
            str(out_parent),
        ],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr

    dest = out_parent / "demo-factory-user"
    assert dest.is_dir()
    inst_seed = dest / "users" / "demo-factory-user" / "seed-phase"
    assert (inst_seed / "seed_intake.json").is_file()
    man = json.loads((inst_seed / "seed-phase-manifest.json").read_text(encoding="utf-8"))
    assert man["user_slug"] == "demo-factory-user"
    meta = json.loads((dest / "instance-metadata.json").read_text(encoding="utf-8"))
    assert meta["instance_id"] == "demo-factory-user"
    assert meta["template_version"] == "9.9.9-test"
