"""Authority class → Comprehension Envelope / Reflection Gate recommendations."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
_s = str(_SCRIPTS)
if _s not in sys.path:
    sys.path.insert(0, _s)


def test_recommend_human_only_heavy() -> None:
    from authority_comprehension_defaults import recommend_for_authority_class

    r = recommend_for_authority_class("human_only")
    assert r["recommended_impact_tier"] == "boundary"
    assert r["recommended_envelope_class"] == "required"
    assert r["recommended_reflection_gate"] == "heavy"
    assert r["rationale"]


def test_recommend_draftable_fast_path() -> None:
    from authority_comprehension_defaults import recommend_for_authority_class

    r = recommend_for_authority_class("draftable")
    assert r["recommended_impact_tier"] == "low"
    assert r["recommended_envelope_class"] == "none"
    assert r["recommended_reflection_gate"] == "none"


def test_recommend_review_required_light() -> None:
    from authority_comprehension_defaults import recommend_for_authority_class

    r = recommend_for_authority_class("review_required")
    assert r["recommended_impact_tier"] == "medium"
    assert r["recommended_envelope_class"] == "optional"
    assert r["recommended_reflection_gate"] == "light"


def test_check_authority_json_memory_governance() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPTS / "check-authority.py"),
            "--surface",
            "memory_governance",
            "--json",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["surface"] == "memory_governance"
    assert data["authority_class"] == "human_only"
    assert data["recommended_envelope_class"] == "required"
    assert data["recommended_reflection_gate"] == "heavy"


def test_check_authority_json_prepared_context() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPTS / "check-authority.py"),
            "--surface",
            "prepared_context",
            "--json",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["authority_class"] == "draftable"
    assert data["recommended_envelope_class"] == "none"
    assert data["recommended_reflection_gate"] == "none"


def test_check_authority_legacy_stdout_unchanged() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPTS / "check-authority.py"),
            "--surface",
            "evidence",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert proc.stdout.strip() == "draftable"
