from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.main.db.get_history", return_value=[])
def test_history_404(_):
    response = client.get("/history", params={"url": "https://nothing.com"})
    assert response.status_code == 404
