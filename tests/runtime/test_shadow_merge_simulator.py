"""Tests for scripts/runtime/shadow_merge_simulator.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SMS = REPO_ROOT / "scripts" / "runtime" / "shadow_merge_simulator.py"


def _gate_skills_fixture() -> str:
    return """# RECURSION GATE — test

## Candidates

### CANDIDATE-0999 (Shadow skills)

```yaml
status: pending
timestamp: 2026-04-01 12:00:00
channel_key: operator:cursor:test
proposal_class: RUNTIME_OBSERVATION_PROPOSAL
mind_category: knowledge
signal_type: operator_runtime_observation_stage
priority_score: 3
summary: "Skill boundary test"
profile_target: WORK — manual apply (see proposed_change and target_surface).
candidate_type: skill_update
target_surface: SKILLS
target_path: null
proposed_change: "Use compact summaries only in strategy notebook."
confidence: null
why_now: null
review_notes: null
```

## Processed
"""


def _gate_misfiled_fixture() -> str:
    return """# RECURSION GATE — test

## Candidates

### CANDIDATE-0998 (Misfiled LIB)

```yaml
status: pending
timestamp: 2026-04-01 12:00:00
channel_key: operator:cursor:test
proposal_class: SELF_KNOWLEDGE_ADD
mind_category: knowledge
signal_type: operator_paste
priority_score: 3
summary: "Add topic about LIB-0149 predictive history bundle"
profile_target: IX-A. KNOWLEDGE
suggested_entry: |
  This is a long enough block about LIB-0149 and reference material that boundary heuristics
  should treat it as library-scoped content rather than a short IX-A topic line alone.
  Repeat: LIB-0149 predictive history is a library index entry not a personality fact.
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

## Processed
"""


def _gate_contradiction_fixture() -> str:
    return """# RECURSION GATE — test

## Candidates

### CANDIDATE-0997 (Conflict flag)

```yaml
status: pending
timestamp: 2026-04-01 12:00:00
channel_key: operator:cursor:test
proposal_class: SELF_KNOWLEDGE_ADD
mind_category: knowledge
signal_type: operator_paste
priority_score: 3
summary: "Contradiction probe"
profile_target: IX-A. KNOWLEDGE
review_notes: contradiction noted with prior ACT entry — needs human resolution
suggested_entry: "Test"
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

## Processed
"""


def _write_fork(tmp_path: Path, gate_body: str) -> Path:
    user_dir = tmp_path / "users" / "grace-mar"
    user_dir.mkdir(parents=True)
    (user_dir / "self.md").write_text("# self\n\n### IX-A\n\n(knowledge)\n", encoding="utf-8")
    gate_path = user_dir / "recursion-gate.md"
    gate_path.write_text(gate_body, encoding="utf-8")
    return gate_path


def test_skills_candidate_surface_preview(tmp_path: Path) -> None:
    _write_fork(tmp_path, _gate_skills_fixture())
    out = tmp_path / "report.md"
    r = subprocess.run(
        [
            sys.executable,
            str(SMS),
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
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    text = out.read_text(encoding="utf-8")
    assert "Target surface (resolved): **SKILLS**" in text
    assert "Predicted best-fit (keywords)" in text
    assert "Keyword score signals" in text
    assert "### SKILLS" in text
    assert "self-skills" in text.lower() or "SKILLS" in text
    assert "## Support snapshot" in text


def test_simulator_does_not_mutate_canonical_files(tmp_path: Path) -> None:
    gate_path = _write_fork(tmp_path, _gate_skills_fixture())
    self_path = tmp_path / "users" / "grace-mar" / "self.md"
    before_gate = gate_path.read_bytes()
    before_self = self_path.read_bytes()
    out = tmp_path / "report.md"
    subprocess.run(
        [
            sys.executable,
            str(SMS),
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
        check=True,
    )
    assert gate_path.read_bytes() == before_gate
    assert self_path.read_bytes() == before_self
    assert out.is_file()


def test_cross_surface_misfiled_surfaces_classification(tmp_path: Path) -> None:
    _write_fork(tmp_path, _gate_misfiled_fixture())
    out = tmp_path / "report.md"
    subprocess.run(
        [
            sys.executable,
            str(SMS),
            "-u",
            "grace-mar",
            "--repo-root",
            str(tmp_path),
            "--candidate",
            "CANDIDATE-0998",
            "-o",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        check=True,
    )
    text = out.read_text(encoding="utf-8")
    assert "## Classification risk" in text
    assert "Misfiled" in text or "SELF-LIBRARY" in text or "medium" in text.lower()


def test_contradiction_signal_in_narrative_section(tmp_path: Path) -> None:
    _write_fork(tmp_path, _gate_contradiction_fixture())
    out = tmp_path / "report.md"
    subprocess.run(
        [
            sys.executable,
            str(SMS),
            "-u",
            "grace-mar",
            "--repo-root",
            str(tmp_path),
            "--candidate",
            "CANDIDATE-0997",
            "-o",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        check=True,
    )
    text = out.read_text(encoding="utf-8")
    assert "## Narrative risk" in text
    assert "contradiction" in text.lower() or "conflict" in text.lower()


def test_observation_envelope_appears_when_ledger_present(tmp_path: Path) -> None:
    _write_fork(tmp_path, _gate_skills_fixture())
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    obs = {
        "obs_id": "obs_20260101T120000Z_shadowaa",
        "timestamp": "2026-01-01T12:00:00Z",
        "lane": "work-strategy",
        "source_kind": "manual_note",
        "title": "T",
        "summary": "supporting",
        "record_mutation_candidate": True,
        "source_path": None,
        "source_refs": ["docs/x.md"],
        "tags": [],
        "confidence": 0.5,
        "contradiction_refs": ["prior/act/1"],
        "notes": None,
    }
    (obs_dir / "index.jsonl").write_text(json.dumps(obs) + "\n", encoding="utf-8")

    # Add source_observation_ids to gate candidate YAML (same file rewrite)
    gate_path = tmp_path / "users" / "grace-mar" / "recursion-gate.md"
    body = gate_path.read_text(encoding="utf-8")
    body = body.replace(
        "review_notes: null\n```",
        "review_notes: null\nsource_observation_ids:\n  - \"obs_20260101T120000Z_shadowaa\"\n```",
    )
    gate_path.write_text(body, encoding="utf-8")

    out = tmp_path / "report-env.md"
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    subprocess.run(
        [
            sys.executable,
            str(SMS),
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
        check=True,
        env=env,
    )
    text = out.read_text(encoding="utf-8")
    assert "Uncertainty envelope" in text or "conflicting" in text.lower() or "evidence_state" in text


def test_build_report_markdown_import() -> None:
    import importlib.util
    import sys

    name = "shadow_merge_simulator_test_mod"
    spec = importlib.util.spec_from_file_location(name, SMS)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[name] = m
    spec.loader.exec_module(m)
    sc = m.ShadowCandidate(
        candidate_id="DIRECT-PROPOSAL",
        proposal_summary="x",
        proposed_change="y",
        yaml_target="SKILLS",
    )
    md = m.build_report_markdown(
        built_iso="2026-04-01T00:00:00Z",
        mode="simulation_only (proposal text)",
        sc=sc,
        row=None,
        env=None,
        missing_obs=[],
    )
    assert "# Shadow Merge Report" in md
    assert "SKILLS" in md
    assert "Predicted best-fit (keywords)" in md


def _load_sms():
    import importlib.util
    import sys

    name = "shadow_merge_simulator_unit"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SMS)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def test_infer_best_fit_surface_library_for_roman_reference() -> None:
    m = _load_sms()
    sc = m.ShadowCandidate(
        candidate_id="CANDIDATE-0043",
        yaml_target="SELF",
        proposal_summary="Add Roman imperial continuity reference preference",
        proposed_change=(
            "Treat Roman imperial continuity as a governed reference tradition and source shelf for future synthesis."
        ),
    )
    best, _scores = m.infer_best_fit_surface(sc)
    assert best == "SELF-LIBRARY"


def test_narrative_risk_keyword_high_when_decisive_without_evidence() -> None:
    m = _load_sms()
    sc = m.ShadowCandidate(
        candidate_id="CANDIDATE-0044",
        yaml_target="SELF",
        proposal_summary="Permanent identity lock",
        proposed_change="This must be treated as definitive and canonical forever.",
    )
    level, reason = m.narrative_risk_keyword_overlay(sc)
    assert level == "high"
    assert reason


def test_sketch_classify_mismatch_raises_level() -> None:
    m = _load_sms()
    level, reason = m.sketch_classify_risk_vs_keywords(
        "SELF",
        "SELF-LIBRARY",
        contradiction_refs=[],
        supporting_evidence_refs=[],
    )
    assert level == "high"
    assert reason


def test_proposal_file_json_subprocess(tmp_path: Path) -> None:
    js = {
        "gate_candidate_id": "CANDIDATE-8001",
        "created_at": "2026-01-01T00:00:00Z",
        "candidate_type": "other",
        "target_surface": "EVIDENCE",
        "proposal_summary": "Evidence stub link",
        "proposed_change": "Add READ entry pointer.",
        "source_observation_ids": [],
        "lane_origin": "work-strategy",
        "status": "pending",
    }
    jpath = tmp_path / "payload.json"
    jpath.write_text(json.dumps(js), encoding="utf-8")
    out = tmp_path / "out.md"
    subprocess.run(
        [
            sys.executable,
            str(SMS),
            "--repo-root",
            str(tmp_path),
            "--proposal-file",
            str(jpath),
            "-o",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        check=True,
    )
    text = out.read_text(encoding="utf-8")
    assert "CANDIDATE-8001" in text
    assert "EVIDENCE" in text
    assert "## Support snapshot" in text
