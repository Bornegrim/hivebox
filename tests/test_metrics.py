import pytest
from unittest.mock import patch
from app.metrics import (
    get_metrics,
    TEMPERATURE_REQUESTS,
    TEMPERATURE_CACHE_HITS,
    TEMPERATURE_AVG,
)


class TestMetricsModule:
    def test_get_metrics_returns_prometheus_format(self):
        # Increment some counters for testing
        TEMPERATURE_REQUESTS.inc()
        TEMPERATURE_CACHE_HITS.inc()
        TEMPERATURE_AVG.set(25.5)

        result = get_metrics()

        # Should return prometheus format bytes
        assert isinstance(result, bytes)
        result_str = result.decode("utf-8")
        assert "temperature_requests_total" in result_str
        assert "temperature_cache_hits_total" in result_str
        assert "temperature_average_celsius" in result_str

    def test_temperature_requests_counter(self):
        # Get initial value
        initial_value = TEMPERATURE_REQUESTS._value._value

        # Increment counter
        TEMPERATURE_REQUESTS.inc()

        # Verify increment
        assert TEMPERATURE_REQUESTS._value._value == initial_value + 1

    def test_temperature_cache_hits_counter(self):
        # Get initial value
        initial_value = TEMPERATURE_CACHE_HITS._value._value

        # Increment counter
        TEMPERATURE_CACHE_HITS.inc()

        # Verify increment
        assert TEMPERATURE_CACHE_HITS._value._value == initial_value + 1

    def test_temperature_avg_gauge(self):
        # Set gauge value
        TEMPERATURE_AVG.set(23.7)

        # Verify gauge value
        assert TEMPERATURE_AVG._value._value == pytest.approx(23.7)
