from __future__ import annotations

import os
import platform
import subprocess
import webbrowser
from typing import Any

import requests


DUCKDUCKGO_ENDPOINT = "https://api.duckduckgo.com/"


APP_ALIASES = {
    "chrome": ["google-chrome", "chrome", "chromium", "chromium-browser"],
    "firefox": ["firefox"],
    "edge": ["microsoft-edge", "msedge"],
    "notepad": ["notepad"],
    "calculator": ["gnome-calculator", "kcalc", "calc", "calculator"],
}


PROCESS_ALIASES = {
    "chrome": ["chrome", "chromium", "google-chrome", "msedge"],
    "firefox": ["firefox"],
    "edge": ["msedge", "microsoft-edge"],
    "notepad": ["notepad", "gedit", "nano"],
    "calculator": ["gnome-calculator", "kcalc", "calc"],
}


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


def _run_safely(command: list[str]) -> bool:
    try:
        subprocess.Popen(command)  # noqa: S603
        return True
    except Exception:
        return False


def open_website(url: str) -> str:
    normalized = url.strip()
    if not normalized:
        return "Missing URL."
    if not normalized.startswith(("http://", "https://")):
        normalized = f"https://{normalized}"
    opened = webbrowser.open(normalized)
    if opened:
        return f"Opened website: {normalized}"
    return f"Failed to open website: {normalized}"


def open_app(app_name: str) -> str:
    target = app_name.strip().lower()
    if not target:
        return "Missing app name."

    system = platform.system().lower()
    candidates = APP_ALIASES.get(target, [target])

    if system == "darwin":
        ok = _run_safely(["open", "-a", app_name])
        return f"Opened app: {app_name}" if ok else f"Failed to open app: {app_name}"

    if system == "windows":
        for candidate in candidates:
            if _run_safely(["cmd", "/c", "start", "", candidate]):
                return f"Opened app: {candidate}"
        return f"Failed to open app: {app_name}"

    for candidate in candidates:
        if _run_safely([candidate]):
            return f"Opened app: {candidate}"
    return f"Failed to open app: {app_name}"


def close_app(app_name: str) -> str:
    target = app_name.strip().lower()
    if not target:
        return "Missing app/process name."

    processes = PROCESS_ALIASES.get(target, [target])
    system = platform.system().lower()

    if system == "windows":
        for proc in processes:
            subprocess.run(["taskkill", "/IM", f"{proc}.exe", "/F"], check=False)  # noqa: S603
        return f"Close command sent for: {', '.join(processes)}"

    for proc in processes:
        subprocess.run(["pkill", "-f", proc], check=False)  # noqa: S603
    return f"Close command sent for: {', '.join(processes)}"
