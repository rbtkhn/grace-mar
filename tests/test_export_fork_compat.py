"""Fork export: self_skills / self_evidence keys, deprecated mirrors, _compat map."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_export_fork_has_new_keys_and_compat() -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from export_fork import export_fork

    data = export_fork("grace-mar", include_raw=True)
    assert data["version"] == "1.2"
    assert "_compat" in data
    dep = data["_compat"]["deprecated_keys"]
    assert dep["skills"] == "self_skills"
    assert dep["evidence"] == "self_evidence"
    assert dep["library"] == "self_library"
    assert "self_skills" in data
    assert "self_evidence" in data
    sk = data["self_skills"].get("raw")
    assert sk is not None
    assert data["skills"]["raw"] == sk
    ev = data["self_evidence"].get("raw")
    assert ev is not None
    assert data["evidence"]["raw"] == ev
