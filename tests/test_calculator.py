import pytest

from mini_agent.tools.calculator import calculator_tool, evaluate_expression


@pytest.mark.parametrize(
    ("expression", "expected"),
    [("2 + 3", 5), ("128 * 726", 92928), ("(10 - 4) / 2", 3.0)],
)
def test_evaluate_supported_arithmetic(expression: str, expected: int | float) -> None:
    assert evaluate_expression(expression) == expected


@pytest.mark.parametrize("expression", ["2 ** 8", "__import__('os')", "1 < 2"])
def test_evaluate_rejects_unsupported_syntax(expression: str) -> None:
    with pytest.raises(ValueError):
        evaluate_expression(expression)


@pytest.mark.asyncio
async def test_calculator_validates_missing_expression() -> None:
    result = await calculator_tool.execute({})
    assert result.success is False
    assert result.output.startswith("Invalid tool arguments:")


@pytest.mark.asyncio
async def test_calculator_turns_division_error_into_failure() -> None:
    result = await calculator_tool.execute({"expression": "1 / 0"})
    assert result.success is False
    assert "division by zero" in result.output
