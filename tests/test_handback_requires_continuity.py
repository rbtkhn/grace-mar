"""Handback server OpenClaw path requires continuity gate."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def handback_module():
    import importlib

    sdir = str(REPO_ROOT / "scripts")
    if sdir not in sys.path:
        sys.path.insert(0, sdir)
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    import handback_server as hs

    importlib.reload(hs)
    return hs


def test_openclaw_stage_returns_428_when_no_receipt(handback_module, monkeypatch: pytest.MonkeyPatch) -> None:
    hs = handback_module
    monkeypatch.setattr(
        hs,
        "_continuity_gate_openclaw",
        lambda uid: (False, "no valid continuity receipt", {}),
    )
    def _no_stage(*a, **k):
        raise AssertionError("_run_stage should not run when continuity fails")

    monkeypatch.setattr(hs, "_run_stage", _no_stage)
    client = hs.app.test_client()
    rv = client.post(
        "/stage",
        json={
            "content": "we read a book",
            "source": "openclaw_stage",
            "user_id": "grace-mar",
        },
    )
    assert rv.status_code == 428
    data = rv.get_json()
    assert data.get("continuity_required") is True


def test_openclaw_stage_proceeds_when_receipt_ok(handback_module, monkeypatch: pytest.MonkeyPatch) -> None:
    hs = handback_module
    monkeypatch.setattr(
        hs,
        "_continuity_gate_openclaw",
        lambda uid: (
            True,
            "",
            {
                "continuity_receipt_path": "runtime/continuity/receipts/test.json",
                "continuity_receipt_valid": True,
                "continuity_checked_at": "2026-03-25T12:00:00Z",
            },
        ),
    )
    monkeypatch.setattr(hs, "_run_stage", lambda *a, **k: (True, 0))
    client = hs.app.test_client()
    rv = client.post(
        "/stage",
        json={
            "content": "we read a book",
            "source": "openclaw_stage",
            "user_id": "grace-mar",
        },
    )
    assert rv.status_code == 200
    data = rv.get_json()
    assert data.get("ok") is True


def test_browser_stage_skips_continuity_gate(handback_module, monkeypatch: pytest.MonkeyPatch) -> None:
    hs = handback_module
    called: list[bool] = []

    def boom(uid: str):
        called.append(True)
        return (False, "should not run", {})

    monkeypatch.setattr(hs, "_continuity_gate_openclaw", boom)
    monkeypatch.setattr(hs, "_run_stage", lambda *a, **k: (False, 0))
    client = hs.app.test_client()
    rv = client.post(
        "/stage",
        json={"content": "we read a page", "user_id": "grace-mar"},
    )
    assert rv.status_code == 200
    assert not called
