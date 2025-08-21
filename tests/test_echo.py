from fastapi.testclient import TestClient

from ssdlc_demo.main import app


def test_echo_roundtrip() -> None:
    client = TestClient(app)
    res = client.post("/echo", json={"message": "hello"})
    assert res.status_code == 200
    assert res.json() == {"message": "hello"}


def test_echo_validation_error() -> None:
    client = TestClient(app)
    res = client.post("/echo", json={})
    assert res.status_code == 422 