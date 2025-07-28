from prometheus_client import Counter, Gauge, generate_latest

TEMPERATURE_REQUESTS = Counter(
    "temperature_requests_total", "Total number of /temperature requests received"
)

TEMPERATURE_CACHE_HITS = Counter(
    "temperature_cache_hits_total",
    "Number of times temperature data was served from cache",
)

TEMPERATURE_AVG = Gauge(
    "temperature_average_celsius", "Most recent average temperature value"
)


def get_metrics():
    return generate_latest()
