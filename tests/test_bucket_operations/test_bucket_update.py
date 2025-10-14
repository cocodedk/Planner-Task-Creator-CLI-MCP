"""
Tests for bucket_update module
"""

import pytest
import requests
from planner_lib.bucket_update import update_bucket_op


@pytest.fixture
def mock_bucket():
    """Return mock bucket data with ETag"""
    return {
        "id": "bucket-id-1",
        "name": "Sprint 1",
        "planId": "plan-id-1",
        "@odata.etag": "W/\"abc123\""
    }


class TestBucketUpdate:
    """Tests for update_bucket_op function"""

    def test_update_bucket_success(self, mock_token, mock_bucket, mocker):
        """Test updating a bucket name successfully"""
        mock_get = mocker.patch("planner_lib.bucket_update.get_json")
        mock_patch = mocker.patch("planner_lib.bucket_update.patch_json")

        mock_get.return_value = mock_bucket
        mock_patch.return_value = {}

        result = update_bucket_op("bucket-id-1", "Sprint 1 - Complete", mock_token)

        assert result["ok"] is True
        assert result["bucketId"] == "bucket-id-1"
        assert result["oldName"] == "Sprint 1"
        assert result["newName"] == "Sprint 1 - Complete"

        # Verify API calls
        mock_get.assert_called_once()
        mock_patch.assert_called_once()

        patch_call = mock_patch.call_args
        assert patch_call[0][2]["name"] == "Sprint 1 - Complete"
        assert patch_call[0][3] == "W/\"abc123\""

    def test_update_bucket_etag_conflict_retry(self, mock_token, mock_bucket, mocker):
        """Test retry on ETag conflict (412 Precondition Failed)"""
        mock_get = mocker.patch("planner_lib.bucket_update.get_json")
        mock_patch = mocker.patch("planner_lib.bucket_update.patch_json")

        # First GET returns initial ETag
        # Second GET (after 412) returns new ETag
        updated_bucket = mock_bucket.copy()
        updated_bucket["@odata.etag"] = "W/\"xyz789\""
        mock_get.side_effect = [mock_bucket, updated_bucket]

        # First PATCH fails with 412, second succeeds
        http_error = requests.HTTPError()
        http_error.response = type('obj', (object,), {'status_code': 412})
        mock_patch.side_effect = [http_error, {}]

        result = update_bucket_op("bucket-id-1", "New Name", mock_token)

        assert result["ok"] is True
        assert result["newName"] == "New Name"

        # Verify retry logic
        assert mock_get.call_count == 2
        assert mock_patch.call_count == 2

    def test_update_bucket_other_error(self, mock_token, mock_bucket, mocker):
        """Test that non-412 errors are not retried"""
        mock_get = mocker.patch("planner_lib.bucket_update.get_json")
        mock_patch = mocker.patch("planner_lib.bucket_update.patch_json")

        mock_get.return_value = mock_bucket

        http_error = requests.HTTPError()
        http_error.response = type('obj', (object,), {'status_code': 404})
        mock_patch.side_effect = http_error

        with pytest.raises(requests.HTTPError):
            update_bucket_op("bucket-id-1", "New Name", mock_token)

        # Verify no retry for non-412 errors
        assert mock_get.call_count == 1
        assert mock_patch.call_count == 1

    def test_update_bucket_not_found(self, mock_token, mocker):
        """Test updating non-existent bucket"""
        mock_get = mocker.patch("planner_lib.bucket_update.get_json")
        mock_get.side_effect = Exception("Bucket not found")

        with pytest.raises(Exception) as exc_info:
            update_bucket_op("invalid-bucket-id", "New Name", mock_token)

        assert "Bucket not found" in str(exc_info.value)
