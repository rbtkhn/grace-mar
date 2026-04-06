"""
Portable parse helpers for voice_avatar + latency_mode in runtime_config.json.

Used by bot/avatar_controller.py (grace-mar) and future voice_pipeline. Keep this
file identical in companion-self and grace-mar template/instance pairs.

Emotion precedence for avatar (see docs/voice-runtime-config.md):
1. runtime emotion_mapping (score bands / named keys)
2. Hardcoded defaults in emotion_from_score()
3. expression_scaffold avatar_mapping.emotion_map (label → renderer label) — applied in AvatarController
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

LatencyMode = Literal["ultra_low", "balanced", "governed"]


@dataclass
class SttSettings:
    provider: str = "deepgram"
    model: str = "nova-2"
    language: str = "en"
    streaming: bool = True


@dataclass
class TtsSettings:
    provider: str = "cartesia"
    voice_id: str = ""
    model: str = "sonic-3"
    streaming: bool = True
    speed: float = 1.0
    stability: float = 0.85


@dataclass
class BargeInSettings:
    enabled: bool = False
    vad_sensitivity: str = "medium"


@dataclass
class VoiceCacheSettings:
    enabled: bool = False
    ttl_minutes: int = 45
    size: int = 600


@dataclass
class EmotionMappingConfig:
    """Maps critique_score to base emotion labels (before scaffold emotion_map)."""

    low_threshold: float = 0.75
    high_threshold: float = 0.90
    low_emotion: str = "thoughtful"
    medium_emotion: str = "neutral"
    high_emotion: str = "happy"


@dataclass
class AvatarNestedSettings:
    enabled: bool = False
    type: str = "none"
    model_path: Optional[str] = None
    renderer_url: Optional[str] = None
    emotion_mapping: Optional[dict[str, Any]] = None


@dataclass
class VoiceAvatarSettings:
    """Normalized voice_avatar block."""

    voice_stack_enabled: bool = False
    latency_mode: LatencyMode = "balanced"
    stt: SttSettings = field(default_factory=SttSettings)
    tts: TtsSettings = field(default_factory=TtsSettings)
    avatar: AvatarNestedSettings = field(default_factory=AvatarNestedSettings)
    barge_in: BargeInSettings = field(default_factory=BargeInSettings)
    cache: VoiceCacheSettings = field(default_factory=VoiceCacheSettings)


def _parse_stt(raw: dict[str, Any]) -> SttSettings:
    r = raw or {}
    return SttSettings(
        provider=str(r.get("provider") or "deepgram"),
        model=str(r.get("model") or "nova-2"),
        language=str(r.get("language") or "en"),
        streaming=bool(r.get("streaming", True)),
    )


def _parse_tts(raw: dict[str, Any]) -> TtsSettings:
    r = raw or {}
    return TtsSettings(
        provider=str(r.get("provider") or "cartesia"),
        voice_id=str(r.get("voice_id") or ""),
        model=str(r.get("model") or "sonic-3"),
        streaming=bool(r.get("streaming", True)),
        speed=float(r.get("speed", 1.0)),
        stability=float(r.get("stability", 0.85)),
    )


def _parse_barge_in(raw: dict[str, Any]) -> BargeInSettings:
    r = raw or {}
    sens = str(r.get("vad_sensitivity") or "medium")
    if sens not in ("low", "medium", "high"):
        sens = "medium"
    return BargeInSettings(enabled=bool(r.get("enabled", False)), vad_sensitivity=sens)


def _parse_cache(raw: dict[str, Any]) -> VoiceCacheSettings:
    r = raw or {}
    return VoiceCacheSettings(
        enabled=bool(r.get("enabled", False)),
        ttl_minutes=int(r.get("ttl_minutes", 45)),
        size=int(r.get("size", 600)),
    )


def _parse_emotion_mapping(raw: dict[str, Any] | None) -> EmotionMappingConfig:
    if not raw or not isinstance(raw, dict):
        return EmotionMappingConfig()
    # Named keys from sketch (high_confidence → emotion string)
    if all(k in raw for k in ("low_confidence", "medium_confidence", "high_confidence")):
        return EmotionMappingConfig(
            low_threshold=float(raw.get("low_max_score", 0.75)),
            high_threshold=float(raw.get("high_min_score", 0.90)),
            low_emotion=str(raw["low_confidence"]),
            medium_emotion=str(raw["medium_confidence"]),
            high_emotion=str(raw["high_confidence"]),
        )
    low_e = str(raw.get("low_emotion") or raw.get("low") or "thoughtful")
    med_e = str(raw.get("medium_emotion") or raw.get("medium") or "neutral")
    high_e = str(raw.get("high_emotion") or raw.get("high") or "happy")
    return EmotionMappingConfig(
        low_threshold=float(raw.get("low_max_score", raw.get("low_threshold", 0.75))),
        high_threshold=float(raw.get("high_min_score", raw.get("high_threshold", 0.90))),
        low_emotion=low_e,
        medium_emotion=med_e,
        high_emotion=high_e,
    )


def _parse_avatar_nested(
    raw: dict[str, Any] | None,
    *,
    legacy_type: str,
    legacy_model_path: Optional[str],
    legacy_renderer_url: Optional[str],
) -> AvatarNestedSettings:
    if isinstance(raw, dict):
        t = str(raw.get("type") or "none").strip().lower()
        if t not in ("live2d", "vrm", "none"):
            t = "none"
        en = bool(raw.get("enabled", False))
        em = raw.get("emotion_mapping")
        em_dict = em if isinstance(em, dict) else None
        return AvatarNestedSettings(
            enabled=en and t != "none",
            type=t,
            model_path=_none_str(raw.get("model_path")),
            renderer_url=_none_str(raw.get("renderer_url")),
            emotion_mapping=em_dict,
        )
    t = legacy_type.strip().lower()
    if t not in ("live2d", "vrm", "none"):
        t = "none"
    return AvatarNestedSettings(
        enabled=(t != "none"),
        type=t,
        model_path=legacy_model_path,
        renderer_url=legacy_renderer_url,
        emotion_mapping=None,
    )


def _none_str(v: Any) -> Optional[str]:
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def parse_voice_avatar_block(block: dict[str, Any] | None) -> VoiceAvatarSettings:
    """Normalize voice_avatar object from runtime_config (may be empty)."""
    b = block or {}
    voice_on = bool(b.get("enabled", False))

    lm = str(b.get("latency_mode") or "balanced").strip().lower()
    if lm not in ("ultra_low", "balanced", "governed"):
        lm = "balanced"

    legacy_type = str(b.get("avatar_type") or "none")
    legacy_path = _none_str(b.get("avatar_model_path"))
    legacy_url = _none_str(b.get("renderer_url"))

    avatar_sub = b.get("avatar")
    avatar = _parse_avatar_nested(
        avatar_sub if isinstance(avatar_sub, dict) else None,
        legacy_type=legacy_type,
        legacy_model_path=legacy_path,
        legacy_renderer_url=legacy_url,
    )

    return VoiceAvatarSettings(
        voice_stack_enabled=voice_on,
        latency_mode=lm,  # type: ignore[arg-type]
        stt=_parse_stt(b.get("stt") if isinstance(b.get("stt"), dict) else {}),
        tts=_parse_tts(b.get("tts") if isinstance(b.get("tts"), dict) else {}),
        avatar=avatar,
        barge_in=_parse_barge_in(b.get("barge_in") if isinstance(b.get("barge_in"), dict) else {}),
        cache=_parse_cache(b.get("cache") if isinstance(b.get("cache"), dict) else {}),
    )


def emotion_mapping_config_from_avatar(avatar: AvatarNestedSettings) -> EmotionMappingConfig:
    """Build EmotionMappingConfig from nested avatar.emotion_mapping JSON."""
    return _parse_emotion_mapping(avatar.emotion_mapping)


def emotion_from_score(score: float, cfg: EmotionMappingConfig) -> str:
    if score < cfg.low_threshold:
        return cfg.low_emotion
    if score < cfg.high_threshold:
        return cfg.medium_emotion
    return cfg.high_emotion


def merge_critique_for_latency_mode(
    constitutional_critique: dict[str, Any] | None,
    latency_mode: str,
) -> dict[str, Any]:
    """
    Shallow copy of constitutional_critique with effective fields for a voice path.

    - governed: stricter (more critique triggers from confidence / length).
    - balanced: unchanged.
    - ultra_low: fewer triggers (higher long_response bar; threshold tuned for confidence path).
    """
    base = dict(constitutional_critique or {})
    mode = (latency_mode or "balanced").strip().lower()
    if mode not in ("ultra_low", "balanced", "governed"):
        mode = "balanced"

    if mode == "balanced":
        return base

    out = copy.copy(base)

    if mode == "governed":
        # More critique: high threshold so typical scores still fall below
        out["trigger_threshold"] = max(float(out.get("trigger_threshold", 0.78)), 0.92)
        out["long_response_chars"] = min(int(out.get("long_response_chars", 800)), 600)
        return out

    if mode == "ultra_low":
        # Less critique: only very low confidence triggers; longer bar for length heuristic
        out["trigger_threshold"] = min(float(out.get("trigger_threshold", 0.78)), 0.45)
        out["long_response_chars"] = max(int(out.get("long_response_chars", 800)), 2400)
        return out

    return out
