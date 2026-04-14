"""Tests for scripts/build_gate_board.py (derived Kanban view; read-only)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"

FIXTURE_GATE = """# Test gate

## Candidates

### CANDIDATE-9001 (contradiction pending)

```yaml
status: pending
mind_category: knowledge
profile_target: IX-A. KNOWLEDGE
channel_key: operator:cursor
summary: unresolved contradiction with Record
```

### CANDIDATE-9002 (approved active)

```yaml
status: approved
mind_category: knowledge
profile_target: IX-A. KNOWLEDGE
channel_key: operator:cursor
summary: approved not yet merged
```

### CANDIDATE-9003 (needs evidence)

```yaml
status: pending
mind_category: knowledge
profile_target: IX-A. KNOWLEDGE
channel_key: operator:cursor
summary: This is a long enough summary line for the test fixture to avoid the new bucket.
```

## Processed

### CANDIDATE-9004 (merged)

```yaml
status: approved
mind_category: personality
profile_target: IX-C. PERSONALITY
channel_key: operator:cursor
summary: integrated history
```

### CANDIDATE-9005 (rejected processed)

```yaml
status: rejected
mind_category: knowledge
profile_target: IX-A. KNOWLEDGE
channel_key: telegram:x
summary: rejected in processed
```

"""


def test_build_gate_board_subprocess(tmp_path: Path) -> None:
    uid = "fixture-gate-board"
    root = tmp_path / "repo"
    udir = root / "users" / uid
    udir.mkdir(parents=True)
    (udir / "recursion-gate.md").write_text(FIXTURE_GATE, encoding="utf-8")
    (udir / "self.md").write_text("# Self\n\n", encoding="utf-8")
    out = tmp_path / "gate-board.md"

    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "build_gate_board.py"),
            "-u",
            uid,
            "--repo-root",
            str(root),
            "--output",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    text = out.read_text(encoding="utf-8")
    assert "CANDIDATE-9001" in text
    assert "CANDIDATE-9002" in text
    assert "CANDIDATE-9003" in text
    assert "CANDIDATE-9004" in text
    assert "CANDIDATE-9005" in text

    # Section headers and placement (Kanban columns)
    assert "## Needs contradiction check" in text
    idx_c = text.index("CANDIDATE-9001")
    idx_section = text.rindex("## Needs contradiction check", 0, idx_c)
    assert idx_section < idx_c

    idx_a = text.index("CANDIDATE-9002")
    idx_ap = text.rindex("## Approved", 0, idx_a)
    assert idx_ap < idx_a

    idx_e = text.index("CANDIDATE-9003")
    idx_ne = text.rindex("## Needs evidence", 0, idx_e)
    assert idx_ne < idx_e

    idx_m = text.index("CANDIDATE-9004")
    idx_mg = text.rindex("## Merged", 0, idx_m)
    assert idx_mg < idx_m

    idx_r = text.index("CANDIDATE-9005")
    idx_rj = text.rindex("## Rejected", 0, idx_r)
    assert idx_rj < idx_r
