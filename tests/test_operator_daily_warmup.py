"""Focused tests for scripts/operator_daily_warmup.py output contract."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import operator_daily_warmup as odw  # noqa: E402


def test_build_operator_daily_warmup_includes_depth_and_polling_reminder(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(odw, "_read", lambda _: "stub")
    monkeypatch.setattr(odw, "_pending_candidates", lambda *_: [])
    monkeypatch.setattr(odw, "_last_activity_oneliner", lambda _: "ACT-9999 sample activity")
    monkeypatch.setattr(odw, "_session_lines_tail", lambda *_: ["tail one", "tail two"])
    monkeypatch.setattr(odw, "_integrity_errors", lambda _: [])
    monkeypatch.setattr(odw, "_git_status_lines", lambda: [])
    monkeypatch.setattr(odw, "velocity_oneliner", lambda _: "Pipeline velocity (7d): 5 merge(s), 0 approval(s) — tier L1 active.")
    monkeypatch.setattr(odw, "load_fork_config", lambda: {"max_pending_candidates": 10})
    monkeypatch.setattr(
        odw,
        "get_wap_snapshot",
        lambda _uid: {
            "campaign_status": {"primary_date": "May 19, 2026", "days_until_primary": 54},
            "territory_blockers": [{"action": "Address blocker alpha."}],
            "brief_readiness": {"status_counts": {"ready": 5, "watch": 7, "needs_refresh": 1}},
            "content_queue": {"status_counts": {"idea": 2, "draft": 1, "review": 1, "posted": 0}},
            "next_actions": ["Prepare voter registration deadline work."],
        },
    )

    warmup = odw.build_operator_daily_warmup("grace-mar")

    assert "## Pipeline velocity (operator depth)" in warmup
    assert "tier L1 active" in warmup
    assert "## Good morning — KY-4 polling + prediction markets" in warmup
    assert "Polymarket" in warmup
    assert "polling-and-markets.md" in warmup
