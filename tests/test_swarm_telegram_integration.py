from __future__ import annotations

import asyncio
import importlib
import importlib.util
import json
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "auto-research" / "_shared"
SWARM = ROOT / "auto-research" / "swarm"


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
    }


def test_shared_promote_artifact_writes_staged_event(tmp_path, monkeypatch):
    helper = _load("artifact_promotion_shared_test", SHARED / "artifact_promotion.py")
    tmp_repo = tmp_path / "repo"
    artifact_path = tmp_repo / "auto-research" / "self-proposals" / "accepted" / "accepted-test.json"
    gate_path = tmp_repo / "users" / "demo" / "recursion-gate.md"
    artifact_path.parent.mkdir(parents=True)
    gate_path.parent.mkdir(parents=True)
    artifact_path.write_text(json.dumps(_accepted_artifact(), indent=2) + "\n", encoding="utf-8")
    gate_path.write_text("# Gate\n\n## Candidates\n\n## Processed\n", encoding="utf-8")

    monkeypatch.setattr(helper, "REPO_ROOT", tmp_repo)
    monkeypatch.setattr(helper, "profile_dir", lambda user_id: tmp_repo / "users" / user_id)
    monkeypatch.setattr(helper, "read_path", lambda path: path.read_text(encoding="utf-8"))
    events: list[dict] = []

    def _fake_append_pipeline_event(user_id, event_type, candidate_id, merge=None, extras=None):
        events.append(
            {
                "user_id": user_id,
                "event_type": event_type,
                "candidate_id": candidate_id,
                "merge": merge or {},
                "extras": extras or {},
            }
        )
        return {"event": event_type, "candidate_id": candidate_id}

    monkeypatch.setattr(helper, "append_pipeline_event", _fake_append_pipeline_event)

    result = helper.promote_artifact_to_gate(
        artifact_path,
        user_id="demo",
        review_note="Operator reviewed grounding and wants gate visibility.",
        lane_name="swarm",
        candidate_source="auto-research/swarm",
        extra_auto_research_metadata={"swarm_origin_lane": "self-proposals"},
    )

    updated_gate = gate_path.read_text(encoding="utf-8")
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))

    assert result["candidate_id"] == "CANDIDATE-0001"
    assert 'lane: "swarm"' in updated_gate
    assert 'candidate_source: "auto-research/swarm"' in updated_gate
    assert 'swarm_origin_lane: "self-proposals"' in updated_gate
    assert events[0]["event_type"] == "staged"
    assert events[0]["merge"]["candidate_source"] == "auto-research/swarm"
    assert artifact["staged_candidate_id"] == "CANDIDATE-0001"
    assert artifact["promotion_lane"] == "swarm"


def test_swarm_orchestrator_refreshes_state(tmp_path, monkeypatch):
    orchestrator = _load("swarm_orchestrator_state_test", SWARM / "orchestrator.py")
    tmp_repo = tmp_path / "repo"
    accepted_dir = tmp_repo / "auto-research" / "self-proposals" / "accepted"
    swarm_dir = tmp_repo / "auto-research" / "swarm"
    accepted_dir.mkdir(parents=True)
    swarm_dir.mkdir(parents=True)

    first = _accepted_artifact()
    second = _accepted_artifact()
    second["promoted_to_gate_at"] = "2026-03-31T18:00:00+00:00"
    second["staged_candidate_id"] = "CANDIDATE-0099"

    newest = accepted_dir / "accepted-new.json"
    older = accepted_dir / "accepted-old.json"
    newest.write_text(json.dumps(first, indent=2) + "\n", encoding="utf-8")
    older.write_text(json.dumps(second, indent=2) + "\n", encoding="utf-8")

    monkeypatch.setattr(orchestrator, "REPO_ROOT", tmp_repo)
    monkeypatch.setattr(orchestrator, "AUTO_RESEARCH_DIR", tmp_repo / "auto-research")
    monkeypatch.setattr(orchestrator, "SWARM_DIR", swarm_dir)
    monkeypatch.setattr(orchestrator, "STATE_PATH", swarm_dir / "swarm-state.json")
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

    state = orchestrator.refresh_swarm_state(user_id="demo")

    assert state["artifact_count"] == 2
    assert state["pending_artifact_count"] == 1
    assert state["promoted_artifact_count"] == 1
    assert state["top_artifact"]["artifact_name"] == "accepted-new.json"
    assert orchestrator.STATE_PATH.is_file()


def test_swarm_orchestrator_runs_auto_dream(monkeypatch):
    orchestrator = _load("swarm_orchestrator_dream_test", SWARM / "orchestrator.py")
    calls: list[dict] = []

    def _fake_run_auto_dream_job(*, user_id: str, apply: bool, emit_event: bool, write_artifacts: bool, strict_mode: bool):
        calls.append(
            {
                "user_id": user_id,
                "apply": apply,
                "emit_event": emit_event,
                "write_artifacts": write_artifacts,
                "strict_mode": strict_mode,
            }
        )
        return {"user_id": user_id, "self_memory": {"changed": False}, "contradiction_digest": {"reviewable_count": 0, "relation_counts": {}}}

    monkeypatch.setattr(orchestrator, "_run_auto_dream_job", _fake_run_auto_dream_job)
    summary = orchestrator.run_auto_dream(user_id="demo", dry_run=True, strict_mode=True)

    assert summary["user_id"] == "demo"
    assert calls == [
        {
            "user_id": "demo",
            "apply": False,
            "emit_event": False,
            "write_artifacts": False,
            "strict_mode": True,
        }
    ]


class _DummyMessage:
    def __init__(self) -> None:
        self.replies: list[str] = []

    async def reply_text(self, text: str) -> None:
        self.replies.append(text)


class _DummyUpdate:
    def __init__(self, chat_id: int = 1, user_id: int = 2) -> None:
        self.message = _DummyMessage()
        self.effective_chat = types.SimpleNamespace(id=chat_id)
        self.effective_user = types.SimpleNamespace(id=user_id)


class _DummyContext:
    def __init__(self, args: list[str] | None = None) -> None:
        self.args = args or []


def _load_bot_module():
    try:
        import telegram  # noqa: F401
        return importlib.import_module("bot.bot")
    except Exception as exc:  # pragma: no cover - environment-dependent skip
        pytest.skip(f"bot module unavailable in test environment: {exc}")


def test_swarm_status_command_is_operator_only(monkeypatch):
    bot_mod = _load_bot_module()
    update = _DummyUpdate()
    context = _DummyContext()

    monkeypatch.setattr(bot_mod, "OPERATOR_CHAT_ID", "999")
    monkeypatch.setattr(bot_mod, "_is_operator_chat", lambda update: False)

    asyncio.run(bot_mod.swarm_status_command(update, context))

    assert update.message.replies == ["this command is operator-only."]


def test_swarm_promote_command_stages_candidate(monkeypatch):
    bot_mod = _load_bot_module()
    update = _DummyUpdate(chat_id=123, user_id=456)
    context = _DummyContext(["latest", "Operator", "reviewed", "grounding"])

    monkeypatch.setattr(bot_mod, "OPERATOR_CHAT_ID", "123")
    monkeypatch.setattr(bot_mod, "_is_operator_chat", lambda update: True)
    monkeypatch.setattr(
        bot_mod,
        "SWARM_ORCHESTRATOR",
        types.SimpleNamespace(promote_swarm_artifact=lambda *args, **kwargs: None),
    )

    async def _fake_run_blocking(func, *args, **kwargs):
        assert args == ("latest",)
        assert kwargs["review_note"] == "Operator reviewed grounding"
        assert kwargs["user_id"] == bot_mod.USER_ID
        return {
            "candidate_id": "CANDIDATE-0101",
            "artifact_relpath": "auto-research/self-proposals/accepted/example.json",
        }

    monkeypatch.setattr(bot_mod, "_run_blocking", _fake_run_blocking)

    asyncio.run(bot_mod.swarm_promote_command(update, context))

    assert "CANDIDATE-0101 staged" in update.message.replies[0]


def test_swarm_dream_command_returns_summary(monkeypatch):
    bot_mod = _load_bot_module()
    update = _DummyUpdate(chat_id=123, user_id=456)
    context = _DummyContext()

    monkeypatch.setattr(bot_mod, "OPERATOR_CHAT_ID", "123")
    monkeypatch.setattr(bot_mod, "_is_operator_chat", lambda update: True)
    monkeypatch.setattr(
        bot_mod,
        "SWARM_ORCHESTRATOR",
        types.SimpleNamespace(
            run_auto_dream=lambda *args, **kwargs: None,
            format_auto_dream_status=lambda summary: "autoDream status\nself-memory changed: False",
        ),
    )

    async def _fake_run_blocking(func, *args, **kwargs):
        assert kwargs["user_id"] == bot_mod.USER_ID
        return {
            "user_id": bot_mod.USER_ID,
            "self_memory": {"changed": False},
            "contradiction_digest": {"reviewable_count": 0, "relation_counts": {}},
        }

    monkeypatch.setattr(bot_mod, "_run_blocking", _fake_run_blocking)

    asyncio.run(bot_mod.swarm_dream_command(update, context))

    assert update.message.replies == ["autoDream status\nself-memory changed: False"]
