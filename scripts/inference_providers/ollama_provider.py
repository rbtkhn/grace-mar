"""Ollama provider — local inference via Ollama's OpenAI-compatible API."""

from __future__ import annotations

from openai import OpenAI

from .base import InferenceProvider, InferenceResult

DEFAULT_BASE_URL = "http://localhost:11434/v1"


class OllamaProvider(InferenceProvider):
    """Local-first inference via an Ollama server.

    Ollama exposes an OpenAI-compatible /v1/chat/completions endpoint,
    so we reuse the OpenAI SDK with a different base_url. This means
    all existing call patterns work unchanged.
    """

    def __init__(
        self,
        default_model: str = "gemma3:4b",
        base_url: str = DEFAULT_BASE_URL,
    ):
        self._client = OpenAI(base_url=base_url, api_key="ollama")
        self._default_model = default_model

    def chat_completion(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        max_tokens: int = 200,
        temperature: float = 0.9,
    ) -> InferenceResult:
        resolved = model or self._default_model
        response = self._client.chat.completions.create(
            model=resolved,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        usage = getattr(response, "usage", None)
        return InferenceResult(
            text=response.choices[0].message.content.strip(),
            prompt_tokens=getattr(usage, "prompt_tokens", 0) if usage else 0,
            completion_tokens=getattr(usage, "completion_tokens", 0) if usage else 0,
            model=resolved,
            provider="ollama",
        )

    def provider_name(self) -> str:
        return "ollama"

    def supports_multimodal(self) -> bool:
        return False

    def context_window_tokens(self) -> int:
        return 32_000

    def supports_audio(self) -> bool:
        return False
