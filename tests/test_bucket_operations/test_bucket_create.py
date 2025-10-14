"""
Tests for bucket_create module
"""

import pytest
from planner_lib.bucket_create import create_bucket_op


@pytest.fixture
def mock_bucket():
    """Return mock bucket data"""
    return {
        "id": "new-bucket-id-123",
        "name": "Sprint 1",
        "planId": "plan-id-1",
        "orderHint": " !"
    }


class TestBucketCreate:
    """Tests for create_bucket_op function"""

    def test_create_bucket_success(self, mock_token, mock_bucket, mocker):
        """Test creating a bucket successfully"""
        mock_post = mocker.patch("planner_lib.bucket_create.post_json")
        mock_post.return_value = mock_bucket

        result = create_bucket_op("plan-id-1", "Sprint 1", mock_token)

        assert result["ok"] is True
        assert result["bucketId"] == "new-bucket-id-123"
        assert result["name"] == "Sprint 1"
        assert result["planId"] == "plan-id-1"

        # Verify API call
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert "planner/buckets" in call_args[0][0]
        assert call_args[0][1] == mock_token
        assert call_args[0][2]["name"] == "Sprint 1"
        assert call_args[0][2]["planId"] == "plan-id-1"
        assert call_args[0][2]["orderHint"] == " !"

    def test_create_bucket_with_special_chars(self, mock_token, mocker):
        """Test creating a bucket with special characters in name"""
        special_bucket = {
            "id": "bucket-id-special",
            "name": "Q1-2024 Sprint #1",
            "planId": "plan-id-1",
            "orderHint": " !"
        }
        mock_post = mocker.patch("planner_lib.bucket_create.post_json")
        mock_post.return_value = special_bucket

        result = create_bucket_op("plan-id-1", "Q1-2024 Sprint #1", mock_token)

        assert result["ok"] is True
        assert result["name"] == "Q1-2024 Sprint #1"

    def test_create_bucket_api_error(self, mock_token, mocker):
        """Test handling API error during bucket creation"""
        mock_post = mocker.patch("planner_lib.bucket_create.post_json")
        mock_post.side_effect = Exception("Invalid plan ID")

        with pytest.raises(Exception) as exc_info:
            create_bucket_op("invalid-plan", "Sprint 1", mock_token)

        assert "Invalid plan ID" in str(exc_info.value)
