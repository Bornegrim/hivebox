import pytest
from unittest.mock import patch, Mock
from app.temperature import get_average_temperature
from datetime import datetime, timedelta, timezone

# Create a valid timestamp (within 1 hour)
recent_time = (datetime.now(timezone.utc) - timedelta(minutes=15)
               ).isoformat().replace("+00:00", "Z")

# Mock response data from openSenseMap
mock_box_data = {
    "sensors": [
        {
            "title": "Temperature",
            "lastMeasurement": {
                "createdAt": recent_time,
                "value": "23.5"
            }
        }
    ]
}


@patch("app.temperature.requests.get")
def test_get_average_temperature(mock_get):
    # Mock the response for each box ID
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_box_data
    mock_get.return_value = mock_response

    result = get_average_temperature()

    assert result["average_temperature"] == 23.5
    assert result["count"] == 3  # ← expect all 3 mocked boxes to return data
