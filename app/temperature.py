import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

sensebox_ids = os.getenv("SENSEBOX_IDS", "")
SENSEBOX_IDS = [box_id.strip() for box_id in sensebox_ids.split(",") if box_id.strip()]

API_URL_TEMPLATE = "https://api.opensensemap.org/boxes/{}"


def get_average_temperature():
    temperatures = []
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)

    for box_id in SENSEBOX_IDS:
        try:
            response = requests.get(API_URL_TEMPLATE.format(box_id), timeout=5)
            response.raise_for_status()
            box = response.json()

            for sensor in box.get("sensors", []):
                title = sensor.get("title")
                if title and "temp" in title.lower():
                    last_measurement = sensor.get("lastMeasurement")
                    if isinstance(last_measurement, dict):
                        timestamp_str = last_measurement.get("createdAt")
                        value_str = last_measurement.get("value")
                        if timestamp_str:
                            timestamp = datetime.fromisoformat(
                                timestamp_str.replace("Z", "+00:00")
                            )
                            if timestamp >= one_hour_ago and value_str is not None:
                                try:
                                    value = float(value_str)
                                    temperatures.append(value)
                                except ValueError:
                                    continue
        except requests.RequestException:
            continue

    if temperatures:
        avg = round(sum(temperatures) / len(temperatures), 2)

        # ✅ Add status field based on average
        if avg <= 10:
            status = "Too Cold"
        elif 11 <= avg <= 36:
            status = "Good"
        else:
            status = "Too Hot"

        return {
            "average_temperature": avg,
            "count": len(temperatures),
            "status": status,
        }
    else:
        return {
            "average_temperature": None,
            "message": "No recent temperature data found.",
            "status": "Unavailable",
        }
