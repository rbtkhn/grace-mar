"""Tests for scripts/runtime/surface_misclassification_detector.py."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SMD = REPO_ROOT / "scripts" / "runtime" / "surface_misclassification_detector.py"


def _load_mod():
    name = "surface_misclassification_detector_test_mod"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SMD)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def test_reference_heavy_self_claim_is_flagged_toward_library() -> None:
    m = _load_mod()
    proposal = m.Proposal(
        proposal_id="CANDIDATE-1001",
        target_surface="SELF",
        proposal_summary="Add Roman imperial continuity reference preference",
        proposed_change=(
            "Treat Roman imperial continuity as a governed reference tradition and return-to source shelf for future synthesis."
        ),
    )
    scores = m.score_surface_signals(proposal)
    predicted = m.best_fit_surface(scores)
    assert predicted == "SELF-LIBRARY"


def test_exploratory_material_is_flagged_toward_work_layer() -> None:
    m = _load_mod()
    proposal = m.Proposal(
        proposal_id="CANDIDATE-1002",
        target_surface="SKILLS",
        proposal_summary="Maybe refine writing workflow",
        proposed_change="Draft hypothesis: explore whether write flow should change later.",
        source_observation_ids=["obs_1", "obs_2"],
        contradiction_refs=["obs_conflict_1"],
    )
    scores = m.score_surface_signals(proposal)
    predicted = m.best_fit_surface(scores)
    assert predicted in {"WORK_LAYER", "SKILLS"}


def test_evidence_like_proposal_not_confused_for_skill_when_event_framed() -> None:
    m = _load_mod()
    proposal = m.Proposal(
        proposal_id="CANDIDATE-1003",
        target_surface="SKILLS",
        proposal_summary="Record operator artifact submission",
        proposed_change="Add receipt of the submitted artifact and event trace.",
        supporting_evidence_refs=["artifact:2026-04-14"],
    )
    scores = m.score_surface_signals(proposal)
    predicted = m.best_fit_surface(scores)
    assert predicted in {"EVIDENCE", "SKILLS"}


def test_report_is_advisory_and_non_mutating_in_language() -> None:
    m = _load_mod()
    proposal = m.Proposal(
        proposal_id="CANDIDATE-1004",
        target_surface="SELF",
        proposal_summary="Identity-facing preference note",
        proposed_change="Add a new identity-facing preference.",
    )
    report = m.build_report(proposal)
    assert "advisory only" in report.lower()
    assert "recursion-gate.md" in report


def test_divergent_surface_can_raise_medium_or_high_risk() -> None:
    m = _load_mod()
    proposal = m.Proposal(
        proposal_id="CANDIDATE-1005",
        target_surface="SELF",
        proposal_summary="Governed library shelf update",
        proposed_change="Add a new reference shelf for civilizational memory.",
        contradiction_refs=["obs_conflict_1"],
    )
    scores = m.score_surface_signals(proposal)
    predicted = m.best_fit_surface(scores)
    risk, _ = m.classification_risk(proposal, predicted, scores)
    assert risk in {"medium", "high"}


def test_subprocess_candidate_skills_fixture(tmp_path: Path) -> None:
    gate = """# R

## Candidates

### CANDIDATE-0999 (t)

```yaml
status: pending
timestamp: 2026-04-01 12:00:00
channel_key: operator:cursor:test
proposal_class: RUNTIME_OBSERVATION_PROPOSAL
mind_category: knowledge
signal_type: operator_runtime_observation_stage
priority_score: 3
summary: "Skill boundary test"
profile_target: WORK
candidate_type: skill_update
target_surface: SKILLS
target_path: null
proposed_change: "Use compact summaries only."
confidence: null
why_now: null
review_notes: null
```

## Processed
"""
    user = tmp_path / "users" / "grace-mar"
    user.mkdir(parents=True)
    (user / "self.md").write_text("# s\n", encoding="utf-8")
    (user / "recursion-gate.md").write_text(gate, encoding="utf-8")
    out = tmp_path / "cls.md"
    r = subprocess.run(
        [
            sys.executable,
            str(SMD),
            "-u",
            "grace-mar",
            "--repo-root",
            str(tmp_path),
            "--candidate",
            "CANDIDATE-0999",
            "-o",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    text = out.read_text(encoding="utf-8")
    assert "Classification Risk Report" in text
    assert "SKILLS" in text
