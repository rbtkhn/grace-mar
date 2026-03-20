"""pipeline_correlation: staged → applied lookup."""

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from pipeline_correlation import find_staged_event_id_for_candidate  # noqa: E402


def test_find_staged_event_id_latest():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        p = Path(f.name)
        f.write(
            json.dumps(
                {
                    "ts": "2026-01-01T00:00:00",
                    "event": "staged",
                    "candidate_id": "CANDIDATE-0001",
                    "event_id": "evt_old",
                }
            )
            + "\n"
        )
        f.write(
            json.dumps(
                {
                    "ts": "2026-01-02T00:00:00",
                    "event": "staged",
                    "candidate_id": "CANDIDATE-0001",
                    "event_id": "evt_new",
                }
            )
            + "\n"
        )

    try:
        assert find_staged_event_id_for_candidate(p, "CANDIDATE-0001") == "evt_new"
    finally:
        p.unlink(missing_ok=True)


def test_find_staged_event_id_missing():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        p = Path(f.name)
        f.write("{}\n")
    try:
        assert find_staged_event_id_for_candidate(p, "CANDIDATE-9999") is None
    finally:
        p.unlink(missing_ok=True)


def test_find_staged_event_id_no_event_id_field():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        p = Path(f.name)
        f.write(
            json.dumps(
                {"ts": "2026-01-01T00:00:00", "event": "staged", "candidate_id": "CANDIDATE-0002"}
            )
            + "\n"
        )
    try:
        assert find_staged_event_id_for_candidate(p, "candidate-0002") is None
    finally:
        p.unlink(missing_ok=True)
