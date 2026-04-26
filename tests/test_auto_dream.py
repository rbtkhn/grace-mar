from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import auto_dream
import contradiction_digest
import score_adapter


def _gate_text(*blocks: str) -> str:
    joined = "\n\n".join(blocks)
    return f"# Gate\n\n## Candidates\n\n{joined}\n\n## Processed\n"


def test_contradiction_digest_flags_duplicate_and_contradiction(tmp_path):
    users_dir = tmp_path / "users"
    user_dir = users_dir / "demo"
    user_dir.mkdir(parents=True)
    (user_dir / "self.md").write_text(
        """# SELF

trait: independent

### IX-A. KNOWLEDGE
```yaml
- id: LEARN-0001
  topic: Mars
  observation: "Mars has two moons named Phobos and Deimos."
  evidence_id: ACT-0001
```
""",
        encoding="utf-8",
    )
    (user_dir / "recursion-gate.md").write_text(
        _gate_text(
            """### CANDIDATE-0001
```yaml
status: pending
mind_category: knowledge
summary: Duplicate of existing Mars knowledge already in record.
profile_target: IX-A. KNOWLEDGE
prompt_section: YOUR KNOWLEDGE
suggested_entry: "Mars has two moons named Phobos and Deimos."
prompt_addition: "None"
source_exchange:
  operator: "We repeated the exact same Mars line with enough context to ground review safely."
```""",
            """### CANDIDATE-0002
```yaml
status: pending
mind_category: personality
summary: Observed dependent behavior in group work; prefers heavy scaffolding.
profile_target: IX-C. PERSONALITY
prompt_section: YOUR PERSONALITY
suggested_entry: "Often relies on partner prompts before starting - dependent in pairs."
prompt_addition: "Needs stronger scaffolding than usual in pair work."
source_exchange:
  operator: "Observed dependent behavior in group work and reliance on partner prompts before starting tasks."
```""",
        ),
        encoding="utf-8",
    )

    digest = contradiction_digest.generate_contradiction_digest(user_id="demo", users_dir=users_dir)
    counts = digest["relation_counts"]

    assert counts["duplicate"] == 1
    assert counts["contradiction"] == 1
    assert digest["reviewable_count"] == 2
    entry = next(item for item in digest["entries"] if item["candidate_id"] == "CANDIDATE-0002")
    artifact, errors = contradiction_digest.build_promotable_artifact(entry)
    assert artifact is not None
    assert errors == []


def test_contradiction_digest_strict_mode_escalates_dense_overlap(tmp_path):
    users_dir = tmp_path / "users"
    user_dir = users_dir / "demo"
    user_dir.mkdir(parents=True)
    (user_dir / "self.md").write_text(
        """# SELF

### IX-A. KNOWLEDGE
```yaml
- id: LEARN-0001
  topic: Focus
  observation: "Reflective writing routines often happen after school."
  evidence_id: ACT-0001
```
""",
        encoding="utf-8",
    )
    (user_dir / "recursion-gate.md").write_text(
        _gate_text(
            """### CANDIDATE-0001
```yaml
status: pending
mind_category: knowledge
summary: Quiet focus blocks support reflective writing routines after school.
profile_target: IX-A. KNOWLEDGE
prompt_section: YOUR KNOWLEDGE
suggested_entry: "Quiet focus blocks support reflective writing routines."
prompt_addition: "Calm study blocks can help afternoon focus."
source_exchange:
  operator: "Observed quiet focus blocks supporting reflective writing routines after school."
```""",
        ),
        encoding="utf-8",
    )

    normal_digest = contradiction_digest.generate_contradiction_digest(user_id="demo", users_dir=users_dir)
    strict_digest = contradiction_digest.generate_contradiction_digest(
        user_id="demo",
        users_dir=users_dir,
        strict_mode=True,
    )

    normal_entry = normal_digest["entries"][0]
    strict_entry = strict_digest["entries"][0]
    assert normal_entry["relationship_type"] == "refinement"
    assert strict_entry["relationship_type"] == "contradiction"


def test_auto_dream_maintains_self_memory_and_writes_digest(tmp_path, monkeypatch):
    monkeypatch.delenv("CURSOR_MODEL", raising=False)
    users_dir = tmp_path / "users"
    user_dir = users_dir / "demo"
    user_dir.mkdir(parents=True)
    (user_dir / "self.md").write_text("# SELF\n", encoding="utf-8")
    (user_dir / "recursion-gate.md").write_text("# Gate\n\n## Candidates\n\n## Processed\n", encoding="utf-8")
    (user_dir / "self-memory.md").write_text(
        """# MEMORY - Self-memory (short / medium / long)

Last rotated: 2026-01-01

## Short-term

- repeat me
- repeat me
""",
        encoding="utf-8",
    )

    events: list[dict] = []

    monkeypatch.setattr(auto_dream, "_run_json_command", lambda *args, **kwargs: {"ok": True, "errors": []})
    monkeypatch.setattr(auto_dream, "_run_text_command", lambda *args, **kwargs: (0, "Governance check: OK", ""))
    monkeypatch.setattr(
        auto_dream,
        "append_pipeline_event",
        lambda user_id, event_type, candidate_id, merge=None, extras=None: events.append(
            {
                "user_id": user_id,
                "event_type": event_type,
                "candidate_id": candidate_id,
                "merge": merge or {},
            }
        )
        or {"event": event_type},
    )

    summary = auto_dream.run_auto_dream(
        user_id="demo",
        users_dir=users_dir,
        apply=True,
        emit_event=True,
        write_artifacts=False,
    )

    memory_text = (user_dir / "self-memory.md").read_text(encoding="utf-8")
    digest_path = user_dir / "derived" / "contradictions" / "auto-dream-digest.json"

    assert summary["self_memory"]["changed"] is True
    assert "## Medium-term" in memory_text
    assert memory_text.count("- repeat me") == 1
    assert digest_path.is_file()
    assert events[0]["event_type"] == "maintenance"
    assert events[0]["merge"]["action"] == "auto_dream"
    handoff_path = user_dir / "last-dream.json"
    assert handoff_path.is_file()
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    assert handoff.get("agent_surface", {}).get("cursor_model") == "unknown"
    assert handoff.get("handoffSchemaVersion") == 3
    assert summary.get("agent_surface", {}).get("cursor_model") == "unknown"


def test_auto_dream_strict_mode_halts_before_writes_on_failed_checks(tmp_path, monkeypatch):
    users_dir = tmp_path / "users"
    user_dir = users_dir / "demo"
    user_dir.mkdir(parents=True)
    (user_dir / "self.md").write_text("# SELF\n", encoding="utf-8")
    (user_dir / "recursion-gate.md").write_text("# Gate\n\n## Candidates\n\n## Processed\n", encoding="utf-8")
    memory_path = user_dir / "self-memory.md"
    memory_path.write_text(
        """# MEMORY - Self-memory (short / medium / long)

## Short-term

- repeat me
- repeat me
""",
        encoding="utf-8",
    )

    events: list[dict] = []
    monkeypatch.setattr(auto_dream, "_run_json_command", lambda *args, **kwargs: {"ok": False, "errors": ["integrity failed"]})
    monkeypatch.setattr(auto_dream, "_run_text_command", lambda *args, **kwargs: (0, "Governance check: OK", ""))
    monkeypatch.setattr(
        auto_dream,
        "append_pipeline_event",
        lambda *args, **kwargs: events.append({"called": True}) or {"event": "maintenance"},
    )

    summary = auto_dream.run_auto_dream(
        user_id="demo",
        users_dir=users_dir,
        apply=True,
        emit_event=True,
        write_artifacts=True,
        strict_mode=True,
    )

    assert summary["ok"] is False
    assert summary["halted"] is True
    assert summary["contradiction_digest"]["skipped"] is True
    assert summary["self_memory"]["changed"] is False
    assert summary["self_memory"]["would_change"] is True
    assert memory_path.read_text(encoding="utf-8").count("- repeat me") == 2
    assert not (user_dir / "derived" / "contradictions" / "auto-dream-digest.json").exists()
    assert events == []


def test_score_bundle_includes_maintenance_readiness():
    bundle = score_adapter.build_score_bundle(
        integrity_json={"ok": True},
        governance_ok=True,
        metrics_json={
            "pipeline_health": {"approval_rate": 0.9, "pending_count": 0},
            "record_completeness": {"total_ix": 60},
            "intent_drift": {"total_conflicts": 1},
        },
        proposal_quality={"quality": 0.8},
        contradiction_digest={
            "reviewable_count": 3,
            "relation_counts": {"duplicate": 1, "refinement": 1, "contradiction": 1},
        },
        uniqueness=None,
        growth_density=None,
        baseline_scalar=None,
    )

    assert "maintenance_readiness" in bundle["components"]
    assert 0.0 <= bundle["components"]["maintenance_readiness"] <= 1.0
    assert "contradiction_digest" in bundle["optional_metrics"]


def test_score_bundle_strict_maintenance_hard_gates_low_readiness():
    bundle = score_adapter.build_score_bundle(
        integrity_json={"ok": True},
        governance_ok=True,
        metrics_json={
            "pipeline_health": {"approval_rate": 0.9, "pending_count": 0},
            "record_completeness": {"total_ix": 60},
            "intent_drift": {"total_conflicts": 1},
        },
        proposal_quality={"quality": 0.8},
        contradiction_digest={
            "reviewable_count": 3,
            "relation_counts": {"duplicate": 1, "refinement": 1, "contradiction": 1},
        },
        uniqueness=None,
        growth_density=None,
        baseline_scalar=None,
        strict_maintenance=True,
    )

    assert bundle["ok"] is False
    assert bundle["hard_gates"]["maintenance_ready"] is False
    assert bundle["scalar"] == 0.0


def test_format_auto_dream_summary_headline_prefix():
    summary = {
        "ok": True,
        "user_id": "grace-mar",
        "phase": "both",
        "strict_mode": False,
        "halted": False,
        "self_memory": {
            "changed": False,
            "added_sections": [],
            "deduped_lines": 0,
            "blank_lines_collapsed": 0,
        },
        "integrity": {"ok": True},
        "governance": {"ok": True},
        "contradiction_digest": {"relation_counts": {}, "reviewable_count": 0},
        "handoff_path": str(ROOT / "users" / "grace-mar" / "last-dream.json"),
    }
    out = auto_dream.format_auto_dream_summary(summary)
    first = out.split("\n", 1)[0]
    assert first.startswith("Dream: ok ")
    assert "handoff=yes" in first
    assert "autoDream status" in out


def test_format_auto_dream_summary_strict_headline_halted():
    summary = {
        "ok": False,
        "user_id": "grace-mar",
        "phase": "both",
        "strict_mode": True,
        "halted": True,
        "self_memory": {"changed": False},
        "integrity": {"ok": False},
        "governance": {"ok": True},
        "contradiction_digest": {
            "reviewable_count": 0,
            "relation_counts": {},
            "skipped": True,
            "skip_reason": "strict maintenance halted after integrity/governance failure",
        },
    }
    out = auto_dream.format_auto_dream_summary(summary)
    assert out.startswith("Dream: HALTED ")
    assert "strict autoDream" in out
