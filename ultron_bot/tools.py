from __future__ import annotations

from typing import Any

import requests


DUCKDUCKGO_ENDPOINT = "https://api.duckduckgo.com/"


def web_lookup(query: str) -> str:
    """Retrieve lightweight real-time context from DuckDuckGo Instant Answer API."""
    params = {
        "q": query,
        "format": "json",
        "no_redirect": "1",
        "no_html": "1",
        "skip_disambig": "1",
    }
    response = requests.get(DUCKDUCKGO_ENDPOINT, params=params, timeout=12)
    response.raise_for_status()
    payload: dict[str, Any] = response.json()

    abstract = payload.get("AbstractText") or ""
    answer = payload.get("Answer") or ""
    related_topics = payload.get("RelatedTopics") or []

    snippets: list[str] = []
    if answer:
        snippets.append(f"Answer: {answer}")
    if abstract:
        snippets.append(f"Abstract: {abstract}")

    for topic in related_topics[:3]:
        if isinstance(topic, dict) and topic.get("Text"):
            snippets.append(f"Related: {topic['Text']}")

    if not snippets:
        return "No web snippets found for the query."

    return "\n".join(snippets)
