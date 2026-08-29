"""Application configuration models."""

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Runtime settings with safe defaults for local experiments."""

    model: str = "gpt-5.6"
    max_steps: int = Field(default=10, ge=1)
    timeout: float = Field(default=30.0, gt=0)
