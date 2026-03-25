"""Control plane YAML validation and render stability."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.skipif(
    importlib.util.find_spec("jsonschema") is None,
    reason="jsonschema not installed",
)
def test_validate_control_plane_exits_zero() -> None:
    rc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "work_dev" / "validate_control_plane.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert rc.returncode == 0, rc.stderr + rc.stdout


def test_integration_status_enum_rejects_bad_status(tmp_path: Path) -> None:
    jsonschema = pytest.importorskip("jsonschema")
    bad = {
        "version": 1,
        "items": [
            {
                "id": "x",
                "title": "t",
                "surface": "s",
                "status": "not_a_real_status",
                "source_of_truth": ["README.md"],
                "notes": [],
            }
        ],
    }
    schema = json.loads(
        (REPO_ROOT / "schemas" / "work_dev" / "integration_status.schema.json").read_text(encoding="utf-8")
    )
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=bad, schema=schema)  # noqa: PT012


def test_rendered_integration_status_exists_and_has_banner() -> None:
    p = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "generated" / "integration-status.generated.md"
    assert p.is_file()
    text = p.read_text(encoding="utf-8")
    assert "GENERATED FILE" in text
    assert "identity_export_openclaw_hook" in text
