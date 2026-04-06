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
