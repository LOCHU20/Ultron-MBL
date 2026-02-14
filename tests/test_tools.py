from ultron_bot.tools import open_website


def test_open_website_normalizes_scheme(monkeypatch):
    captured = {}

    def fake_open(url):
        captured["url"] = url
        return True

    monkeypatch.setattr("ultron_bot.tools.webbrowser.open", fake_open)
    result = open_website("example.com")

    assert captured["url"] == "https://example.com"
    assert "Opened website" in result
