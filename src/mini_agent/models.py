"""Core data passed between model and tool boundaries."""

from typing import Literal

from pydantic import BaseModel


class Message(BaseModel):
    """One item in a model conversation."""

    role: Literal["system", "user", "assistant", "tool"]
    content: str


class ToolCall(BaseModel):
    """A request to invoke a named tool with JSON-like arguments."""

    name: str
    arguments: dict[str, object]


class ToolResult(BaseModel):
    """The normalized outcome returned by every tool."""

    tool_name: str
    success: bool
    output: str
