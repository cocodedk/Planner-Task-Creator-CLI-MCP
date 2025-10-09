"""
Tests for resolution module (004-resolution)
"""

import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from planner_lib.resolution import (
    case_insensitive_match,
    resolve_plan,
    resolve_bucket,
    list_user_plans,
    list_plan_buckets
)


def test_case_insensitive_match():
    """Test case-insensitive matching"""
    items = [
        {"name": "Test Item", "id": "1"},
        {"name": "Another Item", "id": "2"},
        {"name": "TEST ITEM", "id": "3"}
    ]

    matches = case_insensitive_match(items, "name", "test item")
    assert len(matches) == 2
    assert matches[0]["id"] == "1"
    assert matches[1]["id"] == "3"


def test_resolve_plan_by_id(mocker, mock_token):
    """Test resolving plan by GUID"""
    plan_id = "12345678-1234-1234-1234-123456789abc"

    result = resolve_plan(mock_token, plan_id)

    assert result["id"] == plan_id


def test_resolve_plan_by_name(mocker, mock_token, mock_plans):
    """Test resolving plan by name"""
    mocker.patch("planner_lib.resolution_plans.list_user_plans", return_value=mock_plans)

    result = resolve_plan(mock_token, "My Plan")

    assert result["id"] == "plan-id-1"
    assert result["title"] == "My Plan"


def test_resolve_plan_case_insensitive(mocker, mock_token, mock_plans):
    """Test case-insensitive plan resolution"""
    mocker.patch("planner_lib.resolution_plans.list_user_plans", return_value=mock_plans)

    result = resolve_plan(mock_token, "my plan")

    assert result["id"] == "plan-id-1"


def test_resolve_plan_not_found(mocker, mock_token, mock_plans):
    """Test plan not found error"""
    mocker.patch("planner_lib.resolution_plans.list_user_plans", return_value=mock_plans)

    with pytest.raises(ValueError) as exc_info:
        resolve_plan(mock_token, "Nonexistent Plan")

    error = json.loads(str(exc_info.value))
    assert error["code"] == "NotFound"
    assert "Nonexistent Plan" in error["message"]
    assert len(error["candidates"]) == 2


def test_resolve_plan_ambiguous(mocker, mock_token):
    """Test ambiguous plan resolution"""
    duplicate_plans = [
        {"id": "plan-id-1", "title": "My Plan", "groupName": "Team A"},
        {"id": "plan-id-2", "title": "My Plan", "groupName": "Team B"}
    ]
    mocker.patch("planner_lib.resolution_plans.list_user_plans", return_value=duplicate_plans)

    with pytest.raises(ValueError) as exc_info:
        resolve_plan(mock_token, "My Plan")

    error = json.loads(str(exc_info.value))
    assert error["code"] == "Ambiguous"
    assert len(error["candidates"]) == 2


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


def test_list_user_plans(mocker, mock_token, mock_requests):
    """Test listing user plans"""
    mock_requests["response"].json.return_value = {
        "value": [
            {"id": "plan-1", "title": "Plan 1", "owner": "group-1"}
        ]
    }

    # Mock group details
    def mock_get_side_effect(url, headers):
        if "groups" in url:
            response = mocker.MagicMock()
            response.status_code = 200
            response.json.return_value = {"displayName": "Team Name"}
            response.raise_for_status.return_value = None
            return response
        return mock_requests["response"]

    mock_requests["get"].side_effect = mock_get_side_effect

    plans = list_user_plans(mock_token)

    assert len(plans) == 1
    assert plans[0]["id"] == "plan-1"


def test_list_plan_buckets(mocker, mock_token, mock_requests, mock_buckets):
    """Test listing plan buckets"""
    mock_requests["response"].json.return_value = {"value": mock_buckets}

    buckets = list_plan_buckets("plan-id-1", mock_token)

    assert len(buckets) == 3
    assert buckets[0]["name"] == "To Do"
