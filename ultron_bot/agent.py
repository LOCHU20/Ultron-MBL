from __future__ import annotations

from dataclasses import dataclass

from ultron_bot.config import AppConfig
from ultron_bot.llm import LLMClient, OllamaClient, OpenAIClient
from ultron_bot.memory import MemoryStore
from ultron_bot.tools import close_app, open_app, open_website, web_lookup


@dataclass
class AgentResponse:
    text: str
    used_web: bool
    system_action: bool = False


class UltronAgent:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.memory = MemoryStore(config.memory_db)
        self.client = self._build_client()

    def _build_client(self) -> LLMClient:
        if self.config.llm_provider.lower() == "ollama":
            return OllamaClient(model=self.config.ollama_model)
        return OpenAIClient(model=self.config.openai_model)

    def _autonomous_prompt(self, user_text: str, web_context: str | None) -> list[dict[str, str]]:
        recent = self.memory.recent(limit=self.config.max_context_messages)

        system = {
            "role": "system",
            "content": (
                f"{self.config.persona}\n"
                "Autonomous directive: before answering, internally plan in 3 steps: "
                "(1) identify user objective, (2) retrieve relevant memory, "
                "(3) propose best action with clear assumptions. "
                "Do not reveal hidden chain-of-thought; provide concise rationale instead."
            ),
        }

        context_messages = [
            {"role": item.role, "content": item.content}
            for item in recent
            if item.role in {"user", "assistant"}
        ]

        if web_context:
            context_messages.append(
                {
                    "role": "system",
                    "content": f"Real-time web snippets (may be noisy):\n{web_context}",
                }
            )

        context_messages.append({"role": "user", "content": user_text})
        return [system, *context_messages]

    def _handle_system_command(self, user_text: str) -> AgentResponse | None:
        lowered = user_text.lower().strip()

        if lowered.startswith("open website:"):
            url = user_text.split(":", 1)[1].strip()
            result = open_website(url)
            self.memory.add("user", user_text)
            self.memory.add("assistant", result)
            return AgentResponse(text=result, used_web=False, system_action=True)

        if lowered.startswith("open app:"):
            app_name = user_text.split(":", 1)[1].strip()
            result = open_app(app_name)
            self.memory.add("user", user_text)
            self.memory.add("assistant", result)
            return AgentResponse(text=result, used_web=False, system_action=True)

        if lowered.startswith("close app:"):
            app_name = user_text.split(":", 1)[1].strip()
            result = close_app(app_name)
            self.memory.add("user", user_text)
            self.memory.add("assistant", result)
            return AgentResponse(text=result, used_web=False, system_action=True)

        return None

    def respond(self, user_text: str, allow_web: bool = True) -> AgentResponse:
        command_response = self._handle_system_command(user_text)
        if command_response:
            return command_response

        web_context = None
        used_web = False

        if allow_web and user_text.lower().startswith("web:"):
            lookup_query = user_text.split(":", 1)[1].strip()
            if lookup_query:
                web_context = web_lookup(lookup_query)
                used_web = True

        messages = self._autonomous_prompt(user_text=user_text, web_context=web_context)
        answer = self.client.chat(messages)

        self.memory.add("user", user_text)
        self.memory.add("assistant", answer)

        return AgentResponse(text=answer, used_web=used_web)
