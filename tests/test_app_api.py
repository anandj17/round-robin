from fastapi.testclient import TestClient
from src.api.app_api import AppProcess
import pytest

@pytest.fixture
def client():
    app_api = AppProcess("test")
    return TestClient(app_api.get_app())

def test_process_endpoint(client):
    test_payload = {"game": "CALL OF DUTY", "gamerID": "BEAST", "points": 20}

    response = client.post("/process", json=test_payload)

    assert response.status_code == 200
    assert response.json() == test_payload

def test_invalid_json(client):
    invalid_json_data = "INVALID_JSON"  # Simulate a non-JSON payload

    response = client.post("/process", data=invalid_json_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid JSON"}

def test_internal_server_error(client, monkeypatch):
    async def mock_json(*args, **kwargs):
        raise Exception("Unexpected Error")  # Simulate a server-side error

    monkeypatch.setattr("fastapi.Request.json", mock_json)

    response = client.post("/process", json={"test": "data"})

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}