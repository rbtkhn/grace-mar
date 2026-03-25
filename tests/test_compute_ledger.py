"""Integration compute-ledger append helper."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from emit_compute_ledger import append_integration_ledger  # noqa: E402


def test_append_integration_ledger_writes_line(tmp_path: Path) -> None:
    append_integration_ledger(
        "u1",
        operation="test_op",
        runtime="test_rt",
        success=True,
        wall_ms=10,
        bytes_processed=100,
        source_artifact_count=2,
        repo_root=tmp_path,
    )
    p = tmp_path / "users" / "u1" / "compute-ledger.jsonl"
    assert p.is_file()
    line = p.read_text(encoding="utf-8").strip().splitlines()[-1]
    o = json.loads(line)
    assert o["operation"] == "test_op"
    assert o["bucket"] == "integration"
    assert o["success"] is True
