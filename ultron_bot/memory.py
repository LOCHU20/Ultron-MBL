from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass
class MemoryItem:
    role: str
    content: str
    created_at: str


class MemoryStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = Path(db_path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversation_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def add(self, role: str, content: str) -> None:
        timestamp = datetime.utcnow().isoformat()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO conversation_memory(role, content, created_at) VALUES (?, ?, ?)",
                (role, content, timestamp),
            )
            conn.commit()

    def recent(self, limit: int = 8) -> list[MemoryItem]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT role, content, created_at
                FROM conversation_memory
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [MemoryItem(*row) for row in reversed(rows)]

    def export(self) -> Iterable[MemoryItem]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT role, content, created_at
                FROM conversation_memory
                ORDER BY id ASC
                """
            ).fetchall()
        for row in rows:
            yield MemoryItem(*row)
