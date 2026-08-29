"""Provider-independent LLM client boundary."""

from abc import ABC, abstractmethod

from mini_agent.models import Message


class LLMClient(ABC):
    """Interface implemented later by OpenAI, Claude, or local providers."""

    @abstractmethod
    async def generate(self, messages: list[Message]) -> str:
        """Generate one textual response for a conversation."""


class MockLLMClient(LLMClient):
    """Deterministic client for learning and unit tests."""

    async def generate(self, messages: list[Message]) -> str:
        if not messages:
            return "mock response"
        return f"mock response to: {messages[-1].content}"
