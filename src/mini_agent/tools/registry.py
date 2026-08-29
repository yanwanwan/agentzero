"""In-memory lookup and dispatch for tools."""

from mini_agent.models import ToolCall, ToolResult
from mini_agent.tools.base import Tool


class ToolNotFoundError(LookupError):
    """Raised when a requested tool has not been registered."""


class DuplicateToolError(ValueError):
    """Raised when a tool name is registered more than once."""


class ToolRegistry:
    """Own the set of tools available to a future agent runtime."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise DuplicateToolError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise ToolNotFoundError(f"Unknown tool: {name}") from exc

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())

    async def execute(self, tool_call: ToolCall) -> ToolResult:
        """Resolve and run a call while keeping every outcome in one model."""

        try:
            tool = self.get(tool_call.name)
        except ToolNotFoundError as exc:
            return ToolResult(
                tool_name=tool_call.name,
                success=False,
                output=str(exc),
            )
        return await tool.execute(tool_call.arguments)
