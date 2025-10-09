"""
Tests for bucket resolution
"""

import pytest
import json
from planner_lib.resolution import resolve_bucket, list_plan_buckets


def test_resolve_bucket_by_id(mocker, mock_token):
    """Test resolving bucket by GUID"""
    bucket_id = "12345678-1234-1234-1234-123456789abc"

    result = resolve_bucket(mock_token, "plan-id-1", bucket_id)

    assert result["id"] == bucket_id


def test_resolve_bucket_by_name(mocker, mock_token, mock_buckets):
    """Test resolving bucket by name"""
    mocker.patch("planner_lib.resolution_buckets.list_plan_buckets", return_value=mock_buckets)

    result = resolve_bucket(mock_token, "plan-id-1", "To Do")

    assert result["id"] == "bucket-id-1"
    assert result["name"] == "To Do"


def test_resolve_bucket_not_found(mocker, mock_token, mock_buckets):
    """Test bucket not found error"""
    mocker.patch("planner_lib.resolution_buckets.list_plan_buckets", return_value=mock_buckets)

    with pytest.raises(ValueError) as exc_info:
        resolve_bucket(mock_token, "plan-id-1", "Nonexistent Bucket")

    error = json.loads(str(exc_info.value))
    assert error["code"] == "NotFound"
    assert len(error["candidates"]) == 3


def test_list_plan_buckets(mocker, mock_token, mock_requests, mock_buckets):
    """Test listing plan buckets"""
    mock_requests["response"].json.return_value = {"value": mock_buckets}

    buckets = list_plan_buckets("plan-id-1", mock_token)

    assert len(buckets) == 3
    assert buckets[0]["name"] == "To Do"


