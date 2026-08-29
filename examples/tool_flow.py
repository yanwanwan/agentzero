"""Run the complete ToolCall -> ToolResult learning path."""

import asyncio

from mini_agent.models import ToolCall
from mini_agent.tools import ToolRegistry, calculator_tool, search_mock_tool


async def main() -> None:
    registry = ToolRegistry()
    registry.register(calculator_tool)
    registry.register(search_mock_tool)

    calls = [
        ToolCall(name="calculator", arguments={"expression": "128 * 726"}),
        ToolCall(name="search_mock", arguments={"query": "agent runtime"}),
    ]
    for call in calls:
        result = await registry.execute(call)
        print(result.model_dump())


if __name__ == "__main__":
    asyncio.run(main())
