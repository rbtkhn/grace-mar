"""OpenAI provider — wraps the standard OpenAI Chat Completions API."""

from __future__ import annotations

from openai import OpenAI

from .base import InferenceProvider, InferenceResult


class OpenAIProvider(InferenceProvider):
    """Cloud inference via the OpenAI API (GPT-4o, GPT-4o-mini, etc.)."""

    def __init__(self, api_key: str, default_model: str = "gpt-4o"):
        self._client = OpenAI(api_key=api_key)
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
            provider="openai",
        )

    def provider_name(self) -> str:
        return "openai"

    def supports_multimodal(self) -> bool:
        return True

    def context_window_tokens(self) -> int:
        return 128_000

    def supports_audio(self) -> bool:
        return True

    @property
    def raw_client(self) -> OpenAI:
        """Access the underlying SDK client for audio transcription etc."""
        return self._client
