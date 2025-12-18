from fastapi.testclient import TestClient

from ssdlc_demo.main import app


def test_anime_quote_success(monkeypatch) -> None:
    class DummyResponse:
        status_code = 200

        def json(self):
            return {
                "status": "success",
                "data": {
                    "content": "Test quote",
                    "anime": {"id": 1, "name": "Naruto", "altName": "NARUTO"},
                    "character": {"id": 2, "name": "Naruto Uzumaki"},
                },
            }

    def fake_get(url, timeout=5):  # type: ignore[no-untyped-def]
        assert url == "https://api.animechan.io/v1/quotes/random"
        assert timeout == 5
        return DummyResponse()

    import ssdlc_demo.main as main_mod

    monkeypatch.setattr(main_mod.requests, "get", fake_get)

    client = TestClient(app)
    res = client.get("/anime/quote")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "success"
    assert body["data"]["content"] == "Test quote"


def test_anime_quote_upstream_error(monkeypatch) -> None:
    class DummyResponse:
        status_code = 500

        def json(self):
            return {}

    def fake_get(url, timeout=5):  # type: ignore[no-untyped-def]
        return DummyResponse()

    import ssdlc_demo.main as main_mod

    monkeypatch.setattr(main_mod.requests, "get", fake_get)

    client = TestClient(app)
    res = client.get("/anime/quote")
    assert res.status_code == 502


def test_anime_quote_invalid_json(monkeypatch) -> None:
    class DummyResponse:
        status_code = 200

        def json(self):  # type: ignore[no-untyped-def]
            raise ValueError("invalid json")

    def fake_get(url, timeout=5):  # type: ignore[no-untyped-def]
        return DummyResponse()

    import ssdlc_demo.main as main_mod

    monkeypatch.setattr(main_mod.requests, "get", fake_get)

    client = TestClient(app)
    res = client.get("/anime/quote")
    assert res.status_code == 502
