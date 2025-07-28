import pytest
from unittest.mock import patch, Mock
from app.temperature import (
    extract_temperatures,
    determine_status,
    fetch_box_data,
    get_average_temperature,
)
from datetime import datetime, timezone, timedelta


class TestExtractTemperatures:
    def test_extract_valid_temperature(self):
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        recent_time = datetime.now(timezone.utc) - timedelta(minutes=30)

        box_data = {
            "sensors": [
                {
                    "title": "Temperature Sensor",
                    "lastMeasurement": {
                        "createdAt": recent_time.isoformat().replace("+00:00", "Z"),
                        "value": "25.3",
                    },
                }
            ]
        }

        temps = extract_temperatures(box_data, one_hour_ago)
        assert len(temps) == 1
        assert temps[0] == pytest.approx(25.3)

    def test_extract_old_temperature_ignored(self):
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        old_time = datetime.now(timezone.utc) - timedelta(hours=2)

        box_data = {
            "sensors": [
                {
                    "title": "Temperature Sensor",
                    "lastMeasurement": {
                        "createdAt": old_time.isoformat().replace("+00:00", "Z"),
                        "value": "25.3",
                    },
                }
            ]
        }

        temps = extract_temperatures(box_data, one_hour_ago)
        assert len(temps) == 0

    def test_extract_invalid_value_ignored(self):
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        recent_time = datetime.now(timezone.utc) - timedelta(minutes=30)

        box_data = {
            "sensors": [
                {
                    "title": "Temperature Sensor",
                    "lastMeasurement": {
                        "createdAt": recent_time.isoformat().replace("+00:00", "Z"),
                        "value": "invalid",
                    },
                }
            ]
        }

        temps = extract_temperatures(box_data, one_hour_ago)
        assert len(temps) == 0

    def test_extract_no_temp_sensors(self):
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)

        box_data = {
            "sensors": [
                {
                    "title": "Humidity Sensor",
                    "lastMeasurement": {
                        "createdAt": datetime.now(timezone.utc)
                        .isoformat()
                        .replace("+00:00", "Z"),
                        "value": "60",
                    },
                }
            ]
        }

        temps = extract_temperatures(box_data, one_hour_ago)
        assert len(temps) == 0

    def test_extract_multiple_temp_sensors(self):
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        recent_time = datetime.now(timezone.utc) - timedelta(minutes=30)

        box_data = {
            "sensors": [
                {
                    "title": "Temperature Indoor",
                    "lastMeasurement": {
                        "createdAt": recent_time.isoformat().replace("+00:00", "Z"),
                        "value": "22.1",
                    },
                },
                {
                    "title": "Temperature Outdoor",
                    "lastMeasurement": {
                        "createdAt": recent_time.isoformat().replace("+00:00", "Z"),
                        "value": "25.9",
                    },
                },
            ]
        }

        temps = extract_temperatures(box_data, one_hour_ago)
        assert len(temps) == 2
        assert pytest.approx(22.1) in temps
        assert pytest.approx(25.9) in temps


class TestDetermineStatus:
    def test_status_unavailable(self):
        assert determine_status(None) == "Unavailable"

    def test_status_too_cold(self):
        assert determine_status(5.0) == "Too Cold"
        assert determine_status(10.0) == "Too Cold"

    def test_status_good(self):
        assert determine_status(11.0) == "Good"
        assert determine_status(25.0) == "Good"
        assert determine_status(36.0) == "Good"

    def test_status_too_hot(self):
        assert determine_status(37.0) == "Too Hot"
        assert determine_status(50.0) == "Too Hot"


class TestFetchBoxData:
    @patch("app.temperature.requests.get")
    def test_fetch_box_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test_box"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_box_data("test_box_id")

        assert result == {"id": "test_box"}
        mock_get.assert_called_once_with(
            "https://api.opensensemap.org/boxes/test_box_id", timeout=5
        )

    @patch("app.temperature.requests.get")
    def test_fetch_box_data_failure(self, mock_get):
        import requests

        mock_get.side_effect = requests.RequestException("Network error")

        result = fetch_box_data("test_box_id")

        assert result is None


class TestGetAverageTemperatureEdgeCases:
    @patch("app.temperature.get_cached")
    @patch("app.temperature.set_cached")
    @patch("app.temperature.fetch_box_data")
    @patch("app.temperature.SENSEBOX_IDS", ["box1", "box2"])
    def test_no_temperature_data_available(
        self, mock_fetch, mock_set_cached, mock_get_cached
    ):
        mock_get_cached.return_value = None
        mock_fetch.return_value = None  # No data from any box

        result = get_average_temperature()

        assert result["average_temperature"] is None
        assert result["message"] == "No recent temperature data found."
        assert result["status"] == "Unavailable"

    @patch("app.temperature.get_cached")
    @patch("app.temperature.set_cached")
    @patch("app.temperature.fetch_box_data")
    @patch("app.temperature.SENSEBOX_IDS", ["box1"])
    def test_single_temperature_reading(
        self, mock_fetch, mock_set_cached, mock_get_cached
    ):
        mock_get_cached.return_value = None

        recent_time = datetime.now(timezone.utc) - timedelta(minutes=30)
        mock_fetch.return_value = {
            "sensors": [
                {
                    "title": "Temperature",
                    "lastMeasurement": {
                        "createdAt": recent_time.isoformat().replace("+00:00", "Z"),
                        "value": "22.7",
                    },
                }
            ]
        }

        result = get_average_temperature()

        assert result["average_temperature"] == pytest.approx(22.7)
        assert result["count"] == 1
        assert result["status"] == "Good"
