from ultron_bot.memory import MemoryStore


def test_memory_roundtrip(tmp_path):
    db = tmp_path / "mem.db"
    store = MemoryStore(str(db))

    store.add("user", "hello")
    store.add("assistant", "world")

    recent = store.recent(limit=2)
    assert len(recent) == 2
    assert recent[0].content == "hello"
    assert recent[1].content == "world"
