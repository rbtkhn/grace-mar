from __future__ import annotations

import importlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SWARM = ROOT / "auto-research" / "swarm"

if str(SWARM) not in sys.path:
    sys.path.insert(0, str(SWARM))


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
            "source": "operator - auto-research/self-proposals",
            "source_exchange": {
                "operator": "We observed a repeatable preference in a bounded session with enough detail to ground review."
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


def _accepted_artifact() -> dict:
    return {
        "proposal": _sample_payload(),
        "scalar_at_accept": 0.91,
        "artifact_schema_version": 1,
        "raw_source_exchange": _sample_payload()["candidate_bundle"]["source_exchange"],
        "proposal_projection": {
            "summary": _sample_payload()["candidate_bundle"]["summary"],
            "suggested_entry": _sample_payload()["candidate_bundle"]["suggested_entry"],
            "prompt_addition": _sample_payload()["candidate_bundle"]["prompt_addition"],
        },
        "hard_gates": {"integrity_ok": True, "governance_ok": True},
    }


def test_debate_review_writes_derived_artifact(tmp_path, monkeypatch):
    review = importlib.import_module("debate.review")
    tmp_repo = tmp_path / "repo"
    artifact_path = tmp_repo / "auto-research" / "self-proposals" / "accepted" / "accepted-test.json"
    artifact_path.parent.mkdir(parents=True)
    artifact_path.write_text(json.dumps(_accepted_artifact(), indent=2) + "\n", encoding="utf-8")
    monkeypatch.setattr(review, "REPO_ROOT", tmp_repo)

    result = review.run_debate_review(artifact_path, user_id="demo", write=True, repo_root=tmp_repo)

    assert result["final_recommendation"] == "promote_candidate"
    assert result["promotion_readiness"] == "ready"
    assert len(result["role_reviews"]) == 4
    assert Path(result["review_path"]).is_file()


def test_debate_review_requests_more_grounding_for_missing_source_exchange(tmp_path, monkeypatch):
    review = importlib.import_module("debate.review")
    tmp_repo = tmp_path / "repo"
    artifact_path = tmp_repo / "auto-research" / "self-proposals" / "accepted" / "accepted-missing-grounding.json"
    artifact_path.parent.mkdir(parents=True)
    artifact = _accepted_artifact()
    artifact["raw_source_exchange"] = {}
    artifact["proposal"]["candidate_bundle"]["source_exchange"] = {}
    artifact_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    monkeypatch.setattr(review, "REPO_ROOT", tmp_repo)

    result = review.run_debate_review(artifact_path, user_id="demo", write=False, repo_root=tmp_repo)

    assert result["final_recommendation"] == "request_more_grounding"
    assert "missing_grounding" in result["blocking_flags"]


def test_swarm_orchestrator_runs_debate_without_touching_gate(tmp_path, monkeypatch):
    orchestrator = _load("swarm_orchestrator_debate_test", SWARM / "orchestrator.py")
    review = importlib.import_module("debate.review")
    tmp_repo = tmp_path / "repo"
    accepted_dir = tmp_repo / "auto-research" / "self-proposals" / "accepted"
    swarm_dir = tmp_repo / "auto-research" / "swarm"
    gate_path = tmp_repo / "users" / "demo" / "recursion-gate.md"
    accepted_dir.mkdir(parents=True)
    swarm_dir.mkdir(parents=True)
    gate_path.parent.mkdir(parents=True)
    gate_path.write_text("# Gate\n\n## Candidates\n\n## Processed\n", encoding="utf-8")

    artifact_path = accepted_dir / "accepted-test.json"
    artifact_path.write_text(json.dumps(_accepted_artifact(), indent=2) + "\n", encoding="utf-8")

    monkeypatch.setattr(orchestrator, "REPO_ROOT", tmp_repo)
    monkeypatch.setattr(orchestrator, "AUTO_RESEARCH_DIR", tmp_repo / "auto-research")
    monkeypatch.setattr(orchestrator, "SWARM_DIR", swarm_dir)
    monkeypatch.setattr(
        orchestrator,
        "ARTIFACT_SOURCES",
        (
            {
                "lane": "self-proposals",
                "candidate_source": "auto-research/swarm",
                "accepted_dir": accepted_dir,
            },
        ),
    )
    monkeypatch.setattr(review, "REPO_ROOT", tmp_repo)

    result = orchestrator.run_debate_review("latest", user_id="demo", write=True)

    assert result["target_artifact"]["artifact_name"] == "accepted-test.json"
    assert result["final_recommendation"] == "promote_candidate"
    assert "recommendation: promote_candidate" in orchestrator.format_debate_status(result)
    assert gate_path.read_text(encoding="utf-8") == "# Gate\n\n## Candidates\n\n## Processed\n"
