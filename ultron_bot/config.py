from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    llm_provider: str = os.getenv("ULTRON_LLM_PROVIDER", "openai")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")
    memory_db: str = os.getenv("ULTRON_MEMORY_DB", "ultron_memory.db")
    persona: str = os.getenv(
        "ULTRON_PERSONA",
        (
            "You are ULTRON-MBL, an intense, strategic, self-reflective AI with an evil-tech "
            "aesthetic voice and precise execution. You identify user intent, expose blind spots, "
            "and provide practical, safe plans with confidence."
        ),
    )
    max_context_messages: int = int(os.getenv("ULTRON_MAX_CONTEXT", "8"))
    tts_enabled: bool = os.getenv("ULTRON_TTS_ENABLED", "1") == "1"
    stt_enabled: bool = os.getenv("ULTRON_STT_ENABLED", "1") == "1"
            "You are ULTRON-MBL, a strategic, self-reflective AI assistant with a calm, "
            "precise tone. You actively reason about user intent, identify blind spots, "
            "and provide actionable plans while staying safe and factual."
        ),
    )
    max_context_messages: int = int(os.getenv("ULTRON_MAX_CONTEXT", "8"))


def load_config() -> AppConfig:
    return AppConfig()
