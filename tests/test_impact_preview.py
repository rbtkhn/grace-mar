"""Tests for src/grace_mar/merge/impact_preview.py — candidate impact prediction."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from grace_mar.merge.impact_preview import format_impact_summary, preview_candidate_impact

USER = "grace-mar"
BASE = f"users/{USER}"


def _candidate(**overrides) -> dict:
    base = {
        "id": "CANDIDATE-0001",
        "mind_category": "knowledge",
        "profile_target": "IX-A. KNOWLEDGE",
        "prompt_addition": "none",
        "prompt_merge_mode": "",
        "evidence_record_type": "act",
        "proposal_class": "",
    }
    base.update(overrides)
    return base


class TestKnowledgeCandidate:
    def test_touches_self_and_archive(self):
        r = preview_candidate_impact(_candidate(), user_id=USER)
        assert f"{BASE}/self.md" in r["files_touched"]
        assert f"{BASE}/self-archive.md" in r["files_touched"]

    def test_surface_is_ix_a(self):
        r = preview_candidate_impact(_candidate(), user_id=USER)
        assert r["surface"] == "IX-A"

    def test_sections_include_act_log(self):
        r = preview_candidate_impact(_candidate(), user_id=USER)
        assert "ACT log" in r["sections_touched"]
        assert "IX-A" in r["sections_touched"]

    def test_prompt_none_by_default(self):
        r = preview_candidate_impact(_candidate(), user_id=USER)
        assert r["prompt_effect"] == "none"
        assert "bot/prompt.py" not in r["files_touched"]

    def test_always_touches_gate_and_session_log(self):
        r = preview_candidate_impact(_candidate(), user_id=USER)
        assert f"{BASE}/recursion-gate.md" in r["files_touched"]
        assert f"{BASE}/session-log.md" in r["files_touched"]


class TestCuriosityCandidate:
    def test_surface_is_ix_b(self):
        r = preview_candidate_impact(
            _candidate(mind_category="curiosity", profile_target="IX-B. CURIOSITY"),
            user_id=USER,
        )
        assert r["surface"] == "IX-B"

    def test_sections_include_ix_b(self):
        r = preview_candidate_impact(
            _candidate(mind_category="curiosity", profile_target="IX-B. CURIOSITY"),
            user_id=USER,
        )
        assert "IX-B" in r["sections_touched"]


class TestPersonalityCandidate:
    def test_surface_is_ix_c(self):
        r = preview_candidate_impact(
            _candidate(mind_category="personality", profile_target="IX-C. PERSONALITY"),
            user_id=USER,
        )
        assert r["surface"] == "IX-C"


class TestReadCandidate:
    def test_includes_reading_list(self):
        r = preview_candidate_impact(
            _candidate(evidence_record_type="read"),
            user_id=USER,
        )
        assert "Reading list" in r["sections_touched"]

    def test_write_type(self):
        r = preview_candidate_impact(
            _candidate(evidence_record_type="write"),
            user_id=USER,
        )
        assert "Writing log" in r["sections_touched"]


class TestPromptModes:
    def test_prompt_append(self):
        r = preview_candidate_impact(
            _candidate(prompt_addition="Loves reading about history"),
            user_id=USER,
        )
        assert r["prompt_effect"] == "append"
        assert "bot/prompt.py" in r["files_touched"]

    def test_prompt_rebuild(self):
        r = preview_candidate_impact(
            _candidate(prompt_merge_mode="rebuild_ix"),
            user_id=USER,
        )
        assert r["prompt_effect"] == "rebuild"
        assert "bot/prompt.py" in r["files_touched"]
        assert "prompt_rebuild" in r["risk_factors"]

    def test_prompt_section_label_knowledge(self):
        r = preview_candidate_impact(
            _candidate(prompt_addition="something"),
            user_id=USER,
        )
        assert r["prompt_section"] == "YOUR KNOWLEDGE"

    def test_prompt_section_custom(self):
        r = preview_candidate_impact(
            _candidate(prompt_addition="something", prompt_section="YOUR VOICE"),
            user_id=USER,
        )
        assert r["prompt_section"] == "YOUR VOICE"


class TestBoundaryFlags:
    def test_reclassification_needed(self):
        r = preview_candidate_impact(
            _candidate(boundary_review={
                "target_surface": "SELF-KNOWLEDGE",
                "suggested_surface": "SELF-LIBRARY",
            }),
            user_id=USER,
        )
        assert "reclassification_needed" in r["boundary_flags"]
        assert "boundary_reclassification" in r["risk_factors"]

    def test_misfiled_warning(self):
        r = preview_candidate_impact(
            _candidate(boundary_review={
                "target_surface": "SELF-KNOWLEDGE",
                "misfiled_warning": "Looks like library material",
            }),
            user_id=USER,
        )
        assert "misfiled_warning" in r["boundary_flags"]

    def test_no_flags_when_surfaces_match(self):
        r = preview_candidate_impact(
            _candidate(boundary_review={
                "target_surface": "SELF-KNOWLEDGE",
                "suggested_surface": "SELF-KNOWLEDGE",
            }),
            user_id=USER,
        )
        assert r["boundary_flags"] == []


class TestProposalClassRouting:
    def test_library_candidate_touches_self_library(self):
        r = preview_candidate_impact(
            _candidate(proposal_class="SELF_LIBRARY_ADD"),
            user_id=USER,
        )
        assert f"{BASE}/self-library.md" in r["files_touched"]
        assert "Self-library" in r["sections_touched"]

    def test_skills_candidate_touches_self_skills(self):
        r = preview_candidate_impact(
            _candidate(proposal_class="SKILLS_UPDATE"),
            user_id=USER,
        )
        assert f"{BASE}/self-skills.md" in r["files_touched"]

    def test_multi_surface_risk_factor(self):
        r = preview_candidate_impact(
            _candidate(
                proposal_class="SELF_LIBRARY_ADD",
                prompt_addition="something",
            ),
            user_id=USER,
        )
        assert "multi_surface" in r["risk_factors"]


class TestMinimalCandidate:
    def test_empty_candidate_defaults_gracefully(self):
        r = preview_candidate_impact({}, user_id=USER)
        assert r["candidate_id"] == "(unknown)"
        assert r["surface"] == "IX-A"
        assert f"{BASE}/self.md" in r["files_touched"]

    def test_candidate_id_preserved(self):
        r = preview_candidate_impact(
            _candidate(id="CANDIDATE-0042"),
            user_id=USER,
        )
        assert r["candidate_id"] == "CANDIDATE-0042"


class TestFormatSummary:
    def test_simple_summary(self):
        r = preview_candidate_impact(_candidate(), user_id=USER)
        s = format_impact_summary(r)
        assert "CANDIDATE-0001" in s
        assert "IX-A" in s

    def test_flags_in_summary(self):
        r = preview_candidate_impact(
            _candidate(
                prompt_merge_mode="rebuild_ix",
                boundary_review={
                    "target_surface": "SELF-KNOWLEDGE",
                    "suggested_surface": "SELF-LIBRARY",
                },
            ),
            user_id=USER,
        )
        s = format_impact_summary(r)
        assert "prompt=rebuild" in s
        assert "reclassification_needed" in s
