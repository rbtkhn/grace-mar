"""Tests for bot/constitutional_layer.py (mocked OpenAI; no network)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from unittest.mock import MagicMock

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def constitutional_env(tmp_path: Path):
    """Repo root with runtime_config + profile with seed-phase constitution."""
    profile = tmp_path / "users" / "u1"
    seed = profile / "seed-phase"
    seed.mkdir(parents=True)
    shutil.copytree(REPO_ROOT / "tests/fixtures/seed-phase/valid-minimal", seed, dirs_exist_ok=True)
    (tmp_path / "runtime_config.json").write_text(
        json.dumps(
            {
                "constitutional_critique": {
                    "enabled": True,
                    "trigger_threshold": 0.99,
                    "long_response_chars": 5000,
                    "scope_flags": ["memory_write"],
                    "cache_ttl_seconds": 3600,
                    "max_added_tokens": 400,
                    "use_cheaper_model": True,
                },
                "monitoring": {"log_critique_decisions": False},
            }
        ),
        encoding="utf-8",
    )
    return tmp_path, profile


def test_constitutional_critique_revision_path(constitutional_env, monkeypatch):
    repo_root, profile_dir = constitutional_env
    monkeypatch.delenv("CONSTITUTIONAL_REDIS_URL", raising=False)

    from bot import constitutional_layer as cl

    cl._l1.clear()
    cl._cache_hits = 0
    cl._cache_misses = 0
    cl._redis_client = None
    cl._cfg_cache = None
    cl._cfg_mtime = None
    cl._const_cache = None

    client = MagicMock()

    def create_side_effect(*args, **kwargs):
        m = MagicMock()
        if kwargs.get("response_format"):
            m.choices = [
                MagicMock(
                    message=MagicMock(
                        content='{"violations":["too long"],"score":0.4,"suggestion":"use fewer words","early_exit":false}'
                    )
                )
            ]
        else:
            m.choices = [MagicMock(message=MagicMock(content="short ok"))]
        return m

    client.chat.completions.create.side_effect = create_side_effect

    out = cl.maybe_apply_constitutional_critique(
        repo_root=repo_root,
        profile_dir=profile_dir,
        user_message="hello there",
        assistant_text="this is a test reply that needs a critique pass",
        channel_key="telegram:1",
        client=client,
        confidence=0.5,
        main_model="gpt-4o-mini",
    )
    assert out == "short ok"
    assert client.chat.completions.create.call_count == 2

    out2 = cl.maybe_apply_constitutional_critique(
        repo_root=repo_root,
        profile_dir=profile_dir,
        user_message="hello there",
        assistant_text="this is a test reply that needs a critique pass",
        channel_key="telegram:1",
        client=client,
        confidence=0.5,
        main_model="gpt-4o-mini",
    )
    assert out2 == "short ok"
    assert client.chat.completions.create.call_count == 2
    assert cl._cache_hits >= 1


def test_constitutional_disabled_no_calls(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("CONSTITUTIONAL_REDIS_URL", raising=False)
    (tmp_path / "runtime_config.json").write_text(
        '{"constitutional_critique":{"enabled":false}}', encoding="utf-8"
    )
    profile = tmp_path / "users" / "x"
    seed = profile / "seed-phase"
    seed.mkdir(parents=True)
    shutil.copy2(
        REPO_ROOT / "tests/fixtures/seed-phase/valid-minimal/seed_constitution.json",
        seed / "seed_constitution.json",
    )

    from bot import constitutional_layer as cl

    cl._cfg_cache = None
    cl._cfg_mtime = None
    client = MagicMock()
    out = cl.maybe_apply_constitutional_critique(
        repo_root=tmp_path,
        profile_dir=profile,
        user_message="hi",
        assistant_text="hello back",
        channel_key="t:1",
        client=client,
        confidence=0.1,
    )
    assert out == "hello back"
    client.chat.completions.create.assert_not_called()
