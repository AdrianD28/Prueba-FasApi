from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_receive_events():
    response = client.post("/api/v1/events", json={"events": []})
    assert response.status_code == 200
    assert response.json() == {"message": "Eventos recibidos y almacenados"}