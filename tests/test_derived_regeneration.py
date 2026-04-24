"""Tests for repo-owned derived regeneration helpers and scripts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from derived_regeneration import (  # noqa: E402
    TARGETS_BY_ID,
    build_manifest_payload,
    expand_with_downstream,
    select_targets_for_paths,
    topologically_sort_targets,
)

CHANGE_DETECTOR = REPO_ROOT / "scripts" / "canonical_change_detector.py"
REGEN = REPO_ROOT / "scripts" / "regenerate_all_derived.py"
BUILD_MANIFEST = REPO_ROOT / "scripts" / "build_derived_regeneration_manifest.py"
REPORT_HEALTH = REPO_ROOT / "scripts" / "report_rebuild_health.py"


def _run(args: list[str | Path], *, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *map(str, args)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=check,
    )


def test_select_targets_for_self_library_change() -> None:
    selected = select_targets_for_paths(["users/grace-mar/self-library.md"])
    ids = {target.target_id for target in selected}
    assert "library-index" in ids
    assert "review-dashboard" not in ids


def test_select_targets_for_recursion_gate_change() -> None:
    selected = select_targets_for_paths(["users/grace-mar/recursion-gate.md"])
    ids = {target.target_id for target in selected}
    assert "review-dashboard" in ids
    assert "gate-board" in ids
    assert "governance-posture" in ids


def test_change_detector_json_reports_matching_target() -> None:
    proc = _run(
        [
            CHANGE_DETECTOR,
            "--paths",
            "users/grace-mar/self-library.md",
            "--json",
        ]
    )
    payload = json.loads(proc.stdout)
    assert payload["changedPaths"] == ["users/grace-mar/self-library.md"]
    target_ids = {row["targetId"] for row in payload["targets"]}
    assert "library-index" in target_ids


def test_expand_with_downstream_adds_lane_dashboards() -> None:
    selected = [TARGETS_BY_ID["work-lanes-dashboard-json"]]
    expanded = expand_with_downstream(selected)
    ids = [target.target_id for target in topologically_sort_targets(expanded)]
    assert ids.index("work-lanes-dashboard-json") < ids.index("lane-dashboards")


def test_regenerate_all_derived_dry_run_writes_receipt(tmp_path: Path) -> None:
    receipt = tmp_path / "receipt.json"
    proc = _run(
        [
            REGEN,
            "--paths",
            "users/grace-mar/self-library.md",
            "--dry-run",
            "--receipt-output",
            receipt,
        ]
    )
    assert proc.returncode == 0, proc.stderr
    assert receipt.is_file()
    payload = json.loads(receipt.read_text(encoding="utf-8"))
    assert payload["receiptKind"] == "derived_rebuild"
    assert payload["resultStatus"] == "dry_run"
    assert payload["recordAuthority"] == "none"
    assert payload["gateEffect"] == "none"
    assert payload["targets"][0]["targetId"] == "library-index"


def test_build_manifest_payload_has_dependency_data() -> None:
    payload = build_manifest_payload()
    assert payload["schemaVersion"] == "1.0.0-derived-regeneration-manifest"
    targets = {row["targetId"]: row for row in payload["targets"]}
    assert "derived-regeneration-manifest" in targets
    assert targets["lane-dashboards"]["dependsOn"] == ["work-lanes-dashboard-json"]


def test_build_manifest_script_writes_manifest(tmp_path: Path) -> None:
    out = tmp_path / "manifest.json"
    proc = _run([BUILD_MANIFEST, "--output", out])
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["recordAuthority"] == "none"
    assert payload["gateEffect"] == "none"


def test_report_rebuild_health_summarizes_receipts(tmp_path: Path) -> None:
    receipts_dir = tmp_path / "receipts"
    receipts_dir.mkdir()
    receipt = {
        "receiptKind": "derived_rebuild",
        "createdAt": "2026-04-24T12:00:00Z",
        "targets": [{"targetId": "library-index", "elapsedMs": 12}],
        "resultStatus": "ok",
        "recordAuthority": "none",
        "gateEffect": "none",
    }
    (receipts_dir / "r1.json").write_text(json.dumps(receipt), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps(build_manifest_payload()), encoding="utf-8")
    out = tmp_path / "summary.json"
    proc = _run(
        [
            REPORT_HEALTH,
            "--receipts-dir",
            receipts_dir,
            "--manifest",
            manifest,
            "--output",
            out,
        ]
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["recordAuthority"] == "none"
    assert payload["gateEffect"] == "none"
    assert payload["receiptCount"] == 1
    assert payload["manifestTargetCount"] >= 1


def test_target_registry_contains_expected_foundation_targets() -> None:
    expected = {
        "derived-regeneration-manifest",
        "library-index",
        "work-lanes-dashboard-json",
        "lane-dashboards",
        "review-dashboard",
        "gate-board",
        "governance-posture",
        "strategy-notebook-graph",
    }
    assert expected.issubset(TARGETS_BY_ID.keys())
