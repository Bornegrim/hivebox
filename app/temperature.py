import requests
from datetime import datetime, timedelta, timezone

SENSEBOX_IDS = [
    "5ade1acf223bd80019a1011c",
    "5c21ff8f919bf8001adf2488",
    "5eba5fbad46fb8001b799786"
]

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
                            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

                            if timestamp >= one_hour_ago and value_str is not None:
                                try:
                                    value = float(value_str)
                                    temperatures.append(value)
                                except ValueError:
                                    continue
        except requests.RequestException:
            continue  # Skip unreachable or broken boxes

    if temperatures:
        avg_temp = sum(temperatures) / len(temperatures)
        return {"average_temperature": round(avg_temp, 2), "count": len(temperatures)}
    else:
        return {"average_temperature": None, "message": "No recent temperature data found."}
