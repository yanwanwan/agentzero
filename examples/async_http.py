"""Compare three serial and concurrent HTTP-shaped I/O operations offline."""

import asyncio

import httpx

from mini_agent.http_demo import compare_request_timings


async def delayed_response(request: httpx.Request) -> httpx.Response:
    await asyncio.sleep(0.2)
    return httpx.Response(200, request=request)


async def main() -> None:
    urls = [f"https://example.test/{index}" for index in range(1, 4)]
    transport = httpx.MockTransport(delayed_response)
    async with httpx.AsyncClient(transport=transport) as client:
        timing = await compare_request_timings(client, urls)

    print(f"serial:     {timing.serial_seconds:.3f}s")
    print(f"concurrent: {timing.concurrent_seconds:.3f}s")


if __name__ == "__main__":
    asyncio.run(main())
