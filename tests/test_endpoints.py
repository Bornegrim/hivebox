import pytest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta, timezone

client = TestClient(app)

# Mock data for consistent testing
recent_time = (
    (datetime.now(timezone.utc) - timedelta(minutes=15))
    .isoformat()
    .replace("+00:00", "Z")
)

mock_temperature_data = {"average_temperature": 23.5, "count": 3, "status": "Good"}

mock_box_data = {
    "sensors": [
        {
            "title": "Temperature",
            "lastMeasurement": {"createdAt": recent_time, "value": "23.5"},
        }
    ]
}


class TestTemperatureEndpoint:
    @patch("app.temperature.SENSEBOX_IDS", ["box1", "box2", "box3"])
    @patch("app.temperature.set_cached")
    @patch("app.temperature.get_cached")
    @patch("app.temperature.requests.get")
    def test_temperature_endpoint_success(
        self, mock_get, mock_get_cached, mock_set_cached
    ):
        # Mock cache miss
        mock_get_cached.return_value = None

        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_box_data
        mock_get.return_value = mock_response

        response = client.get("/temperature")

        assert response.status_code == 200
        data = response.json()
        assert "average_temperature" in data
        assert "count" in data
        assert "status" in data

    @patch("app.temperature.get_cached")
    def test_temperature_endpoint_from_cache(self, mock_get_cached):
        # Mock cache hit
        import json

        mock_get_cached.return_value = json.dumps(mock_temperature_data)

        response = client.get("/temperature")

        assert response.status_code == 200
        data = response.json()
        assert data["average_temperature"] == pytest.approx(23.5)
        assert data["count"] == 3


class TestMetricsEndpoint:
    def test_metrics_endpoint(self):
        response = client.get("/metrics")

        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
        # Check for Prometheus metric format
        assert "temperature_requests_total" in response.text


class TestStoreEndpoint:
    @patch("app.main.store_temperature_data")
    @patch("app.main.get_average_temperature")
    def test_store_endpoint_success(self, mock_get_temp, mock_store):
        mock_get_temp.return_value = mock_temperature_data
        mock_store.return_value = None  # Successful storage

        response = client.get("/store")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Temperature data stored successfully."
        mock_store.assert_called_once_with(mock_temperature_data)


class TestReadyzEndpoint:
    @patch("app.main.requests.get")
    @patch("app.main.SENSEBOX_IDS", ["box1", "box2", "box3"])
    def test_readyz_all_boxes_accessible(self, mock_get):
        # Mock all boxes as accessible
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = client.get("/readyz")

        assert response.status_code == 200

    @patch("app.main.check_cache")
    @patch("app.main.requests.get")
    @patch("app.main.SENSEBOX_IDS", ["box1", "box2"])
    def test_readyz_majority_inaccessible_with_cache(self, mock_get, mock_check_cache):
        # Mock majority of boxes as inaccessible
        mock_get.side_effect = Exception("Connection failed")
        # Mock cache exists
        mock_check_cache.return_value = True

        response = client.get("/readyz")

        assert response.status_code == 200

    @patch("app.main.check_cache")
    @patch("app.main.requests.get")
    @patch("app.main.SENSEBOX_IDS", ["box1", "box2"])
    def test_readyz_majority_inaccessible_no_cache(self, mock_get, mock_check_cache):
        # Mock majority of boxes as inaccessible
        mock_get.side_effect = Exception("Connection failed")
        # Mock no cache
        mock_check_cache.return_value = False

        response = client.get("/readyz")

        assert response.status_code == 503
