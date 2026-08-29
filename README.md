# Mini Agent Runtime

这是一个用于学习 Agent 底层机制的最小 Python 工程。当前阶段故意不使用
LangChain、LangGraph、MCP、RAG 或 Multi-Agent，也还没有完整 Agent Loop。

## 现在已经有的两条链路

```text
Message -> LLMClient

ToolCall -> ToolRegistry -> Tool -> Pydantic validation -> ToolResult
```

这样拆开学习的原因是：模型调用和工具执行是两个不同的边界。先分别理解、测试，
下一阶段再把它们连接成循环，会更容易定位错误。

## 环境与验收

需要 Python 3.12 和 uv。在项目根目录执行：

```powershell
$env:UV_CACHE_DIR="$PWD\.uv-cache"
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

两个可直接运行的学习实验：

```powershell
uv run python examples/tool_flow.py
uv run python examples/async_http.py
```

## 从工具执行链开始读

```python
import asyncio

from mini_agent.models import ToolCall
from mini_agent.tools import ToolRegistry, calculator_tool, search_mock_tool


async def main() -> None:
    registry = ToolRegistry()
    registry.register(calculator_tool)
    registry.register(search_mock_tool)

    result = await registry.execute(
        ToolCall(name="calculator", arguments={"expression": "128 * 726"})
    )
    print(result.model_dump())


asyncio.run(main())
```

预期输出中的 `output` 是 `92928`。推荐按下面顺序阅读源码：

1. `models.py`：数据如何跨边界传递。
2. `tools/base.py`：Pydantic 校验和统一结果包装。
3. `tools/registry.py`：工具如何注册、查找和分发。
4. `tools/calculator.py`：为什么不直接使用 `eval()`。
5. `llm.py`：如何用抽象隔离具体模型供应商。
6. `http_demo.py`：串行 I/O 与并发 I/O 的区别。

## async HTTP 小实验

`http_demo.py` 提供 `fetch_serial()`、`fetch_concurrent()` 和
`compare_request_timings()`。测试通过 `httpx.MockTransport` 离线运行，稳定且不依赖
公网；`examples/async_http.py` 会离线模拟 3 个各耗时约 0.2 秒的请求。串行总耗时
约 0.6 秒，并发总耗时约 0.2 秒。你也可以换成三个真实 URL 再观察差异。

并发不等于并行：这里的收益来自一个请求等待网络时，事件循环可以推进其他请求。

## 本阶段边界

这一版不会让 LLM 自动决定是否调用工具，也不会把 ToolResult 再送回 LLM。
那正是下一阶段要实现的最小 Agent Loop；在此之前，建议先修改一个工具、增加一个
输入字段，并为它补测试，以确认自己已经掌握当前的数据流。
