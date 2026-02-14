from __future__ import annotations

import threading
import tkinter as tk
from tkinter import scrolledtext

from ultron_bot.agent import UltronAgent


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

    def _on_send(self, _event=None) -> None:
        user_text = self.entry.get().strip()
        if not user_text:
            return

        self.entry.delete(0, tk.END)
        self._append(f"You> {user_text}\n")
        self._append("ULTRON> thinking...\n")

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
