from __future__ import annotations

import json
from typing import Any, Dict, List

import httpx


class LLMClient:
    """Thin wrapper around OpenAI-compatible completion endpoints."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    async def generate_completion(self, model: str, messages: List[Dict[str, Any]]) -> str:
        """Call the chat completions endpoint and return the generated text."""

        if not self.base_url or not self.api_key:
            # Fall back to deterministic stub when credentials are missing.
            content = "\n\n".join(message["content"] for message in messages if message["role"] == "user")
            return f"[stubbed completion for {model}]\n{content}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": model, "messages": messages}
        url = f"{self.base_url}/chat/completions"

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, content=json.dumps(payload))
            response.raise_for_status()
            data = response.json()

        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError) as exc:  # pragma: no cover - defensive branch
            raise ValueError("Unexpected response schema from LLM service") from exc
