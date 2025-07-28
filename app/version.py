import os


APP_VERSION = os.getenv("APP_VERSION", "0.0.1")


def get_version():
    return {"version": f"v{APP_VERSION}"}
