"""Focused tests for the self-proposals auto-research lane."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LANE = ROOT / "auto-research" / "self-proposals"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _sample_payload() -> dict:
    return {
        "hypothesis": "Grounded proposals with explicit source exchange are easier to review safely.",
        "expected_delta": 0.08,
        "grounding_mode": "strict",
        "proposal_type": "recursion_gate_candidate",
        "target_surface": "self",
        "candidate_bundle": {
            "title": "Auto-research grounded proposal",
            "summary": "Create a grounded SELF-facing candidate with explicit source exchange.",
            "source": "operator — auto-research/self-proposals",
            "source_exchange": {
                "operator": "We observed a repeatable preference in a bounded session."
            },
            "mind_category": "knowledge",
            "signal_type": "auto_research_proposal",
            "priority_score": 3,
            "profile_target": "IX-A. KNOWLEDGE",
            "suggested_entry": "Grounded proposals should carry source exchange and a concise suggested entry.",
            "prompt_section": "YOUR KNOWLEDGE",
            "prompt_addition": "You only learn new things through grounded, reviewed updates.",
            "new_vs_record": "Synthetic novelty note for testing only.",
            "proposal_class": "SIMULATION_RESULT",
        },
        "evaluation_notes": "Test payload.",
    }


def _run_main(module, argv: list[str]):
    old_argv = sys.argv[:]
    try:
        sys.argv = argv
        return module.main()
    finally:
        sys.argv = old_argv


def test_proposal_io_parses_markdown_block(tmp_path):
    proposal_io = _load("proposal_io_test", LANE / "proposal_io.py")
    payload = _sample_payload()
    train = tmp_path / "train.md"
    train.write_text(
        "# Draft\n\n```json\n" + json.dumps(payload, indent=2) + "\n```\n",
        encoding="utf-8",
    )

    parsed = proposal_io.load_train_payload(train)
    errors = proposal_io.validate_payload(parsed)

    assert parsed["hypothesis"] == payload["hypothesis"]
    assert errors == []


def test_validate_grounding_rejects_placeholder_source_in_strict_mode():
    proposal_io = _load("proposal_io_grounding_test", LANE / "proposal_io.py")
    payload = _sample_payload()
    payload["candidate_bundle"]["source_exchange"]["operator"] = "Synthetic scaffold placeholder. Replace with real source."

    errors = proposal_io.validate_grounding(payload, strict=True)

    assert any("placeholder grounding markers" in error for error in errors)


def test_sandbox_merge_inserts_candidate_before_processed(tmp_path):
    sandbox_merge = _load("sandbox_merge_test", LANE / "sandbox_merge.py")
    repo_root = tmp_path / "repo"
    user_dir = repo_root / "users" / "demo"
    user_dir.mkdir(parents=True)
    (user_dir / "recursion-gate.md").write_text(
        "# Gate\n\n## Candidates\n\n## Processed\n",
        encoding="utf-8",
    )
    (user_dir / "self.md").write_text("# self\n", encoding="utf-8")

    sandbox = sandbox_merge.materialize_sandbox(
        tmp_path / "sandbox",
        _sample_payload(),
        user_id="demo",
        repo_root=repo_root,
    )
    updated_gate = (tmp_path / "sandbox" / "users" / "demo" / "recursion-gate.md").read_text(encoding="utf-8")

    assert sandbox["candidate_id"].startswith("CANDIDATE-")
    assert f"### {sandbox['candidate_id']}" in updated_gate
    assert updated_gate.index(f"### {sandbox['candidate_id']}") < updated_gate.index("## Processed")
    assert "auto_research:" in sandbox["candidate_block"]


def test_score_adapter_builds_bounded_scalar():
    score_adapter = _load("score_adapter_test", LANE / "score_adapter.py")
    proposal_quality = {
        "quality": 0.9,
        "completeness": 1.0,
        "groundedness": 1.0,
        "reviewability": 0.8,
        "prompt_alignment": 0.8,
    }
    bundle = score_adapter.build_score_bundle(
        integrity_json={"ok": True},
        governance_ok=True,
        metrics_json={
            "pipeline_health": {"approval_rate": 0.8, "pending_count": 4},
            "record_completeness": {"total_ix": 72},
            "intent_drift": {"total_conflicts": 0},
        },
        proposal_quality=proposal_quality,
        uniqueness={"composite_uniqueness": 0.6},
        growth_density={"evidence_backing_pct": 90.0, "topic_diversity": 0.4},
        baseline_scalar=0.5,
    )

    assert bundle["ok"] is True
    assert 0.0 <= bundle["scalar"] <= 1.0
    assert bundle["comparison"]["delta_from_baseline"] is not None


def test_score_proposal_quality_penalizes_source_drift():
    score_adapter = _load("score_adapter_drift_test", LANE / "score_adapter.py")
    payload = _sample_payload()
    payload["candidate_bundle"]["summary"] = "Quantum macroeconomic blockchain orchids whisper in six impossible dimensions."
    payload["candidate_bundle"]["suggested_entry"] = payload["candidate_bundle"]["summary"]
    payload["candidate_bundle"]["prompt_addition"] = payload["candidate_bundle"]["summary"]

    scored = score_adapter.score_proposal_quality(payload, "candidate block")

    assert scored["novel_term_ratio"] > 0.5
    assert scored["alignment_score"] < 0.5
    assert scored["drift_penalty"] > 0.3


def test_promote_helper_serializes_pending_candidate():
    promote = _load("promote_to_gate_test", LANE / "promote_to_gate.py")
    artifact = {
        "proposal": _sample_payload(),
        "scalar_at_accept": 0.91,
        "artifact_schema_version": 1,
        "_artifact_relpath": "auto-research/self-proposals/accepted/example.json",
        "_promotion_review_note": "Operator reviewed raw source and wants gate visibility.",
        "raw_source_exchange": _sample_payload()["candidate_bundle"]["source_exchange"],
    }
    gate_text = "# Gate\n\n## Candidates\n\n## Processed\n"

    candidate_id, candidate_block = promote.build_promoted_candidate_block(artifact, gate_text)

    assert candidate_id == "CANDIDATE-0001"
    assert "status: pending" in candidate_block
    assert "proposal_class: SIMULATION_RESULT" in candidate_block
    assert 'accepted_artifact: "auto-research/self-proposals/accepted/example.json"' in candidate_block
    assert 'review_note: "Operator reviewed raw source and wants gate visibility."' in candidate_block


def test_prepare_strict_grounding_returns_zero_scalar_for_scaffold_payload(tmp_path):
    prepare = _load("prepare_grounding_test", LANE / "prepare.py")
    train = tmp_path / "train.md"
    payload = copy.deepcopy(_sample_payload())
    payload["grounding_mode"] = "scaffold"
    payload["candidate_bundle"]["source_exchange"]["operator"] = "Synthetic scaffold placeholder. Replace with real source."
    train.write_text("# Draft\n\n```json\n" + json.dumps(payload, indent=2) + "\n```\n", encoding="utf-8")

    old_train = prepare.TRAIN_PATH
    prepare.TRAIN_PATH = train
    try:
        result = prepare.run_prepare(strict_grounding=True)
    finally:
        prepare.TRAIN_PATH = old_train

    assert result["score_bundle"]["ok"] is False
    assert result["score_bundle"]["scalar"] == 0.0
    assert result["grounding_errors"]


def test_archive_winner_writes_transparent_metadata_fields(tmp_path):
    archive = _load("archive_winner_test", LANE / "archive_winner.py")
    archive.ACCEPTED_DIR = tmp_path / "accepted"
    archive.EXPERIMENTS_DIR = tmp_path / "experiments"
    archive.ACCEPTED_DIR.mkdir(parents=True)
    archive.EXPERIMENTS_DIR.mkdir(parents=True)

    input_path = archive.EXPERIMENTS_DIR / "last_score.json"
    payload = {
        "proposal": _sample_payload(),
        "score_bundle": {
            "ok": True,
            "scalar": 0.92,
            "components": {"proposal_quality": 0.9},
            "hard_gates": {"integrity_ok": True, "governance_ok": True},
        },
    }
    input_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    rc = _run_main(archive, ["archive_winner.py", "--input", str(input_path)])

    assert rc == 0
    outputs = list(archive.ACCEPTED_DIR.glob("accepted-*.json"))
    assert len(outputs) == 1
    artifact = json.loads(outputs[0].read_text(encoding="utf-8"))
    assert artifact["accepted_for"] == "research_only"
    assert artifact["operator_warning"] == "accepted for research, not approved for Record"
    assert artifact["scalar_at_accept"] == 0.92
    assert artifact["raw_source_exchange"] == payload["proposal"]["candidate_bundle"]["source_exchange"]
    assert artifact["proposal_projection"]["summary"] == payload["proposal"]["candidate_bundle"]["summary"]
    assert artifact["proposal_fingerprint"]


def test_archive_winner_rejects_duplicate_fingerprint_without_force(tmp_path):
    archive = _load("archive_winner_dupe_test", LANE / "archive_winner.py")
    archive.ACCEPTED_DIR = tmp_path / "accepted"
    archive.EXPERIMENTS_DIR = tmp_path / "experiments"
    archive.ACCEPTED_DIR.mkdir(parents=True)
    archive.EXPERIMENTS_DIR.mkdir(parents=True)

    payload = {
        "proposal": _sample_payload(),
        "score_bundle": {
            "ok": True,
            "scalar": 0.95,
            "components": {},
            "hard_gates": {"integrity_ok": True, "governance_ok": True},
        },
    }
    first_input = archive.EXPERIMENTS_DIR / "first.json"
    second_input = archive.EXPERIMENTS_DIR / "second.json"
    first_input.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    second_input.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    assert _run_main(archive, ["archive_winner.py", "--input", str(first_input)]) == 0
    try:
        _run_main(archive, ["archive_winner.py", "--input", str(second_input)])
    except SystemExit as exc:
        assert "duplicate proposal_fingerprint" in str(exc)
    else:
        raise AssertionError("expected duplicate fingerprint rejection")


def test_promote_to_gate_requires_review_note(tmp_path):
    promote = _load("promote_to_gate_review_note_test", LANE / "promote_to_gate.py")
    artifact_path = tmp_path / "accepted.json"
    artifact = {
        "proposal": _sample_payload(),
        "scalar_at_accept": 0.91,
        "artifact_schema_version": 1,
        "raw_source_exchange": _sample_payload()["candidate_bundle"]["source_exchange"],
    }
    artifact_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")

    try:
        _run_main(
            promote,
            ["promote_to_gate.py", "--artifact", str(artifact_path)],
        )
    except SystemExit as exc:
        assert "--review-note is required" in str(exc)
    else:
        raise AssertionError("expected review-note requirement")


def test_promote_to_gate_refuses_scaffold_grounding_artifact():
    promote = _load("promote_to_gate_scaffold_test", LANE / "promote_to_gate.py")
    payload = _sample_payload()
    payload["grounding_mode"] = "scaffold"
    artifact = {
        "proposal": payload,
        "scalar_at_accept": 0.91,
        "artifact_schema_version": 1,
        "_artifact_relpath": "auto-research/self-proposals/accepted/example.json",
        "_promotion_review_note": "Reviewed",
        "raw_source_exchange": payload["candidate_bundle"]["source_exchange"],
    }

    try:
        promote.build_promoted_candidate_block(artifact, "# Gate\n\n## Candidates\n\n## Processed\n")
    except ValueError as exc:
        assert "scaffold-grounding artifacts may not be promoted" in str(exc)
    else:
        raise AssertionError("expected scaffold grounding refusal")
