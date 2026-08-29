"""Small async HTTP experiments; this is not part of an agent loop."""

import asyncio
from dataclasses import dataclass
from time import perf_counter

import httpx


@dataclass(frozen=True)
class TimingComparison:
    """Elapsed seconds for serial and concurrent I/O."""

    serial_seconds: float
    concurrent_seconds: float


async def fetch_serial(client: httpx.AsyncClient, urls: list[str]) -> list[int]:
    """Fetch URLs one after another and return their status codes."""

    status_codes: list[int] = []
    for url in urls:
        response = await client.get(url)
        status_codes.append(response.status_code)
    return status_codes


async def fetch_concurrent(client: httpx.AsyncClient, urls: list[str]) -> list[int]:
    """Start all URL requests together and return status codes in input order."""

    responses = await asyncio.gather(*(client.get(url) for url in urls))
    return [response.status_code for response in responses]


async def compare_request_timings(
    client: httpx.AsyncClient, urls: list[str]
) -> TimingComparison:
    """Measure serial and concurrent runs using the same client and URLs."""

    started = perf_counter()
    await fetch_serial(client, urls)
    serial_seconds = perf_counter() - started

    started = perf_counter()
    await fetch_concurrent(client, urls)
    concurrent_seconds = perf_counter() - started

    return TimingComparison(serial_seconds, concurrent_seconds)
