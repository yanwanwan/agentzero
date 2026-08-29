import pytest

from mini_agent.models import ToolCall
from mini_agent.tools.calculator import calculator_tool
from mini_agent.tools.registry import (
    DuplicateToolError,
    ToolNotFoundError,
    ToolRegistry,
)
from mini_agent.tools.search_mock import search_mock_tool


def test_register_get_and_list_tools() -> None:
    registry = ToolRegistry()
    registry.register(calculator_tool)
    assert registry.get("calculator") is calculator_tool
    assert registry.list_tools() == [calculator_tool]


def test_duplicate_registration_is_explicit() -> None:
    registry = ToolRegistry()
    registry.register(calculator_tool)
    with pytest.raises(DuplicateToolError, match="already registered"):
        registry.register(calculator_tool)


def test_unknown_tool_lookup_is_explicit() -> None:
    with pytest.raises(ToolNotFoundError, match="Unknown tool"):
        ToolRegistry().get("missing")


@pytest.mark.asyncio
async def test_registry_executes_calculator_call() -> None:
    registry = ToolRegistry()
    registry.register(calculator_tool)
    result = await registry.execute(
        ToolCall(name="calculator", arguments={"expression": "128 * 726"})
    )
    assert result.success is True
    assert result.output == "92928"


@pytest.mark.asyncio
async def test_registry_executes_async_search_mock() -> None:
    registry = ToolRegistry()
    registry.register(search_mock_tool)
    result = await registry.execute(
        ToolCall(name="search_mock", arguments={"query": "agent runtime"})
    )
    assert result.success is True
    assert result.output == "Search results for: agent runtime"


@pytest.mark.asyncio
async def test_registry_normalizes_unknown_tool_as_failure() -> None:
    result = await ToolRegistry().execute(ToolCall(name="missing", arguments={}))
    assert result.success is False
    assert result.tool_name == "missing"
