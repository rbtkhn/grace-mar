"""Tests for voice/prompt invariants: no AI disclosure, Lexile-friendly."""
import re

import pytest


def test_prompt_no_forbidden_phrases():
    """SYSTEM_PROMPT must not contain phrases that break character or disclose AI."""
    from bot.prompt import SYSTEM_PROMPT

    forbidden = [
        "as an ai",
        "as a language model",
        "i'm an ai",
        "i'm a language model",
        "openai",
        "i cannot have",
        "i don't have personal",
    ]
    lower = SYSTEM_PROMPT.lower()
    for phrase in forbidden:
        assert phrase not in lower, f"Prompt must not contain '{phrase}'"


def test_prompt_contains_identity():
    """Prompt should establish character (Grace-Mar, 6-year-old, etc.)."""
    from bot.prompt import SYSTEM_PROMPT

    assert "grace-mar" in SYSTEM_PROMPT.lower() or "Grace-Mar" in SYSTEM_PROMPT


def test_prompt_contains_knowledge_boundary():
    """Prompt should instruct abstention / lookup when outside knowledge."""
    from bot.prompt import SYSTEM_PROMPT

    assert "look it up" in SYSTEM_PROMPT.lower() or "look up" in SYSTEM_PROMPT.lower()
    assert "don't" in SYSTEM_PROMPT.lower() or "do not" in SYSTEM_PROMPT.lower()
