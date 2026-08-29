"""Tool definition and validated execution."""

from collections.abc import Awaitable, Callable

from pydantic import BaseModel, ValidationError

from mini_agent.models import ToolResult

ToolHandler = Callable[[BaseModel], Awaitable[str]]


class Tool:
    """A named async operation with a Pydantic input boundary."""

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: type[BaseModel],
        handler: ToolHandler,
    ) -> None:
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.handler = handler

    async def execute(self, arguments: dict[str, object]) -> ToolResult:
        """Validate arguments, invoke the handler, and normalize its outcome."""

        try:
            validated_input = self.input_schema.model_validate(arguments)
            output = await self.handler(validated_input)
        except ValidationError as exc:
            return ToolResult(
                tool_name=self.name,
                success=False,
                output=f"Invalid tool arguments: {exc}",
            )
        except Exception as exc:
            return ToolResult(
                tool_name=self.name,
                success=False,
                output=f"Tool execution failed: {exc}",
            )

        return ToolResult(tool_name=self.name, success=True, output=output)
