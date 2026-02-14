from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any

import requests


class LLMClient(ABC):
    @abstractmethod
    def chat(self, messages: list[dict[str, str]]) -> str:
        raise NotImplementedError


class OpenAIClient(LLMClient):
    def __init__(self, model: str) -> None:
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.endpoint = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    def chat(self, messages: list[dict[str, str]]) -> str:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")
        response = requests.post(
            f"{self.endpoint}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={"model": self.model, "messages": messages, "temperature": 0.6},
            timeout=60,
        )
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        return payload["choices"][0]["message"]["content"]


class OllamaClient(LLMClient):
    def __init__(self, model: str, host: str | None = None) -> None:
        self.model = model
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")

    def chat(self, messages: list[dict[str, str]]) -> str:
        response = requests.post(
            f"{self.host}/api/chat",
            json={"model": self.model, "messages": messages, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        return payload["message"]["content"]
