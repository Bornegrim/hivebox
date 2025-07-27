from fastapi import FastAPI
from app.version import get_version
from app.temperature import get_average_temperature

app = FastAPI(title="HiveBox", version="0.0.1")

@app.get("/version")
def version():
    return get_version()

@app.get("/temperature")
def temperature():
    return get_average_temperature()