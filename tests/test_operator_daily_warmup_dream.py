"""Tests for last-dream block formatting in operator_daily_warmup."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import operator_daily_warmup as odu  # noqa: E402
from dream_execution_paths import coffee_menu_hint_from_dream  # noqa: E402


def _minimal_dream() -> dict:
    return {
        "generated_at": "2026-04-02T00:00:00+00:00",
        "ok": True,
        "integrity_ok": True,
        "governance_ok": True,
        "self_memory_changed": False,
        "reviewable_count": 1,
        "contradiction_count": 0,
        "tomorrow_inherits": "Tomorrow inherits (hint): **Daily Brief (generator + watch slices; optional KY-4 intel when chosen)** — calendar rotation; not policy or Record.",
        "civmem_echoes": [],
        "civmem_index_missing": False,
    }


def _quiet_dream() -> dict:
    return {
        "generated_at": "2026-04-02T00:00:00+00:00",
        "ok": True,
        "integrity_ok": True,
        "governance_ok": True,
        "self_memory_changed": False,
        "reviewable_count": 0,
        "contradiction_count": 0,
        "artifact_draft_count": 0,
        "followups": [],
        "tomorrow_inherits": "Tomorrow inherits (hint): **Daily Brief** — hint.",
        "civmem_echoes": [],
        "civmem_index_missing": False,
        "quietRun": True,
    }


def test_format_last_dream_collapsed_fewer_lines() -> None:
    lines = odu._format_last_dream_block(_minimal_dream(), verbose_dream=False)
    text = "\n".join(lines)
    assert "Last dream" in text
    assert "night handoff" in text
    assert "Contradiction digest" in text
    assert "Tomorrow inherits" in text
    assert "Coffee (24h rollup)" not in text
    assert "Agent surface" not in text


def test_quiet_handoff_one_line() -> None:
    lines = odu._format_last_dream_block(_quiet_dream(), verbose_dream=False)
    text = "\n".join(lines)
    assert "quiet handoff" in text
    assert "Last dream (quiet handoff) —" in text
    assert "integrity: pass" in text
    assert "tomorrow inherits:" in text
    assert odu.should_collapse_dream_handoff(_quiet_dream(), verbose_dream=False) is True


def test_quiet_handoff_includes_coffee_echo_line() -> None:
    d = _quiet_dream()
    d["last_coffee_echo"] = {
        "highlight": "Yesterday’s work-start coffee is still the thread. Menu pick: A.",
        "conductor": "toscanini",
    }
    lines = odu._format_last_dream_block(d, verbose_dream=False)
    text = "\n".join(lines)
    assert "Dream picked up yesterday’s" in text
    assert "toscanini" in text


def test_quiet_handoff_includes_conductor_echo_line() -> None:
    d = _quiet_dream()
    d["conductor_rollup_24h"] = {
        "pick_count": 1,
        "outcome_count": 1,
        "completed_passes": 1,
        "off_menu_refusals": 0,
        "last_master": "bernstein",
        "echo": "bernstein carried the latest conductor line; last close: public-stake",
    }
    lines = odu._format_last_dream_block(d, verbose_dream=False)
    text = "\n".join(lines)
    assert "Conductor echo" in text
    assert "bernstein carried" in text


def test_signal_handoff_not_collapsed() -> None:
    d = _minimal_dream()
    assert odu.should_collapse_dream_handoff(d, verbose_dream=False) is False
    lines = odu._format_last_dream_block(d, verbose_dream=False)
    text = "\n".join(lines)
    assert "night handoff" in text
    assert "Contradiction digest: reviewable=1" in text


def test_should_collapse_respects_quietrun_false() -> None:
    d = _quiet_dream()
    d["quietRun"] = False
    assert odu.should_collapse_dream_handoff(d, verbose_dream=False) is False


def test_should_collapse_false_when_verbose() -> None:
    assert odu.should_collapse_dream_handoff(_quiet_dream(), verbose_dream=True) is False


def test_collapsed_includes_agent_surface_when_handoff_has_cursor_model() -> None:
    d = _minimal_dream()
    d["agent_surface"] = {"cursor_model": "Test Model X"}
    lines = odu._format_last_dream_block(d, verbose_dream=False)
    text = "\n".join(lines)
    assert "Agent surface" in text
    assert "Cursor model" in text
    assert "Test Model X" in text


def test_verbose_includes_agent_surface_when_present() -> None:
    d = _minimal_dream()
    d["agent_surface"] = {"cursor_model": "VerboseModel"}
    lines = odu._format_last_dream_block(d, verbose_dream=True)
    text = "\n".join(lines)
    assert "Ran:" in text
    assert "Agent surface" in text
    assert "VerboseModel" in text


def test_verbose_appends_coffee_echo_line() -> None:
    d = _quiet_dream()
    d["reviewable_count"] = 1
    d["last_coffee_echo"] = {
        "highlight": "A short echo line for tests.",
    }
    lines = odu._format_last_dream_block(d, verbose_dream=True)
    text = "\n".join(lines)
    assert "Dream picked up yesterday’s" in text
    assert "A short echo line for tests" in text


def test_format_last_dream_verbose_includes_rollup_keys() -> None:
    d = _minimal_dream()
    d["coffee_rollup_24h"] = {"count": 2, "by_mode": {"work-start": 2}, "by_picked": {"A": 1}}
    d["execution_paths"] = [
        {"id": "today_field", "title": "T", "first_move": "x", "stop_rule": "s", "signals_used": []},
        {"id": "build", "title": "B", "first_move": "y", "stop_rule": "s", "signals_used": []},
        {"id": "steward", "title": "S", "first_move": "z", "stop_rule": "s", "signals_used": []},
    ]
    d["suggested_execution_path_index"] = 0
    lines = odu._format_last_dream_block(d, verbose_dream=True)
    text = "\n".join(lines)
    assert "Coffee (24h rollup)" in text
    assert "menu picks" in text
    assert "Execution paths" in text


def test_build_operator_daily_warmup_accepts_verbose_dream_kwarg() -> None:
    out = odu.build_operator_daily_warmup("grace-mar", verbose_dream=False)
    assert "Daily operator warmup" in out

def test_collapsed_omits_civ_mem_by_default() -> None:
    d = _minimal_dream()
    lines = odu._format_last_dream_block(d, verbose_dream=False)
    text = "\n".join(lines)
    assert "Civ-mem" not in text


def test_collapsed_show_civ_mem_opt_in() -> None:
    d = _minimal_dream()
    lines = odu._format_last_dream_block(d, verbose_dream=False, show_civ_mem=True)
    text = "\n".join(lines)
    assert "Civ-mem" in text


def test_compress_lines_truncates() -> None:
    long_body = [f"- line {i}" for i in range(10)]
    out = odu._compress_lines(long_body, max_lines=4)
    assert len(out) == 4
    assert "(+7 more" in out[-1]


def test_coffee_menu_hint_maps_paths() -> None:
    d = {
        "execution_paths": [
            {"id": "today_field", "title": "Daily Brief / field"},
            {"id": "build", "title": "Build"},
            {"id": "steward", "title": "Steward"},
        ],
        "suggested_execution_path_index": 2,
        "execution_path_suggestion_reason": "gate_backlog",
    }
    hint = coffee_menu_hint_from_dream(d)
    assert hint is not None
    assert "**B — Steward**" in hint
    assert "gate backlog" in hint


def test_coffee_menu_hint_unknown_id_falls_back_to_index() -> None:
    d = {
        "execution_paths": [
            {"id": "today_field", "title": "T"},
            {"id": "build", "title": "B"},
        ],
        "suggested_execution_path_index": 1,
        "execution_path_suggestion_reason": "calendar_mod3",
    }
    hint = coffee_menu_hint_from_dream(d)
    assert hint is not None
    assert "**A — Build**" in hint


def test_coffee_menu_hint_returns_none_without_paths() -> None:
    assert coffee_menu_hint_from_dream({}) is None

