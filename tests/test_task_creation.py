"""
Tests for task creation module (005-task-creation)
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from planner_lib.task_creation import parse_labels, create_task


def test_parse_labels_empty():
    """Test parsing empty labels"""
    assert parse_labels(None) == {}
    assert parse_labels("") == {}
    assert parse_labels("   ") == {}


def test_parse_labels_single():
    """Test parsing single label"""
    result = parse_labels("Label1")
    assert result == {"category1": True}


def test_parse_labels_multiple():
    """Test parsing multiple labels"""
    result = parse_labels("Label1,Label3,Label5")
    assert result == {"category1": True, "category3": True, "category5": True}


def test_parse_labels_case_insensitive():
    """Test case-insensitive label parsing"""
    result = parse_labels("label2,LABEL4")
    assert result == {"category2": True, "category4": True}


def test_parse_labels_with_spaces():
    """Test parsing labels with spaces"""
    result = parse_labels("Label1, Label2 , Label3")
    assert result == {"category1": True, "category2": True, "category3": True}


def test_parse_labels_invalid():
    """Test parsing invalid labels (should be filtered out)"""
    result = parse_labels("Label1,NotALabel,Label2")
    assert result == {"category1": True, "category2": True}


def test_create_task_minimal(mocker, mock_token, mock_requests, mock_task):
    """Test creating task with minimal fields"""
    mock_requests["response"].json.return_value = mock_task

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Test Task"
    )

    assert result["taskId"] == "task-id-123"
    assert result["bucketId"] == "bucket-id-1"

    # Verify POST was called
    mock_requests["post"].assert_called_once()
    call_args = mock_requests["post"].call_args
    payload = call_args[1]["json"]

    assert payload["title"] == "Test Task"
    assert payload["planId"] == "plan-id-1"
    assert payload["bucketId"] == "bucket-id-1"


def test_create_task_with_due_date(mocker, mock_token, mock_requests, mock_task):
    """Test creating task with due date"""
    mock_requests["response"].json.return_value = mock_task

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Test Task",
        due_date="2024-12-31"
    )

    call_args = mock_requests["post"].call_args
    payload = call_args[1]["json"]

    assert payload["dueDateTime"] == "2024-12-31T17:00:00Z"


def test_create_task_with_labels(mocker, mock_token, mock_requests, mock_task):
    """Test creating task with labels"""
    mock_requests["response"].json.return_value = mock_task

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Test Task",
        labels="Label1,Label3"
    )

    call_args = mock_requests["post"].call_args
    payload = call_args[1]["json"]

    assert payload["appliedCategories"] == {"category1": True, "category3": True}


def test_create_task_with_description(mocker, mock_token, mock_requests, mock_task):
    """Test creating task with description"""
    # First call returns task, second returns details with etag
    mock_requests["response"].json.side_effect = [
        mock_task,
        {"@odata.etag": "W/\"test-etag\"", "description": ""},
        {}
    ]

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Test Task",
        description="This is a test description"
    )

    # Verify POST and PATCH were called
    assert mock_requests["post"].call_count == 1
    assert mock_requests["get"].call_count == 1
    assert mock_requests["patch"].call_count == 1

    # Verify PATCH payload
    patch_call = mock_requests["patch"].call_args
    assert patch_call[1]["json"]["description"] == "This is a test description"


def test_create_task_all_fields(mocker, mock_token, mock_requests, mock_task):
    """Test creating task with all optional fields"""
    mock_requests["response"].json.side_effect = [
        mock_task,
        {"@odata.etag": "W/\"test-etag\""},
        {}
    ]

    result = create_task(
        token=mock_token,
        plan_id="plan-id-1",
        bucket_id="bucket-id-1",
        title="Complete Task",
        description="Full description",
        due_date="2024-12-31",
        labels="Label1,Label2"
    )

    # Verify task was created with all fields
    post_call = mock_requests["post"].call_args
    payload = post_call[1]["json"]

    assert payload["title"] == "Complete Task"
    assert payload["dueDateTime"] == "2024-12-31T17:00:00Z"
    assert payload["appliedCategories"] == {"category1": True, "category2": True}
