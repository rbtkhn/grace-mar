"""Policy mode checks on stage_candidate_from_observations (exit before ledger access when blocked)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "runtime" / "stage_candidate_from_observations.py"


def test_reference_only_blocks_before_obs_lookup() -> None:
    env = {**os.environ, "GRACE_MAR_POLICY_MODE": "reference_only"}
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--lane",
            "work-strategy",
            "--id",
            "obs_never_read",
            "--candidate-type",
            "other",
            "--target-surface",
            "SELF",
            "--proposal-summary",
            "x",
            "--proposed-change",
            "y",
        ],
        env=env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 2
    assert "policy mode" in (r.stderr or "").lower()
