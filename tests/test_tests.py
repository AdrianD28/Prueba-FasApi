from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_tests():
    response = client.get("/api/v1/tests/")
    assert response.status_code == 200
    assert "message" in response.json()