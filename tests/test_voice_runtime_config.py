"""Tests for scripts/voice_runtime_config.py (identical file in companion-self)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_SCRIPTS = _REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from voice_runtime_config import (  # noqa: E402
    merge_critique_for_latency_mode,
    parse_voice_avatar_block,
    emotion_from_score,
    emotion_mapping_config_from_avatar,
)


def test_parse_defaults_empty_block() -> None:
    s = parse_voice_avatar_block(None)
    assert s.voice_stack_enabled is False
    assert s.latency_mode == "balanced"
    assert s.avatar.type == "none"
    assert s.avatar.enabled is False
    assert s.stt.provider == "deepgram"


def test_parse_legacy_flat_avatar_no_nested_key() -> None:
    s = parse_voice_avatar_block(
        {
            "enabled": True,
            "avatar_type": "live2d",
            "avatar_model_path": "/models/x",
            "renderer_url": "http://r",
        }
    )
    assert s.voice_stack_enabled is True
    assert s.avatar.enabled is True
    assert s.avatar.type == "live2d"
    assert s.avatar.model_path == "/models/x"
    assert s.avatar.renderer_url == "http://r"


def test_nested_avatar_disabled_overrides_type() -> None:
    s = parse_voice_avatar_block(
        {
            "enabled": True,
            "avatar": {"enabled": False, "type": "live2d"},
        }
    )
    assert s.avatar.type == "live2d"
    assert s.avatar.enabled is False


def test_nested_avatar_empty_dict_ignores_legacy_type() -> None:
    s = parse_voice_avatar_block(
        {
            "enabled": True,
            "avatar_type": "live2d",
            "avatar": {},
        }
    )
    assert s.avatar.type == "none"
    assert s.avatar.enabled is False


def test_latency_mode_invalid_falls_back_balanced() -> None:
    s = parse_voice_avatar_block({"latency_mode": "nope"})
    assert s.latency_mode == "balanced"


def test_merge_critique_balanced_unchanged() -> None:
    cc = {"trigger_threshold": 0.78, "long_response_chars": 800}
    out = merge_critique_for_latency_mode(cc, "balanced")
    assert out == cc
    assert out is not cc


def test_merge_critique_governed_stricter() -> None:
    cc = {"trigger_threshold": 0.78, "long_response_chars": 800}
    out = merge_critique_for_latency_mode(cc, "governed")
    assert out["trigger_threshold"] >= 0.92
    assert out["long_response_chars"] <= 600


def test_merge_critique_ultra_low_relaxed() -> None:
    cc = {"trigger_threshold": 0.78, "long_response_chars": 800}
    out = merge_critique_for_latency_mode(cc, "ultra_low")
    assert out["trigger_threshold"] <= 0.45
    assert out["long_response_chars"] >= 2400


def test_emotion_mapping_from_named_keys() -> None:
    from voice_runtime_config import AvatarNestedSettings

    av = AvatarNestedSettings(
        enabled=True,
        type="live2d",
        emotion_mapping={
            "low_confidence": "a",
            "medium_confidence": "b",
            "high_confidence": "c",
            "low_max_score": 0.5,
            "high_min_score": 0.95,
        },
    )
    cfg = emotion_mapping_config_from_avatar(av)
    assert emotion_from_score(0.4, cfg) == "a"
    assert emotion_from_score(0.7, cfg) == "b"
    assert emotion_from_score(0.96, cfg) == "c"
