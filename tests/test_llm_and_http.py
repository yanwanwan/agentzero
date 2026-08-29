import asyncio

import httpx
import pytest

from mini_agent.http_demo import (
    compare_request_timings,
    fetch_concurrent,
    fetch_serial,
)
from mini_agent.llm import MockLLMClient
from mini_agent.models import Message


@pytest.mark.asyncio
async def test_mock_llm_uses_latest_message() -> None:
    client = MockLLMClient()
    response = await client.generate([Message(role="user", content="learn tools")])
    assert response == "mock response to: learn tools"


@pytest.mark.asyncio
async def test_serial_and_concurrent_fetch_same_responses() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        await asyncio.sleep(0.001)
        return httpx.Response(200, request=request)

    transport = httpx.MockTransport(handler)
    urls = ["https://example.test/1", "https://example.test/2"]
    async with httpx.AsyncClient(transport=transport) as client:
        assert await fetch_serial(client, urls) == [200, 200]
        assert await fetch_concurrent(client, urls) == [200, 200]


@pytest.mark.asyncio
async def test_timing_comparison_returns_non_negative_values() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(204, request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        timing = await compare_request_timings(client, ["https://example.test"])
    assert timing.serial_seconds >= 0
    assert timing.concurrent_seconds >= 0
