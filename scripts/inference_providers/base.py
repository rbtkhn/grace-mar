"""Abstract base for inference providers.

Each provider wraps a specific LLM backend (cloud API, local server,
on-device SDK) behind a uniform interface so the bot and scripts can
swap inference targets without changing call sites.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class InferenceResult:
    """Uniform return type from all providers."""

    text: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    model: str = ""
    provider: str = ""
    metadata: dict = field(default_factory=dict)


class InferenceProvider(ABC):
    """Minimal interface every provider must implement."""

    @abstractmethod
    def chat_completion(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        max_tokens: int = 200,
        temperature: float = 0.9,
    ) -> InferenceResult:
        """Send a chat-completion request and return the result."""

    @abstractmethod
    def provider_name(self) -> str:
        """Short identifier: 'openai', 'ollama', 'edge'."""

    def supports_multimodal(self) -> bool:
        """Whether this provider can handle image inputs."""
        return False

    def context_window_tokens(self) -> int:
        """Max context the provider's model can handle."""
        return 128_000

    def supports_audio(self) -> bool:
        """Whether this provider can transcribe audio."""
        return False
