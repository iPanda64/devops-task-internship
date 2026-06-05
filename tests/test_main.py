"""Minimal smoke tests. CI runs these."""

import redis
from unittest.mock import patch

from fastapi.testclient import TestClient


def _client():
    from app.main import app
    return TestClient(app)


def test_health_endpoint_responds():
    with patch("app.main.r") as mock_redis:
        mock_redis.ping.return_value = True
        response = _client().get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["redis"] is True


def test_health_endpoint_reports_redis_failure():
    with patch("app.main.r") as mock_redis:
        mock_redis.ping.side_effect = redis.RedisError("Connection error")
        response = _client().get("/health")
    
    assert response.status_code == 503
    assert response.json()["status"] == "unhealthy"
    assert response.json()["redis"] is False


def test_visits_increments():
    with patch("app.main.r") as mock_redis:
        mock_redis.incr.return_value = 42
        response = _client().get("/visits")
    assert response.status_code == 200
    assert response.json() == {"visits": 42}


def test_visits_count_does_not_increment():
    with patch("app.main.r") as mock_redis:
        mock_redis.get.return_value = "10"
        response = _client().get("/visits/count")
    assert response.status_code == 200
    assert response.json() == {"visits": 10}
    mock_redis.incr.assert_not_called()


def test_visits_reset():
    with patch("app.main.r") as mock_redis:
        response = _client().post("/visits/reset")
    assert response.status_code == 200
    assert response.json() == {"visits": 0}
    mock_redis.set.assert_called_with("visits", 0)
