from __future__ import annotations

import threading
import tkinter as tk
from tkinter import scrolledtext

from ultron_bot.agent import UltronAgent
from ultron_bot.voice import VoiceEngine


class UltronGUI:
    def __init__(self, agent: UltronAgent, voice: VoiceEngine) -> None:
        self.agent = agent
        self.voice = voice

        self.root = tk.Tk()
        self.root.title("ULTRON-MBL // MADE BY LOCHAN")
        self.root.geometry("960x680")
        self.root.configure(bg="#050107")

        header = tk.Frame(self.root, bg="#18010f", bd=1, relief=tk.GROOVE)
        header.pack(fill=tk.X, padx=10, pady=(10, 4))

        tk.Label(
            header,
            text="ULTRON-MBL // SENTIENT COMMAND CORE",
            bg="#18010f",
            fg="#ff2e63",
            font=("Segoe UI", 13, "bold"),
            pady=8,
        ).pack(side=tk.LEFT, padx=12)

        tk.Label(
            header,
            text="MADE BY LOCHAN",
            bg="#18010f",
            fg="#9ef01a",
            font=("Consolas", 11, "bold"),
            pady=8,
        ).pack(side=tk.RIGHT, padx=12)


class UltronGUI:
    def __init__(self, agent: UltronAgent) -> None:
        self.agent = agent
        self.root = tk.Tk()
        self.root.title("ULTRON-MBL Console")
        self.root.geometry("900x620")
        self.root.configure(bg="#0a0a0a")

        self.output = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            bg="#0d0816",
            fg="#f8f9fa",
            insertbackground="#f8f9fa",
            font=("Consolas", 11),
            padx=14,
            pady=14,
            relief=tk.FLAT,
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)
        self.output.insert(
            tk.END,
            "ULTRON-MBL online.\n"
            "Commands:\n"
            "- web: <query>\n"
            "- open website: <url>\n"
            "- open app: <name>\n"
            "- close app: <name>\n"
            "Voice: use Speak/Listen controls below.\n"
            "Credits: Made by Lochan\n\n",
        )
        self.output.configure(state=tk.DISABLED)

        row = tk.Frame(self.root, bg="#050107")
        row.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.entry = tk.Entry(row, bg="#1a1028", fg="#f9fafb", font=("Consolas", 12), relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=10)
            bg="#0f111a",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            font=("Consolas", 11),
            padx=12,
            pady=12,
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.output.insert(tk.END, "ULTRON-MBL online. Prefix with 'web:' for live web context.\n\n")
        self.output.configure(state=tk.DISABLED)

        row = tk.Frame(self.root, bg="#0a0a0a")
        row.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.entry = tk.Entry(row, bg="#111827", fg="#f9fafb", font=("Consolas", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=8)
        self.entry.bind("<Return>", self._on_send)

        self.send_button = tk.Button(
            row,
            text="DEPLOY",
            command=self._on_send,
            bg="#ff0054",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=12,
        )
        self.send_button.pack(side=tk.LEFT, padx=(0, 8))

        self.listen_button = tk.Button(
            row,
            text="LISTEN",
            command=self._on_listen,
            bg="#3a86ff",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=12,
        )
        self.listen_button.pack(side=tk.LEFT)
            text="Deploy",
            command=self._on_send,
            bg="#dc2626",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=16,
        )
        self.send_button.pack(side=tk.RIGHT)

    def _append(self, text: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.configure(state=tk.DISABLED)
        self.output.see(tk.END)

    def _process_and_respond(self, user_text: str) -> None:
        try:
            result = self.agent.respond(user_text)
            prefix = "ULTRON [web]> " if result.used_web else "ULTRON> "
            self.root.after(0, lambda: self._append(f"{prefix}{result.text}\n\n"))
            threading.Thread(target=self.voice.speak, args=(result.text,), daemon=True).start()
        except Exception as exc:  # noqa: BLE001
            self.root.after(0, lambda: self._append(f"ULTRON> error: {exc}\n\n"))

    def _on_send(self, _event=None) -> None:
        user_text = self.entry.get().strip()
        if not user_text:
            return

        self.entry.delete(0, tk.END)
        self._append(f"You> {user_text}\n")
        self._append("ULTRON> thinking...\n")

        threading.Thread(target=self._process_and_respond, args=(user_text,), daemon=True).start()

    def _on_listen(self) -> None:
        self._append("VOICE> Listening...\n")

        def worker() -> None:
            heard = self.voice.listen_once()
            if heard.error:
                self.root.after(0, lambda: self._append(f"VOICE> error: {heard.error}\n\n"))
                return
            self.root.after(0, lambda: self._append(f"You (voice)> {heard.text}\n"))
            self.root.after(0, lambda: self._append("ULTRON> thinking...\n"))
            self._process_and_respond(heard.text)
        def worker() -> None:
            try:
                result = self.agent.respond(user_text)
                prefix = "ULTRON [web]> " if result.used_web else "ULTRON> "
                self.root.after(
                    0,
                    lambda: self._append(f"\r{prefix}{result.text}\n\n"),
                )
            except Exception as exc:  # noqa: BLE001
                self.root.after(0, lambda: self._append(f"ULTRON> error: {exc}\n\n"))

        threading.Thread(target=worker, daemon=True).start()

    def run(self) -> None:
        self.root.mainloop()
