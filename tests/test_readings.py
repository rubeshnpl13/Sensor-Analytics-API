from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient


def valid_payload() -> dict[str, object]:
    return {
        "device_id": "greenhouse-01",
        "metric": "temperature",
        "value": 21.5,
        "timestamp": datetime.now(UTC).isoformat(),
    }


def test_valid_reading_is_accepted(client: TestClient) -> None:
    response = client.post("/api/v1/readings", json=valid_payload())
    assert response.status_code == 201
    body = response.json()
    assert body["device_id"] == "greenhouse-01"
    assert body["metric"] == "temperature"


def test_unknown_metric_is_rejected(client: TestClient) -> None:
    payload = valid_payload() | {"metric": "voltage"}
    response = client.post("/api/v1/readings", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "metric"]


def test_implausible_value_is_rejected(client: TestClient) -> None:
    payload = valid_payload() | {"value": 500.0}
    response = client.post("/api/v1/readings", json=payload)
    assert response.status_code == 422


def test_humidity_above_100_is_rejected(client: TestClient) -> None:
    payload = valid_payload() | {"metric": "humidity", "value": 140.0}
    response = client.post("/api/v1/readings", json=payload)
    assert response.status_code == 422


def test_naive_timestamp_is_rejected(client: TestClient) -> None:
    payload = valid_payload() | {"timestamp": "2026-08-30T12:00:00"}
    response = client.post("/api/v1/readings", json=payload)
    assert response.status_code == 422


def test_future_timestamp_is_rejected(client: TestClient) -> None:
    future = datetime.now(UTC) + timedelta(hours=1)
    payload = valid_payload() | {"timestamp": future.isoformat()}
    response = client.post("/api/v1/readings", json=payload)
    assert response.status_code == 422


def test_invalid_device_id_is_rejected(client: TestClient) -> None:
    payload = valid_payload() | {"device_id": "bad id!"}
    response = client.post("/api/v1/readings", json=payload)
    assert response.status_code == 422