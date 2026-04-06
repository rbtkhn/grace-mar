"""
Optional avatar command layer (Live2D / VRM / Airi-style renderers).

Governance: consumes already-finalized text and optional critique metadata.
Does not call the LLM or merge into the Record.

**Enablement:** `voice_avatar.enabled` must be true (voice stack). The avatar
renderer is active only when the nested `avatar.enabled` is true and
`avatar.type` is not `none`. Legacy flat `avatar_type` / `avatar_model_path` /
`renderer_url` on `voice_avatar` are still read when the `avatar` subtree is
absent (deprecated — prefer nested `avatar`).

Callers obtain a controller via load_avatar_controller(config) — no global
singleton; hold the instance per process or per session as appropriate.
"""

from __future__ import annotations

import json
import logging
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Literal, Optional

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from voice_runtime_config import (  # noqa: E402
    EmotionMappingConfig,
    emotion_from_score,
    emotion_mapping_config_from_avatar,
    parse_voice_avatar_block,
)

logger = logging.getLogger(__name__)

AvatarType = Literal["live2d", "vrm", "none"]


@dataclass
class AvatarCommand:
    emotion: str = "neutral"
    mouth_intensity: float = 0.0
    eye_angle_x: float = 0.0
    eye_angle_y: float = 0.0
    blink_rate: float = 1.0
    head_tilt: float = 0.0
    idle_animation: str = "subtle"
    speaking: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


SenderFn = Callable[[dict[str, Any]], bool]


class AvatarController:
    """Maps governed text + signals to renderer-facing commands."""

    def __init__(
        self,
        *,
        avatar_type: AvatarType = "none",
        model_path: Optional[str] = None,
        renderer_url: Optional[str] = None,
        sender: Optional[SenderFn] = None,
        emotion_mapping_config: Optional[EmotionMappingConfig] = None,
    ) -> None:
        self.avatar_type: AvatarType = avatar_type
        self.model_path = model_path
        self.renderer_url = renderer_url
        self._sender = sender
        self.enabled = avatar_type != "none"
        self._emotion_cfg = emotion_mapping_config or EmotionMappingConfig()

        if self.enabled:
            logger.info("AvatarController: type=%s model=%s renderer=%s", avatar_type, model_path, renderer_url)

    def generate_commands(
        self,
        text: str,
        critique_score: float,
        expression_scaffold: Optional[Dict[str, Any]] = None,
    ) -> AvatarCommand:
        if not self.enabled:
            return AvatarCommand()

        length_factor = min(1.0, len(text) / 180.0) if text else 0.0

        emotion = emotion_from_score(critique_score, self._emotion_cfg)

        if expression_scaffold and expression_scaffold.get("avatar_mapping"):
            mapping = expression_scaffold["avatar_mapping"]
            emap = mapping.get("emotion_map") or {}
            if isinstance(emap, dict) and emotion in emap:
                emotion = str(emap[emotion])

        mouth_intensity = round(
            length_factor * (0.6 if emotion == "happy" else 0.85),
            2,
        )

        return AvatarCommand(
            emotion=emotion,
            mouth_intensity=mouth_intensity,
            eye_angle_x=0.0,
            eye_angle_y=0.0,
            blink_rate=1.2 if emotion == "thoughtful" else 0.9,
            head_tilt=0.0,
            idle_animation="subtle" if not text else "listening",
            speaking=bool(text),
        )

    def send_to_renderer(self, command: AvatarCommand) -> bool:
        if not self.enabled:
            return False

        payload = {
            "type": "avatar_command",
            "timestamp": time.time(),
            "avatar_type": self.avatar_type,
            "renderer_url": self.renderer_url,
            "command": command.to_dict(),
        }

        if self._sender is not None:
            return self._sender(payload)

        logger.debug("avatar payload: %s", json.dumps(payload, default=str)[:500])
        return True


def load_avatar_controller(
    config: Optional[Dict[str, Any]] = None,
    *,
    sender: Optional[SenderFn] = None,
) -> AvatarController:
    """Build a controller from repo-root runtime_config dict (or empty)."""
    cfg = config or {}
    block = cfg.get("voice_avatar")
    parsed = parse_voice_avatar_block(block if isinstance(block, dict) else None)

    if not parsed.voice_stack_enabled:
        return AvatarController(avatar_type="none", sender=sender)

    av = parsed.avatar
    if not av.enabled or av.type == "none":
        return AvatarController(avatar_type="none", sender=sender)

    raw_type = av.type.strip().lower()
    if raw_type not in ("live2d", "vrm", "none"):
        logger.warning("Unknown avatar type %r; disabling avatar", raw_type)
        return AvatarController(avatar_type="none", sender=sender)

    at: AvatarType = raw_type  # type: ignore[assignment]
    em_cfg = emotion_mapping_config_from_avatar(av)
    return AvatarController(
        avatar_type=at,
        model_path=av.model_path,
        renderer_url=av.renderer_url,
        sender=sender,
        emotion_mapping_config=em_cfg,
    )
