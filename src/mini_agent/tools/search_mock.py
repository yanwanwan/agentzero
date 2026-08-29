"""Offline search-shaped tool used to practise async dispatch."""

import asyncio

from pydantic import BaseModel, Field

from mini_agent.tools.base import Tool


class SearchInput(BaseModel):
    query: str = Field(min_length=1)


async def search_mock_handler(input_data: BaseModel) -> str:
    """Return deterministic output while still yielding to the event loop."""

    request = SearchInput.model_validate(input_data)
    await asyncio.sleep(0)
    return f"Search results for: {request.query}"


search_mock_tool = Tool(
    name="search_mock",
    description="Return a deterministic mock search result without networking.",
    input_schema=SearchInput,
    handler=search_mock_handler,
)
