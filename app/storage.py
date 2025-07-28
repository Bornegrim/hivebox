import os
from minio import Minio
from minio.error import S3Error
import json

S3_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
S3_ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "minioadmin")
S3_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
S3_BUCKET = os.getenv("S3_BUCKET", "hivebox-data")
S3_FILE_NAME = os.getenv("S3_FILE_NAME", "temperature_data.json")
S3_REGION = os.getenv("S3_REGION", "eu-north-1")

# Use lazy initialization to avoid connection at import time
client = None


def get_client():
    global client
    if client is None:
        client = Minio(
            endpoint=S3_ENDPOINT,
            access_key=S3_ACCESS_KEY,
            secret_key=S3_SECRET_KEY,
            region=S3_REGION,
            secure=False,  # Set to True if using HTTPS
        )
    return client


def store_temperature_data(data: dict):
    try:
        client = get_client()
        found = client.bucket_exists(S3_BUCKET)
        if not found:
            client.make_bucket(S3_BUCKET)
            print("Created bucket", S3_BUCKET)
        else:
            print("Bucket", S3_BUCKET, "already exists")

        temp_file = "/tmp/temperature_data.json"
        with open(temp_file, "w") as f:
            json.dump(data, f)
        client.fput_object(
            S3_BUCKET,
            S3_FILE_NAME,
            temp_file,
        )
        print(
            temp_file,
            "successfully uploaded as object",
            S3_FILE_NAME,
            "to bucket",
            S3_BUCKET,
        )
    except S3Error as e:
        print("Error occurred while uploading data:", e)
