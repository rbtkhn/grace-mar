"""Dream.json budget behavior on civ-mem and rollup (auto_dream handoff path)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import auto_dream  # noqa: E402


def _minimal_user(tmp_path: Path) -> Path:
    users_dir = tmp_path / "users"
    ud = users_dir / "demo"
    ud.mkdir(parents=True)
    (ud / "self.md").write_text("# SELF\n", encoding="utf-8")
    (ud / "recursion-gate.md").write_text("# Gate\n\n## Candidates\n\n## Processed\n", encoding="utf-8")
    (ud / "self-memory.md").write_text(
        "# MEMORY\n\n## Short-term\n\nhello\n",
        encoding="utf-8",
    )
    return users_dir


def test_apply_civmem_budget_disabled(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    users_dir = _minimal_user(tmp_path)
    monkeypatch.setattr(auto_dream, "_run_json_command", lambda *a, **k: {"ok": True, "errors": []})
    monkeypatch.setattr(auto_dream, "_run_text_command", lambda *a, **k: (0, "ok", ""))
    monkeypatch.setattr(auto_dream, "_load_dream_budget_dict", lambda: {"allow_civ_mem_echo": False})
    monkeypatch.setattr(auto_dream, "append_pipeline_event", lambda *a, **k: {"event": "maintenance"})
    summary = auto_dream.run_auto_dream(
        user_id="demo",
        users_dir=users_dir,
        apply=True,
        emit_event=True,
        write_artifacts=False,
    )
    assert summary["civmem_echoes"] == []
    assert summary.get("civmem_suppressed_reason") == "disabled_by_budget"
    assert summary.get("civmem_index_missing") is False


def test_apply_civmem_budget_suppressed_on_governance(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    users_dir = _minimal_user(tmp_path)
    monkeypatch.setattr(auto_dream, "_run_json_command", lambda *a, **k: {"ok": True, "errors": []})
    monkeypatch.setattr(auto_dream, "_run_text_command", lambda *a, **k: (1, "", "gov fail"))
    monkeypatch.setattr(
        auto_dream,
        "_load_dream_budget_dict",
        lambda: {
            "allow_civ_mem_echo": True,
            "suppress_analogy_when_governance_alert": True,
            "suppress_analogy_when_integrity_fails": True,
        },
    )
    monkeypatch.setattr(auto_dream, "append_pipeline_event", lambda *a, **k: {"event": "maintenance"})
    summary = auto_dream.run_auto_dream(
        user_id="demo",
        users_dir=users_dir,
        apply=True,
        emit_event=True,
        write_artifacts=False,
    )
    assert summary["civmem_echoes"] == []
    assert summary.get("civmem_suppressed_reason") == "suppressed_governance_alert"


def test_max_civ_mem_echoes_slices(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    users_dir = _minimal_user(tmp_path)
    monkeypatch.setattr(auto_dream, "_run_json_command", lambda *a, **k: {"ok": True, "errors": []})
    monkeypatch.setattr(auto_dream, "_run_text_command", lambda *a, **k: (0, "ok", ""))
    monkeypatch.setattr(auto_dream, "_load_dream_budget_dict", lambda: {"max_civ_mem_echoes": 2})
    monkeypatch.setattr(auto_dream, "append_pipeline_event", lambda *a, **k: {"event": "maintenance"})

    def fake_compute(**kwargs):
        limit = kwargs.get("limit") or 99
        rows = [
            {"path": "a.md", "overlap": 9, "snippet": "x", "analogy_label": "L", "specificity_pass": True, "score": 1.0},
            {"path": "b.md", "overlap": 8, "snippet": "y", "analogy_label": "L", "specificity_pass": True, "score": 1.0},
            {"path": "c.md", "overlap": 7, "snippet": "z", "analogy_label": "L", "specificity_pass": True, "score": 1.0},
        ]
        return rows[:limit], False

    monkeypatch.setattr(auto_dream, "compute_civmem_echoes", fake_compute)
    summary = auto_dream.run_auto_dream(
        user_id="demo",
        users_dir=users_dir,
        apply=True,
        emit_event=True,
        write_artifacts=False,
    )
    assert len(summary["civmem_echoes"]) == 2


def test_rollup_disabled_replaces_with_empty_shape(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    users_dir = _minimal_user(tmp_path)
    monkeypatch.setattr(auto_dream, "_run_json_command", lambda *a, **k: {"ok": True, "errors": []})
    monkeypatch.setattr(auto_dream, "_run_text_command", lambda *a, **k: (0, "ok", ""))
    monkeypatch.setattr(auto_dream, "_load_dream_budget_dict", lambda: {"allow_rollup": False})
    monkeypatch.setattr(auto_dream, "append_pipeline_event", lambda *a, **k: {"event": "maintenance"})
    summary = auto_dream.run_auto_dream(
        user_id="demo",
        users_dir=users_dir,
        apply=True,
        emit_event=True,
        write_artifacts=False,
    )
    cr = summary["coffee_rollup_24h"]
    assert isinstance(cr, dict)
    assert cr.get("count") == 0
    assert cr.get("note") == "rollup_disabled_by_budget"
