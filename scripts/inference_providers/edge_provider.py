"""Google AI Edge provider — on-device inference via Gemini Nano / Gemma.

This is a Python stub for Phase 2. The actual native SDK integration
(Kotlin via AI Edge SDK on Android, Swift on iOS) is deferred to Phase 4.

For desktop local-first testing, use the Ollama provider with a Gemma
model instead — it gives equivalent capability validation without
requiring the mobile SDK.
"""

from __future__ import annotations

from .base import InferenceProvider, InferenceResult


class EdgeProvider(InferenceProvider):
    """Placeholder for Google AI Edge SDK integration.

    Raises NotImplementedError until the native bridge is wired.
    The provider contract is defined so downstream code can reference
    it without conditional imports.
    """

    def __init__(self, model: str = "gemini-nano-4b"):
        self._model = model

    def chat_completion(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        max_tokens: int = 200,
        temperature: float = 0.9,
    ) -> InferenceResult:
        raise NotImplementedError(
            "Google AI Edge provider requires the native SDK bridge "
            "(Android: ML Kit GenAI / AICore; iOS: equivalent). "
            "Use LLM_PROVIDER=ollama with a Gemma model for desktop testing."
        )

    def provider_name(self) -> str:
        return "edge"

    def supports_multimodal(self) -> bool:
        return True

    def context_window_tokens(self) -> int:
        return 32_000

    def supports_audio(self) -> bool:
        return False
