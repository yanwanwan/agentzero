import pytest
from pydantic import ValidationError

from mini_agent.config import Settings
from mini_agent.models import Message, ToolCall, ToolResult


def test_settings_have_expected_defaults() -> None:
    settings = Settings()
    assert settings.model == "gpt-5.6"
    assert settings.max_steps == 10
    assert settings.timeout == 30.0


def test_settings_reject_non_positive_timeout() -> None:
    with pytest.raises(ValidationError):
        Settings(timeout=0)


def test_message_serializes_to_json() -> None:
    message = Message(role="user", content="hello")
    assert message.model_dump() == {"role": "user", "content": "hello"}
    assert '"content":"hello"' in message.model_dump_json()


def test_message_rejects_unknown_role() -> None:
    with pytest.raises(ValidationError):
        Message(role="visitor", content="hello")  # type: ignore[arg-type]


def test_tool_call_and_result_models() -> None:
    call = ToolCall(name="calculator", arguments={"expression": "2 + 2"})
    result = ToolResult(tool_name=call.name, success=True, output="4")
    assert call.arguments["expression"] == "2 + 2"
    assert result.model_dump()["success"] is True
