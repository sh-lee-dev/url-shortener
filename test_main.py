from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_shorten_url():
    response = client.post("/shorten", json={"url": "https://google.com"})
    assert response.status_code == 200
    assert "short_code" in response.json()

def test_redirect():
    response = client.post("/shorten", json={"url": "https://google.com"})
    code = response.json()["short_code"]
    origin_url = client.get(f"/{code}")
    assert origin_url.json()["original_url"] == "https://google.com"

def test_invalid_url():
    response = client.post("/shorten", json={"url": "Hello"})
    assert response.status_code == 400

def test_not_found():
    wrong_code = client.get("/WrongCode")
    assert wrong_code.status_code == 404

