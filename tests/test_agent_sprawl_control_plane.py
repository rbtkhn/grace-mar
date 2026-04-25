from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "work_dev" / "audit_agent_sprawl.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("audit_agent_sprawl_mod", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _surface(
    surface_id: str,
    *,
    status: str = "implemented",
    category: str = "external_runtime",
    writes: list[str] | None = None,
    merge_authority: str = "none",
    canonical_record_access: str = "read-only",
    gate_effect: str = "none",
    receipt_required: bool = True,
    capability_contract: str = "docs/contracts/example.yaml",
    extra: dict | None = None,
) -> dict:
    payload = {
        "id": surface_id,
        "name": surface_id.replace("-", " ").title(),
        "status": status,
        "category": category,
        "reads": ["repo working tree"],
        "writes": writes if writes is not None else ["artifacts/example/"],
        "canonical_record_access": canonical_record_access,
        "merge_authority": merge_authority,
        "gate_effect": gate_effect,
        "receipt_required": receipt_required,
        "capability_contract": capability_contract,
        "owner_lane": "work-dev",
        "notes": "test fixture",
    }
    if extra:
        payload.update(extra)
    return payload


def _build_registry(root: Path, surfaces: list[dict]) -> Path:
    (root / "docs" / "contracts").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "contracts" / "example.yaml").write_text(
        "contract_id: test-v1\n",
        encoding="utf-8",
    )
    config_path = root / "config" / "agent-surfaces.v1.json"
    _write_json(config_path, {"schemaVersion": "1.0.0", "surfaces": surfaces})
    return config_path


def _run_cli(repo_root: Path, config_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(repo_root),
            "--config",
            str(config_path),
            *args,
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def test_clean_registry_passes(tmp_path: Path) -> None:
    config_path = _build_registry(
        tmp_path,
        [
            _surface("openclaw-export"),
            _surface(
                "doctrine-drift-radar",
                category="read_only_audit",
                canonical_record_access="read-only",
                gate_effect="advisory-only",
                receipt_required=False,
                capability_contract="",
                writes=[],
            ),
        ],
    )
    mod = _load_module()
    report = mod.audit_registry(config_path, tmp_path)
    assert report["ok"] is True
    assert report["errors"] == []
    assert report["warnings"] == []

    proc = _run_cli(tmp_path, config_path)
    assert proc.returncode == 0
    assert "0 errors, 0 warnings" in proc.stdout


def test_duplicate_id_fails(tmp_path: Path) -> None:
    config_path = _build_registry(
        tmp_path,
        [_surface("dup-surface"), _surface("dup-surface", writes=["artifacts/other/"])],
    )
    mod = _load_module()
    report = mod.audit_registry(config_path, tmp_path)
    assert report["ok"] is False
    assert any(item["kind"] == "duplicate_id" for item in report["errors"])


def test_merge_authority_not_none_fails(tmp_path: Path) -> None:
    config_path = _build_registry(
        tmp_path,
        [_surface("bad-merge", merge_authority="companion_gate")],
    )
    mod = _load_module()
    report = mod.audit_registry(config_path, tmp_path)
    assert any(item["kind"] == "merge_authority_must_be_none" for item in report["errors"])


def test_invalid_canonical_record_access_fails(tmp_path: Path) -> None:
    config_path = _build_registry(
        tmp_path,
        [_surface("bad-record-access", canonical_record_access="write")],
    )
    mod = _load_module()
    report = mod.audit_registry(config_path, tmp_path)
    assert any(item["kind"] == "invalid_canonical_record_access" for item in report["errors"])


def test_invalid_gate_effect_fails(tmp_path: Path) -> None:
    config_path = _build_registry(
        tmp_path,
        [_surface("bad-gate-effect", gate_effect="merge")],
    )
    mod = _load_module()
    report = mod.audit_registry(config_path, tmp_path)
    assert any(item["kind"] == "invalid_gate_effect" for item in report["errors"])


def test_missing_receipt_requirement_fails_unless_explicitly_exempt(tmp_path: Path) -> None:
    failing_config = _build_registry(
        tmp_path / "failing",
        [_surface("missing-receipt", receipt_required=False)],
    )
    passing_config = _build_registry(
        tmp_path / "passing",
        [
            _surface(
                "receipt-exempt",
                receipt_required=False,
                extra={"receipt_required_exempt": True},
            )
        ],
    )
    mod = _load_module()

    failing_report = mod.audit_registry(failing_config, tmp_path / "failing")
    assert any(item["kind"] == "missing_receipt_requirement" for item in failing_report["errors"])

    passing_report = mod.audit_registry(passing_config, tmp_path / "passing")
    assert passing_report["ok"] is True
    assert not any(item["kind"] == "missing_receipt_requirement" for item in passing_report["errors"])


def test_overlapping_write_categories_warn_but_exit_zero(tmp_path: Path) -> None:
    config_path = _build_registry(
        tmp_path,
        [
            _surface(
                "workbench-a",
                category="workbench_runner",
                capability_contract="",
                writes=["artifacts/work-dev/workbench-receipts/"],
            ),
            _surface(
                "workbench-b",
                category="workbench_runner",
                capability_contract="",
                writes=["artifacts/work-dev/workbench-receipts/"],
            ),
        ],
    )
    mod = _load_module()
    report = mod.audit_registry(config_path, tmp_path)
    assert report["ok"] is True
    assert report["errors"] == []
    assert any(item["kind"] == "overlapping_writes_same_category" for item in report["warnings"])

    proc = _run_cli(tmp_path, config_path)
    assert proc.returncode == 0
    assert "Warnings:" in proc.stdout


def test_json_output_includes_expected_top_level_keys(tmp_path: Path) -> None:
    config_path = _build_registry(
        tmp_path,
        [
            _surface("clean-surface"),
            _surface(
                "clean-audit",
                category="read_only_audit",
                canonical_record_access="read-only",
                gate_effect="advisory-only",
                receipt_required=False,
                capability_contract="",
                writes=[],
            ),
        ],
    )
    proc = _run_cli(tmp_path, config_path, "--json")
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert set(payload) >= {"errors", "warnings", "counts", "surfaces"}
    assert payload["counts"]["surfaces"] == 2
    assert isinstance(payload["errors"], list)
    assert isinstance(payload["warnings"], list)
    assert isinstance(payload["surfaces"], list)
