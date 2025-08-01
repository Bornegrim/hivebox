import os
import requests
import json
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from app.cache import get_cached, set_cached
from app.metrics import TEMPERATURE_REQUESTS, TEMPERATURE_CACHE_HITS, TEMPERATURE_AVG


load_dotenv()
CACHE_KEY = "temperature_avg"
sensebox_ids = os.getenv("SENSEBOX_IDS", "")
SENSEBOX_IDS = [box_id.strip() for box_id in sensebox_ids.split(",") if box_id.strip()]

API_URL_TEMPLATE = "https://api.opensensemap.org/boxes/{}"


def fetch_box_data(box_id):
    try:
        response = requests.get(API_URL_TEMPLATE.format(box_id), timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def extract_temperatures(box, one_hour_ago):
    temps = []
    for sensor in box.get("sensors", []):
        title = sensor.get("title", "")
        if "temp" in title.lower():
            last_measurement = sensor.get("lastMeasurement", {})
            timestamp_str = last_measurement.get("createdAt")
            value_str = last_measurement.get("value")
            if timestamp_str and value_str is not None:
                try:
                    timestamp = datetime.fromisoformat(
                        timestamp_str.replace("Z", "+00:00")
                    )
                    if timestamp >= one_hour_ago:
                        value = float(value_str)
                        temps.append(value)
                except (ValueError, TypeError):
                    continue
    return temps


def determine_status(avg):
    if avg is None:
        return "Unavailable"
    if avg <= 10:
        return "Too Cold"
    elif 11 <= avg <= 36:
        return "Good"
    else:
        return "Too Hot"


def get_average_temperature():
    TEMPERATURE_REQUESTS.inc()

    cached = get_cached(CACHE_KEY)
    if cached:
        TEMPERATURE_CACHE_HITS.inc()
        return json.loads(cached)
    temperatures = []
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)

    for box_id in SENSEBOX_IDS:
        box = fetch_box_data(box_id)
        if box:
            temperatures.extend(extract_temperatures(box, one_hour_ago))

    if temperatures:
        avg = round(sum(temperatures) / len(temperatures), 2)
        TEMPERATURE_AVG.set(avg)
        status = determine_status(avg)
        result = {
            "average_temperature": avg,
            "count": len(temperatures),
            "status": status,
        }
        set_cached(CACHE_KEY, json.dumps(result))
        return result
    else:
        return {
            "average_temperature": None,
            "message": "No recent temperature data found.",
            "status": "Unavailable",
        }
