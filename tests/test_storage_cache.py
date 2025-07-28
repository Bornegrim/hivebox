import pytest
from unittest.mock import patch, Mock, mock_open
from app.storage import store_temperature_data
from app.cache import get_cached, set_cached, check_cache
import json


class TestStorageModule:
    @patch("app.storage.get_client")
    @patch("builtins.open", new_callable=mock_open)
    def test_store_temperature_data_success(self, mock_file, mock_get_client):
        # Mock MinIO client methods
        mock_client = Mock()
        mock_client.bucket_exists.return_value = True
        mock_client.fput_object.return_value = None
        mock_get_client.return_value = mock_client

        test_data = {"temperature": 25.0, "count": 1}

        store_temperature_data(test_data)

        # Verify client was retrieved
        mock_get_client.assert_called_once()

        # Verify bucket check
        mock_client.bucket_exists.assert_called_once_with("hivebox-data")

        # Verify file write
        mock_file.assert_called_once_with("/tmp/temperature_data.json", "w")
        handle = mock_file()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        assert json.loads(written_data) == test_data

        # Verify upload
        mock_client.fput_object.assert_called_once_with(
            "hivebox-data", "temperature_data.json", "/tmp/temperature_data.json"
        )

    @patch("app.storage.get_client")
    @patch("builtins.open", new_callable=mock_open)
    def test_store_temperature_data_create_bucket(self, mock_file, mock_get_client):
        # Mock bucket doesn't exist initially
        mock_client = Mock()
        mock_client.bucket_exists.return_value = False
        mock_client.make_bucket.return_value = None
        mock_client.fput_object.return_value = None
        mock_get_client.return_value = mock_client

        test_data = {"temperature": 25.0}

        store_temperature_data(test_data)

        # Verify bucket creation
        mock_client.make_bucket.assert_called_once_with("hivebox-data")

    @patch("app.storage.S3Error", Exception)
    @patch("app.storage.get_client")
    @patch("builtins.open", new_callable=mock_open)
    def test_store_temperature_data_s3_error(self, mock_file, mock_get_client):
        # Mock S3 error during upload
        mock_client = Mock()
        mock_client.bucket_exists.return_value = True
        mock_client.fput_object.side_effect = Exception("S3 upload failed")
        mock_get_client.return_value = mock_client

        test_data = {"temperature": 25.0}

        # Should not raise exception, just print error
        store_temperature_data(test_data)


class TestCacheModule:
    @patch("app.cache.r")
    def test_get_cached_success(self, mock_redis):
        mock_redis.get.return_value = b'{"test": "data"}'

        result = get_cached("test_key")

        assert result == b'{"test": "data"}'
        mock_redis.get.assert_called_once_with("test_key")

    @patch("app.cache.r")
    def test_get_cached_none(self, mock_redis):
        mock_redis.get.return_value = None

        result = get_cached("nonexistent_key")

        assert result is None
        mock_redis.get.assert_called_once_with("nonexistent_key")

    @patch("app.cache.r")
    def test_set_cached(self, mock_redis):
        mock_redis.setex.return_value = True

        set_cached("test_key", "test_value")

        mock_redis.setex.assert_called_once_with("test_key", 300, "test_value")

    @patch("app.cache.r")
    def test_check_cache_exists(self, mock_redis):
        mock_redis.exists.return_value = 1

        result = check_cache("test_key")

        assert result == 1
        mock_redis.exists.assert_called_once_with("test_key")

    @patch("app.cache.r")
    def test_check_cache_not_exists(self, mock_redis):
        mock_redis.exists.return_value = 0

        result = check_cache("nonexistent_key")

        assert result == 0
        mock_redis.exists.assert_called_once_with("nonexistent_key")
