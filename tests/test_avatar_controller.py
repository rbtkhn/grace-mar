"""Tests for bot/avatar_controller.py."""

from __future__ import annotations

from bot.avatar_controller import AvatarController, load_avatar_controller


def test_load_disabled_when_voice_avatar_off() -> None:
    ctrl = load_avatar_controller({})
    assert not ctrl.enabled

    ctrl2 = load_avatar_controller(
        {"voice_avatar": {"enabled": False, "avatar_type": "live2d"}}
    )
    assert not ctrl2.enabled


def test_load_legacy_flat_when_voice_on() -> None:
    ctrl = load_avatar_controller(
        {
            "voice_avatar": {
                "enabled": True,
                "avatar_type": "live2d",
                "avatar_model_path": "m",
            }
        }
    )
    assert ctrl.enabled
    assert ctrl.avatar_type == "live2d"


def test_load_nested_avatar_off_disables_despite_type() -> None:
    ctrl = load_avatar_controller(
        {
            "voice_avatar": {
                "enabled": True,
                "avatar": {"enabled": False, "type": "live2d"},
            }
        }
    )
    assert not ctrl.enabled


def test_load_nested_avatar_on() -> None:
    ctrl = load_avatar_controller(
        {
            "voice_avatar": {
                "enabled": True,
                "avatar": {"enabled": True, "type": "vrm"},
            }
        }
    )
    assert ctrl.enabled
    assert ctrl.avatar_type == "vrm"


def test_generate_commands_uses_runtime_emotion_mapping() -> None:
    ctrl = load_avatar_controller(
        {
            "voice_avatar": {
                "enabled": True,
                "avatar": {
                    "enabled": True,
                    "type": "live2d",
                    "emotion_mapping": {
                        "low_max_score": 0.5,
                        "high_min_score": 0.95,
                        "low_emotion": "calm",
                        "medium_emotion": "alert",
                        "high_emotion": "joy",
                    },
                },
            }
        }
    )
    cmd = ctrl.generate_commands("hi", 0.6, None)
    assert cmd.emotion == "alert"


def test_generate_commands_respects_scaffold_map() -> None:
    ctrl = AvatarController(avatar_type="live2d", model_path="x")
    cmd = ctrl.generate_commands(
        "hello there",
        0.95,
        {"avatar_mapping": {"emotion_map": {"happy": "smiling"}}},
    )
    assert cmd.emotion == "smiling"
    assert cmd.speaking is True


def test_send_to_renderer_uses_custom_sender() -> None:
    seen: list[dict] = []

    def sender(payload: dict) -> bool:
        seen.append(payload)
        return True

    ctrl = AvatarController(avatar_type="vrm", sender=sender)
    cmd = ctrl.generate_commands("hi", 0.99, None)
    assert ctrl.send_to_renderer(cmd) is True
    assert seen and seen[0]["type"] == "avatar_command"
    assert seen[0]["command"]["emotion"] == "happy"
