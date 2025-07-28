import os
import valkey

VALKEY_HOST = os.getenv("VALKEY_HOST", "valkey")
VALKEY_PORT = int(os.getenv("VALKEY_PORT", 6379))
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))
VALKEY_PASSWORD = os.getenv("VALKEY_PASSWORD", None)

r = valkey.Valkey(host=VALKEY_HOST, port=VALKEY_PORT, db=0)


def get_cached(key: str):
    print(f"Fetching from cache: {key}")
    return r.get(key)


def set_cached(key: str, value: str):
    print(f"Setting cache: {key}")
    r.setex(key, CACHE_TTL, value)


def check_cache(key: str):
    print(f"Checking cache for key: {key}")
    return r.exists(key)
