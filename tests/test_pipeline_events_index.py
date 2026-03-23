"""Pipeline-events single-pass index for parse_review_candidates."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def tmp_user_profile(tmp_path, monkeypatch):
    """Minimal users/<id>/ tree with gate + pipeline-events.jsonl."""
    uid = "perf-test-user"
    ud = tmp_path / "users" / uid
    ud.mkdir(parents=True)
    gate = ud / "recursion-gate.md"
    gate.write_text(
        """# Gate

## Candidates

### CANDIDATE-0001 (test one)
```yaml
status: pending
timestamp: 2025-01-01
summary: "alpha"
profile_target: IX-A.1
```

### CANDIDATE-0002 (test two)
```yaml
status: pending
timestamp: 2025-01-02
summary: "beta"
profile_target: IX-B.1
```

## Processed
""",
        encoding="utf-8",
    )
    (ud / "self.md").write_text("# Self\n", encoding="utf-8")

    lines = []
    for i in range(20):
        lines.append(
            json.dumps(
                {
                    "candidate_id": "CANDIDATE-0001",
                    "event": "staged",
                    "ts": f"2025-01-01T00:00:{i:02d}Z",
                }
            )
        )
    for i in range(15):
        lines.append(
            json.dumps(
                {
                    "candidate_id": "CANDIDATE-0002",
                    "event": "applied",
                    "ts": f"2025-01-02T00:00:{i:02d}Z",
                }
            )
        )
    (ud / "pipeline-events.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")

    import sys

    sys.path.insert(0, str(REPO_ROOT))
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import recursion_gate_review as rgr

    def _pd(u: str):
        if u == uid:
            return ud
        return REPO_ROOT / "users" / u

    monkeypatch.setattr(rgr, "_profile_dir", _pd)
    monkeypatch.setattr(rgr, "DEFAULT_USER", uid)
    return uid, rgr, ud


def test_pipeline_events_index_last_eight_per_candidate(tmp_user_profile):
    uid, rgr, _ud = tmp_user_profile
    idx = rgr._pipeline_events_index(uid)
    assert len(idx["CANDIDATE-0001"]) == 8
    assert idx["CANDIDATE-0001"][-1]["ts"] == "2025-01-01T00:00:19Z"
    assert len(idx["CANDIDATE-0002"]) == 8
    assert idx["CANDIDATE-0002"][-1]["ts"] == "2025-01-02T00:00:14Z"


def test_parse_review_candidates_reads_pipeline_file_once(tmp_user_profile):
    uid, rgr, ud = tmp_user_profile
    pe = ud / "pipeline-events.jsonl"
    real_read = Path.read_text
    calls = {"n": 0}

    def counting_read(self, *args, **kwargs):
        if self.resolve() == pe.resolve():
            calls["n"] += 1
        return real_read(self, *args, **kwargs)

    with patch.object(Path, "read_text", counting_read):
        rows = rgr.parse_review_candidates(user_id=uid)

    assert calls["n"] == 1
    assert len(rows) == 2
    assert len(rows[0]["audit_trail"]) <= 8


def test_pipeline_events_for_candidate_matches_index(tmp_user_profile):
    uid, rgr, _ud = tmp_user_profile
    idx = rgr._pipeline_events_index(uid)
    assert rgr._pipeline_events_for_candidate(uid, "CANDIDATE-0001") == idx["CANDIDATE-0001"]
