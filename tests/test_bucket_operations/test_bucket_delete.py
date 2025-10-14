"""
Tests for bucket_delete module
"""

import pytest
from planner_lib.bucket_delete import delete_bucket_op


@pytest.fixture
def mock_bucket():
    """Return mock bucket data with ETag"""
    return {
        "id": "bucket-id-1",
        "name": "Old Sprint",
        "planId": "plan-id-1",
        "@odata.etag": "W/\"abc123\""
    }


class TestBucketDelete:
    """Tests for delete_bucket_op function"""

    def test_delete_bucket_success(self, mock_token, mock_bucket, mocker):
        """Test deleting a bucket successfully"""
        mock_get = mocker.patch("planner_lib.bucket_delete.get_json")
        mock_delete = mocker.patch("planner_lib.bucket_delete.delete_json")

        mock_get.return_value = mock_bucket
        mock_delete.return_value = {}

        result = delete_bucket_op("bucket-id-1", mock_token)

        assert result["ok"] is True
        assert result["bucketId"] == "bucket-id-1"

        # Verify API calls
        mock_get.assert_called_once()
        assert "planner/buckets/bucket-id-1" in mock_get.call_args[0][0]

        mock_delete.assert_called_once()
        assert "planner/buckets/bucket-id-1" in mock_delete.call_args[0][0]
        assert mock_delete.call_args[0][2] == "W/\"abc123\""

    def test_delete_bucket_not_found(self, mock_token, mocker):
        """Test deleting non-existent bucket"""
        mock_get = mocker.patch("planner_lib.bucket_delete.get_json")
        mock_get.side_effect = Exception("Bucket not found")

        with pytest.raises(Exception) as exc_info:
            delete_bucket_op("invalid-bucket-id", mock_token)

        assert "Bucket not found" in str(exc_info.value)

    def test_delete_bucket_etag_required(self, mock_token, mock_bucket, mocker):
        """Test that ETag is fetched before deletion"""
        mock_get = mocker.patch("planner_lib.bucket_delete.get_json")
        mock_delete = mocker.patch("planner_lib.bucket_delete.delete_json")

        mock_get.return_value = mock_bucket
        mock_delete.return_value = {}

        delete_bucket_op("bucket-id-1", mock_token)

        # Verify ETag was extracted and used
        mock_delete.assert_called_once()
        assert mock_delete.call_args[0][2] == mock_bucket["@odata.etag"]
