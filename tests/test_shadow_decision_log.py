"""Shadow decision JSONL."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from work_dev.log_shadow_decision import append_shadow_decision  # noqa: E402


def test_append_shadow_decision(tmp_path: Path) -> None:
    p = tmp_path / "shadow.jsonl"
    append_shadow_decision(
        {"runtime": "t", "task_type": "x", "agent_action": "a", "human_action": "b"},
        log_path=p,
    )
    line = p.read_text(encoding="utf-8").strip()
    o = json.loads(line)
    assert o["runtime"] == "t"
    assert "ts" in o
