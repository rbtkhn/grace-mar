"""emit_pipeline_event.append_pipeline_event returns emitted dict."""

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import emit_pipeline_event as epe  # noqa: E402


def test_append_pipeline_event_writes_and_returns_id(monkeypatch):
    with tempfile.TemporaryDirectory() as td:
        user = "test-user-emit"
        fake_root = Path(td)
        monkeypatch.setattr(epe, "REPO_ROOT", fake_root)
        out = epe.append_pipeline_event(
            user,
            "maintenance",
            None,
            merge={"action": "unit_test_emit"},
        )
        assert out.get("event_id", "").startswith("evt_")
        assert out.get("fork_id") == user
        assert out["event"] == "maintenance"
        path = fake_root / "users" / user / "pipeline-events.jsonl"
        assert path.is_file()
        line = path.read_text(encoding="utf-8").strip().splitlines()[-1]
        row = json.loads(line)
        assert row["event_id"] == out["event_id"]
