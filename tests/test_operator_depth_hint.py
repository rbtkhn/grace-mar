"""Tests for scripts/operator_depth_hint.py."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import operator_depth_hint as odh  # noqa: E402

UTC = timezone.utc


def _line(event: str, ts: datetime) -> str:
    o = {"ts": ts.isoformat(), "event": event, "candidate_id": "CANDIDATE-0001"}
    return json.dumps(o)


def test_tier_from_counts():
    assert odh._tier_from_counts(0, 0) == 0
    assert odh._tier_from_counts(3, 0) == 1
    assert odh._tier_from_counts(0, 5) == 1
    assert odh._tier_from_counts(8, 0) == 2
    assert odh._tier_from_counts(20, 0) == 3


def test_analyze_velocity_window(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    uid = "u1"
    ud = tmp_path / "users" / uid
    ud.mkdir(parents=True)
    now = datetime(2026, 3, 1, 12, 0, 0, tzinfo=UTC)
    old = now - timedelta(days=10)
    lines = [
        _line("applied", old),
        _line("applied", now - timedelta(days=1)),
        _line("applied", now - timedelta(days=2)),
        _line("applied", now - timedelta(days=3)),
        _line("approved", now - timedelta(hours=1)),
    ]
    (ud / "pipeline-events.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")

    monkeypatch.setattr(odh, "profile_dir", lambda u: tmp_path / "users" / u)
    snap = odh.analyze_velocity(uid, window_days=7, now=now)
    assert snap.applied == 3
    assert snap.approved == 1
    assert snap.tier >= 1


def test_maybe_emit_only_on_tier_increase(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(odh, "profile_dir", lambda u: tmp_path / "users" / u)
    emitted: list[bool] = []

    def fake_append(*a, **k):
        emitted.append(True)

    monkeypatch.setattr(odh, "append_harness_event", fake_append)

    uid = "u1"
    snap = odh.VelocitySnapshot(7, 3, 0, 1)
    e1, _ = odh.maybe_emit_tier_hint(uid, snap, dry_run=False)
    assert e1 is True
    assert len(emitted) == 1

    e2, _ = odh.maybe_emit_tier_hint(uid, snap, dry_run=False)
    assert e2 is False
    assert len(emitted) == 1

    snap2 = odh.VelocitySnapshot(7, 10, 0, 2)
    e3, _ = odh.maybe_emit_tier_hint(uid, snap2, dry_run=False)
    assert e3 is True
    assert len(emitted) == 2
