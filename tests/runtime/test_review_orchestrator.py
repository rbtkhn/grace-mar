"""Tests for scripts/runtime/review_orchestrator.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "runtime" / "review_orchestrator.py"
RO_MOD = REPO_ROOT / "scripts" / "runtime" / "review_orchestrator.py"


def _base_obs(oid: str, lane: str, summary: str, refs: list[str]) -> dict:
    return {
        "obs_id": oid,
        "timestamp": "2026-01-01T12:00:00Z",
        "lane": lane,
        "source_kind": "evidence_ref",
        "title": "t",
        "summary": summary,
        "record_mutation_candidate": False,
        "source_path": None,
        "source_refs": refs,
        "tags": [],
        "confidence": 0.9,
        "contradiction_refs": [],
        "notes": None,
    }


def test_build_review_packet_markdown_unit():
    sys.path.insert(0, str(REPO_ROOT / "scripts" / "runtime"))
    import importlib.util

    spec = importlib.util.spec_from_file_location("review_orchestrator", RO_MOD)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)

    env = {
        "evidence_state": "sufficient",
        "fabricated_history_risk": "low",
        "reasons": ["r1"],
        "missing_evidence_refs": [],
        "conflicting_refs": [],
        "promotion_recommendation": "allow",
    }
    obs = [_base_obs("obs_20260101T120000Z_aaaaaaaa", "work-strategy", "a", ["x"])]
    md = mod.build_review_packet_markdown(
        mode="pre_gate",
        built_iso="2026-01-01T00:00:00Z",
        target_label="obs_20260101T120000Z_aaaaaaaa",
        observations=obs,
        env=env,
        candidate_row=None,
        gate_text_derived=False,
    )
    assert "# Review Packet" in md
    assert "## Evidence Pass" in md
    assert "## Contradiction Pass" in md
    assert "## Boundary Pass" in md
    assert "## Promotion-Risk Pass" in md
    assert "## Synthesis" in md
    assert "## Operator Questions" in md


def test_pre_gate_subprocess(tmp_path: Path) -> None:
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    a = _base_obs("obs_20260101T120000Z_aaaaaaaa", "lane-a", "one", ["ref/1"])
    b = _base_obs("obs_20260101T130000Z_bbbbbbbb", "lane-a", "two", ["ref/2"])
    b["timestamp"] = "2026-01-01T13:00:00Z"
    (obs_dir / "index.jsonl").write_text(json.dumps(a) + "\n" + json.dumps(b) + "\n", encoding="utf-8")
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--mode",
            "pre_gate",
            "--lane",
            "lane-a",
            "--id",
            a["obs_id"],
            "--id",
            b["obs_id"],
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )
    assert r.returncode == 0, r.stderr
    assert "Evidence Pass" in r.stdout
    assert a["obs_id"] in r.stdout


def test_candidate_review_subprocess(tmp_path: Path) -> None:
    user = "testuser"
    udir = tmp_path / "users" / user
    udir.mkdir(parents=True)
    gate = udir / "recursion-gate.md"
    gate.write_text(
        """## Candidates

### CANDIDATE-9999 (orchestrator fixture)

```yaml
status: pending
timestamp: 2026-01-15T12:00:00Z
summary: Fixture summary for packet
mind_category: knowledge
profile_target: IX-A.1
```

## Processed
""",
        encoding="utf-8",
    )
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--mode",
            "candidate_review",
            "--candidate",
            "CANDIDATE-9999",
            "--user",
            user,
            "--repo-root",
            str(tmp_path),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    assert "CANDIDATE-9999" in r.stdout
    assert "gate-text-derived" in r.stdout
    assert "Boundary Pass" in r.stdout
