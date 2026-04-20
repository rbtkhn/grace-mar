"""Tests for scripts/runtime/review_orchestrator.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "runtime" / "review_orchestrator.py"
RO_MOD = REPO_ROOT / "scripts" / "runtime" / "review_orchestrator.py"

EXPECTED_PHASE_IDS: tuple[str, ...] = (
    "phase_1_retrieval",
    "phase_2_invalidators",
    "phase_3_boundary",
    "phase_4_promotion_risk",
    "phase_5_synthesis",
    "phase_6_operator_questions",
)


def _base_obs(oid: str, lane: str, summary: str, refs: list[str]) -> dict:
    return {
        "obs_id": oid,
        "timestamp": "2026-01-01T12:00:00Z",
        "lane": lane,
        "source_kind": "evidence_ref",
        "title": "t",
        "summary": summary,
        "record_mutation_candidate": False,
        "source_path": None,
        "source_refs": refs,
        "tags": [],
        "confidence": 0.9,
        "contradiction_refs": [],
        "notes": None,
    }


def test_build_review_packet_markdown_unit():
    sys.path.insert(0, str(REPO_ROOT / "scripts" / "runtime"))
    import importlib.util

    mod_name = "review_orchestrator_test_fixture"
    spec = importlib.util.spec_from_file_location(mod_name, RO_MOD)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)

    env = {
        "evidence_state": "sufficient",
        "fabricated_history_risk": "low",
        "reasons": ["r1"],
        "missing_evidence_refs": [],
        "conflicting_refs": [],
        "promotion_recommendation": "allow",
    }
    obs = [_base_obs("obs_20260101T120000Z_aaaaaaaa", "work-strategy", "a", ["x"])]
    anchor = mod.ReviewAnchor(
        task_anchor="Unit-test task anchor",
        constraint_anchor="Stay within fixture observations.",
        active_scope="pre_gate; lane=work-strategy; obs=obs_20260101T120000Z_aaaaaaaa",
    )
    md, phase_checks, phase_results = mod.build_review_packet_markdown(
        mode="pre_gate",
        built_iso="2026-01-01T00:00:00Z",
        target_label="obs_20260101T120000Z_aaaaaaaa",
        observations=obs,
        env=env,
        candidate_row=None,
        gate_text_derived=False,
        anchor=anchor,
    )
    assert [pr.phase_id for pr in phase_results] == list(mod.PHASE_ORDER)
    assert [pr.phase_id for pr in phase_results] == list(EXPECTED_PHASE_IDS)
    assert all(pr.status == "completed" for pr in phase_results)
    assert "# Review Packet" in md
    assert "## Task Anchor" in md
    assert "Unit-test task anchor" in md
    assert "pre_gate; lane=work-strategy" in md
    assert "## Evidence Pass" in md
    assert "Anchor fidelity" in md
    assert "## Contradiction Pass" in md
    assert "## Boundary Pass" in md
    assert "## Promotion-Risk Pass" in md
    assert "## Synthesis" in md
    assert "## Operator Questions" in md
    assert len(phase_checks) == 6
    assert phase_checks[0]["phase"] == "evidence_pass"
    assert phase_checks[0]["scope_drift_risk"] in ("low", "medium", "high")


def test_task_anchor_required_exit_code():
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--mode",
            "candidate_review",
            "--candidate",
            "CANDIDATE-0001",
            "--user",
            "grace-mar",
            "--repo-root",
            str(REPO_ROOT),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 2
    assert "task-anchor" in r.stderr.lower()


def test_pre_gate_subprocess(tmp_path: Path) -> None:
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    a = _base_obs("obs_20260101T120000Z_aaaaaaaa", "lane-a", "one", ["ref/1"])
    b = _base_obs("obs_20260101T130000Z_bbbbbbbb", "lane-a", "two", ["ref/2"])
    b["timestamp"] = "2026-01-01T13:00:00Z"
    (obs_dir / "index.jsonl").write_text(json.dumps(a) + "\n" + json.dumps(b) + "\n", encoding="utf-8")
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--mode",
            "pre_gate",
            "--lane",
            "lane-a",
            "--id",
            a["obs_id"],
            "--id",
            b["obs_id"],
            "--task-anchor",
            "Assess observations before staging to gate.",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )
    assert r.returncode == 0, r.stderr
    assert "Evidence Pass" in r.stdout
    assert "## Task Anchor" in r.stdout
    assert "Assess observations before staging to gate." in r.stdout
    assert a["obs_id"] in r.stdout


def test_candidate_review_subprocess(tmp_path: Path) -> None:
    user = "testuser"
    udir = tmp_path / "users" / user
    udir.mkdir(parents=True)
    gate = udir / "recursion-gate.md"
    gate.write_text(
        """## Candidates

### CANDIDATE-9999 (orchestrator fixture)

```yaml
status: pending
timestamp: 2026-01-15T12:00:00Z
summary: Fixture summary for packet
mind_category: knowledge
profile_target: IX-A.1
```

## Processed
""",
        encoding="utf-8",
    )
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--mode",
            "candidate_review",
            "--candidate",
            "CANDIDATE-9999",
            "--user",
            user,
            "--repo-root",
            str(tmp_path),
            "--task-anchor",
            "Review pending candidate for gate hygiene.",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    assert "CANDIDATE-9999" in r.stdout
    assert "gate-text-derived" in r.stdout
    assert "Boundary Pass" in r.stdout
    assert "Review pending candidate for gate hygiene." in r.stdout


def test_receipt_out_json(tmp_path: Path) -> None:
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    a = _base_obs("obs_20260101T120000Z_aaaaaaaa", "lane-a", "one", ["ref/1"])
    (obs_dir / "index.jsonl").write_text(json.dumps(a) + "\n", encoding="utf-8")
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    receipt_path = tmp_path / "anchor-receipt.json"
    out_md = tmp_path / "packet.md"
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--mode",
            "pre_gate",
            "--lane",
            "lane-a",
            "--id",
            a["obs_id"],
            "--task-anchor",
            "Receipt test anchor",
            "--constraint-anchor",
            "Do not broaden.",
            "--receipt-out",
            str(receipt_path),
            "-o",
            str(out_md),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert data["non_canonical"] is True
    assert data["mode"] == "pre_gate"
    assert data["target"] == a["obs_id"]
    assert data["anchor"]["task_anchor"] == "Receipt test anchor"
    assert data["anchor"]["constraint_anchor"] == "Do not broaden."
    assert "lane-a" in data["anchor"]["active_scope"]
    assert len(data["phase_anchor_checks"]) == 6
    for row in data["phase_anchor_checks"]:
        assert "phase" in row
        assert "scope_drift_risk" in row
    assert "phase_sequence" in data
    assert len(data["phase_sequence"]) == 6
    assert [row["phase_id"] for row in data["phase_sequence"]] == list(EXPECTED_PHASE_IDS)
    for row in data["phase_sequence"]:
        assert row["status"] == "completed"
        assert "summary" in row
        assert isinstance(row["summary"], list)
        assert "halt_recommended" in row
        assert "halt_reason" in row
    assert data["run_id"].startswith("ro_")
    # stdout empty when -o used (md goes to file)
    assert out_md.read_text(encoding="utf-8").startswith("# Review Packet")


def test_orchestrator_outputs_only_operator_paths(tmp_path: Path) -> None:
    """Read-only: script writes only paths the test passes (no canonical Record targets)."""
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    a = _base_obs("obs_20260101T120000Z_aaaaaaaa", "lane-a", "one", ["ref/1"])
    (obs_dir / "index.jsonl").write_text(json.dumps(a) + "\n", encoding="utf-8")
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    receipt_path = tmp_path / "out" / "receipt.json"
    out_md = tmp_path / "out" / "packet.md"
    receipt_path.parent.mkdir(parents=True)
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--mode",
            "pre_gate",
            "--lane",
            "lane-a",
            "--id",
            a["obs_id"],
            "--task-anchor",
            "Read-only path test",
            "--receipt-out",
            str(receipt_path),
            "-o",
            str(out_md),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )
    assert r.returncode == 0, r.stderr
    assert receipt_path.is_file()
    assert out_md.is_file()
    data = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert data["non_canonical"] is True
