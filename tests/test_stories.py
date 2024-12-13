from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_user_stories():
    response = client.get("/api/v1/stories/")
    assert response.status_code == 200
    assert "message" in response.json()