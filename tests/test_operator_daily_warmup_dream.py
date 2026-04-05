"""Tests for last-dream block formatting in operator_daily_warmup."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import operator_daily_warmup as odu  # noqa: E402


def _minimal_dream() -> dict:
    return {
        "generated_at": "2026-04-02T00:00:00+00:00",
        "ok": True,
        "integrity_ok": True,
        "governance_ok": True,
        "self_memory_changed": False,
        "reviewable_count": 1,
        "contradiction_count": 0,
        "tomorrow_inherits": "Tomorrow inherits (hint): **Today / field** — calendar rotation; not policy or Record.",
        "civmem_echoes": [],
        "civmem_index_missing": False,
    }


def test_format_last_dream_collapsed_fewer_lines() -> None:
    lines = odu._format_last_dream_block(_minimal_dream(), verbose_dream=False)
    text = "\n".join(lines)
    assert "Last dream" in text
    assert "Contradiction digest" in text
    assert "Tomorrow inherits" in text
    assert "Coffee (24h rollup)" not in text
    assert "Agent surface" not in text


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

