"""Tests for GRACE_MAR_PROFILE_DIR retriever + simulate_fork_scenario helpers."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _minimal_profile(tmp_path: Path) -> Path:
    prof = tmp_path / "snap"
    prof.mkdir()
    (prof / "self.md").write_text(
        'id: LEARN-0001\ndate: 2020-01-01\ntopic: "cats"\nher_understanding: "fuzzy"\n',
        encoding="utf-8",
    )
    for n in (
        "self-skills.md",
        "skill-think.md",
        "work-alpha-school.md",
        "work-jiang.md",
        "self-archive.md",
    ):
        (prof / n).write_text("", encoding="utf-8")
    (prof / "skill-write.md").write_text(
        """
## WRITE Container

- id: WRITE-0001
status: ACTIVE
dominant_mode: "Personal narrative"
complexity_level: 2
style_level: 2
expression_level: 2
logic_level: 2
edge: "Longer stories"
""".strip()
        + "\n",
        encoding="utf-8",
    )
    return prof


def test_grace_mar_profile_dir_retrieve(tmp_path, monkeypatch):
    prof = _minimal_profile(tmp_path)
    monkeypatch.setenv("GRACE_MAR_PROFILE_DIR", str(prof))
    monkeypatch.setenv("GRACE_MAR_USER_ID", "grace-mar")
    monkeypatch.setenv("GRACE_MAR_RETRIEVER_CACHE", "0")

    import bot.retriever as retriever

    importlib.reload(retriever)
    assert retriever.PROFILE_DIR.resolve() == prof.resolve()
    out = retriever.retrieve("cats fuzzy", top_k=2)
    assert out and "LEARN-0001" in out[0][0]


def test_retriever_labels_skill_write_chunks(tmp_path, monkeypatch):
    prof = _minimal_profile(tmp_path)
    monkeypatch.setenv("GRACE_MAR_PROFILE_DIR", str(prof))
    monkeypatch.setenv("GRACE_MAR_USER_ID", "grace-mar")
    monkeypatch.setenv("GRACE_MAR_RETRIEVER_CACHE", "0")

    import bot.retriever as retriever

    importlib.reload(retriever)
    chunks = retriever.load_record_chunks()
    assert any("SKILLS/WRITE" in text for _, text in chunks)


@patch("openai.OpenAI")
def test_run_single_query_mocked(mock_oi, tmp_path, monkeypatch):
    prof = _minimal_profile(tmp_path)
    monkeypatch.setenv("GRACE_MAR_PROFILE_DIR", str(prof))
    monkeypatch.setenv("GRACE_MAR_USER_ID", "grace-mar")
    monkeypatch.setenv("GRACE_MAR_RETRIEVER_CACHE", "0")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    import bot.retriever as retriever

    importlib.reload(retriever)

    mock_oi.return_value.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="i'd think about it [LEARN-0001]."))]
    )

    from simulate_fork_scenario import _estimate_confidence, _run_single_query

    r = _run_single_query(
        idx=0,
        scenario="Should I get a cat?",
        mode="conservative",
        user_id="grace-mar",
        top_k=4,
        use_chroma=False,
        max_tokens=200,
        model="gpt-4o",
    )
    assert "LEARN-0001" in r["response"]
    assert _estimate_confidence(r["response"]) >= 70


def test_export_prp_respects_profile_dir(tmp_path, monkeypatch):
    prof = _minimal_profile(tmp_path)
    monkeypatch.setenv("GRACE_MAR_PROFILE_DIR", str(prof))
    from export_prp import export_prp

    text = export_prp(user_id="grace-mar")
    assert "cats" in text.lower() or "fuzzy" in text.lower()
    assert "## WRITE" in text
    assert "Current writing range" in text
