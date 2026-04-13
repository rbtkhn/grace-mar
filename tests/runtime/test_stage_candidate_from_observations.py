"""Tests for scripts/runtime/stage_candidate_from_observations.py."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = REPO_ROOT / "scripts"
RUNTIME = REPO_ROOT / "scripts" / "runtime"

for p in (SCRIPTS, RUNTIME):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


@pytest.fixture
def jsonschema_mod():
    return pytest.importorskip("jsonschema")


def _minimal_obs(
    oid: str,
    *,
    lane: str = "work-strategy",
    title: str = "T",
    summary: str = "S",
    source_refs: list[str] | None = None,
    contradiction_refs: list[str] | None = None,
    confidence: float | None = None,
) -> dict:
    return {
        "obs_id": oid,
        "timestamp": "2020-01-01T12:00:00Z",
        "lane": lane,
        "source_kind": "manual_note",
        "title": title,
        "summary": summary,
        "record_mutation_candidate": False,
        "tags": [],
        "source_refs": source_refs or [],
        "contradiction_refs": contradiction_refs or [],
        "confidence": confidence,
    }


def _write_ledger(tmp_path: Path, rows: list[dict]) -> None:
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    path = obs_dir / "index.jsonl"
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def _minimal_gate(user_dir: Path) -> None:
    gate = user_dir / "recursion-gate.md"
    gate.parent.mkdir(parents=True, exist_ok=True)
    gate.write_text(
        "# Gate\n\n## Candidates\n\n## Processed\n\n",
        encoding="utf-8",
    )


def test_stages_candidate_from_valid_ids(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    jsonschema_mod,
) -> None:
    uid = "test-stage-user"
    user_root = tmp_path / "users" / uid
    _minimal_gate(user_root)
    rows = [
        _minimal_obs(
            "obs_20200101T100000Z_aaaaaaaa",
            title="One",
            summary="alpha",
            source_refs=["ref:a"],
            contradiction_refs=["c1"],
            confidence=0.5,
        ),
        _minimal_obs(
            "obs_20200101T110000Z_bbbbbbbb",
            title="Two",
            summary="beta",
            source_refs=["ref:a", "ref:b"],
            contradiction_refs=["c2"],
            confidence=1.0,
        ),
    ]
    _write_ledger(tmp_path, rows)

    monkeypatch.setenv("GRACE_MAR_RUNTIME_LEDGER_ROOT", str(tmp_path))

    import stage_candidate_from_observations as sc

    monkeypatch.setattr(sc, "profile_dir", lambda u: tmp_path / "users" / u)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "stage_candidate_from_observations",
            "-u",
            uid,
            "--lane",
            "work-strategy",
            "--id",
            "obs_20200101T100000Z_aaaaaaaa",
            "--id",
            "obs_20200101T110000Z_bbbbbbbb",
            "--candidate-type",
            "skill_update",
            "--target-surface",
            "SKILLS",
            "--target-path",
            "skills-portable/x.md",
            "--proposal-summary",
            "Summary line for gate",
            "--proposed-change",
            "Do the thing.",
            "--why-now",
            "Because tests.",
            "--dry-run",
        ],
    )
    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        assert sc.main() == 0
    out = buf.getvalue()
    assert "RUNTIME_OBSERVATION_PROPOSAL" in out
    assert "status: pending" in out
    assert "obs_20200101T100000Z_aaaaaaaa" in out
    assert "ref:a" in out and "ref:b" in out
    assert "c1" in out and "c2" in out
    assert "candidate_type: skill_update" in out
    assert "target_surface: SKILLS" in out


def test_rejects_missing_observation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    uid = "u2"
    _minimal_gate(tmp_path / "users" / uid)
    _write_ledger(tmp_path, [])

    monkeypatch.setenv("GRACE_MAR_RUNTIME_LEDGER_ROOT", str(tmp_path))

    import stage_candidate_from_observations as sc

    monkeypatch.setattr(sc, "profile_dir", lambda u: tmp_path / "users" / u)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "x",
            "-u",
            uid,
            "--lane",
            "work-strategy",
            "--id",
            "obs_20200101T100000Z_aaaaaaaa",
            "--candidate-type",
            "other",
            "--target-surface",
            "OTHER",
            "--proposal-summary",
            "x",
            "--proposed-change",
            "y",
            "--dry-run",
        ],
    )
    assert sc.main() == 2


def test_rejects_mixed_lane_without_flag(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    uid = "u3"
    _minimal_gate(tmp_path / "users" / uid)
    rows = [
        _minimal_obs("obs_20200101T100000Z_aaaaaaaa", lane="work-strategy"),
        _minimal_obs("obs_20200101T110000Z_bbbbbbbb", lane="other-lane"),
    ]
    _write_ledger(tmp_path, rows)

    monkeypatch.setenv("GRACE_MAR_RUNTIME_LEDGER_ROOT", str(tmp_path))

    import stage_candidate_from_observations as sc

    monkeypatch.setattr(sc, "profile_dir", lambda u: tmp_path / "users" / u)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "x",
            "-u",
            uid,
            "--lane",
            "work-strategy",
            "--id",
            "obs_20200101T100000Z_aaaaaaaa",
            "--id",
            "obs_20200101T110000Z_bbbbbbbb",
            "--candidate-type",
            "other",
            "--target-surface",
            "OTHER",
            "--proposal-summary",
            "x",
            "--proposed-change",
            "y",
            "--dry-run",
        ],
    )
    assert sc.main() == 2


def test_merge_skip_predicate() -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import process_approved_candidates as pac

    fn = getattr(pac, "_is_runtime_observation_proposal")
    block = "proposal_class: RUNTIME_OBSERVATION_PROPOSAL\nsummary: x\n"
    assert fn({"block": block}) is True
    assert fn({"block": "proposal_class: META_INFRA\n"}) is False


def test_does_not_touch_self(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, jsonschema_mod) -> None:
    uid = "u4"
    user_root = tmp_path / "users" / uid
    _minimal_gate(user_root)
    self_path = user_root / "self.md"
    self_path.write_text("# Self\n", encoding="utf-8")
    rows = [_minimal_obs("obs_20200101T100000Z_aaaaaaaa")]
    _write_ledger(tmp_path, rows)

    monkeypatch.setenv("GRACE_MAR_RUNTIME_LEDGER_ROOT", str(tmp_path))

    import stage_candidate_from_observations as sc

    monkeypatch.setattr(sc, "profile_dir", lambda u: tmp_path / "users" / u)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "x",
            "-u",
            uid,
            "--lane",
            "work-strategy",
            "--id",
            "obs_20200101T100000Z_aaaaaaaa",
            "--candidate-type",
            "other",
            "--target-surface",
            "OTHER",
            "--proposal-summary",
            "x",
            "--proposed-change",
            "y",
            "--dry-run",
        ],
    )
    assert sc.main() == 0
    assert self_path.read_text(encoding="utf-8") == "# Self\n"
