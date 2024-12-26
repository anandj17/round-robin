import pytest
import httpx
import asyncio
from fastapi.testclient import TestClient
from src.router.round_robin import RoundRobinAPI

@pytest.fixture
def client(monkeypatch):
    # Mock backend instances
    def mock_get_backend_instances():
        return [
            "http://localhost:3001",
            "http://localhost:3002",
            "http://localhost:3003",
        ]

    monkeypatch.setattr(
        "src.config.settings.get_backend_instances", mock_get_backend_instances
    )
    app_instance = RoundRobinAPI()
    return TestClient(app_instance.app)

@pytest.mark.asyncio
async def test_route_request_success(client, monkeypatch):
    payload = {"key": "value"}

    # Mock the httpx.AsyncClient.post response
    async def mock_post(*args, **kwargs):
        return httpx.Response(200, json={"message": "Success"})

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    response = client.post("/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Success"}

@pytest.mark.asyncio
async def test_route_request_no_healthy_instances(client, monkeypatch):
    payload = {"key": "value"}

    # Simulate all instances failing
    async def mock_post(*args, **kwargs):
        raise httpx.RequestError("Failed request")

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    response = client.post("/", json=payload)
    assert response.status_code == 503
    assert response.json()["detail"] == "All instances failed: Failed request"

@pytest.mark.asyncio
async def test_route_request_circuit_breaker_blocks_instance(client, monkeypatch):
    payload = {"key": "value"}
    call_count = {"count": 0}

    # Mock post responses for multiple instances
    async def mock_post(*args, **kwargs):
        call_count["count"] += 1
        if call_count["count"] < 3:  # Simulate failures for first 2 calls
            raise httpx.RequestError("Failed request")
        return httpx.Response(200, json={"message": "Success"})

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    response = client.post("/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Success"}

@pytest.mark.asyncio
async def test_route_request_timeout(client, monkeypatch):
    payload = {"key": "value"}

    # Simulate timeout on all instances
    async def mock_post(*args, **kwargs):
        raise httpx.TimeoutException("Timeout")

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    response = client.post("/", json=payload)
    assert response.status_code == 503
    assert "Timeout" in response.json()["detail"]

@pytest.mark.asyncio
async def test_round_robin_mechanism(client, monkeypatch):
    payload = {"key": "value"}
    responses = iter(
        [
            httpx.Response(200, json={"instance": "1"}),
            httpx.Response(200, json={"instance": "2"}),
            httpx.Response(200, json={"instance": "3"}),
        ]
    )

    # Mock post to return sequential responses
    async def mock_post(*args, **kwargs):
        return next(responses)

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    response_1 = client.post("/", json=payload)
    response_2 = client.post("/", json=payload)
    response_3 = client.post("/", json=payload)

    assert response_1.json()["instance"] == "1"
    assert response_2.json()["instance"] == "2"
    assert response_3.json()["instance"] == "3"

@pytest.mark.asyncio
async def test_route_request_slow_instance(client, monkeypatch):
    payload = {"key": "value"}
    instance_responses = {
        "http://localhost:3001/process": {"delay": 5, "response": {"instance": "1"}},
        "http://localhost:3002/process": {"delay": 0, "response": {"instance": "2"}},
        "http://localhost:3003/process": {"delay": 0, "response": {"instance": "3"}},
    }

    # Simulate different instance responses
    async def mock_post(*args, **kwargs):
        url = args[1]
        if args[1] in instance_responses:
            delay = instance_responses[url]["delay"]
            await asyncio.sleep(delay)
            return httpx.Response(200, json=instance_responses[url]["response"])
        return httpx.Response(404)

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    # Make multiple requests
    async def make_request(client, payload):
        response = client.post("/", json=payload)
        return response

    responses = await asyncio.gather(
        *[make_request(client, payload) for _ in range(11)]
    )

    # Validate responses
    expected_instances = ["1", "2", "3", "1", "2", "3", "1", "2", "3", "2", "3"]
    for i, response in enumerate(responses):
        assert response.status_code == 200
        assert response.json()["instance"] == expected_instances[i]

    # Simulate recovery and make additional requests
    await asyncio.sleep(30)

    recovery_responses = await asyncio.gather(
        *[make_request(client, payload) for _ in range(3)]
    )
    recovery_expected = ["1", "2", "3"]
    for i, response in enumerate(recovery_responses):
        assert response.status_code == 200
        assert response.json()["instance"] == recovery_expected[i]