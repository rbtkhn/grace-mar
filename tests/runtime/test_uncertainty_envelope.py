"""Golden tests for uncertainty envelope derivation and CLI scripts."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RUNTIME = REPO_ROOT / "scripts" / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from uncertainty_envelope import compute_envelope  # noqa: E402


def _base(
    oid: str,
    summary: str,
    *,
    refs: list[str] | None = None,
    contra: list[str] | None = None,
    record_mut: bool = False,
    kind: str = "manual_note",
    conf: float | None = None,
) -> dict:
    return {
        "obs_id": oid,
        "timestamp": "2026-01-01T12:00:00Z",
        "lane": "test",
        "source_kind": kind,
        "title": "T",
        "summary": summary,
        "record_mutation_candidate": record_mut,
        "source_path": None,
        "source_refs": refs or [],
        "tags": [],
        "confidence": conf,
        "contradiction_refs": contra or [],
        "notes": None,
    }


def test_conflicted_overrides_sufficient_signals():
    rows = [
        _base(
            "obs_20260101T120000Z_aaaaaaaa",
            "A",
            refs=["evidence/x"],
            contra=["IX-A-1"],
        ),
        _base("obs_20260101T130000Z_bbbbbbbb", "B", refs=["evidence/y"]),
    ]
    env = compute_envelope(rows)
    assert env["evidence_state"] == "conflicted"
    assert env["promotion_recommendation"] == "block"
    assert env["conflicting_refs"]


def test_sufficient_two_obs_with_refs():
    rows = [
        _base("obs_20260101T120000Z_aaaaaaaa", "one", refs=["a/1"]),
        _base("obs_20260101T130000Z_bbbbbbbb", "two", refs=["a/2"]),
    ]
    env = compute_envelope(rows)
    assert env["evidence_state"] == "sufficient"
    assert env["fabricated_history_risk"] == "low"
    assert env["promotion_recommendation"] == "allow"


def test_insufficient_no_refs():
    rows = [
        _base("obs_20260101T120000Z_aaaaaaaa", "x" * 120, refs=[]),
    ]
    env = compute_envelope(rows)
    assert env["evidence_state"] == "insufficient"
    assert env["promotion_recommendation"] == "hold"


def test_fabricated_high_single_durable_without_refs():
    rows = [
        _base(
            "obs_20260101T120000Z_aaaaaaaa",
            "We should update the Record.",
            refs=[],
            record_mut=True,
        ),
    ]
    env = compute_envelope(rows)
    assert env["fabricated_history_risk"] == "high"
    assert env["promotion_recommendation"] == "block"


def test_score_evidence_cli(tmp_path):
    oid = "obs_20260101T120000Z_aaaaaaaa"
    row = _base(oid, "one", refs=["z/9"])
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    (obs_dir / "index.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable,
            str(RUNTIME / "score_evidence_sufficiency.py"),
            "--id",
            oid,
            "--json",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert "evidence_state" in out


def test_flag_fabricated_cli(tmp_path):
    oid = "obs_20260101T120000Z_aaaaaaaa"
    row = _base(oid, "born in 1990 without docs", refs=[], record_mut=True)
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    (obs_dir / "index.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable,
            str(RUNTIME / "flag_fabricated_history_risk.py"),
            "--id",
            oid,
            "--json",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["fabricated_history_risk"] in ("high", "medium", "low")
