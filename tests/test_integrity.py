"""Tests for record integrity: validate-integrity and governance_checker."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def _load_validate_integrity():
    path = SCRIPTS / "validate-integrity.py"
    spec = importlib.util.spec_from_file_location("validate_integrity_mod", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def test_validate_integrity_exits_zero():
    """validate-integrity.py exits 0 when record is valid."""
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "validate-integrity.py"),
            "--user",
            "grace-mar",
            "--require-proposal-class",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"validate-integrity failed: {result.stderr or result.stdout}"


def test_governance_checker_exits_zero():
    """governance_checker.py exits 0 when no violations."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "governance_checker.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"governance_checker failed: {result.stderr or result.stdout}"


def test_validate_template_sync_contract_exits_zero():
    """validate_template_sync_contract.py exits 0 when contract and provenance align."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_template_sync_contract.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"validate_template_sync_contract failed: {result.stderr or result.stdout}"


def test_validate_integrity_json_mode():
    """validate-integrity --json emits valid JSON with ok and errors."""
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "validate-integrity.py"),
            "--user",
            "grace-mar",
            "--require-proposal-class",
            "--json",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "ok" in data
    assert "errors" in data
    assert isinstance(data["errors"], list)
    assert "identity_library_boundary" in data
    assert "ix_a_ok" in data["identity_library_boundary"]
    assert "identity_capability_ok" in data["identity_library_boundary"]


def test_validate_template_sync_contract_warns_on_target_applied_drift(tmp_path):
    contract_path = tmp_path / "instance-contract.json"
    source_path = tmp_path / "template-source.json"
    manifest_path = tmp_path / "template-manifest.json"
    contract_path.write_text(
        json.dumps(
            {
                "schemaVersion": "1.1.0",
                "instanceId": "demo",
                "templateRepo": "https://example.com/template",
                "templateVersionTarget": "0.5.0",
                "templateCommitTarget": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "syncArchitecture": {"appliedProvenancePath": "template-source.json"},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    source_path.write_text(
        json.dumps(
            {
                "schemaVersion": "1.1.0",
                "recordType": "templateAppliedProvenance",
                "companionSelfCommit": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "templateVersion": "0.4.0",
                "syncedAt": "2026-03-28T00:00:00Z",
                "syncedBy": "manual",
                "syncedPaths": ["docs/change-review.md"],
                "templateUpstream": {"repo": "https://example.com/template", "ref": "main"},
                "targetReference": {
                    "instanceContract": "instance-contract.json",
                    "templateVersionTarget": "0.5.0",
                    "templateCommitTarget": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                },
                "auxiliarySyncEvents": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    manifest_path.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "description": "cached mirror",
                "canonicalAsOf": "2026-03-28",
                "templateVersion": "0.5.0",
                "paths": [{"path": "docs/change-review.md", "description": "doc", "optional": False}],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    path = SCRIPTS / "validate_template_sync_contract.py"
    spec = importlib.util.spec_from_file_location("validate_template_sync_contract_mod", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)

    errors, warnings = mod.validate_sync_contract(contract_path, source_path, manifest_path)
    assert errors == []
    assert any("target/applied templateVersion differ" in warning for warning in warnings)
    assert any("target/applied companion-self commit differ" in warning for warning in warnings)


def test_validate_identity_capability_boundary_catches_obvious_bleed(tmp_path):
    user_dir = tmp_path / "demo"
    user_dir.mkdir()
    (user_dir / "self.md").write_text(
        """
## III. LINGUISTIC STYLE

I am a good writer.
""".strip()
        + "\n",
        encoding="utf-8",
    )
    (user_dir / "skill-write.md").write_text(
        """
## WRITE Container

self_concept: creative
""".strip()
        + "\n",
        encoding="utf-8",
    )

    mod = _load_validate_integrity()
    errors = mod.validate_identity_capability_boundary([user_dir])
    assert any("self capability self-description" in err for err in errors)
    assert any("write personality schema" in err for err in errors)
