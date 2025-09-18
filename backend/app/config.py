from __future__ import annotations

from functools import lru_cache
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings."""

    api_prefix: str = Field(default="/api")
    default_llm_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="Default base URL for OpenAI compatible endpoints.",
    )
    default_llm_api_key: str = Field(
        default="",
        description="Default API key used when the client does not provide one.",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
