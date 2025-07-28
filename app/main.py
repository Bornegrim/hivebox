import os
from fastapi import FastAPI, Response, status
from prometheus_client import CONTENT_TYPE_LATEST
import requests

from app.version import get_version
from app.temperature import get_average_temperature, SENSEBOX_IDS
from app.metrics import get_metrics
from app.storage import store_temperature_data
from app.cache import check_cache

APP_VERSION = os.getenv("APP_VERSION", "0.0.1")
app = FastAPI(title="HiveBox", version=APP_VERSION)


@app.get("/version")
def version():
    return get_version()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/temperature")
def temperature():
    return get_average_temperature()


@app.get("/metrics")
def metrics():
    data = get_metrics()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.get("/store")
def store_endpoint():
    data = get_average_temperature()
    store_temperature_data(data)
    return {"message": "Temperature data stored successfully."}


@app.get("/readyz")
def readyz():
    inaccessible = 0
    for box_id in SENSEBOX_IDS:
        try:
            response = requests.get(
                f"https://api.opensensemap.org/boxes/{box_id}", timeout=3
            )
            if response.status_code != 200:
                inaccessible += 1
        except Exception:
            inaccessible += 1
    print(f"Number of inaccessible senseboxes: {inaccessible}")
    if inaccessible > len(SENSEBOX_IDS) // 2:
        print("More than half of the senseboxes are inaccessible.")
        cache_value = check_cache("temperature_avg")
        if not cache_value:
            print("Cache is empty, returning 503 Service Unavailable.")
            return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(status_code=status.HTTP_200_OK)
