"""A deliberately small arithmetic tool without unrestricted eval()."""

import ast
import operator
from collections.abc import Callable

from pydantic import BaseModel, Field

from mini_agent.tools.base import Tool

Number = int | float
BinaryOperator = Callable[[Number, Number], Number]

_OPERATORS: dict[type[ast.operator], BinaryOperator] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_MAX_ABS_VALUE = 1_000_000_000_000_000_000
_MAX_DEPTH = 32


class CalculatorInput(BaseModel):
    expression: str = Field(min_length=1, max_length=200)


def evaluate_expression(expression: str) -> Number:
    """Evaluate literals and +, -, *, / operators using a restricted AST."""

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Expression is not valid arithmetic") from exc
    return _evaluate_node(tree.body, depth=0)


def _evaluate_node(node: ast.AST, depth: int) -> Number:
    if depth > _MAX_DEPTH:
        raise ValueError("Expression is too deeply nested")

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        if isinstance(node.value, bool) or abs(node.value) > _MAX_ABS_VALUE:
            raise ValueError("Numeric literal is outside the allowed range")
        return node.value

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _evaluate_node(node.operand, depth + 1)
        result = value if isinstance(node.op, ast.UAdd) else -value
        return _check_result(result)

    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left = _evaluate_node(node.left, depth + 1)
        right = _evaluate_node(node.right, depth + 1)
        result = _OPERATORS[type(node.op)](left, right)
        return _check_result(result)

    raise ValueError("Only numbers, parentheses, and + - * / are allowed")


def _check_result(value: Number) -> Number:
    if abs(value) > _MAX_ABS_VALUE:
        raise ValueError("Result is outside the allowed range")
    return value


async def calculator_handler(input_data: BaseModel) -> str:
    """Evaluate a validated calculator request."""

    request = CalculatorInput.model_validate(input_data)
    return str(evaluate_expression(request.expression))


calculator_tool = Tool(
    name="calculator",
    description="Evaluate arithmetic containing +, -, *, /, and parentheses.",
    input_schema=CalculatorInput,
    handler=calculator_handler,
)
